# 《超级骷髅兵》全书审查页验证

## 交付状态

| 模块 | 状态 | 证据 |
| --- | --- | --- |
| 离线生成器 | 已完成 | `build_review.py --help` 退出码 0；仅使用 Python 标准库 |
| 逐集审查 | 已完成 | 固定显示 18 集；正文与集标题／章前内容分开计数；未到达的集显示“尚未阅读” |
| 九维与核对信息 | 已完成 | 主张、机制、迁移、边界及章节行号证据可读；疑点、前序修订、逐章观察和 JSON 主档可展开 |
| 全书综合 | 已完成占位逻辑 | 缺少 `book-synthesis.json` 时明确显示“尚未完成”，不生成替代结论 |
| 来源资产 | 已完成 | 只加载证据属于本书来源的人物／场景／机制卡；原有开篇样段和带集数历史的新资产分别标识 |
| 图入口 | 已完成 | 指向独立的 `library/views/plots/src-9ff09c395734410b856f77c77a652834-full-nine/index.html` |
| 浏览器验证 | 已通过 | Edge + Playwright 合成样本；搜索、类型／集数筛选、证据展开、390px 布局与来源隔离均通过 |

## 验证记录

先运行 `node distill-novels\work\full_distill\review_browser.cjs`，测试因 `build_review.py` 尚不存在而失败，确认红灯命中目标缺口。实现后重新运行，输出：

```text
PASS: 18集进度、正文/标题计数、九维证据、综合占位、卡片筛选、来源隔离、XSS转义、离线请求与390px布局均通过。
```

合成样本包含 `script`、`img onerror` 等恶意字符串。浏览器断言没有生成注入元素、没有执行脚本，也没有发起 HTTP/HTTPS 请求；390px 视口满足 `scrollWidth <= clientWidth`。测试还确认 `content.volume_history` 以中文逐集变化展示，不直接暴露开发字段。

隔离样本及生成页位于 `work/full_distill/ui-fixture/`，没有导入正式资料库。本次没有运行默认输出，因此没有修改 `writing-vault`；待逐集报告与资产正式入库后运行：

```text
C:\Users\Administrator\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -X utf8 distill-novels\work\full_distill\build_review.py
```

默认输出为 `writing-vault/library/views/超级骷髅兵全书审查.html`；`--vault` 与 `--output` 可用于隔离复验。

## 主任务复核修正

首次接收生成器时发现它会把本机原文全文嵌入审查 HTML。该版本只对合成样本运行，未对正式库生成或上传。新增私有原文哨兵断言后确认测试失败，随后移除原文读取及展示；测试重跑通过。再删除合成样本的确切原文文件后生成结果字节一致，证明入口不依赖原文在场。发布脚本另行拒绝本机原文路径和 200 字连续原文段落。

第一集入库流程在 `.verify/d01` 隔离恢复库检查通过：42 个备份文件完整恢复；重复入库不改变资产与剧情图；损坏的剧情线成员引用会被提前拒绝。
