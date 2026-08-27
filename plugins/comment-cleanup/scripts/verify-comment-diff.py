#!/usr/bin/env python3
"""註解清理的機械閘門。

兩種模式：

  --snapshot <dir>   比對動手前的快照與現在的工作區（預設用法）。工作區本來就有
                     未 commit 的變更時，唯一能分辨「誰改的」的辦法就是自己留快照。
  <git-ref>          比對某個 git ref 與工作區。只在工作區乾淨時才有意義。

兩種模式的判準相同：把每個檔案的註解與空行剝除後，剩下的 code 必須逐行相同。
相同 → PASS，變更純屬註解；不同 → FAIL，diff 夾帶了 code 變更。

before 與 after 走同一套剝除規則，所以規則本身的不精確不會造成誤判 FAIL——
它只可能漏放行，不可能誤攔。副檔名不認得時一律 FAIL，不猜。
"""

import subprocess
import sys
import os

C_FAMILY = {"line": ["//"], "block": [("/*", "*/")], "quotes": ['"', "'", "`"]}
JSX = {"line": ["//"], "block": [("{/*", "*/}"), ("/*", "*/")], "quotes": ['"', "'", "`"]}
HASH = {"line": ["#"], "block": [], "quotes": ['"', "'"]}
MARKUP = {"line": [], "block": [("<!--", "-->")], "quotes": []}
SQL = {"line": ["--"], "block": [("/*", "*/")], "quotes": ['"', "'"]}
LUA = {"line": ["--"], "block": [("--[[", "]]")], "quotes": ['"', "'"]}
CSS = {"line": [], "block": [("/*", "*/")], "quotes": ['"', "'"]}
SCSS = {"line": ["//"], "block": [("/*", "*/")], "quotes": ['"', "'"]}

EXT_MAP = {}
for ext in (".js", ".mjs", ".cjs", ".ts", ".mts", ".cts", ".java", ".c", ".h", ".cc",
            ".cpp", ".hpp", ".go", ".rs", ".swift", ".kt", ".kts", ".cs", ".scala",
            ".php", ".dart", ".m", ".mm", ".proto", ".gradle", ".groovy"):
    EXT_MAP[ext] = C_FAMILY
for ext in (".jsx", ".tsx"):
    EXT_MAP[ext] = JSX
for ext in (".py", ".sh", ".bash", ".zsh", ".rb", ".yml", ".yaml", ".toml", ".tf",
            ".tfvars", ".pl", ".r", ".ex", ".exs", ".nix", ".dockerfile", ".gitignore"):
    EXT_MAP[ext] = HASH
for ext in (".html", ".htm", ".xml", ".vue", ".svelte", ".md", ".mdx", ".svg"):
    EXT_MAP[ext] = MARKUP
EXT_MAP[".sql"] = SQL
EXT_MAP[".lua"] = LUA
EXT_MAP[".css"] = CSS
for ext in (".scss", ".sass", ".less"):
    EXT_MAP[ext] = SCSS

BASENAME_MAP = {"Dockerfile": HASH, "Makefile": HASH, "Justfile": HASH}


def lang_for(path):
    base = os.path.basename(path)
    if base in BASENAME_MAP:
        return BASENAME_MAP[base]
    _, ext = os.path.splitext(base)
    return EXT_MAP.get(ext.lower())


def strip_comments(text, lang):
    """回傳剝除註解與空行後的 code 行序列。"""
    out = []
    block_end = None
    for lineno, raw in enumerate(text.split("\n")):
        # shebang 有功能，不當註解剝除，否則刪掉它閘門看不出來
        if lineno == 0 and raw.startswith("#!"):
            out.append(raw.rstrip())
            continue
        buf = []
        i = 0
        n = len(raw)
        while i < n:
            if block_end is not None:
                idx = raw.find(block_end, i)
                if idx == -1:
                    i = n
                else:
                    i = idx + len(block_end)
                    block_end = None
                continue
            ch = raw[i]
            if ch in lang["quotes"]:
                buf.append(ch)
                i += 1
                while i < n:
                    if raw[i] == "\\":
                        buf.append(raw[i:i + 2])
                        i += 2
                        continue
                    buf.append(raw[i])
                    if raw[i] == ch:
                        i += 1
                        break
                    i += 1
                continue
            matched = False
            for start, end in lang["block"]:
                if raw.startswith(start, i):
                    block_end = end
                    i += len(start)
                    matched = True
                    break
            if matched:
                continue
            for token in lang["line"]:
                if raw.startswith(token, i):
                    i = n
                    matched = True
                    break
            if matched:
                continue
            buf.append(ch)
            i += 1
        code = "".join(buf).rstrip()
        if code.strip():
            out.append(code)
    return out


def git(args):
    return subprocess.run(["git"] + args, capture_output=True, text=True)


def compare(path, before_text, after_text):
    """回傳 None 表示通過，否則回傳失敗說明。"""
    lang = lang_for(path)
    if lang is None:
        return path + " — 無法辨識的副檔名，閘門不猜，一律視為未通過"
    b = strip_comments(before_text, lang)
    a = strip_comments(after_text, lang)
    if b != a:
        return path + " — 剝除註解後 code 仍有差異" + first_divergence(b, a)
    return None


def read_text(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def porcelain_paths(text):
    """把 git status --porcelain 的輸出轉成路徑集合。"""
    paths = set()
    for line in text.split("\n"):
        if len(line) < 4:
            continue
        rest = line[3:]
        # rename/copy 是 "old -> new"，兩邊都算
        if " -> " in rest:
            old, new = rest.split(" -> ", 1)
            paths.add(old.strip().strip('"'))
            paths.add(new.strip().strip('"'))
        else:
            paths.add(rest.strip().strip('"'))
    return paths


def mode_snapshot(snapdir):
    files_root = os.path.join(snapdir, "files")
    status_before_path = os.path.join(snapdir, "status-before.txt")
    scope_path = os.path.join(snapdir, "scope.txt")
    for required in (files_root, status_before_path, scope_path):
        if not os.path.exists(required):
            print("FAIL: 快照不完整，缺少 " + required)
            return 1

    violations = []

    # 一、範圍外編輯的偵測。快照只涵蓋範圍內的檔案，動了範圍外的檔案它看不見，
    #     所以先用 git status 的路徑集合把守。
    before_paths = porcelain_paths(read_text(status_before_path))
    scope = set(ln.strip() for ln in read_text(scope_path).split("\n") if ln.strip())
    now = git(["status", "--porcelain"])
    if now.returncode != 0:
        print("FAIL: git status 失敗 — " + now.stderr.strip())
        return 1
    after_paths = porcelain_paths(now.stdout)

    for path in sorted(after_paths - before_paths):
        if path not in scope:
            violations.append(path + " — 動到了範圍外的檔案（動手前它是乾淨的）")
    for path in sorted(before_paths - after_paths):
        violations.append(path + " — 動手前有的變更消失了，使用者的改動被還原掉")

    # 二、逐檔比對快照與工作區
    checked = []
    unchanged = 0
    for dirpath, _, filenames in os.walk(files_root):
        for name in filenames:
            snap_file = os.path.join(dirpath, name)
            rel = os.path.relpath(snap_file, files_root)
            if not os.path.exists(rel):
                violations.append(rel + " — 檔案在工作區消失了")
                continue
            with open(snap_file, "rb") as fh:
                before_bytes = fh.read()
            with open(rel, "rb") as fh:
                after_bytes = fh.read()
            # 位元組相同就不必判語言：認不得副檔名但根本沒動的檔案不該被誤攔
            if before_bytes == after_bytes:
                unchanged += 1
                continue
            try:
                problem = compare(rel, before_bytes.decode("utf-8"),
                                  after_bytes.decode("utf-8"))
            except UnicodeDecodeError as exc:
                problem = rel + " — 不是 UTF-8 文字檔：" + str(exc)
            if problem:
                violations.append(problem)
            else:
                checked.append(rel)

    for path in checked:
        print("  ok    " + path)
    if unchanged:
        print("  --    " + str(unchanged) + " 個檔案未被動過")
    for msg in violations:
        print("  FAIL  " + msg)

    untracked = sorted(p for p in after_paths if p not in scope and p in before_paths)
    if untracked:
        print("")
        print("備註：範圍外本來就有變更的檔案（沒被清理，也沒被動到）：")
        for path in untracked:
            print("  " + path)

    print("")
    if violations:
        print("FAIL: " + str(len(violations)) + " 項未通過。從快照整批還原，改走 report-only。")
        return 1
    print("PASS: " + str(len(checked)) + " 個檔案的變更純屬註解與空行（另有 "
          + str(unchanged) + " 個未被動過）。")
    return 0


def mode_ref(base):
    status = git(["diff", "--name-status", base])
    if status.returncode != 0:
        print("FAIL: git diff 失敗 — " + status.stderr.strip())
        return 1

    entries = [ln.split("\t") for ln in status.stdout.strip().split("\n") if ln.strip()]
    if not entries:
        print("PASS: 相對於 " + base + " 沒有任何變更")
        return 0

    violations = []
    checked = []
    for parts in entries:
        code = parts[0]
        path = parts[-1]
        if code[0] != "M":
            violations.append(path + " — 檔案被 " + code + "（新增/刪除/改名），註解清理不該做這件事")
            continue
        before = git(["show", base + ":" + path])
        if before.returncode != 0:
            violations.append(path + " — 讀不到 " + base + " 版本")
            continue
        try:
            after = read_text(path)
        except (IOError, UnicodeDecodeError) as exc:
            violations.append(path + " — 讀取工作區版本失敗：" + str(exc))
            continue
        problem = compare(path, before.stdout, after)
        if problem:
            violations.append(problem)
        else:
            checked.append(path)

    for path in checked:
        print("  ok    " + path)
    for msg in violations:
        print("  FAIL  " + msg)

    print("")
    if violations:
        print("FAIL: " + str(len(violations)) + " 個檔案未通過（已檢查 "
              + str(len(entries)) + " 個）。整批還原，改走 report-only。")
        return 1
    print("PASS: " + str(len(checked)) + " 個檔案的變更純屬註解與空行。")
    return 0


def main():
    args = sys.argv[1:]
    if args and args[0] == "--snapshot":
        if len(args) < 2:
            print("FAIL: --snapshot 需要快照目錄路徑")
            return 1
        return mode_snapshot(args[1])
    return mode_ref(args[0] if args else "HEAD")


def first_divergence(before, after):
    for idx in range(min(len(before), len(after))):
        if before[idx] != after[idx]:
            return ("\n          第 " + str(idx + 1) + " 行 code（剝除註解後計）："
                    "\n            - " + before[idx].strip()[:100]
                    + "\n            + " + after[idx].strip()[:100])
    if len(before) > len(after):
        return "\n          少了 " + str(len(before) - len(after)) + " 行 code：" \
               + before[len(after)].strip()[:100]
    return "\n          多了 " + str(len(after) - len(before)) + " 行 code：" \
           + after[len(before)].strip()[:100]


if __name__ == "__main__":
    sys.exit(main())
