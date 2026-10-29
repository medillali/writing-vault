# 主代理接续检查点 v20

2026-10-26继续原同一任务，不在卷/书中途final。目标：失落叶三书全量、全书审计/跨书有效管理、fresh实际完整备份与隔离完整恢复。其他书既验状态保留；不新开代理/聊天/goal，不Git推送/提交，不写记忆。

## 本轮已实际完成

- 斩龙卷四report全文1100行及handoff读完；独立finalize_zhanlong_vol04_review.py重放4连续性对象、异常描述、佩儿关系、英雄盔edge精确获批差分；2865引用通过。reader-state相比早before并非byte不变：只status/current_state.coverage/next_work三项产物完成元信息变化，其余阅读事实完全相等，已明确签收而非冒称全state未变。
- 卷5/6原实际全读与最终签收由既有记录承接，finalize05/06成功。4/5/6已串行import成功。现在六卷正式：1378正文、1386raw、649卡=271人物300场景78机制，源图revision6，659中文阅读页。无额外旧开篇卡。verify_full_book_reading.py zhanlong passed，正式audit/full-reading-validation.json已存。
- import_volume.py支持新自审/差分证明复制和包内Markdown链接重定位；卷6handoff的report.md断链已精准改vol06.md，当前verify_zhanlong_current_links.py 680md/4418links无错。
- persist_zhanlong_volume_provenance.py已实际存6卷590份冻结稿/主审/差分before到正式audit/volume-provenance，逐字节SHA一致；MD源副本用.md.source.txt避免将暂存链接冒正式导航。不要无故改冻结分卷/签收。
- prepare_zhanlong_audit_pools.py已经全6卷建池：historical232、local2462，pending_inputs=[]，0自动语义终评。当前两池未装判断，不重建。所有原unresolved/reader精确保留。

## 正在并行的现有读者（只使用原代理，勿spawn）

- /root/zongheng_vol03_full：local v1=467/v4=373共840；已交v1 batch001—007(140项)且继续；之后负责bookroot/book-synthesis-draft.json/md，36九维，照天下无双schema。
- /root/zongheng_vol04_full：local v2=448/v5=301共749，文件放audit/whole-book/local-v02-v05-review/；已交batch001—009(180项)且继续；之后end-state-audit-draft.json顶层findings。另root要求核1266灵斩龙第一铸造师/957兄角色，对已交batch003南宫会籍0005-02拟补全书后证，先proposal不改SHA。
- /root/zongheng_vol05_full：local v3=474/v6=399共873；已交v3 batch001—003(60)正继续004；之后character-arc-audit-draft.json顶层characters。已有input-manifest各SHA。发现740/744原“10小时内”而旧notes/异常误读“后”，正准备priority-corrections-proposal.json/md给root核，未改正式卷。
- 读者不写池/正式库/全书签收或出版。每批<=20人工具体理由/后证，root真正逐项读后才记录。

## root实际已读并签的终评进度

primary-audit-review-progress.json目前 **282独立候选/16批**：历史卷1全部31(2批)、卷2全部30(2批)、卷3全部41(3批)=102；local v1 batch001—004=80、v2 batch001—003=60、v3 batch001—002=40，共180。其余local当前虽交尚未root读签。

- root历史原题0—109都完整读过，0—101已手写终评。102—109只是卷四前8题已读未判。下一历史可从110开始继续到140，卷4共39/indices102—140；卷5应141—184，卷6应185—231，实际再查。
- 手写脚本在audit/whole-book/write_primary_history_v01.py/v02.py/v03.py，生成各自adjudications-history-vNN-batchXXX.json。**不要重跑**：初稿与精准修订已保before/delta，脚本会因已有文件拒绝覆盖，正式终评以当前JSON为准。
- 3个root修订脚本已跑：correct_zhanlong_history01_before_sign.py补NPC冉闵1108身体全重塑/1109炼戒、1086本人认抹/1109回会替错指1090；correct_zhanlong_history02_before_sign.py把罗林末刀精确833问剑；correct_zhanlong_history_time_and_actors.py改2历史条目的528时点、七城胜果明确1346/1347/1357、银戈1178主末刀而非子舒独杀，以及国战线程后证。before及delta全存。
- 读者5local v3 batch001曾有“尚余4分钟已复活”误句，root已授权唯一rationale最小修订；before在local-v03-v06-review/corrections/batch001-time/before.json，旧SHA b88b...，新JSON053d1ebc...，verify_zhanlong_local03_time_delta.py独立验只1理由改/其余逐值相同，root完整读新理由后已重签。不要用旧SHA重新签。
- localv02 batch003南宫妹妹最终归属待读者补1266 proposal，旧批目前已签，改后需root核delta重签；不要求额外入盟UI以忽略后实际角色。

## 近期root额外实际阅读与精确事实

- root本轮完整原文BEGIN-END重读1091—1094，笔记primary-wuhan-reread.json：武汉真到、同现场南北区；上海指队籍，唐林一人队长；北片20余普通持刀者，南片殖装体，1A4B17C余D约50/2C活口；主轻伤不能泛所有人无伤。
- root本轮又完整BEGIN-END重读528 L42760—42848，无截断，primary-528-reread.json。主被问剑杀/爆寒铁，系统等4分钟后主出现60分钟无敌，林/牧复活；寒铁由小白→林→再亲赠小白，未归主。绝非活动尚余四分钟已复活，也非每人死亡另禁24h。
- 830—833定向原文全部罗林命中已实际读：绝望霜毁，832杀西奥多/夺元戎/主奥破盾夺回，833问剑系统末刀，炎龙伤将后斩尸头，非主独杀。
- 原文1178 L85954明确银戈主系统末刀；安娜子舒杀另对象，不可再混。1346东城报已拿七城/1347秦雯与1357燕赵后述印证。旧1359泛引已从root终评改掉。
- 原文839/840信号与12层：沈+天昕锁信号，主实际进窗，正规技术科非破解室，总经理室后基地，孙洪经理，沈文件破译简码74%。幕后完整法院链仍不同层。
- 原文922南宫决确接受主盟，957本人称斩龙骑士，1266主称斩龙第一兵器铸造师南宫灵；别只用926送现实剑补UI。
- 1108派生四栏root完整读：NPC冉闵身体全重塑，主亲见锻炉；1109实炼王戒。玩家冉闵老K另人。流霜记忆1068本人提沧澜印记，1146百龙骑/1316数百实控空，非千匹马全交。
- 全源定向卡尔/卡特252后无续、圣魂盾/冰壶/空虚扇252后无续（只有其他500餐费），洛阳252后无续；西溪318真抵/319买五票游。巴林315后无续，314两剑priority必须保。灭神锤/百战炎魔刀490后专名无续，454主捡锤/489李牧提刀，旧卖款不能第二记。

## root审阅工具

- read_zhanlong_historical.py start end：完整历史题+原记录+章行，20项约4k；目前已读0—109。
- read_zhanlong_adjudications.py <relative-batch>[@start:end]：完整原子题/判定/理由/后证章行，重复归属一次，去机械重复metadata；20项约3k。**一次functions.exec输出最好<=10k或显式max_output_tokens**，此前v3batch001长输出截断，已经重读精简版完整20后才签。不要据截断记录签。
- validate_zhanlong_adjudication_batches.py relative...：原题/原record精确、SID/rev/章行与判断结构、不重复校验，非文学读声明；过后record_primary_audit_batch.py zhanlong relative...。已真完整读的才能调用record。
- query_zhanlong_history01.py i以及02.py i start end：root定向原文命中检索（非全章阅读），02有15组，已有全部查询页实读，勿冒原文全书重读。

## 后续必须完成

1. root剩余历史130项人工终评；所有local2462完整逐项主审，改后重签，合并两池的candidate集合须与签收全集完全相等。
2. 740“内/后”等研究错误做显式priority overlay，原卷与旧notes留，所有下游解释服从真实源。root核字面实际原文，不凭agent描述即终签。
3. 36全书九维、人物全弧与重点事实实际逐项主审；全审计冻结、正式发布与独立validate_book_audit验收，synthesis精确输入签收发布。
4. 跨书对比与8源统一内容管理：catalog-config、START-HERE/CONTENT-GUIDE/RESEARCH-QUEUE等刷新真实范围；另两蜗牛仅开篇仍开篇，既有全研究保。书写顺序是纵横→无双→斩龙，不以顺序断质量。
5. fresh实际全量备份+隔离完整恢复尚未执行。backup_and_restore_final.py已有实现，先finaldocs再prepare_support_restore_plan.py。绝不将590文件证据复制或小支持恢复叫完整备份。
6. 到上述全完成才final，无逐卷确认，不新问抽样深度。最终memory citation沿前既用Memory.md/rollout条目要求。
