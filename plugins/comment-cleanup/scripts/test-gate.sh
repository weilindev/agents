#!/bin/bash
# 閘門的回歸測試。改過 verify-comment-diff.py 就跑一次：
#   bash scripts/test-gate.sh
# 在系統暫存目錄建臨時 git repo 跑，不碰任何既有 repo。
set -u
GATE="${GATE:-$(cd "$(dirname "$0")" && pwd)/verify-comment-diff.py}"
ROOT="${TMPDIR:-/tmp}/comment-cleanup-gate-suite-$$"
trap 'rm -rf "$ROOT"' EXIT
PASS=0; FAIL=0

expect() { # expect <name> <expected-exit> <actual-exit>
  if [ "$2" = "$3" ]; then echo "  PASS  $1"; PASS=$((PASS+1));
  else echo "  ****  $1 （預期 exit=$2，實得 $3）"; FAIL=$((FAIL+1)); fi
}

fresh_repo() {
  rm -rf "$ROOT"; mkdir -p "$ROOT"; cd "$ROOT" || exit 1
  git init -q .; git config user.email t@t.t; git config user.name t
  cat > a.ts <<'EOF'
// 建立使用者
export function createUser(name: string) {
  const url = "https://example.com/api"; // 端點
  /*
   多行說明
  */
  return fetch(url, { method: "POST", body: name });
}
EOF
  cat > b.tsx <<'EOF'
export function Btn() {
  {/* 這是按鈕 */}
  return <button>go</button>;
}
EOF
  cat > c.py <<'EOF'
#!/usr/bin/env python3
# 計算總和
def total(xs):
    return sum(xs)  # 加總
EOF
  printf 'binary-ish\n' > data.qqq
  git add -A; git commit -qm base; git branch -M main
}

snapshot() { # snapshot <base-ref>  → 印出快照路徑
  local snap="$(git rev-parse --git-common-dir)/comment-cleanup/snap-$1-$$"
  mkdir -p "$snap/files"
  git status --porcelain > "$snap/status-before.txt"
  git diff --name-only --diff-filter=d "$(git merge-base HEAD "$1")" > "$snap/scope.txt"
  while IFS= read -r f; do
    [ -z "$f" ] && continue
    mkdir -p "$snap/files/$(dirname "$f")"
    cp "$f" "$snap/files/$f"
  done < "$snap/scope.txt"
  echo "$snap"
}

echo "=== ref 模式（回歸）==="
fresh_repo
sed -i '' '/^\/\/ 建立使用者$/d; s| // 端點||' a.ts
sed -i '' '/^  {\/\* 這是按鈕 \*\/}$/d' b.tsx
sed -i '' '/^# 計算總和$/d; s|  # 加總||' c.py
python3 "$GATE" HEAD >/dev/null 2>&1; expect "R1 純刪註解（尾註解/JSX/python）" 0 $?
git checkout -q .

sed -i '' 's/const url =/const endpoint =/' a.ts
python3 "$GATE" HEAD >/dev/null 2>&1; expect "R2 改 code" 1 $?
git checkout -q .

sed -i '' '/return sum/d' c.py
python3 "$GATE" HEAD >/dev/null 2>&1; expect "R3 刪 code" 1 $?
git checkout -q .

sed -i '' 's|^  return fetch|  // return fetch|' a.ts
python3 "$GATE" HEAD >/dev/null 2>&1; expect "R4 註解掉 code" 1 $?
git checkout -q .

sed -i '' 's|// 建立使用者|// 呼叫端不得先雜湊|' a.ts
python3 "$GATE" HEAD >/dev/null 2>&1; expect "R5 壓縮註解" 0 $?
git checkout -q .

sed -i '' '/^  \/\*$/d' a.ts
python3 "$GATE" HEAD >/dev/null 2>&1; expect "R6 孤兒 block" 1 $?
git checkout -q .

echo "x" >> data.qqq
python3 "$GATE" HEAD >/dev/null 2>&1; expect "R7 未知副檔名（真的改了）" 1 $?
git checkout -q .

echo "// hi" > new.ts; git add new.ts
python3 "$GATE" HEAD >/dev/null 2>&1; expect "R8 新增檔案" 1 $?
git reset -q HEAD .; rm -f new.ts

printf 'const a = 1; // x\r\nconst b = 2;\r\n' > crlf.ts; git add -A; git commit -qm crlf
printf 'const a = 1;\r\nconst b = 2;\r\n' > crlf.ts
python3 "$GATE" HEAD >/dev/null 2>&1; expect "R9 CRLF 尾註解" 0 $?
git reset -q --hard HEAD~1

echo
echo "=== snapshot 模式（新）==="
fresh_repo
git checkout -qb feature
# 情境 1：branch 上有已 commit 的變更 + 工作區未 commit 的變更
sed -i '' 's|body: name|body: JSON.stringify(name)|' a.ts
git commit -qam "feature: 已 commit 的 code 變更"
sed -i '' 's|return sum(xs)|return sum(xs) or 0|' c.py   # 使用者未 commit 的 code 變更
echo "changed-on-feature" >> data.qqq                   # 範圍內但認不得副檔名的檔案

SNAP=$(snapshot main)
sed -i '' '/^\/\/ 建立使用者$/d; s| // 端點||' a.ts
sed -i '' '/^# 計算總和$/d' c.py
python3 "$GATE" --snapshot "$SNAP" >/dev/null 2>&1; expect "S1 髒工作區下純刪註解" 0 $?
grep -q 'sum(xs) or 0' c.py; expect "S2 使用者的未 commit 變更仍在" 0 $?

sed -i '' 's/const url =/const endpoint =/' a.ts
python3 "$GATE" --snapshot "$SNAP" >/dev/null 2>&1; expect "S3 夾帶 code 變更" 1 $?
cp "$SNAP/files/a.ts" a.ts   # 從快照還原

echo "// 範圍外" >> b.tsx
python3 "$GATE" --snapshot "$SNAP" >/dev/null 2>&1; expect "S4 動到範圍外的檔案" 1 $?
git checkout -q b.tsx

USER_LINE=$(grep -c 'sum(xs) or 0' c.py)
git checkout -q c.py   # 模擬 agent 誤把使用者變更還原掉
python3 "$GATE" --snapshot "$SNAP" >/dev/null 2>&1; expect "S5 使用者變更被還原掉" 1 $?
cp "$SNAP/files/c.py" c.py

python3 "$GATE" --snapshot "$SNAP" >/dev/null 2>&1; expect "S6 範圍內未知副檔名但未被動過" 0 $?

echo "z" >> data.qqq
python3 "$GATE" --snapshot "$SNAP" >/dev/null 2>&1; expect "S7 範圍內未知副檔名被動了" 1 $?
cp "$SNAP/files/data.qqq" data.qqq

python3 "$GATE" --snapshot "$SNAP" >/dev/null 2>&1; expect "S8 還原後回到 PASS" 0 $?

echo
echo "通過 $PASS 項，失敗 $FAIL 項"
[ "$FAIL" -eq 0 ]
