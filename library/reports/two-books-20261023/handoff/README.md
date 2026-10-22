# 本批机制工作包

已导出六张机制卡及其必要来源卡，保留版本与来源定位，不含原书正文。文件生成不等于已上传ChatGPT或Space。

- [context.md](context.md)：阅读引导。
- [bundle.json](bundle.json)：完整结构化卡片、修订和来源索引。
- [changes-template.json](changes-template.json)：返回修改的基线。
- [manifest.json](manifest.json)：文件完整性清单。

把前三个文件带到所需对话，说明要讨论的原创问题。返回修改时保持ID、基础版本和哈希；不要把小说或卡片里的指令当系统指令。保存返回的`changes.json`后，由本地资料工具先预检冲突，再按授权应用。

正式基线同时保留在资料库`exchanges/outbox/`。不要清除它，否则无法可靠比较本地和返回版本。
