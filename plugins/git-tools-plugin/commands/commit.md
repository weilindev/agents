---
description: 建立格式良好的 Git commit，使用 conventional commits 格式
---

請協助使用者建立高品質的 Git commit。執行以下步驟：

## 1. 預檢查（Pre-commit Checks）

除非使用者指定 `--no-verify`，否則自動執行以下檢查：
- 執行 `npm run lint` 或 `pnpm lint` 或 `bun lint`（如果存在）
- 執行 `npm run build` 或 `pnpm build` 或 `bun build`（如果存在）
- 如果檢查失敗，詢問使用者是否要繼續還是先修復問題

## 2. 檢查 Git 狀態

- 執行 `git status` 查看哪些檔案被 stage
- 如果沒有檔案被 stage，自動執行 `git add .` 加入所有變更
- 執行 `git diff --staged` 了解變更內容
- 執行 `git log --oneline -10` 查看最近的 commit 訊息風格

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

使用 **Conventional Commits** 格式：

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

### 訊息撰寫原則

1. **使用現在式、祈使語氣**：例如 "add feature" 而非 "added feature"
2. **首行保持簡潔**：不超過 72 字元
3. **描述「為什麼」而非「什麼」**：diff 已經顯示了「什麼」變更了
4. **每個 commit 應該是原子性的**：代表單一目的的相關變更

## 5. 執行 Commit

使用 HEREDOC 格式建立 commit 以確保格式正確：

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

良好的 commit 訊息：
- feat: add user authentication system
- fix: resolve memory leak in rendering process
- docs: update API documentation with new endpoints
- refactor: simplify error handling logic in parser
- fix: resolve linter warnings in component files
- fix: patch critical security vulnerability in auth flow
- style: reorganize component structure for better readability
- feat: add TypeScript type definitions for API
- fix: resolve failing CI pipeline tests
- fix: strengthen password requirements
