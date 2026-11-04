# 网页端、Dot与本地协作入口

项目以两个公开Git仓库共同保存。**开工先读最新main中的本页与[当前状态](project/CURRENT-STATE.md)**，再读[资料总入口](START-HERE.md)、目标书正式研究与检查点。文件优先于旧聊天中的进度描述。

| 仓库 | 保存什么 | 入口 |
|---|---|---|
| [medillali/writing-vault](https://github.com/medillali/writing-vault) | 研究主档、人物、图、阅读副本、历史、检查点、创作框架与执行资料 | [START-HERE](START-HERE.md) · [内容审阅](library/reports/collection/内容审阅.md) |
| [medillali/distill-novels](https://github.com/medillali/distill-novels) | 蒸馏工具、Schema、验证、交接与使用文档 | [SKILL.md](https://github.com/medillali/distill-novels/blob/main/SKILL.md) · [工具使用指南](https://github.com/medillali/distill-novels/blob/main/docs/使用指南.md) |

## 直接交给新端的续接说明

[可复制的跨端续接提示](project/CROSS-END-PROMPT.md)包含仓库地址、当前重点、事实边界与保存要求。无需新建空资料库，也不要重新从开篇迁移已经完成的全书研究。

当前先集中处理《罪恶之城》，交付重点是清晰可探索的剧情树与连贯、可积累、可追溯的人物卡库。网页端研究历史用于回查线索，具体事实仍核对原文；其他故事资产最后处理。正文阅读完成、图卡收束、真实 PC／手机交互与下载验证、用户最终验收分别记录，不能互相替代。

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

每端开始前先检查现有工作树、未提交改动、远程仓库和最新 main；保留正在进行的工作，再以最新 main 为基线使用独立 codex/ 分支，记录改动对象与基线。人物和图主档通过既有工具保存，生成更新加--generated，保留人工笔记、收藏和审阅状态；不直接拼合冲突JSON，也不强制推送。

每轮任务结束后，先完成适合本轮范围的检查，并逐项审阅拟公开的文件与实际 diff；只提交确认可以公开的工程、成果与验证记录。将独立分支推送到已核实的个人仓库，并创建以 main 为目标的 Pull Request（PR）。已有同一轮、同一范围的 PR 时更新它，避免重复创建。

不得直接推送 main，也不自动合并、启用自动合并或部署。公开范围无法确定的内容留在本地并报告；没有安全的可提交变更或遇到权限阻碍时，如实说明。报告仓库、分支、提交、PR 链接、检查结果及剩余阻碍。创建或更新后读回 PR 的文件清单、差异和头提交，确认没有混入其他任务。PR 创建、检查通过、已合并和用户验收是不同状态。

另一端续接时同时核对 main、相关开放 PR 与本地私有检查点；未合并 PR 不等于 main 已更新，旧聊天也不替代文件状态。

本地工具原 origin 是上游，只向已核实的 personal 个人仓库分支推送；资料库也只向已核实的 origin 独立分支推送，再开 PR。新端克隆个人工具库时 origin 即个人仓库，应按实际 remote 核对所有者和目标，不能机械套用本机名称。

## 同步范围

公开同步采用逐文件确认的范围，不把研究目录、历史或交接包整体默认上传。原小说及规范化全文、密钥和凭据、私人笔记、私密工作文件、本机缓存、重复恢复副本、依赖下载包和备份 ZIP 不纳入公开 Git。阅读副本与导出文件同样检查内容，不能因为它们由程序生成就视为可公开。保留用户人工数据；为了显示或发布而脱敏时制作阅读副本，不能修改原始人物档。

[本机归档文件清单](project/sync/local-inputs-manifest.json)逐项记录外层材料的路径与SHA-256；[同步验收回执](project/sync/2026-10-30-receipt.json)记录实际推送与远端克隆结果。本页提供协作入口，不表示仓库内容会自动进入任何聊天的上下文或记忆。

