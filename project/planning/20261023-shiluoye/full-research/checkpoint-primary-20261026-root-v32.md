# v32：三书已真实验收，最终恢复正在运行，尚不能final

已承接v31完成所有人物，不重做研究/once-only发布。最新root29签组185研究项=161人物及关联主体+24重点；161=159单一人物或具名NPC身份条+2接口，不冒独立人数。r5 47/r3 62/r4 52全部根逐字段实际读审签；r3罗戟无源槽、火犁重复误述槽独立保，不造新人物。

- aggregate_zhanlong_reviewed_characters.py已once-only：新character-arc-audit-draft.json 5e900f14862fe025615ace831e85a279132d84aff8b345899a69af6f795a3df6；161对象逐值等签组；271唯一旧卡/272目标链接全覆盖，唯一split卷二6王翦/王将。mapping JSON206194c21c0dd2947a04b4d078e73013c988bbaaa24c5ce4ac2624660ddd268c；profile dfd1acbab8dd50d61c736dfb4ac68db47077b524530e3fb88e0f9566d0e393ee，保傅雷raw旧名而display_name为旗卫百夫长被冒充身份。
- 组装器root新增历史未采用TXT定位豁免；reader3只读指出间接引用边界后，root先新增反例测试复现，再加活动材料(path,SHA)递归闭包严格resolve，reader3实际只读复核通过。又实测旧MD链接不能按内容寻址快照目录解释，MD材料/旧MD快照存provenance，Python材料用.bin原字节防publisher移位；傅雷优先display无损渲染。最终25隔离守卫根实跑全通过。
- 编译器--write已once-only，正式冻结manifest **0d160522d181c89f6f1efaa141c7cadf51fc152443ea7f11050468de22627cf6**，四包原JSON字节保，638计划文件，22699定位引用（非去重引用数）。根真实record_primary_whole_book_review已执行，141签批/29签组2694候选语义逐值一致。publish_book_audit正式--reviewed已执行（profile传入）；validate_book_audit独立passed729冻结SHA/677发布文件/778原正式SHA/125发布导航。包内validate_material_archive也实际passed，无planning依赖。
- accept_book_and_advance.py zhanlong --reviewed已实际执行：三书都full-source-nine-dimensions-and-terminal-audit-complete，catalog8源2844卡active=null。纵横1180/1181 8卷432卡、48弧27重点105历史404原子；无双1599/1609 8卷751卡115弧30重点214历史3916原子；斩龙1378/1386 6卷649卡161研究24重点232历史2462原子。三书4157正文4176片段22卷108综合1832来源卡。蜗牛旧两书463/387不追认本轮重读；两部开篇书仍4单元各自原范围。
- 已刷新START-HERE、CONTENT-GUIDE、QUEUE当前段、collection本批验收当前段、机制索引当前段、写作机制比较序言及receipt。比较八节正文不改，旧序言/receipt精确保qa/cross-book-comparison-before-final-acceptance.json。新collection/三书最终验收.md已建，卡列初字典显示已修432/751/649。**审计发布后不得改ZL根README或reading README的nav外字节**，已冻结保护；二者提前定稿完成并有十纠正MD导航。
- 旧626主档/人工字段本轮再次verify_protected_baseline passed，baseline-protection已存。
- 全库首次check发现旧导航问题，未改冻结原件：纵横新review-changes.md精确copy原vol07；无双新report.md分卷一/二入口，避免同短名误指一卷。5份旧MD快照通过collection/qa/historical-markdown-contexts.json逐个SHA固定原导航上下文及精确旧JSON目标，不伪当当前可读页；directories链接允许真实目录。当前导航与历史上下文链接分别统计。导航改动后已实际全库passed：2844资产/8来源/0原创项目/8图，18检查点、24821当前链接。root新context变量最初误覆盖mapped计数，已改override_target并加type int守卫；最终备份前check输出reading_unit_segments_exactly_once已确认6739（不再是dict）。

## 当前唯一正在运行的必要工作

**exec_command session_id=19252**，命令backup_and_restore_final.py，整个过程不要中断或删目标。Fresh backup paths：

- R/backups/three-books-final-20261026-090719/
- writing-vault-full.zip、core.zip、reports-01/02/03.zip都已生成并逐包路径/大小/哈希核过。
- 正在标准restore(core)内部Vault.validate逐卡来源验证，程序内此处未加源缓存所以比后续check慢；实际进程python PID6680，129MB仍在（不宣完成）。最近stdout `restore core into new isolated directory C:\.codex-verify\novels-final-20261026-090719\writing-vault`。
- 真实恢复目标C:/.codex-verify/novels-final-20261026-090719/writing-vault。restore先临时目录验证再rename、加3报告包，再所有snapshot文件union SHA相等，重建图/卡/支持根文档，最后check(restored)独立三书/材料/导航复验。只有最终exit0和fresh-backup-and-actual-restore-validated才算完成，尚未。
- 备份前全库check已再次passed且full-project-validation已实际更新正确6739；这不是恢复成功。
- 不修改vault，避免快照/恢复比较不一致；只可更新B内部计划。等待时每60秒以内简短有意义中文进度，不重复宣已完，也不final。

## 恢复结束后必须收尾

1. poll session19252，若失败按具体原因修，保已有新快照不直接覆盖，必要另新恢复目录；不能假称成功。
2. 成功后读fresh verification.json与现库collection/backup-verification.json，核9163附近实际文件数/6739/24821/3书均accepted、active null、原TXT排除说明；最终文件数以fresh回执为准。
3. 更新B task_plan.md步骤5/6/7全部complete，progress.md当前段与最终checkpoint（只改内部非snapshot），记录真实备份路径和结果。新finaldoc当前备份指向动态回执，不必改冻结导航。
4. 可open_in_codex本轮最终验收页；最终简短中文给总入口/机制比较/恢复验收，说明原TXT独立保存、本轮未推送Git。全过程无Git提交推送/Space/记忆写入，无新goal或chat。
5. 最末memorycitation沿既定MEMORY38—40/47—50与rollout2026-10-19 58—70，id01a154c6-7f11-7200-8b36-5327b7607a5c。
