# CLAUDE.md

## 這個 repo 是什麼

weilindev 個人工作流用的 Claude Code plugin marketplace。

## 文件慣例

- 一律 zh-TW，不使用 emoji
- 根目錄 README 保持簡短：定位、安裝、插件一覽、授權即可。插件的完整說明放在該插件自己的 README
- commit 用 conventional commits，subject 寫 zh-TW（`feat:` / `fix:` / `docs:` / `chore:`，破壞性變更用 `feat!:`）

## 新增或修改插件

插件放在 `plugins/<name>/`，基本結構：

```
plugins/<name>/
├── .claude-plugin/plugin.json    # 插件元數據
├── skills/<skill>/SKILL.md       # 技能（新插件用這個，不用舊式 commands/）
├── agents/<agent>.md             # 可選：自訂 subagent
└── README.md
```

新增插件要同時更新 `.claude-plugin/marketplace.json` 的 `plugins` 陣列。

**版本號有兩處，必須一致**：`plugins/<name>/.claude-plugin/plugin.json` 的 `version` 與 `marketplace.json` 對應項目的 `version`。改版本時兩邊一起改。

改完驗證兩層 manifest：

```bash
claude plugin validate .
claude plugin validate ./plugins/<name> --strict
```

## comment-cleanup

改過 `plugins/comment-cleanup/scripts/verify-comment-diff.py` 就跑一次閘門的回歸測試：

```bash
bash plugins/comment-cleanup/scripts/test-gate.sh
```

架構上有一條不能破壞的界線：`SKILL.md` 只負責派工與轉述，判準的唯一來源是 `rules.md`，執行流程在 `agents/comment-cleanup.md`。三者職責不可互相搬移——subagent 讀 `rules.md` 而不讀 `SKILL.md`，否則會讀到「去派 subagent」而遞迴。理由與閘門、快照機制寫在 [plugins/comment-cleanup/README.md](plugins/comment-cleanup/README.md)，不要在別處重述。
