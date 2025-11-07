---
description: 建立格式良好的 Git commit，使用 conventional commits 格式
---

請協助使用者建立高品質的 Git commit。執行以下步驟：

## 1. 預檢查（Pre-commit Checks）

除非使用者指定 `--no-verify`，否則自動執行以下檢查：

### 執行檢查

使用偵測到的套件管理器執行以下檢查（如果 package.json 中定義了這些 scripts）：
- 執行 `<套件管理器> run lint`（如果存在）
- 執行 `<套件管理器> run build`（如果存在）
- 如果檢查失敗，詢問使用者是否要繼續還是先修復問題

## 2. 檢查 Git 狀態與語言分析

- 執行 `git status` 查看哪些檔案被 stage
- 如果沒有檔案被 stage，自動執行 `git add .` 加入所有變更
- 執行 `git diff --staged` 了解變更內容
- 執行 `git log --oneline -20` 查看最近的 commit 訊息風格

### **關鍵：語言決策（必須執行）**

**分析最近 20 筆 commit 訊息的語言分佈：**
1. 統計中文、英文、其他語言的 commit 數量
2. 判斷主要使用的語言（佔比超過 50% 視為主要語言）
3. **如果中文佔比 ≥ 30%，必須使用中文**
4. 如果無法判斷或 repository 是新建的，**預設使用繁體中文（zh-TW）**

**語言決策範例：**
- 15 筆中文 + 5 筆英文 → 使用中文 ✓
- 10 筆中文 + 10 筆英文 → 使用中文 ✓（參考用戶偏好）
- 8 筆中文 + 12 筆英文 → 使用中文 ✓（中文佔 40%）
- 2 筆中文 + 18 筆英文 → 使用英文
- 無歷史記錄 → 使用繁體中文 ✓（用戶偏好）

## 3. 分析變更

仔細分析 diff 內容，判斷是否包含多個不同的邏輯變更：

**應該拆分 commit 的情況：**
- 變更涉及不相關的程式碼區域
- 混合了不同類型的變更（例如：feature + bugfix）
- 變更了不同類型的檔案（例如：程式碼 + 文件）
- 變更太大，拆分後更容易審查

**如果需要拆分：**
- 建議使用者將變更拆分成多個 commit
- 協助使用者用 `git add -p` 或指定檔案來分階段 commit

## 4. 建立 Commit 訊息

**開始撰寫前，再次確認已完成步驟 2 的語言決策！**

使用 **Conventional Commits** 格式，並**嚴格遵守步驟 2 決定的語言**：

### Commit 類型說明

- `feat`: 新功能
- `fix`: Bug 修復
- `docs`: 文件變更
- `style`: 程式碼格式調整（不影響功能）
- `refactor`: 重構（既非新功能也非 bug 修復）
- `perf`: 效能改善
- `test`: 測試相關
- `chore`: 建置工具、設定檔等
- `ci`: CI/CD 改善
- `build`: 建置系統或外部依賴變更
- `revert`: 回復先前的 commit

### Commit 訊息格式

```
<type>: <簡短描述>

<可選的詳細說明>
```

**重要：**
- `<type>` 永遠使用英文（feat, fix, docs 等），這是 Conventional Commits 的標準
- `<簡短描述>` 和 `<詳細說明>` 使用步驟 2 決定的語言
- 範例：`feat: 新增使用者認證系統`（類型英文 + 描述中文）

### 訊息撰寫原則

1. **類型前綴永遠使用英文，描述使用步驟 2 決定的語言**：
   - 正確：`feat: 新增使用者認證系統`
   - 正確：`fix: add user authentication`
   - 錯誤：`功能: 新增使用者認證系統`（類型不應翻譯）
   - 錯誤：`feat: 新增 authentication system`（不要混用語言）

2. **使用現在式、祈使語氣**：
   - 中文：「新增功能」、「修復問題」（而非「已新增」、「已修復」）
   - 英文："add feature", "fix issue" (而非 "added", "fixed")

3. **首行保持簡潔**：不超過 72 字元

4. **描述「為什麼」而非「什麼」**：diff 已經顯示了「什麼」變更了

5. **每個 commit 應該是原子性的**：代表單一目的的相關變更

## 5. 執行 Commit

使用 HEREDOC 格式建立 commit 以確保格式正確：

**中文範例：**
```bash
git commit -m "$(cat <<'EOF'
feat: 新增使用者認證系統

實作基於 JWT 的認證機制，包含登入和登出功能
EOF
)"
```

**英文範例：**
```bash
git commit -m "$(cat <<'EOF'
feat: add user authentication system

Implement JWT-based authentication with login and logout endpoints
EOF
)"
```

## 6. 驗證結果

- 執行 `git status` 確認 commit 成功
- 如果 pre-commit hook 修改了檔案，檢查是否需要 amend：
  - 確認作者身份：`git log -1 --format='%an %ae'`
  - 確認尚未 push：`git status` 顯示 "Your branch is ahead"
  - 如果兩者都確認，可以使用 `git commit --amend`
  - 否則，建立新的 commit

## 注意事項

- **絕不** 修改 git config
- **絕不** 執行破壞性 git 命令（如 `push --force`、`hard reset`）除非使用者明確要求
- **絕不** 跳過 hooks（`--no-verify`、`--no-gpg-sign`）除非使用者明確要求
- **絕不** force push 到 main/master 分支
- **避免** `git commit --amend`，除非：(1) 使用者明確要求，或 (2) 在處理 pre-commit hook 的修改
- **只在使用者明確要求時才建立 commit**

## 範例

良好的 commit 訊息範例（類型前綴永遠使用英文，描述根據步驟 2 決定的語言）：

**中文範例（推薦）：**
- `feat: 新增使用者認證系統`
- `fix: 修復渲染過程中的記憶體洩漏`
- `docs: 更新 API 文件與新端點`
- `refactor: 簡化解析器中的錯誤處理邏輯`
- `perf: 優化資料庫查詢效能`
- `test: 新增使用者登入測試案例`

**英文範例：**
- `feat: add user authentication system`
- `fix: resolve memory leak in rendering process`
- `docs: update API documentation with new endpoints`
- `refactor: simplify error handling logic in parser`
- `perf: optimize database query performance`
- `test: add user login test cases`

**關鍵提醒：**
1. **類型前綴（feat, fix 等）永遠使用英文** - 這是 Conventional Commits 的標準
2. **描述部分必須執行步驟 2 的語言決策** - 分析歷史 commit 語言，中文佔比 ≥ 30% 就使用中文
3. **不要混用語言** - 整個描述（包括詳細說明）都要使用同一種語言
