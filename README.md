**[按书名、作者、小说类型浏览书库](书库/README.md)** · **[全书剧情地图](书库/全书剧情地图/README.md)**

# 我的小说资料库

人物、场景、创作机制位于`library`，原创作品位于`books`。JSON为主档，`library/views`为生成的阅读副本，版本历史位于`history`。这是实际个人资料库，未混入演示素材。

## 当前可审查成果

- **[全书地图：拖动、缩放、查看交汇](library/reports/super-skeleton/reading/plot/map.md)**（默认入口）：PC与Codex中像地图一样浏览整本书，附GitHub原图和清晰局部预览。

- **[PC／手机剧情阅读器](library/reports/super-skeleton/reading/plot/reader.md)**：PC分阶段看关系图，手机沿事件卡片阅读；支线跳转、全部前因后果与原位返回。可下载单文件离线使用，进度支持导出导入。

- **[全书一张大树图](library/reports/super-skeleton/reading/plot/whole-book.md)**：从主线分枝、旁支另起，在共享事件交汇；包含163个事件与15条暗线，提供完整PNG、SVG和可拖动缩放的离线页面。
- **[主线与暗线图片版](library/reports/super-skeleton/reading/plot/images.md)**：49张PNG及SVG，沿主线时间推进，明确标注部分回收和未回收的暗线。
- **[《超级骷髅兵》GitHub直接阅读入口](library/reports/super-skeleton/reading/README.md)**：18集完整研究、九维综合、226张中文卡片、主线树与暗线网络、198项疑点回收。
- [人物卡](library/reports/super-skeleton/reading/characters.md) · [场景卡](library/reports/super-skeleton/reading/scenes.md) · [机制卡](library/reports/super-skeleton/reading/patterns.md) · [剧情与暗线](library/reports/super-skeleton/reading/plot/README.md)。点击标题即可阅读，无需下载HTML。
- [全书综合报告](library/reports/super-skeleton/book-synthesis.md)、[疑点账本](library/reports/super-skeleton/question-ledger.md)、[验收说明](library/reports/super-skeleton/验收说明.md)。
- [本机交互审查页](library/views/超级骷髅兵全书审查.html)：需要下载仓库后用浏览器打开，提供搜索、筛选和可缩放剧情图。
- [四书开篇样段入口](library/views/四书实测.html)：保留原先开篇测试。《骷髅魔导师》《重生之贼行天下》《网游之纵横天下》尚未全书蒸馏。
- [卡片目录](library/views/index.md)：当前资料的Markdown副本。研究解释和用户评价分开；所有新研究仍待用户审阅，未自动收藏。

## 保存与恢复

私有资料库：[medillali/writing-vault](https://github.com/medillali/writing-vault)，`main`分支。独立私有工具库：[medillali/distill-novels](https://github.com/medillali/distill-novels)。保存卡片会维护历史，但不会自动进行Git提交；更新后校验、检查diff、按范围提交并推送。

换机将两个仓库克隆到相邻短目录，用工具的`scripts/library.py`读写资料。专用审查页可单独运行`library/reports/super-skeleton/rebuild_review.py`重建，无需原小说。图的重新生成需要工具库，已生成的图可直接离线打开。工作区`novel.cmd`只是本机入口，换机不依赖它。

全库ZIP备份保存研究主档与历史，离线审查ZIP提供直接阅读副本。审查页能筛选与查看，不能直接保存个人备注；持久编辑须通过资料库工具。原TXT仅在本机`private-sources`，不在Git历史或默认备份中；核对原文需要另行携带原书和一致修订。

检查点在`exchanges/runs`，新会话从既有来源和检查点接续，不能重建空库覆盖资料。Space尚未接入，GitHub保存不会自动写入ChatGPT记忆；文件工作包可用于双端衔接，新私库的连接访问范围仍需后续配置。
