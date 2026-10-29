# 《网游之天下无双》元数据准备交接

当前仅准备元数据，**正文0已读**。没有打开normalized原文，没有调用读章器，没有执行Vault检查或入库，也未修改正式库、作者顺序、活动来源、旧队列或《纵横》冻结包。须等主代理确认《纵横》全书审计正式完成并明确启动本卷，才开始正文。

## 来源与完整覆盖口径

- slug：`tianxia-wushuang`；source_id：`src-d8926e2a35f04bcf8139cff0ea516bbd`。
- revision：`d819f7d0ecf5a2004a0a434e987569bbe25015422d45e16676af913292346857`。
- 工作spec、正式来源登记、reading-units及queued run的修订一致；登记章节元数据完全一致。normalized文件存在，大小只用stat核，没有重读正文或重新计算原文hash。
- 全书**1599正文单元**；8个独立卷标题；1个章前内容；1处正文被误切成额外片段。合计1608阅读单元、1609原始证据片段。印刷正文号1—1599连续，无重复/缺号。
- 章前内容`ch-0001` L1—356在`source.preface`，不属于8卷。未来必须另明确实际读者，全文读后才保存补充日志；全8卷1608片段全部读完仍不能漏这1片段而宣全源覆盖。

## 8卷规格

卷标题仅目录元数据，不是本轮正文阅读。

| 卷 | 标题 | 正文单元 | 含卷标题单元 | 原片段数 | raw范围（含卷标题） | 印刷正文范围 | 行范围 |
|---|---|---:|---:|---:|---|---|---|
| 1 | 血色风云 | 90 | 91 | 91 | ch-0002—0092 | 1—90 | 357—8902 |
| 2 | 兄弟盟约 | 135 | 136 | 136 | ch-0093—0228 | 91—225 | 8903—21743 |
| 3 | 天下名将 | 376 | 377 | 378 | ch-0229—0606 | 226—601 | 21744—52260 |
| 4 | 铁血丹心1 | 185 | 186 | 186 | ch-0607—0792 | 602—786 | 52261—65980 |
| 5 | 铁血丹心2 | 265 | 266 | 266 | ch-0793—1058 | 787—1051 | 65981—86173 |
| 6 | 英雄王座 | 234 | 235 | 235 | ch-1059—1293 | 1052—1285 | 86174—103166 |
| 7 | 不醒之梦 | 210 | 211 | 211 | ch-1294—1504 | 1286—1495 | 103167—119331 |
| 8 | 天下无双 | 104 | 105 | 105 | ch-1505—1609 | 1496—1599 | 119332—127662 |

每卷的独立卷标题均在`spec.units[].segments`内，因此现有`check_volume.py`要求日志、笔记、state与图coverage包含它；不要只交正文ID。正文进度仍按1599，不把8标题或误识别片段重复计为正文。

## 卷三唯一误标题映射

reading-units指纹为`0cb9382e080757d374529173582703b664b2ba68b8f468ca80360feadc09fe18`；映射与source spec逐字段核对一致。这里只核记录及ID/行段，没有打开正文确认文学含义。

| 逻辑单元 | 原片段 | 原索引标题/类型 | 行段 |
|---|---|---|---|
| ch-0398 | ch-0398 | 第三百九十四章 明眸似水 | 36185—36243 |
| 同上 | ch-0399 | 第二回合，GO！（被解析器误识别为标题） | 36244—36295 |

两个片段相接、无缺行、没有重复。不要改登记的原ID，不把0399算新章，也不能删除它。启动阅读后应读完两段，各写一条真实全文笔记；逻辑正文完成数只增1。后续若有证据跨两段，分两个证据对象，不能用ch0398的chapter_id挂跨越至36295的行范围。

## 卷三预备目录

`vol03/`已准备：

- [assignment.json](vol03/assignment.json)：376正文、377正文片段加1标题，共378指定ID；原章226—601。上下卷事实尚未输入，不能搬《纵横》人物、技能或关系作本书既知。
- [reader-state.json](vol03/reader-state.json)：`prepared_unread`、`reading_authorized:false`、read/completed空、next=`ch-0229`；不是正在阅读。
- [read-log.json](vol03/read-log.json)：chapters空、complete_volume/book均false。
- [chapter-notes.jsonl](vol03/chapter-notes.jsonl)：空文件，未预填任何事实。

第一段是独立卷标题ch0229 L21744—21746；第一正文ch0230（印刷226）L21747—21847。未来正式启动后先接前卷阶段handoff，再从指定入口读；元数据准备不解除当前禁止提前阅读的门槛。

## 现有工具适配结论

**不需要为此源修改`check_volume.py`或`import_volume.py`的主体逻辑。** 两者已有`tianxia-wushuang`书名分支；`expected`从`units[].segments`展开，天然涵盖卷标题与0398/0399合章。静态语法检查通过。这里没有伪造analysis/cards/graph完整包来“试通过”，也没有初始化Vault抢锁。记录见[metadata-check.json](metadata-check.json)。

| 项目 | 可直接沿用 | 最小注意事项 |
|---|---|---|
| read_chapters.py | 按raw精确行段输出与END | 参数是原索引序号，不是印刷章号；上层要按unit展开全部segment。当前不可运行，它会打开normalized正文 |
| read-log/notes | 一原片段一条，保source/revision/line/reader | 卷三完成时378条而非376；0398/0399两条归一正文单元；实际读完才填full_text_read |
| save_primary_notes.py | 能按expected防越卷/重读 | 硬编码reader=`primary`，未来不宜给本子代理直接用；用本卷专用保存器或显式reader参数。不要克隆纵横work.py的硬编码卷7/源路径 |
| check_volume.py | 书名、卡前缀、九维、图卡映射已支持 | 完成前故意不通过；每个evidence自身claim_kind，knowledge要state/错信belief；不把prepared state当已读 |
| import_volume.py | source名、前卷检查、合图、正文计数支持 | 卷三正式导入前一二卷须已导；仅主代理审阅hash固定后串行执行；8卷合图还须补章前日志才能1609全覆盖 |

`import_volume.py`将新建`run-deep-tianxia-wushuang-20261025`，旧`run-queue-tianxia-wushuang-20261023`仍是历史排队记录，不应删除或把已索引说已读。作者顺序和活动来源切换由主代理在启动门槛满足后处理，当前catalog仍活动《纵横》是正确等待状态。

## 最小辅助建议与不宜运行的脚本

1. 后续阅读进度分开显示`body_units_completed`、`raw_segments_completed`与`volume_headers_completed`；单元须全部segments读完才算完成。
2. 卷三未来保存器要求显式reader，约束assigned IDs，拒绝重复/错修订/越卷；每2—4片段保存，不按`raw号减固定偏移`推印刷号。
3. 每次启动先复核source与reading-units修订/映射未变；若变更，停止依旧边界续读，交主代理确认来源，不自动重置旧状态。
4. 不运行共用`prepare.py`做本轮检查：它会打开三书正文、重算字符并重写source.json，与当前仅元数据任务不符。现有字符数仅沿用spec，没有本轮重新读取正文计算。

本目录的[metadata-check.py](metadata-check.py)只读JSON登记及工具代码，对normalized只做exists/stat，重跑会拒绝覆盖不同状态或任何已有阅读笔记。它不是读章器、不是完整研究preflight，也不授权启动阅读。
