# Comment Cleanup

以第一性原理審查並清理 code 註解，只留下讀者無法從 code 本身得知的資訊。

## 安裝

```bash
/plugin marketplace add weilindev/agents
/plugin install comment-cleanup@weilindev
```

## 使用

```
/comment-cleanup:comment-cleanup
```

也可以直接說「清理註解」「comment cleanup」「註解太多」「審一下註解」，Claude 會自動觸發。

範圍是當前 branch 相對主幹的所有變更，**包含還沒 commit 的**；也可以指定路徑。

## 核心規則

**鐵則：只改註解，不改 code。** 一行可執行的 code 都不動，產出一份每個 `+`／`-` 都是註解行的 diff — 可以不看就 merge。發現該改的 code 會寫進報告，不動手。

每條註解過兩道判準，任一關不過就刪：

1. **看 code 能不能懂？** 能懂就刪 — 註解不該複述 code 已經說出口的事。
2. **是不是過程與轉折？** 是就刪 — 「原本用 X 後來改 Y」屬於 commit message 與 PR，不屬於 code。留結論，不留推導。

值得留下的共通點是：**讀者不知道就會改壞，而 code 與型別都攔不住他** — 不變式、反直覺的選擇、外部依據、跨檔耦合、安全性理由、演算法出處。

有功能的註解（`eslint-disable`、`@ts-expect-error`、授權標頭、對外 SDK 的 JSDoc 等）一律不動。

## 執行方式

只有一條路徑：skill 收到你的請求後**派 `comment-cleanup` subagent**，subagent 清理、過閘門，再把結果轉述回來。沒有「先開清單問你要刪哪些」的版本 —— 安全性押在機械閘門與可還原的快照上，不押在人工逐條核可。

想背景跑就明講「背景跑」，skill 會用 `run_in_background` 派工。

安全性押在三件事上：

**一、動手前先建快照。** 工作區**不必乾淨** —— 這個 plugin 就是給「開發告一段落」用的，那個時間點常常還有沒 commit 的東西。範圍是當前 branch 相對主幹的所有變更（`git diff <merge-base>`，含還沒 commit 的），動手前先把這些檔案複製一份到 `$(git rev-parse --git-common-dir)/comment-cleanup/snapshot-<時間戳>/`。

還原用快照而不是 `git checkout` —— 後者會把你自己還沒 commit 的變更一起洗掉。快照放在 git 目錄而不是 `/tmp`：工作區髒的時候沒有 commit 可以 revert，快照就是唯一的 undo，重開機不能消失。

**二、機械閘門，不是自我保證。** 套用後跑 `scripts/verify-comment-diff.py --snapshot <快照路徑>`，它做兩件事：比對 `git status --porcelain` 確認 subagent 沒動到範圍外的檔案、也沒把你原有的變更洗掉；然後逐檔把註解與空行剝除，比對 code 是否逐行相同。任一項不過 → **從快照整批還原**，降級成 report-only，不准部分保留。閘門過了才跑 typecheck 與唯讀 lint，失敗一樣還原。不跑 test suite：閘門的盲點是刪掉 `@ts-expect-error`、`eslint-disable` 這類有功能的註解，typecheck 與 lint 就能抓到，test 沒有額外覆蓋卻最耗時。

閘門有一個已知盲點：刪掉 `@ts-expect-error`、`eslint-disable` 這類有功能的註解，它看到的仍然是註解行，攔不住 —— 那一層由 typecheck 與 lint 補。

**三、分層信任。** 「一律刪除」六類與 `壓縮` 直接套用；判準二的邊界案例、無法確認出處的 `外部依據`、`建議改 code` 一律只寫報告不動手。判不準就歸到報告 —— 沒有人在旁邊接住誤判，判不準就別賭。

每一條 `壓縮` 的 before/after 都會留存：閘門攔不住改壞的改寫（改爛的註解仍然是註解），這份對照就是它的補償。

## 兩種情境，兩種結束方式

| 你的狀態 | 工作區 | 結束方式 |
| --- | --- | --- |
| 開發完但還沒 commit | 髒 | **只套用不 commit**（`APPLIED`），變更留在工作區，你連同自己的改動一起 commit |
| 已 commit／push／開了 PR | 乾淨 | 落成**單獨一顆 `chore:` commit**（`COMMITTED`），隨時可整包 revert |

情境一不 commit 是因為註解變更跟你的 code 變更在同一批檔案裡，切不開 —— 硬要 commit 就會把你還沒準備好的東西一起送出去。要退回就從快照複製，路徑會寫在回報裡。

`git add` 一律用實際改過的檔案清單，不用 `-A` —— 免得把你原本就存在的 untracked 檔案掃進 commit。

**還沒 `git add` 過的新檔案不在範圍內**（`git diff` 只看 tracked 檔案），它們的註解不會被清。這是刻意的，但不會靜默跳過：回報裡會列出偵測到的 untracked 檔案。

完整報告不落檔，全部放在 subagent 的回報裡再由主 session 原文轉給你 —— Claude Code 本來就擋 subagent 寫報告檔，而且改動本身 `git diff` 看得到，留檔沒有額外價值。快照是唯一寫進 git 目錄的東西，路徑在 `$(git rev-parse --git-common-dir)/comment-cleanup/` 底下。用 `--git-common-dir` 而不是寫死 `.git/`，是因為 linked worktree 的 `.git` 是檔案不是目錄；指向主 repo 也讓快照在 worktree 被移除後還留著。

### 閘門的測試

閘門本身有回歸測試，改過 `verify-comment-diff.py` 就跑一次：

```bash
bash scripts/test-gate.sh
```

17 個案例，涵蓋兩種模式：純刪註解／尾註解／JSX／CRLF 該過，改 code／刪 code／註解掉 code／孤兒 block／動到範圍外／把使用者的變更洗掉該擋。它在系統暫存目錄建臨時 git repo 跑，不碰任何既有 repo。

### 閘門支援的語言

C 家族（js/ts/java/go/rust/swift/kt/cs/php…）、JSX/TSX（含 `{/* */}`）、`#` 系（py/sh/rb/yaml/toml/tf…）、markup（html/xml/vue/svelte/md）、sql、lua、css/scss。**副檔名不認得就一律判為未通過** —— 閘門不猜。

## 三個檔案的職責

| 檔案 | 職責 |
| --- | --- |
| `skills/comment-cleanup/SKILL.md` | 入口。只負責確認 base 分支、派工、轉述結果，不含判準也不自己清理 |
| `skills/comment-cleanup/rules.md` | 判準的唯一來源：鐵則、兩道判準、刪留分類、範圍怎麼定 |
| `agents/comment-cleanup.md` | 執行流程：前置條件、分層、閘門、驗證、commit、報告 |

判準與流程拆成兩個檔是必要的，不是潔癖：subagent 讀 `rules.md` 而不讀 `SKILL.md`，否則它會讀到「去派 subagent」而無限遞迴。subagent 的 `tools` 也刻意不含 `Agent` 與 `Skill`，讓遞迴在工具層就不可能發生。

## 授權

MIT
