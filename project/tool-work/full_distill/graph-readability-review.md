# 全书剧情图可读性修复：RED → GREEN

## 范围与结论

仅修改核心渲染器使用的 `scripts/fictionlib/viewer.html` 及开发测试。没有修改正式 writing-vault、研究 JSON、graph JSON、静态 SVG 导出算法或既有 `.verify/`；未提交或推送 Git。已使用 systematic-debugging 与 test-driven-development 技能，先取得实际 Edge 浏览器失败再实现。

设计与本地实现：完成。独立 fixture 浏览器验证、旧 smoke、53项核心回归：通过。正式全书页面重新渲染与生产数据浏览器验收：由主任务接续，不能以此次 fixture 成功代替正式验收。

## 根因与失败证据

182节点 fixture 复现真实图规模，但内容完全原创且仅写 work/tests 临时目录。原布局主树宽39180、网络宽高15728；`.canvas svg { width:100% }` 将全部逻辑坐标压入视口。分段筛选只隐藏节点而不改坐标或 viewBox，线程选择只淡化非成员，故少量节点仍按整图比例显示。

RED：`work/tests/readability-06LJ5o/measurements.json` 及 `1440-thread.png`、`390-volume.png`。

| 实际浏览器检查 | RED | GREEN |
| --- | ---: | ---: |
| 1440px主树标题实际字号 | 0.389px | 14px |
| 1440px第18集网络标题实际字号 | 0.970px | 14px |
| 390px第18集网络标题实际字号 | 0.757px | 14px |
| 三节点跨集线程可见节点 | 182 | 3 |
| 第18集网络逻辑宽度 | 15728 | 1364 |
| 三节点线程逻辑宽度 | 15728 | 960 |

RED 自动断言因标题不足12px失败，非浏览器启动或脚本异常；已查看失败截图确认微字全环现象。

## 最小实现

- 画布使用逻辑尺寸对应像素的显示比例，默认标题14px；大图在固定高度区域内横向、纵向滚动，不把182节点自动缩到一屏。
- 分段和线程筛选取交集后重新计算树/网络坐标、viewBox及关系路径。网络只保留线程成员；树保留筛选范围内的祖先节点以表达结构。
- 筛选和切换模式后滚至首个可见节点附近，避免大环或宽树的空白初始视口。缩放仍为0.5–3倍，但基于实际尺寸并维持当前视口中心。
- 空交集有明确提示。保留节点点击、键盘、来源详情、已回收状态、仅结构模式与离线运行。
- 静态全图仍可能很大且关系密集，这是记录规模本身；HTML筛选是阅读入口。本次没有引入力导向库、服务端、网络依赖或全新图架构。

## 测试文件

- `tests/render_readability_fixture.py`：构造182节点、18集、三节点跨集线，调用真实 render；不读取正式库。
- `tests/browser_readability.cjs`：启动 Edge，覆盖1440/390视口、全树、18集树/网络、少量线程重排、真实字号、滚动区域、点击、键盘、空交集、缩放、无页面溢出及零外部请求。
- `tests/browser_smoke.cjs`：旧断言 `width='125%'` 已被像素画布有意替换，改为验证实际文字缩放比1.25；先观察旧断言因1200px而失败，再更新测试契约。

GREEN：`work/tests/readability-7OyqBX/passed.json`、`1440-thread.png`、`390-volume.png`。实际查看桌面与移动截图，文字清晰，三个相关节点已重新排布。浏览器脚本错误0，外部请求0。

旧 smoke 使用新建独立演示 `work/tests/readability-smoke-20261022/source-view`，没有覆写既有 demo-final 或真实视图。

## 已执行验证

1. `node tests/browser_readability.cjs <bundled-playwright> <bundled-python>`：RED失败后 GREEN通过。
2. `node tests/browser_smoke.cjs <bundled-playwright> work/tests/readability-smoke-20261022/source-view`：通过。
3. `python -X utf8 -m unittest discover -s tests -p test_graph.py -v`：10项通过。
4. `python -X utf8 -m unittest discover -s tests -v`：53项通过。
5. `git -c safe.directory=<工具目录> diff --check`：通过；仅已有自动换行提示，无空白错误。未更改全局Git信任设置。

使用的运行时均在 `C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/`：Node为 `node/bin/node.exe`，Playwright为 `node/node_modules/playwright`，Python为 `python/python.exe`。

最终待交付变更共4个代码/测试文件，外加本工作记录。正式数据重新渲染和复核完成后才可报告真实全书图可读性验收通过。
