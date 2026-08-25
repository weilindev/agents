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

預設範圍是本次改動（`git merge-base` 之後的 diff），也可以指定路徑。

## 核心規則

**鐵則：只改註解，不改 code。** 一行可執行的 code 都不動，產出一份每個 `+`／`-` 都是註解行的 diff — 可以不看就 merge。發現該改的 code 會寫進報告，不動手。

每條註解過兩道判準，任一關不過就刪：

1. **看 code 能不能懂？** 能懂就刪 — 註解不該複述 code 已經說出口的事。
2. **是不是過程與轉折？** 是就刪 — 「原本用 X 後來改 Y」屬於 commit message 與 PR，不屬於 code。留結論，不留推導。

值得留下的共通點是：**讀者不知道就會改壞，而 code 與型別都攔不住他** — 不變式、反直覺的選擇、外部依據、跨檔耦合、安全性理由、演算法出處。

有功能的註解（`eslint-disable`、`@ts-expect-error`、授權標頭、對外 SDK 的 JSDoc 等）一律不動。

## 流程

定範圍 → 先看鄰居的註解密度 → 逐條判定（刪／留／壓縮／建議改 code）→ **回報清單給你確認後才套用** → 驗證 `git diff` 每行都是註解。

想跳過確認直接套用，在訊息裡加「直接改」或 `--apply`。

完整規則見 `skills/comment-cleanup/SKILL.md`。

## 授權

MIT
