# Novel 工作区

默认使用简体中文。这里包含既有创作框架、小说蒸馏工具和独立个人资料库，处理小说任务时按需读取。

- 工具入口：`distill-novels/SKILL.md`；详细操作：`distill-novels/docs/使用指南.md`。
- 真实长期资料库：`writing-vault/`。新会话先检查其来源、项目和必要检查点，再继续工作；不要每次重新建库。
- 多书管理入口：`writing-vault/library/reports/collection/README.md`；作者顺序与活动来源保存在同目录 `catalog-config.json`，实际阅读以 `exchanges/runs/` 检查点为准。
- 用户要求按作者实际写作顺序推进：失落叶本轮为《网游之纵横天下》→《网游之天下无双》→《斩龙》。三书全量研究已保存，后续内容重整状态见总审阅入口，建档、读完与用户认可须分开；《贼胆》旧研究已迁入，保留旧资料及分段观察，不重复建库。读取章节前同时检查 `collection/reading-units.json` 的合章与误识别片段映射。
- 2026-10-25用户已要求按《超级骷髅兵》标准完成失落叶三书全量蒸馏。沿既有100章续接，逐卷九维、全书人物弧/主暗线/疑点和综合验收，不再询问抽样深度或逐卷确认。执行状态在`.planning/20261023-shiluoye/full-research/`，正式覆盖仍以资料库检查点为准。
- 本机命令：`novel.cmd <子命令>`。直接运行代码时，优先发现可用 Python；本机应用自带运行时位于 `%USERPROFILE%/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe`。
- 蒸馏时阅读实际章节，区分事实、推断、抽象机制和原创项目设定。用 `scripts/library.py` 保存卡片、版本与图；生成更新加 `--generated` 保护人工笔记。
- `distill-novels/work/demo-final/` 仅是原创演示，不要作为用户已有作品或真实蒸馏成果导入 `writing-vault`。
- 用户后续已要求建Git仓库：工具库 `medillali/distill-novels` 与资料库 `medillali/writing-vault` 均已按用户要求设为公开仓库，2026-10-30已重新查询确认。本机工具分支 `codex/persistent-fiction-library` 推送 `personal HEAD:main`，原 `origin` 为上游；资料库为 `origin/main`。编辑不会自动提交或推送。
- Space仍留后续；文件式工作包已可用。跨端协作从资料库 `COLLABORATION.md` 和 `START-HERE.md` 进入；本机GitHub CLI可读写，实际可读范围以各端连接权限为准。只有实际完成远程操作后，才能报告上传或同步成功；不得将GitHub保存称为ChatGPT记忆同步。
- 保留根目录既有创作框架文档，按当前任务范围操作；本文件不授权外部发布或消息发送。

- 2026-10-30用户授权完整同步两仓库的项目内容。外层创作框架、工作台、执行计划与交接包归档到writing-vault/project/；原小说、运行恢复副本和备份ZIP继续留本机。提交同步后的实际核验回执见project/sync/。
