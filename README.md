# WeilinDev Claude Code Marketplace

歡迎來到 WeilinDev 官方 Claude Code 插件市場！這個市場提供各種實用的插件來增強你的 Claude Code 開發體驗。

## 📦 快速開始

### 安裝市場

在 Claude Code 中執行以下命令來新增這個市場：

```bash
/plugin marketplace add weilindev/weilindev-marketplace
```

或者如果你使用 Git URL：

```bash
/plugin marketplace add https://github.com/weilindev/weilindev-marketplace.git
```

### 瀏覽和安裝插件

新增市場後，使用以下命令瀏覽可用的插件：

```bash
/plugin
```

然後從清單中選擇你想要安裝的插件。

## 🔌 可用插件

### Git Tools Plugin

**功能：** Git 工具插件，提供智慧化的 Git 操作功能

**包含：**
- `/commit` - 智慧 Commit 產生器，使用 Conventional Commits 和 emoji
- 自動預檢查（lint、build）
- 智慧分析變更並建議拆分 commit
- 安全保護機制

**安裝：**
```bash
/plugin install git-tools-plugin
```

## 📁 專案結構

```
weilindev-marketplace/
├── .claude-plugin/
│   └── marketplace.json          # Marketplace 配置文件
├── plugins/
│   └── git-tools-plugin/         # Git 工具插件
│       ├── .claude-plugin/
│       │   └── plugin.json       # 插件元數據
│       ├── commands/
│       │   └── commit.md         # 智慧 commit 產生器
│       └── README.md             # 插件說明文件
└── README.md
```

## 🛠️ 建立自己的插件

### 基本插件結構

每個插件都需要以下基本結構：

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json              # 必需：插件元數據
├── commands/                     # 可選：自訂指令
│   └── my-command.md
├── agents/                       # 可選：自訂代理
│   └── my-agent.md
└── hooks/                        # 可選：事件鉤子
    └── hooks.json
```

### plugin.json 範例

```json
{
  "name": "my-plugin",
  "description": "我的第一個插件",
  "version": "1.0.0",
  "author": {
    "name": "Your Name",
    "email": "[email protected]"
  },
  "keywords": ["example", "tutorial"],
  "category": "productivity"
}
```

### 將插件加入市場

1. 在 `plugins/` 目錄中建立你的插件
2. 更新 `.claude-plugin/marketplace.json`，將你的插件加入 `plugins` 陣列
3. 提交並推送到你的 Git 倉庫

## 📚 相關文檔

- [Claude Code 官方文檔](https://docs.claude.com/en/docs/claude-code)
- [Plugin 開發指南](https://docs.claude.com/en/docs/claude-code/plugins)
- [Plugin Marketplace 文檔](https://docs.claude.com/en/docs/claude-code/plugin-marketplaces)
- [MCP Server 文檔](https://docs.claude.com/en/docs/claude-code/mcp)

## 🤝 貢獻

歡迎提交 Pull Request 來新增新的插件或改進現有插件！

### 貢獻步驟

1. Fork 這個倉庫
2. 建立你的功能分支 (`git checkout -b feature/AmazingPlugin`)
3. 在 `plugins/` 目錄中建立你的插件
4. 更新 `.claude-plugin/marketplace.json`
5. 提交你的更改 (`git commit -m 'Add some AmazingPlugin'`)
6. 推送到分支 (`git push origin feature/AmazingPlugin`)
7. 開啟一個 Pull Request

## 📝 授權

MIT License - 詳見 LICENSE 文件

## 📧 聯絡方式

- Email: tawilliam527824@gmail.com

---

**注意：** 這是 Claude Code 的最新功能（2025 年推出）。確保你使用的是最新版本的 Claude Code 來獲得最佳體驗。
