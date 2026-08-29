# weilindev Claude Code Marketplace

個人工作流用的 Claude Code plugin marketplace。

## 安裝

```bash
/plugin marketplace add weilindev/agents
```

新增後用 `/plugin` 瀏覽並安裝。

## 插件

### comment-cleanup

以第一性原理審查並清理 code 註解，只留下讀者無法從 code 本身得知的資訊。

- 鐵則：只改註解不改 code，產出可以不看就 merge 的純註解 diff
- 範圍是當前 branch 相對主幹的所有變更，含還沒 commit 的
- 由 subagent 執行，通過機械閘門才留下改動，不通過就從快照整批還原
- 工作區乾淨時落成單獨一顆 `chore:` commit，髒的時候只套用，交給你一起 commit

```bash
/plugin install comment-cleanup@weilindev
```

細節見 [plugins/comment-cleanup/README.md](plugins/comment-cleanup/README.md)。

## 相關文件

- [Claude Code 官方文件](https://code.claude.com/docs/en/overview)
- [Plugin 開發指南](https://code.claude.com/docs/en/plugins)
- [Plugin Marketplace 文件](https://code.claude.com/docs/en/plugin-marketplaces)

## 授權

MIT
