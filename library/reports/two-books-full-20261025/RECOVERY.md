# 保存与恢复

本批成果的权威主档仍是现有 writing-vault，工具独立在 distill-novels。Git保存资料修订；原书与规范化全文保留在本机，另作私有备份。

本地备份目录是 Novel/backups/full-two-books-20261025。backup-receipt.json列出资料快照ZIP、独立原文ZIP和校验值；本报告的[验收目录](validation/)中，save-and-restore.json记录实际提交及恢复结果。资料ZIP对应已提交内容，不包含其他任务尚未提交的修改。

恢复时先把资料快照解压到新目录，保留现用库。以该目录运行现有 library.py 的 --vault 参数及 validate 子命令，核对来源、版本、证据、派生引用与图结构；验收通过后再决定是否切换。不要把多个版本的JSON直接覆盖混合。

需要重读原文时，单独取出 two-originals-and-normalized-private.zip，按其中source-identities.json核对来源ID和规范化修订。原文备份不在Git；研究库恢复成功也不等于原文已经恢复。恢复验收须同时检查这两个部分。

本目录research保存本轮逐章阅读后的研究批次，rebuild-full.py重建卡片、阶段报告与图数据；render_full.py重建图像和离线地图。全书综合、终态审计和人工评价属于须保留的研究判断，不能用自动生成的目录代替。
