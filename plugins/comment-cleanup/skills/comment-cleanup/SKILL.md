---
name: comment-cleanup
description: 以第一性原理審查並清理 code 註解，刪除翻譯型、冗餘、過期的註解，只留下讀者無法從 code 本身得知的資訊。鐵則是只改註解不改 code，通過機械閘門才留下改動；工作區乾淨時落成單獨一顆 commit，否則套用後交給使用者一起 commit。不需要逐條確認。用於開發告一段落、commit 或開 PR 之前。使用者說「清理註解」「comment cleanup」「註解太多」「審一下註解」時觸發。
argument-hint: "[路徑或範圍]"
model: sonnet
effort: medium
---

# 註解清理

**你自己不執行清理。這個 skill 唯一的動作是派 `comment-cleanup` subagent。**

判準與流程都在 subagent 那邊（`${CLAUDE_PLUGIN_ROOT}/skills/comment-cleanup/rules.md` 與 `${CLAUDE_PLUGIN_ROOT}/agents/comment-cleanup.md`），你不需要讀，也不要把它們的內容抄進派工 prompt。

只有一條路徑：**派工 → 等回報 → 轉述**。沒有互動確認版本，不要自己開清單問使用者要刪哪些——安全性押在機械閘門與可還原的快照上，不押在人工逐條核可。

## 派工前先確認 base 分支

repo 的 CLAUDE.md 有指定主幹就照它（例如 twhn* 系列是 `dev` 不是 `main`），沒指定才看 `git symbolic-ref refs/remotes/origin/HEAD`。

**工作區不必乾淨**，有沒有 commit 過都能派——subagent 動手前會自己建快照，範圍是當前 branch 相對主幹的所有變更（含還沒 commit 的）。

## 派工

用 Agent tool，`subagent_type: "comment-cleanup:comment-cleanup"`——plugin 提供的 agent 帶 plugin 前綴，前面是 plugin 名後面是 agent 名。可用清單裡只有不帶前綴的 `comment-cleanup` 就用那個。

subagent 看不到你的對話歷史，所以 prompt 要自含：

```
清理這個 repo 本次 feature 的 code 註解。
base 分支：<你確認的 base>
範圍：<使用者指定的路徑，含 `/comment-cleanup <路徑>` 帶進來的參數；沒指定就寫「本次改動，自行用 git merge-base 定範圍」>
使用者的額外要求：<原話；沒有就寫「無」>
```

使用者明講要背景跑就 `run_in_background: true`，否則前景等它。

## 收到回報後

subagent 的回報就是報告本身，不會落檔，你這裡是使用者唯一看得到它的地方。轉述以下幾項，其中 `壓縮` before/after、擱置理由、`建議改 code`、有價值的刪除內容四項要**原文照轉**，不要摘要：

- verdict：`COMMITTED`（附 sha）／`APPLIED`（套用了但沒 commit，工作區原本就有變更）／`REPORT-ONLY`（未過閘門，已還原）／`NOTHING-TO-DO`
- 統計：刪 N 條、壓縮 M 條、留報告 K 條
- 閘門與 typecheck/lint 的實際結果
- 快照的絕對路徑
- 沒被清到的 untracked 檔案（有的話）
- 每一條 `壓縮` 的 before/after 原文
- 擱置不動的條目與理由
- `建議改 code` 清單
- 刪掉但對團隊有價值的內容
- 需要使用者接手的事：`建議改 code` 幾項、有沒有判不準而擱置的

`APPLIED` 時要讓使用者知道：變更在工作區等他一起 commit，要退回就從快照複製。
`REPORT-ONLY` 時把原因講具體，並說明工作區已還原、沒有留下半套變更。
