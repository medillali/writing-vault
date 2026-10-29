# 网页端、Dot与本地协作入口

项目以两个公开Git仓库共同保存。**开工先读最新main中的本页与[当前状态](project/CURRENT-STATE.md)**，再读[资料总入口](START-HERE.md)、目标书正式研究与检查点。文件优先于旧聊天中的进度描述。

| 仓库 | 保存什么 | 入口 |
|---|---|---|
| [medillali/writing-vault](https://github.com/medillali/writing-vault) | 研究主档、人物、图、阅读副本、历史、检查点、创作框架与执行资料 | [START-HERE](START-HERE.md) · [内容审阅](library/reports/collection/内容审阅.md) |
| [medillali/distill-novels](https://github.com/medillali/distill-novels) | 蒸馏工具、Schema、验证、交接与使用文档 | [SKILL.md](https://github.com/medillali/distill-novels/blob/main/SKILL.md) · [工具使用指南](https://github.com/medillali/distill-novels/blob/main/docs/使用指南.md) |

## 直接交给新端的续接说明

[可复制的跨端续接提示](project/CROSS-END-PROMPT.md)包含仓库地址、当前重点、事实边界与保存要求。无需新建空资料库，也不要重新从开篇迁移已经完成的全书研究。

当前重点是让剧情地图与人物档案真正服务后续创作。[《纵横天下》全书树](library/reports/zongheng-tianxia/atlas/map.md)、[完整人物库](library/reports/zongheng-tianxia/atlas/characters.md)是最新实作；其他书的新一轮内容重整继续按作者顺序推进。

## 有本地文件系统的端

将两仓库克隆到同一父目录，目录名保持如下：

~~~text
Novel/
  distill-novels/
  writing-vault/
~~~

~~~text
git clone -c core.longpaths=true https://github.com/medillali/distill-novels.git
git clone -c core.longpaths=true https://github.com/medillali/writing-vault.git
python distill-novels/scripts/library.py --vault writing-vault status
~~~

Windows建议将两仓库放在C:/Novel这类较短的父路径，防止运行测试或重建时超过程序自身的路径上限。克隆时使用上面的-c core.longpaths=true，将长路径支持写入该仓库配置，避免深层审计档案检出失败；不修改系统设置。已有检出失败的副本应先保留自己的改动，再在该仓库设置git config core.longpaths true并补检出缺失文件。

核心验证只需Python 3.10+。原图已保存PNG、SVG及内嵌数据的离线HTML；阅读现有成果不必重新生成。重新布局地图才需对应README列出的Node、Graphviz/Viz及浏览器依赖。

父目录原有入口和创作框架保存在[project/workspace](project/workspace/README.md)；需要恢复原目录布局时再按说明复制。执行记录在[project/planning](project/planning/)，历史工作稿在[project/tool-work](project/tool-work/)，导出包在[project/exports](project/exports/)。这些是过程档案，当前事实仍以library与exchanges/runs为准。

## 只有仓库读取能力的端

先读取本页、CURRENT-STATE和目标书审阅入口，再按任务加载具体人物、事件与证据，避免一次加载全库。只读端提出修改时给出文件路径、asset_id、当前revision和明确的替换内容；可返回带基线的changes.json，由具备文件与Git能力的端按[交接流程](https://github.com/medillali/distill-novels/blob/main/references/chatgpt-handoff.md)预览并回收。

没有原文的端可以分析和整理已存研究；需要新增逐章亲读或核对正文时，必须另行取得用户提供的原文件。仓库里的章号索引不是小说正文。

## 多端写入约定

每端开始前拉取最新main并检查现有改动；并行工作使用各自codex/分支，记录改动对象与基线。人物和图主档通过既有工具保存，生成更新加--generated，保留人工笔记、收藏和审阅状态；不直接拼合冲突JSON，也不强制推送。

完成一批后提交可核验的研究与验证记录。推送之后读取远端提交和关键文件，再报告同步成功。另一端先更新仓库再续接，不能把旧聊天状态当作仓库最新状态。

本地工具原origin是上游，只向personal推送个人工具分支；资料库向origin/main推送。新端克隆个人工具库时origin即个人仓库，应按实际remote核对，不能机械套用本机名称。

## 同步范围

本次覆盖研究主档、版本历史、全书报告、地图与人物阅读副本、正式检查点、跨书目录、创作框架、工作台、执行计划、实际验证与交接包。原小说及规范化全文、凭据、本机缓存、重复恢复副本、依赖下载包和备份ZIP不纳入公开Git。

[本机归档文件清单](project/sync/local-inputs-manifest.json)逐项记录外层材料的路径与SHA-256；[同步验收回执](project/sync/2026-10-30-receipt.json)记录实际推送与远端克隆结果。本页提供协作入口，不表示仓库内容会自动进入任何聊天的上下文或记忆。
