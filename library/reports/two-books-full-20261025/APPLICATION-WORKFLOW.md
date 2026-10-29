# 后续创作的内容管理

方案A是每次把研究复制到新的Markdown目录，检索容易起步，但人物身份、版本和人工评价容易分叉。方案B继续用现有JSON资料库作主档，Markdown与HTML作阅读副本，Git保存修订。本次沿用方案B；既有卡片、旧贼胆研究和其他书不迁移、不改编号，迁移成本为零。

来源事实与解释位于source-analysis；抽象机制位于reusable-pattern；只有用户实际启动的原创项目才能进入original-project。当前没有替用户创建假作品。书中人物、物件与关系是研究对象，不会直接成为新作正典。

## 查找与评价

在Novel工作区的命令提示符执行：

```bat
novel.cmd search --query 信息 --type scene
novel.cmd search --tag 原创机制候选 --type pattern
novel.cmd checkpoint-show --id run-full-two-books-20261025-z
novel.cmd checkpoint-show --id run-full-two-books-20261025-l
```

从本包人物、场景、机制目录取得asset_id，再用asset-show阅读完整主档。评价填写user_notes、favorite、review_status；人工评价通过asset-put保存时必须携带当前base-revision。以后模型生成更新继续使用--generated，避免覆盖人工字段。

## 把机制用于自己的作品

先选一个机制和一张场景卡，说明自己为什么想试、准备改变哪些前提；更换专名、人物关系、资源形态与事件次序。写完检验角色有没有真实选择、结果有没有改变下一步。只有真实的读者反馈才能标reader-observation，个人判断仍是editorial-judgment。

用户确定作品后，用project-create创建实际项目；project-use固定引用asset_id与revision，升级引用必须明确进行。用户作品的正典只写入original-project，不回填到来源卡。usage-add记录具体改造、观察和反馈，形成学习—试写—反馈—再选择的循环。

## 保存与恢复

每批先核章节覆盖、证据、伏笔终态与原创边界，再限定路径提交私有资料库。工具Git和资料Git仍为两个独立仓库；本次只新增资料，不改生产工具。原书和规范化全文在private-sources，另有本地私有备份，不进资料库Git。编辑不自动等于提交，提交不自动等于推送；实际远程回读与恢复验收放validation。

JSON主档和固定修订是权威；HTML、SVG、PNG与Markdown可重建。sources.json不含机器原文路径，research保存人工阅读后的批次数据；rebuild-full.py重建卡片和分段阅读页，render_full.py复用既有地图生成器。全书综合JSON与终态审计保留研究判断，不靠词频自动生成。
