# 我的小说资料库

人物与剧情卡位于 library，原创作品位于 books。
完整 JSON 为主档，library/views 为生成的阅读副本。
原始小说放 private-sources，不随默认备份上传。

这是你的真实个人资料库，当前没有演示素材。可以把待分析文件放入 `private-sources/incoming/`，然后在 Novel 工作区请 Codex 分批蒸馏。工作区使用说明在 `../小说工作台.md`。

本目录已建立独立的本地 Git 仓库，尚未连接远程，也不会自动提交每次编辑。脚本保存卡片时会在 `history/` 中保留旧版；需要整体快照时从上级目录运行 `novel.cmd backup --output backups/新名称.zip`。

保存边界：来源索引、研究卡、抽象机制、原创项目、历史和工作包可以迁移。原始书籍、临时缓存和机器配置默认不进入资料库备份。以后准备好私人 GitHub 仓库和 Space 后再连接。
