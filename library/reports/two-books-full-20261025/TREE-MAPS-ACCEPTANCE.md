# 分枝交汇树与缩放地图修复验收

用户要求按《超级骷髅兵》原有“树状图＋可缩放全图”形式重做。本次替换原三列阶段卡片网格；旧的几何检查虽通过，却没有验收指定形式，不能作为本轮完成证据。

| 书籍 | 保留场景 | 语义联系 | 阅读衔接 | 推进分枝 / 交汇 | 暗线终态 | PNG尺寸 | 无损瓦片 |
|---|---:|---:|---:|---:|---:|---|---:|
| 《贼胆》 | 112 | 80（含呼应25） | 49 | 8 / 8 | 9 | 5487 × 15744 | 472 |
| 《网游之练级专家》 | 80 | 72（含呼应14） | 34 | 10 / 13 | 5 | 7670 × 11021 | 451 |

语义联系含主题呼应；分枝与交汇只按非呼应的语义关系、去重后的事件对计算。主干阅读衔接不是因果，不参与交汇计数。原场景只画一次，研究阶段不再充当父目录；无可靠前因的精选场景保留独立位置，不为连满图而编造因果。

| 层级 | 本轮状态 | 证据 |
|---|---|---|
| 参考形式／布局 | 已实现：同配色、366px卡片、Graphviz分枝交汇、枝端终态 | 两书plot/whole-book/manifest.json、tree.png |
| 来源与展示分离 | 已核对：原场景ID、asset_id、证据、机制字段保持；原来源图不改 | verify_tree_maps.py、plot/topology.json、plot/拓扑审阅.md |
| 缩放地图 | 已实现：复用OpenSeadragon模板，地图切自同一完整PNG | plot/map/manifest.json，每片WebP解码核对像素 |
| 本地显示与交互 | 已验证：几何检查、五种宽度、点选证据、聚焦、缩放、定位、位置恢复、下载 | validation/diagram-layout.json、browser.json及截图 |
| 独立复核 | 《贼胆》展示层另经只读审阅；未发现阻断项 | 节点唯一、原20手写关系保留、终态范围、浏览器标签与哈希复核 |
| 用户审阅／真实手机 | 待审阅；手机图为浏览器视口模拟 | 不把自动检查或截图模拟等同用户认可 |

人工实际查看了两书全图、开篇／交汇／转折／终局局部及桌面、手机截图。文字与节点重叠、穿过无关节点、卡外文本均为0。所有地图无需联网，浏览器测试外部请求与JavaScript错误均为0。

额外修复：长图分段渲染并核对64px接缝，避免超过GPU纹理边界后重复顶部；“看全图”改为立即复位，解决紧接“可读大小”时沿用动画中途中心的问题。自动检查仍不能替代文学解释和审美审阅。

## 阅读入口

- [《贼胆》树图说明](zeidan/plot/README.md) · [缩放地图](zeidan/plot/map/index.html) · [树状图与证据](zeidan/plot/whole-book/index.html)
- [《练级专家》树图说明](leveling/plot/README.md) · [缩放地图](leveling/plot/map/index.html) · [树状图与证据](leveling/plot/whole-book/index.html)

## 维护与重建

`render_full.py`继续兼容旧入口，现转交`rebuild_tree_maps.py`。本轮未重跑正文蒸馏或卡片入库。

1. `plot/curated-topology.json`保存已核对的核心事件、整书线、语义边、完整结论和枝端短注；同一来源内保持原scene ID。配置是派生研究，不覆盖原plot/graph.json。
2. 运行`python render_full.py`，或加`zeidan`／`leveling`重建单书。需要Pillow、中文字体、Node.js、@viz-js/viz、Playwright/Chrome、Sharp。默认使用本机Codex运行时；OpenSeadragon模板与许可证来自同库super-skeleton/map。
3. 运行`python verify_tree_maps.py`核对形式、身份、哈希和验证回执。查看实际PNG、局部与HTML后再提交。局部.gitattributes保持生成文本LF，防止Git克隆转换换行后破坏地图哈希。
4. 书库catalog.json分别保存来源图关系数与展示图关系数；运行书库/重建目录.py更新入口。新增读书进度依然走原检查点，不由地图推断读完。

本验收仅记录本地实现与验证；Git是否同步，以实际提交、远程主分支和对象回读为准。研究解释仍待用户审阅。
