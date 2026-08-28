# WeilinDev Claude Code Marketplace

歡迎來到 WeilinDev 官方 Claude Code 插件市場！這個市場提供各種實用的插件來增強你的 Claude Code 開發體驗。

## 📦 快速開始

### 安裝市場

在 Claude Code 中執行以下命令來新增這個市場：

```bash
/plugin marketplace add weilindev/agents
```

或者如果你使用 Git URL：

```bash
/plugin marketplace add https://github.com/weilindev/agents.git
```

### 瀏覽和安裝插件

新增市場後，使用以下命令瀏覽可用的插件：

```bash
/plugin
```

然後從清單中選擇你想要安裝的插件。

## 🔌 可用插件

### Comment Cleanup

**功能：** 以第一性原理審查並清理 code 註解，只留下讀者無法從 code 本身得知的資訊

**包含：**
- `/comment-cleanup:comment-cleanup` - 入口，派 `comment-cleanup` subagent 執行，可背景跑
- 範圍是當前 branch 相對主幹的所有變更，**還沒 commit 的也算**
- 鐵則：只改註解不改 code，產出可以不看就 merge 的純註解 diff
- 兩道判準：看 code 能不能懂／是不是過程與轉折
- 保護有功能的註解（eslint-disable、授權標頭、對外 SDK JSDoc 等）
- 機械閘門：剝除註解後比對 code 是否逐行相同，不同就從快照整批還原
- 工作區乾淨時落成單獨一顆 `chore:` commit；髒的時候只套用，交給你一起 commit

**安裝：**
```bash
/plugin install comment-cleanup@weilindev
```

## 📁 專案結構

```
agents/
├── .claude-plugin/
│   └── marketplace.json                  # Marketplace 配置文件
├── plugins/
│   └── comment-cleanup/                  # 註解清理插件
│       ├── .claude-plugin/
│       │   └── plugin.json               # 插件元數據
│       ├── skills/
│       │   └── comment-cleanup/
│       │       ├── SKILL.md              # 入口：只負責派工與轉述
│       │       └── rules.md              # 判準的唯一來源
│       ├── agents/
│       │   └── comment-cleanup.md        # 執行流程：閘門、驗證、commit
│       ├── scripts/
│       │   ├── verify-comment-diff.py    # 機械閘門：驗證 diff 純屬註解
│       │   └── test-gate.sh              # 閘門的回歸測試（17 案例）
│       └── README.md                     # 插件說明文件
└── README.md
```

## 🛠️ 建立自己的插件

### 基本插件結構

每個插件都需要以下基本結構：

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json              # 可選：插件元數據
├── skills/                       # 建議：技能（新插件用這個）
│   └── my-skill/
│       └── SKILL.md
├── commands/                     # 可選：舊式扁平指令檔（legacy）
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
2. 更新 `.claude-plugin/marketplace.json`，將你的插件加入 `plugins` 陣列（`version` 要與 `plugin.json` 一致）
3. 驗證兩層 manifest：

   ```bash
   claude plugin validate .
   claude plugin validate ./plugins/my-plugin --strict
   ```

4. 提交並推送到你的 Git 倉庫

## 📚 相關文檔

- [Claude Code 官方文檔](https://code.claude.com/docs/en/overview)
- [Plugin 開發指南](https://code.claude.com/docs/en/plugins)
- [Plugin Marketplace 文檔](https://code.claude.com/docs/en/plugin-marketplaces)
- [MCP Server 文檔](https://code.claude.com/docs/en/mcp)

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
