# 貢獻指南

感謝你對 WeilinDev Claude Code Marketplace 的興趣！我們歡迎所有類型的貢獻。

## 如何貢獻

### 回報 Bug

如果你發現 bug，請開啟一個 issue 並包含：
- Bug 的清楚描述
- 重現步驟
- 預期行為
- 實際行為
- 你的環境資訊（Claude Code 版本、作業系統等）

### 提議新功能

如果你有新功能的想法：
1. 先檢查是否已有相關的 issue
2. 開啟一個新的 issue 來討論你的想法
3. 等待維護者的回饋

### 貢獻插件

#### 新增新插件

1. **Fork 這個倉庫**

2. **建立你的插件**

   在 `plugins/` 目錄中建立一個新目錄：

   ```bash
   mkdir -p plugins/your-plugin-name/.claude-plugin
   mkdir -p plugins/your-plugin-name/commands
   mkdir -p plugins/your-plugin-name/agents
   mkdir -p plugins/your-plugin-name/hooks
   ```

3. **建立 plugin.json**

   ```json
   {
     "name": "your-plugin-name",
     "description": "你的插件描述",
     "version": "1.0.0",
     "author": {
       "name": "Your Name",
       "email": "[email protected]"
     },
     "keywords": ["keyword1", "keyword2"],
     "category": "productivity"
   }
   ```

4. **加入你的功能**

   - **Commands**: 在 `commands/` 目錄中建立 `.md` 檔案
   - **Agents**: 在 `agents/` 目錄中建立 `.md` 檔案
   - **Hooks**: 在 `hooks/` 目錄中建立 `hooks.json` 檔案

5. **更新 marketplace.json**

   在 `.claude-plugin/marketplace.json` 的 `plugins` 陣列中加入你的插件：

   ```json
   {
     "name": "your-plugin-name",
     "source": "./plugins/your-plugin-name",
     "description": "你的插件描述",
     "version": "1.0.0",
     "author": {
       "name": "Your Name"
     },
     "keywords": ["keyword1", "keyword2"],
     "category": "productivity"
   }
   ```

6. **建立 README**

   在你的插件目錄中建立 `README.md`，包含：
   - 插件描述
   - 功能列表
   - 安裝說明
   - 使用範例
   - 配置選項（如果有）

7. **本地測試**

   使用 Claude Code 測試你的插件：

   ```bash
   # 在你的專案目錄中
   /plugin marketplace add file:///path/to/your/weilindev-marketplace
   /plugin install your-plugin-name
   ```

8. **提交 Pull Request**

   ```bash
   git checkout -b feature/add-your-plugin
   git add .
   git commit -m "Add your-plugin-name plugin"
   git push origin feature/add-your-plugin
   ```

   然後在 GitHub 上開啟 Pull Request。

#### 改進現有插件

1. Fork 這個倉庫
2. 進行你的修改
3. 更新相關文檔
4. 增加 plugin 的版本號
5. 提交 Pull Request

## 插件開發最佳實踐

### Commands

- 使用清楚的命令名稱
- 在 frontmatter 中提供清楚的描述
- 使用 zh-TW 作為主要語言
- 提供詳細的指示和範例

### Agents

- 清楚定義代理的職責
- 說明可用的工具
- 提供工作流程指引
- 使用友好的語氣

### Hooks

- 預設停用需要使用者確認的 hooks
- 提供清楚的描述
- 考慮效能影響
- 記錄任何副作用

### 版本控制

遵循 [Semantic Versioning](https://semver.org/):
- MAJOR: 不相容的 API 變更
- MINOR: 向後相容的新功能
- PATCH: 向後相容的 bug 修復

### 文檔

- 保持 README 更新
- 包含使用範例
- 記錄所有配置選項
- 提供故障排除指南

## 程式碼審查流程

1. 維護者會審查你的 Pull Request
2. 可能會要求修改
3. 一旦核准，你的 PR 會被合併
4. 你的貢獻會出現在 contributors 列表中

## 社群準則

- 尊重所有貢獻者
- 建設性地提供回饋
- 專注於程式碼，而不是個人
- 幫助新手貢獻者

## 需要幫助？

如果你在貢獻過程中遇到任何問題：
- 查看現有的 issues 和 PR
- 開啟一個新的 issue 尋求幫助
- 聯絡維護者：[email protected]

## 授權

貢獻到這個專案即表示你同意你的貢獻將以 MIT 授權釋出。

---

再次感謝你的貢獻！ 🎉
