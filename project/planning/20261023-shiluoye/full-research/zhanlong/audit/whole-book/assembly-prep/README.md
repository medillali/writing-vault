# 《斩龙》B组装器准备交接

这里只准备组装与验证代码，没有执行真实 `--write`、二次合池、冻结四包、生成primary凭据或正式发布。文学结论仍是研究草稿，不是用户审美批准。

当前固定代码：

- `assemble_zhanlong_signed_audit.py`：SHA256 `3953c5c3f152145199039162b34060508f6e362fdddaf1502f38a6994607e1e8`。
- `test_assemble_zhanlong_signed_audit.py`：SHA256 `b8375b57cd557358eb2b0a3f332784ba8d9c6ae07c81f53c33c4b7130097a06c`。
- `preparation-validation.json`：SHA256 `cbc6465702edf627495bd01169f40c5e2255272c44ac5c4dccc287b081d88679`，保存最新20小样测试实际输出、默认只读结果及受保护文件前后SHA。

实现仅依赖Python标准库。正式写入准备目录时另调用既有 `book_audit_common.load_package` 检查schema，不调用发布或签收函数。既有六个接口的当前SHA在上述验证回执中；脚本冻结时会将这些接口原字节存档。没有修改生产工具。

## 真实输入前提

1. 历史232/本地2462，共2694候选全部真实签收；各批SHA、ID和账本计数恰好相等。
2. root已运行 `merge_zhanlong_adjudications.py --apply`，两池当前字节须等于 `adjudication-progress.json` 的 `pool_after_sha256`，其签收进度SHA也须相等。组装器不再合池，不重造任何终评或证据。
3. 人物总稿与所有已签人物组逐对象相等；24重点与已签三组逐对象相等。人物数量取实际，不套用无双115/30/4130。
4. 36综合须有既有 `primary-synthesis-review.json` 的真实主审和两个总稿SHA，九维36条仍以synthesis分层。组装器只拷原字节作依赖快照，不代写或代签36综合。
5. 正式六卷各六接口及研究组正式pin实际SHA一致；卷六 `review-vol06.json` 原输入逐项SHA一致。

最新默认运行是 `not-ready-no-write`，缺人物总稿。前后两池、已存在研究总稿、冻结清单及primary整书凭据的存在状态/字节保持不变。不能将“20测试通过”写成真实整书已就绪或已验收。

## 字节与引用保全

- 四包JSON直接复制已合并/已签总稿原字节，保留reviewer、source_attribution、reading_attribution及精确later_evidence。三个判断字段、后证数组和证据对象再逐ID比对。
- 四包MD只渲染现有对象；若替换既有可读页，旧MD原字节另存输入快照。报告按audit_domain分别统计answered等状态，不把answered全称剧情伏笔回收。
- 全部签批、签组、签收进度、合池回执、受控delta/proposal/before/history JSON保留。历史文件不作为额外候选重复合入。
- `research_path`/`material_path`与原SHA不改。材料按精确SHA保存至包内，`material-resolution-index.json`保原path+SHA到包内字节映射。
- 旧priority a60优先通过正式 `audit/material-history/manifest.json` 解析；若精确版本不存在就阻断，不悄悄使用当前新版。当前组合层及正式优先层另外动态保存并列于 `priority-reading-index.json`，不硬锁97/100/105为最终版本，也不用新增层倒填旧签组。
- legacy `frozen_volume08_hashes` 在本书明确指实际卷六原review输入快照；本次准备已实际逐项核过23个卷六输入SHA。不是虚构卷八。
- 不复制正文TXT或private-sources。来源ID、revision、章节边界与原读者元数据保留；原正文仍沿既有来源/备份管理。

## 只读命令与恢复接口

默认运行 `assemble_zhanlong_signed_audit.py` 只打印就绪状态。真实 `--write` 留给root完整代码主审、输入齐备后明确调用；已有冻结清单会拒绝覆盖。

独立函数：

```python
validate_material_archive(audit_path)
validate_material_archive(workspace_root, "zhanlong")
```

独立CLI：

```text
python assemble_zhanlong_signed_audit.py --validate-material-archive <发布后audit/whole-book路径>
```

验证只读包内索引、原JSON与包内精确材料/冻结SHA，不读取旧 `.planning` 路径；发布器将 `.py` 移入provenance的情况也有兼容解析。小样已经移除原研究材料文件后重新验证包内恢复可用。此函数不等整书文学主审，也不代替项目最终全量备份恢复。

## 已运行守卫小样

20项测试通过，包括：缺签、未合池、root合池后原字段字节漂移、签后字节变化、判断或研究对象变化、正式pin变化、材料历史版本缺失、历史池原记录覆盖差、36综合未签、路径越界、历史a60式正式版本登记、最新优先层独立保存、准备期间输入变化、拒绝覆写冻结清单、默认无写入、四包原字节不变、动态引用计数及脱离原材料后的包内校验。测试全在独立临时小样内，不生成真实主审凭据。
