# 检查发现

## 2026-10-21
- 用户目标仓库：`mol632991-png/distill-novels`。
- 当前工作区：`C:\Users\Administrator\Documents\ChatGPT\Novel`。
- 本地 Git 为尚无提交的 master，无 remote；已有 docs 和远程附件目录，保留现状。
- 记忆索引未发现 Novel / 小说 / distill 的相关记录。
- 仓库为公开仓库，默认分支 main；当前 GitHub 连接报告 pull=true、push=false。
- 已核实目标是 Skill + 标准库 Python 预处理脚本，不是现成 Web 应用。
- 远程检查基准提交：`ede0e6a496e8907c02b8d9d4bd58034761932821`。
- 现有产物是按维度汇总的 Markdown 和每书分析；没有单卡存储、跨项目检索、图数据、备份恢复命令或测试。
- `prepare_sources.py` 的 source_id 为顺序编号 + 内容哈希。导入集合改变可能改变相同书籍的 ID；内容修订也改变 ID。需分别管理作品身份与内容修订。
- 每次运行直接重写 manifest.json；EPUB 按压缩包内文件名字典排序，未按 spine；章节仅记录标题，没有偏移位置。这些会影响增量保存和剧情因果分析。
- 本地 `docs/工作架构框架-v0.3.md` 已设计 Character Cards、Story Bible、Secret Table、Promise Ledger、Trope/Beat 经验库。该文档仍为设计，不是已实现能力；本次可以沿用参考与原创分离、事实与计划分离规则，不默认承接其市场与语言假设。
- 用户已明确：Codex 与 ChatGPT 两端都经常使用，需要方便衔接。
- 官方资料链接：Projects <https://learn.chatgpt.com/docs/projects>；Memories <https://learn.chatgpt.com/docs/customization/memories>；Space <https://learn.chatgpt.com/docs/space>。
- 官方文档核实：ChatGPT 网页记忆与 Codex 本地记忆分开；ChatGPT 项目需上传或连接文件，不能仅凭会话同步认定本地文件同步。设计上将记忆作为入口提示，完整资产保存到可版本化资料库。
- 已通过 Git OpenSSL TLS 后端克隆上游到 `Novel/distill-novels`，未更改全局 Git 设置或关闭证书校验。
- 基线实测已复现：添加排序靠前的 a.txt 后，b.txt 的 ID 从 `book-01-eedacd7d` 变为 `book-02-eedacd7d`。
- 基线实测已复现：同一输出目录先处理 b.txt 再仅处理 a.txt，manifest 只剩 a.txt；旧规范化文本仍可能留在目录，但已不在最新清单内。
- 基线实测已复现：EPUB 内 chapter2 → chapter10 的 spine 被脚本读成 chapter10 → chapter2。
- 实测记录在 `distill-novels/work/audit-20261021/observations.json`；全部输入为本次构造的简短英文测试文本，无真实小说资料。

## 2026-10-22 真实输入发现
- 四本TXT均GB18030，无解码替换字符；全角缩进、第一集和带卷名的章号是原解析器的真实缺口。
- 卷字正文不能因以“第一卷”开头就被分章；卷类分支要求分隔符，普通章号与序章保留无空格兼容。最终索引与已登记证据逐本一致。
- 来源图应保留局部回收与未知项，尤其不能把前世回忆当当前未来、把第一人称幻想当已实现能力。
- 全关系树有标签密集现象，当前用分段、暗线筛选和缩放；全书图性能与实体手机使用仍待后续。
- 四书正式库已有24卡4图，后续会话应沿用exchanges/runs检查点，不重建库。


## 2026-10-22 GitHub与换机验证补充

- 当前GitHub CLI账号 medillali 可创建和读写私人仓库；GitHub插件没有建库接口，且读取新建私库返回404。已实际使用CLI完成建库与读回验证，不将插件权限视为已接通。
- Windows深层克隆目录出现WinError 3，受控235字符写入成功、275字符失败；迁移验证副本到短目录后53项通过。没有修改系统长路径设置；该问题与早先未复现的WinError 5分别记录。
- Git仓库归属检查仅使用命令局部的精确safe.directory；网络Git临时使用OpenSSL并保留TLS校验。没有修改全局凭据或用户配置。
- 源小说与缓存未进入两个私有仓库历史；已上传的是工具及结构化研究资料。GitHub恢复不要求原书在场，继续阅读时仍需原文。
- 本机Git分支codex/persistent-fiction-library对应personal/main，推送明确使用git push personal HEAD:main；新克隆直接使用main/origin。资料库为main/origin。


## 2026-10-22 PC与手机阅读设计
- 引用讨论《设计树状图阅读方式》（6ada2180-ff90-83ec-bf54-902749421c64）建议PC全书骨架→剧情阶段→事件详情，手机沿线卡片→分叉与汇合→局部关系图。引用内容仅作为设计资料。
- 需要共同事件身份与原位返回；保留全部前因后果及折叠数量。完整大图保留作导出与总览，不再作为默认可读正文。
- 当前主档为163事件/265关系/46正式线索/15暗线；资料库HEAD a22937b9d38e26b4770c7b31f352a93f757aa30b，工作区干净。
- 保留事实、研究推断、读者认知和用户评价边界；图的阶段导航属于阅读分组。

### PC／手机阅读器：最终发现

- 引用讨论的分端方案已落地，163事件与265关系逐项等价于源图；53个阶段／剧情线范围提前布局。
- 独立审查指出并复测修复：原型属性／数组进度ID、关系证据展开返回、小于10%视图恢复、键盘原生滚动与缩小方向。
- OpenSeadragon适合整图缩放，Excalidraw适合手动编辑与PNG/SVG导出，Cytoscape.js适合作后续节点关系引擎；已附官方来源。没有自动安装、迁移或上传个人资料。
- GitHub为私有文件保存；响应式HTML实现与实际手机网页托管是不同验收项。


## 2026-10-23 用户改为全书地图优先
- 本轮用户明确希望像地图一样缩放一张完整图，替代前轮默认卡片入口；卡片页保留次级入口。
- OpenSeadragon6.1.1与589个无损WebP图块内嵌HTML，无CDN；整张原PNG仅供下载，不整体解码进画布。
- 窗口切换要保存图像像素缩放而非归一化视口比例；方向键交给OSD，缩放键统一一次处理。
- GitHub仓库不运行HTML，交付图片预览和下载入口；未开启公共Pages。Codex实际本机预览使用127.0.0.1:8765，服务退出后可打开离线HTML或重启命令。
