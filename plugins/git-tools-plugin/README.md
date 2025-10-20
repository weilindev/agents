# Git Tools Plugin

Git 工具插件，提供智慧化的 Git 操作功能，幫助你建立高品質的 commit 和管理版本控制。

## ✨ 功能

### `/commit` - 智慧 Commit 產生器

自動建立格式良好的 Git commit，使用 Conventional Commits 格式並加上視覺化的 emoji。

**主要特色：**

- 🔍 **自動預檢查**：執行 lint、build 等檢查確保程式碼品質
- 🧠 **智慧分析**：分析變更內容，建議是否拆分成多個 commit
- 🎯 **Conventional Commits**：自動產生符合規範的 commit 訊息
- 🎨 **Emoji 標記**：為每種 commit 類型加上對應的 emoji
- 📊 **變更審查**：檢查 git diff 和最近的 commit 風格
- ✅ **安全保護**：防止破壞性操作和不當的 commit

## 📦 安裝

```bash
/plugin install git-tools-plugin
```

## 🚀 使用方式

### 基本使用

```bash
/commit
```

這會執行完整的 commit 流程：
1. 執行 pre-commit 檢查（lint、build）
2. 檢查 git 狀態和變更
3. 分析是否需要拆分 commit
4. 產生適當的 commit 訊息
5. 執行 commit

### 跳過預檢查

```bash
/commit --no-verify
```

## 📝 Commit 類型和 Emoji

| Emoji | 類型 | 說明 | 範例 |
|-------|------|------|------|
| ✨ | `feat` | 新功能 | ✨ feat: add user authentication |
| 🐛 | `fix` | Bug 修復 | 🐛 fix: resolve memory leak |
| 📝 | `docs` | 文件更新 | 📝 docs: update API documentation |
| 💄 | `style` | 程式碼格式 | 💄 style: format code with prettier |
| ♻️ | `refactor` | 重構 | ♻️ refactor: simplify error handling |
| ⚡️ | `perf` | 效能改善 | ⚡️ perf: optimize database queries |
| ✅ | `test` | 測試 | ✅ test: add unit tests for auth |
| 🔧 | `chore` | 工具、設定 | 🔧 chore: update dependencies |
| 🚀 | `ci` | CI/CD | 🚀 ci: add GitHub Actions workflow |
| 🚑️ | `fix` | 緊急修復 | 🚑️ fix: patch security vulnerability |
| 🎨 | `style` | 程式碼結構 | 🎨 style: reorganize components |
| 🔥 | `refactor` | 移除程式碼 | 🔥 refactor: remove deprecated code |
| 🏷️ | `feat` | 型別定義 | 🏷️ feat: add TypeScript types |
| 💚 | `fix` | 修復 CI | 💚 fix: resolve failing tests |
| 🔒️ | `fix` | 安全修復 | 🔒️ fix: strengthen auth requirements |
| 🚸 | `feat` | 改善 UX | 🚸 feat: improve form validation |
| ♿️ | `feat` | 無障礙功能 | ♿️ feat: add ARIA labels |
| 💥 | `feat` | 破壞性變更 | 💥 feat: redesign API endpoints |
| 📦️ | `chore` | 套件更新 | 📦️ chore: update build output |
| ➕ | `chore` | 新增依賴 | ➕ chore: add lodash |
| ➖ | `chore` | 移除依賴 | ➖ chore: remove unused package |

## 💡 最佳實踐

### Commit 訊息撰寫

1. **使用祈使語氣**：`add feature` 而非 `added feature`
2. **首行簡潔**：不超過 72 字元
3. **描述「為什麼」**：解釋變更的原因，而非只說明「什麼」變更了
4. **原子性 commit**：每個 commit 應該代表單一目的的變更

### 何時拆分 Commit

應該將變更拆分成多個 commit 的情況：

- ✅ 變更涉及不相關的程式碼區域
- ✅ 混合了不同類型的變更（feature + bugfix）
- ✅ 同時修改程式碼和文件
- ✅ 變更太大，難以審查

### 範例

**好的 commit：**
```
✨ feat: add user authentication system

Implement JWT-based authentication with login and logout endpoints.
Includes middleware for protected routes and token refresh logic.
```

**不好的 commit：**
```
update stuff
```

## 🔒 安全機制

此插件包含多項安全保護：

- ❌ 不會修改 git config
- ❌ 不會執行破壞性命令（除非明確要求）
- ❌ 不會跳過 git hooks（除非使用 `--no-verify`）
- ❌ 不會 force push 到 main/master
- ❌ 謹慎使用 `--amend`

## 🤝 貢獻

歡迎提交 issue 或 pull request 來改進這個插件！

## 📄 授權

MIT License - 詳見 LICENSE 文件
