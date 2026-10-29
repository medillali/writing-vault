# root v18：卷六初冻结整包已实际全量主审，待定向修订

沿v17继续，原用户三书全量任务不在阶段final；正式斩卷1—3=748正文317卡，实际1378/1378全文已齐。正式库2512卡8来源0原创8图已核valid，卷3 links336MD/2217条0错。尚未整书/三书最终验收与最终全备份restore。

## 卷六真实主审进度（不要重读已读部分）

agent5原冻结manifest=b5f408525fba0be8d7a3ef6e192878b5c7a40d8519c442ce7b3897464337786a；analysis 00b06caef1c6337c86b717c7578acc1e0578d0cda5fb640189e5f623df51bac2，cards 4b99ae67a20c7ee97fa1a2668cbebdd3bd653b9344797a5b2f683f0aaf2f402b，graph 265873e7749d081b7ba25a7f81b252abc83c923d787143f8d51c4db3e38fb2ce。

root已实际完整读：45九维(每维5)、102卡(32人物/58场景12机制)、全部70节点49边23线，32character_states/24open_questions/29source_anomalies/12reusable摘要/4tradeoffs，report1—246全部/handoff1—33全部。未读chapter_unresolved_index207行不冒成此处逐条主审；这个原串终审后做。analysis.thread_states与graph.threads需最终assert相等或定向读差，不用重复读相同对象。

所有25个JSON阅读回执在zhanlong/vol06-primary-review-progress.json；辅助record_primary_volume_review.py只在实际读后加--read记录，遇同section同文件改SHA会拒，原签收不可静默重标。文本阅读SHA/范围/待改点另在vol06-primary-text-review.json。不是root独读卷6原文，原文52批全部agent5。

root还补读了1386 L99736—99805原文部分以核最后盟主/订婚/电话/军营动作（1386整体早已root完整重读过）；首调用read_source_lines参数少cid失败后已正确调用，不能把失败算阅读。主最后仍少将与师长已见，空军军种由1359agent6段证据，不拿1386军营直升机猜。

## 已退给agent5的限定修订

1. pacing v06-attrition-ladder“雨压火炮→西破城”需澄清，1385布盾甲护引线后炮雨中仍fire；不能直接当雨停炮导致败。
2. continuity04 v06-open-end-not-erasure是保存索引流程非文学观察，改长期承诺由职位/身体/物件再现分步回收；事实/行证保。
3. continuity05 source-interface-anomalies限项“检查通过待主审”改为文本漂移实际辨识/因果限制，不夸源错好。
4. 主卡NPC不可复缩为NPC军不能玩家返；霜卡stage/handoff100龙骑只允留未独演全到；薛柔卡“薛景：姐姐”改明确妹妹，柔姐姐。
5. **58场景applicability/failure_mode全部同句套话**，须独立新文件各场景手写具体两字段，保事实/why等其余内容。root已完整读原58卡，不会用回执冒新字段已读。
6. graph两edge soul-army→canglan-soul、lanse-loss→upper-god仅主题/同时并置，setup拟改echo，不改证据/label。其他图/线终态均已读。

agent5目前followup_task在跑，明确先独立新文件拟delta，不改原冻结，待root实际审新字再一次apply/验其余未变/再冻结。除以上，45九维和所有卡图已读可通过；若新字变更需只读delta且保原已审摘要。原note/reader/read_at和索引不得改。

root已预先提醒agent3卷4和agent4卷5不要模板app/fail，不用研究流程凑九维。两者仍写包未交最终冻结，尚无根主审。agent5卷3原149已保，卷3root包正式后不交其重整。

## 导入辅助与下一

import_volume.py whitelist现又支持chapter-unresolved-index.json及prefreeze-reference-corrections.json/-2.json，使卷6报告链接届时可达。未来delta额外MD/JSON若有链接还需明确加白名单；不改已冻结notes。

先等审agent5新116字段+限定delta，验证原已审其余完全相等；完成review-vol06但不得跳卷4/5先导入。可以并行根主审已冻结卷4/5。六卷全正式后freeze全书池并通知既有代理：agent3 local1+4+36综合、agent4 local2+5+focused、agent5 local3+6+全书人物弧。root所有history/汇总/全量实际主审/出版终验。候选当前前3卷102历史1389local，零自动终点判定。

全项目最后仍需蜗牛管理/跨书机制、保护基线、全库证据和链接、fresh final backup+真正完整isolated restore；无Git提交推送/Space/memory写。最终才用先前memorycitation block。

## 主审后续的机械兼容修正

root读到卷6章索引用original_unresolved（不是前3卷unresolved），且1180卷题显式空数组。已修改prepare_zhanlong_audit_pools.py兼容两字段，保全部原行/空卷题在local_issue_records，并用empty_record_indices显式记空位置但不伪造候选；book_audit_common.load_package只允许被明确登记且确实空数组的章索引跳过候选覆盖。非空原问题仍必须有候选。所有实际逐章未决字符串+reader均验证相等。

已实际运行收池：前3卷仍102历史/1389local、零自动终评；validate_original_unresolved_compat.py实际核卷1=242、2=228、3=247、6=206非空行，只有6卷题index0空记录。test_book_audit_scripts.py六测试及test_primary_whole_book_review.py六测试均通过；先误用python -m unittest带.leading-path报Empty module name，已改直接python脚本运行成功，不是产品bug。WORKFLOW/cross-book-preparation头部已更新“全文齐/正式前3卷”。
