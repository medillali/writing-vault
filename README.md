# 我的小说资料库

人物与剧情卡位于 library，原创作品位于 books。
完整 JSON 为主档，library/views 为生成的阅读副本。
原始小说放 private-sources，不随默认备份上传。

这是你的真实个人资料库，未导入演示素材。2026-10-22已登记《骷髅魔导师》《超级骷髅兵》《重生之贼行天下》《网游之纵横天下》四本全文来源，保存开篇16段研究：12人物卡、8场景卡、4机制卡、4图。

- [四书实测阅读入口](library/views/四书实测.html)：筛选卡片、查看章节证据、打开主线与暗线图。
- [卡片目录](library/views/index.md)：生成的Markdown阅读副本。
- [测试范围与证据](library/reports/2026-10-22-four-books.md)。这是开篇样段测试，尚未全书蒸馏。
- 分析检查点在 `exchanges/runs/`，后续继续使用既有来源ID与章节索引。卡片均为待审阅草稿，尚未替用户收藏。

可以把待分析文件放入 `private-sources/incoming/`，然后在Novel工作区请Codex分批蒸馏。工作区使用说明在 `../小说工作台.md`。

本目录已连接并推送到私有GitHub仓库 [medillali/writing-vault](https://github.com/medillali/writing-vault)，分支 `main`、远程 `origin`。2026-10-22已从GitHub重新克隆，验证24卡、4图、4检查点、备份恢复与工作包往返。它不会自动提交每次编辑；脚本保存卡片时会在 `history/` 中保留旧版。

工具与 [换机恢复说明](https://github.com/medillali/distill-novels/blob/main/docs/GitHub与换机恢复.md) 在独立私有仓库 [medillali/distill-novels](https://github.com/medillali/distill-novels)。换机时将两库克隆到相邻短目录，使用工具中的 `scripts/library.py`；根工作区的 `novel.cmd` 是本机入口，不随这两个仓库克隆。

完成修改后先校验、查看diff，再选择文件提交并运行 `git push origin main`。需要整体快照时，本机可从上级目录运行 `novel.cmd backup --output backups/新名称.zip`。

保存边界：来源索引、研究卡、抽象机制、原创项目、历史和工作包可以迁移。原始书籍、临时缓存和机器配置不在已推送的Git历史中，也默认不进入ZIP备份。Space尚未接入，GitHub保存不会自动写入ChatGPT记忆；从ChatGPT连接读取新私库还需配置对应仓库权限。
