# 《超级骷髅兵》九维深化研究

已完成18集、183章（含序章）的全文阅读与研究复核，深入分析世界观、人物、情节、文风、叙事、对话、节奏、主题、连续性。

这是供用户审查的研究草稿。事实、解释和可迁移机制分开；读者认知与角色认知分开。研究复核不等于用户已接受这些风格规则。

每集研究保存为 `volNN.json` 和 `volNN.md`，人物与精选素材进入长期卡库；完整JSON为主档，HTML为阅读副本。个人笔记、收藏和审阅状态由用户掌握。

正式进度以 `exchanges/runs/run-deep-super-skeleton-20261022.json` 为准。183个正文/序章与18个集标题、1段章前说明分别计数，索引202段不等于202章。

本书总审查材料已交付；其他三本尚未扩大其开篇研究范围。原书留在本机，Space未接入。

## 阅读与审查

**[打开GitHub直接阅读入口](reading/README.md)**。该入口提供226张中文卡片、18集报告导航、分集主线树、46条跨集剧情线与198项疑点账本。

| 想看什么 | 直接阅读 |
|---|---|
| 像地图一样缩放、拖动整张全书图 | [全书地图阅读入口](reading/plot/map.md) |
| PC分层关系图、手机卡片、支线原位返回 | [双端剧情阅读器](reading/plot/reader.md) |
| 在一张可缩放大图中看清全书 | [全书分枝交汇图](reading/plot/whole-book.md) |
| 主线树与暗线的图片、未回收标记 | [49张PNG/SVG图片入口](reading/plot/images.md) |
| 全书的九维综合与人物弧 | [综合报告](book-synthesis.md) |
| 人物目标、关系、变化与终点状态 | [104张人物卡](reading/characters.md) |
| 精选场景的因果机制 | [74张场景卡](reading/scenes.md) |
| 可迁移到原创创作的方法 | [48张机制卡](reading/patterns.md) |
| 主线、暗线、伏笔与回收 | [剧情目录](reading/plot/README.md) |
| 哪些问题有答案、哪些仍不确定 | [疑点账本](question-ledger.md) |

本机统一入口为资料库内 `library/views/超级骷髅兵全书审查.html`。页面可按集阅读九维条目、查看行号证据、筛选人物和素材，并进入主线树/暗线网络。`audit/review-NN.md` 保留每集审查发现与修订记录；它与用户本人确认通过是两个独立状态。

建议先检查重要人物在各集的变化，再选择有价值的场景和机制收藏，最后核对未决问题与伏笔回收。事实不清的条目可以留下个人笔记；不要直接覆盖生成主档。来源分析卡和可迁移机制分别保存，原创创作时应重新设计人物、条件和因果组合。

## 从备份或另一台设备恢复审查入口

HTML 是可重新生成的阅读副本，Git和标准备份保存研究主档。恢复整个资料库后，在有 Python 3 的环境运行：

```text
python library/reports/super-skeleton/rebuild_review.py
```

脚本会根据所在目录找到资料库，并生成上述 HTML；这一操作无需原书TXT。剧情图另用蒸馏工具重新生成（在工具仓库目录运行，并将 `../writing-vault` 换成实际资料库路径）：

```text
python scripts/library.py --vault ../writing-vault graph-render --owner-kind source --owner-id src-9ff09c395734410b856f77c77a652834 --output ../writing-vault/library/views/plots/src-9ff09c395734410b856f77c77a652834-full-nine
```

以上重建只提供已有研究和证据定位。要核对原文或继续蒸馏，仍须在本机接入同一来源修订的原书。

## 更新GitHub阅读副本

图片已随仓库保存，直接打开即可。修改研究主档后，需要先重新生成SVG与PNG，再生成阅读页：

```text
python library/reports/super-skeleton/rebuild_plot_images.py
node library/reports/super-skeleton/render_plot_images.cjs
```

图片生成依赖Python/Pillow及中文字体（Microsoft YaHei或Noto Sans CJK）；PNG渲染依赖Node.js/Playwright及Chromium浏览器。Windows使用已安装Edge时可设置环境变量`PLOT_BROWSER_CHANNEL=msedge`。图中的蓝色主干为小说阅读顺序，回叙保留原标记；彩色旁路及状态取自既有研究记录。

修改卡片和图的主档后，从资料库根目录运行：

```text
python library/reports/super-skeleton/rebuild_github_reading.py
```

脚本只生成`reading/`中的Markdown与清单，不修改研究JSON、个人笔记和历史。提交并推送后，GitHub网页即可查看新版；它不会自动更新Space或记忆。
