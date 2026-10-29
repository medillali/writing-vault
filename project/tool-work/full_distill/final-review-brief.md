# 整书收尾审查约定

仅在18集报告已交接后执行最终审计。阶段稿与当前卡不可混写：保留每集当时的未知、推断和误判，整书后文以累计状态补记，不回写旧报告制造早知。

## 综合报告

`book-synthesis.json` 包含 source_id/revision、coverage、overview、dimensions。九维各至少3项，每项有 claim/mechanism/application/limitation/claim_kind/evidence；至少连接两个相隔阶段，既分析有效处，也说明代价与局限，不把主角成功当所有选择合理。抽象创作方法，不续写原书、复制角色设定或长引原文。MD另展示主线阶段、角色弧、伏笔与认知差、可选收藏建议和用户审查重点。

审查页另外直接展示以下可选字段：`stages`数组，每项title/summary/evidence；`character_arcs`数组，每项name/initial/turns/ending/unresolved/evidence（文字字段用字符串）；`review_focus`字符串数组。最终问题主档统一保存`question-ledger.json`，沿用1—7账本entries结构与四种status，页面按状态折叠展示。

## 疑点与伏笔

全部18集questions及revisions_to_earlier必须覆盖。已有question-ledger-01-07只截止7，不能直接称整书结论。使用 answered/partial/open/text-uncertain，逐项有来源问题、原证据、终点结论、答案证据及未决边界；文字错置和口径差不自动归罪作者。后文未回答不等于伏笔作废，也不要把章节未再提及当人物死亡。

问题保持每个原始questions条目一项，不因重复主题删除；`origin_volume`、`source_question_index`（从1开始）、question及origin_evidence与最终分集稿完全一致。整书核查后每项加`reviewed_at_book_end: true`；顶层completion为`complete_as_of_volume_18`且pending_questions为空。这些标签只能在实际复核全部后文后填写，不通过复制阶段账本直接升级状态。

18稿齐全后可先运行`prepare_final_ledger.py`一次，生成`question-ledger-review.json`：自动排列原问题并带入早期结论供复核，每一项整书标志均为false。审计代理逐项完成回答、证据和状态后才能将对应标志设true；最后`finish_ledger.py`检查完整性并生成正式JSON/MD，免去重复抄录原问题及排版。两个脚本都不能代替文学复核。

跨集同key要真是同一问题，不能因共享人名、地点或关键词合并。状态审计覆盖全部局部线程的最新进展和跨集图，特别已死亡/被吸收对象的旧追踪目标、旧封印解除、承诺是否兑现、认知对象不同。只关闭已经明确回答的窄问题。

## 人物当前卡

检查所有独立人物卡的末次出现与重要后续信息。第1—9已知遗漏见character-state-audit-01-09.md；执行时先排除后续已覆盖或改变者。死亡、吸收、身份揭示、重伤、主体分离分别记录，不把复制傀儡当原人格复活。当前卡保留身份与已证状态，分集历史不改；generated保存，人工备注、收藏、review_status不变。区分全书已读范围和本卡最后有效证据范围。

人物最终审计交付`character-final-audit.json/md`：complete_as_of_volume=18，checked_asset_ids为实际审查全部索引独立人物ID；updates数组每项asset_id、reason、evidence，以及content_updates（仅summary/goal/conflict/arc_change/relationships/knowledge_limits），可选identity_notes字符串数组。只列确需纠正或补记者，不重造卡或改旧history。主任务的apply_book_end.py负责校验、generated保存和覆盖说明更新；审计代理不直接写正式库。

## 验收

核对18集/183正文序章/202索引段、全部阅读块及证据边界；检查无悬空图引用、主线树和暗线网络可用；实际桌面和390px审查入口可筛选并查看证据。备份不含原TXT、可恢复、恢复库可独立重建同一页面；远程私有仓库提交SHA与本地一致，最终从短路径重克隆复核。文学研究质量与工具结构检查分开，用户卡片审阅状态仍待用户决定。
