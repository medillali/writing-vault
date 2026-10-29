# 《纵横天下》整书树图交付记录

范围：仅`writing-vault/library/reports/zongheng-tianxia/atlas/tree/`和本目录`tree-*`。未修改正式源图、人物库、既有map.md或其他代理文件。

完成：按《超级骷髅兵》现有Graphviz／Viz.js→Python中文SVG→Playwright渲染→内嵌离线阅读器流程，生成一张整书分枝交汇大图。

- 260个唯一事件／场景，75 event +185 scene；全书原227条边完整保留（209原研究边+18 editorial边），语义和方向不变。
- 图面删除70个分组：1 story、8 volume、61 arc。卷号仍可定位，不绘父子目录关系。
- 因果实线，铺垫／揭示／回收／转折虚线，主题呼应细点线。主题呼应不计入交汇。
- 7条editorial全书线枝端终态，3 resolved／4 partial；安妮、明宇身份两条hidden均resolved。旧卷末状态保留在查阅数据中，未当全书未知。
- 110图内起点、27分枝、40交汇。正式图语义层稀疏，主线程只指定4条边，所以诚实保留独立起点；没有虚造因果或阅读顺序边。
- 原dot坐标横向空白较多；逐层单调连续横向压缩空白，保留卡片宽度、左右次序、上下层级与拓扑路径，原坐标和变换参数存档。最终5371×11834。
- 主代理补充要求后，加入31个关键转折／30条展示层reading-order细蓝点划线，无箭头，明确不是因果，不计原227语义边、110起点、27分枝、40交汇。原严格语义SVG/manifest/layout另存semantic-only备查。
- 产物：tree.png、tree-preview.png、tree.svg、index.html、tree-junction-preview.png、tree-opening-preview.png、manifest.json、integrity-check.json、browser-check.json、layout-check.json。
- 实际查看总图与终局局部PNG，中文字清晰，终局共享事件、分枝与身份终态可读。
- 实际浏览器检查：1028行文字，0溢出、0节点重叠、0边穿无关卡片、0外部请求、0JS错误；搜索、事件／关系点击、章节行号证据、邻居跳转、枝端终态、SVG下载、线程／卷／交汇聚焦、缩放拖动均通过。

重建：`writing-vault\library\reports\zongheng-tianxia\atlas\tree\rebuild.cmd`。不联网、不安装软件，使用本机Codex Python/Pillow、Node/Viz/Playwright与Chromium 1228。

给主代理的接入：

1. 地图入口链接`tree/index.html`、`tree/tree.png`、`tree/tree.svg`，预览`tree/tree-preview.png`。
2. 人物档案→事件可用`tree/index.html#事件ID`；阅读器已支持深链定位。
3. 事件→人物可后置写入本目录`character-links.json`，格式`{事件ID: [{"name":"人物名", "href":"相对档案路径"}]}`，重建后事件面板自动显示链接。该文件非正式源图，不会改人物身份。
4. 未更改atlas/map.md，主代理负责替换总入口与人物互链。

研究解释仍待用户审阅；本地阅读副本修复不等于重新阅读全书、用户认可或远程推送。
