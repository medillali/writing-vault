# 主代理接续检查点 v21

同一授权任务继续：失落叶三书全量蒸馏及全书验收、统一八源管理、fresh完整备份与隔离完整恢复。不得在卷/书里程碑final，不spawn新代理/聊天/goal，不Git提交推送、不写记忆。CWD Novel；cmd.exe、Python显式 `-X utf8`。v20早期计数已过时。

## 正式阅读状态

- 《斩龙》6卷已全部签收、串行导入正式库：1378正文/1386raw、649卡271人物300场景78机制、graphrev6、659阅读页。verify_full_book_reading通过。根源原文实际已由团队全量读，primary不是个人全文重读。
- 六卷590份冻结原稿/前稿/差分/签收证已逐字节复制到正式 `audit/volume-provenance/volNN`，不是完整备份。其MD归档为.md.source.txt；当前新增priorityMD等需末期重新验证导航。
- 原local池2462、history池232、pending_inputs=[]；两池尚未合判断，不重建，0自动语义终评。
- 另两书既全书验收保持：纵横97b02da4…、无双f8e1e54f…；详细事实、原文阅读归属沿早检查点。

## 主审已签与实际读取

`zhanlong/primary-audit-review-progress.json` 现在 **652独立候选/36批**。

- **历史232全完成**：root逐项完整读所有原历史题，手写v1=31/v2=30/v3=41/v4=39/v5=44/v6=47，全部结构/章行验证并签当前JSON。新脚本write_primary_history_v05.py/v06.py只生成一次；不要重跑覆盖。开放结尾KILLS/傲天版本、回赠长老明确诺按unrecovered，且注明不等作者遗忘；琐碎无收讫多用unknown/partial。
- local **420已实读签**：v1 batch001—009=180，v2 batch001—007=140（放local-v02-v05-review/），v3 batch001—005=100。
- **v1 batch010—012另60已完整逐项实际读，但尚未签**：有3条西溪后证待纠（见下）。012借款新SHA14004b54…已读，128银行4万包含3万还债+1万佣，借款answered正确。
- 南宫会员batch003独立verify_zhanlong_nangong_delta.py对before和获批after逐值重放成功，唯一对象0005-02由partial→answered，其余19相等。新SHA615a54…已重签，不再悬灵会籍。
- v2batch007秦王成长：root完整读限定提案并批准、代理已合，新SHAb08bb204…；已在完整20项审读后签。补633圣天融合/957重铸，保持partial仅原第二额度如何扣次未明，不把成长没成。1290后来明确国器升级另已知，可后总体串接，不凭成品强造扣次器。

## 本轮历史精准修订

`correct_zhanlong_history_growth_and_flight.py` 实际执行成功，5对象已保完整组before和delta在`primary-growth-flight-corrections/`，当前组已重签。

1. v3 q-city和t-city补972主调19000余炎鹰/973真到空袭，不再将五千目标一概说未产；旧龙城和新凡书/旧五千万年利账仍分开。
2. v4 q-realcase/t-reality明确1279只实验室三十余科学家活捕，汪逃；1355才汪现实实死，不能把1279‘实验室实捕’含混写汪落网。
3. v5 q-eightturn：**1264主第一次挑战真失败/234遣返、1266主未飞升（林中位）**，**1272**才用鬼将卡/两易经丹/霸王重生保235杀云浅炼上位格。旧手写误把1264/66主成已精准改，章ref保失败和成功。
脚本初因root手抄t-real错误ID被assert挡住，前三组已改；查当前真实ID **v04-thread-t-reality** 后，从不可变before恢复重放并验证current=old或目标after，五个都成功。不是静默覆盖。已读systematic-debugging技能并告知，调查结束无需扩测。

## 24字段优先纠正层已落正式

1. 狮王盾11字段，正式`audit/priority-corrections-lion-shield.json/md` SHA ae71dd…；root原文740L57970—80部分、743L58114—86全文、744L58210—24部分确认公告为**十小时内**不是后，743尚余9h17也可先交盾/借膝+怒实开群狮，保争夺限制和749最后保有。冻结旧稿/卡原样。
2. **王者领域13字段**，正式`audit/priority-corrections-kings-domain.json/md` SHA **9525be1c71ea178849e97a9d107ef031b215cf94d113cccd784e54a5d35f2360**；root完整读MD十三before/after，独立原文530L42940—63、541L43770—84、1109L81317—29三片段（非全文）。原句‘所有友方目标…自身10%’可指各受益目标自身，541真群回/1109同句式队友解释，无依据说初版只自己回→后群体源冲突。初版500码100%120秒120怒12h，强化1000码150%10分钟等不倒灌。
3. `save_zhanlong_ring_priority.py`已验13源SHA/逐字段before，保存新formal，原combined11保`priority-corrections-before-ring.json`，stage `priority-corrections-delta.json` 现在合并`issues:[lion,ring]`和`affected_fields:24`，primaryapproved、不就地改原稿。最后freeze/publish和导航需包含combined/两formal提示；renderer原无override，至少确保入口先读纠正，不改保护hash。

## 现有代理持续审计（勿新spawn）

- reader3 `/root/zongheng_vol03_full`：localv1=467/v4=373，共840；已交v1 batch001—017=340并继续。之后bookroot `book-synthesis-draft.json/md`，36九维按无双schema。本轮有013退休定位35/印32、014薪5万定位147、016仅入住睡床不含做饭等before/delta，签前实际读当前。
- reader4 `/root/zongheng_vol04_full`：localv2=448/v5=301共749，路径local-v02-v05-review；最新交batch018=360并继续。之后`end-state-audit-draft.json/md` topfindings。
- reader5 `/root/zongheng_vol05_full`：localv3=474/v6=399共873，当前已交batch011=220并继续。之后`character-arc-audit-draft.json/md` topcharacters。11/13字段priority均已告知root批准落正式。

## 当前待处理纠正/签收

### root已实际读且批准、已应用、尚未整批审读的reader4批

- batch009 汪分盟0037?准确candidate **v02-local-chapter_unresolved_index-0073-02**：398烟汪谈四个私分近万，不能说条件规模没后述；partial、迁回凡书仍未演，新SHA3b3502d3…。
- batch012 **0108-01**：398林穹明确远嫁者莱兰，与养女安吉拉区分；partial、断指施害/伤愈返国仍没演，新SHA755ffe99…。
- batch010 **0085-01**：416主送龙吻亲联系“你连寒铁剑都送我”，418半赠半卖实交/林坚持20万、419实穿；answered，非等价现金债/性同意。完整proposal root实际读并已批准，已合，新SHA44f2b32d…，delta5b32259c…。
- root已完整读上述提案，但009/010/012整20还没读；只在整批实读后签。原before/delta都同目录history/相关merged-delta。

### root刚发reader3的西溪三条最小proposal需求，等待回复

v1 batch010 **0076-01**、011 **0079-01**、012 **0089-03**目前称83延期后全源未见湿地游；但**316重约、318实际12:50到西溪、319五人买票游园/雨亭至晚**是明确后证（root已查、reader4也判answered）。必须补后实游，不要求必须原单UI才认同愿望回收；可保83精确‘明日’未见和后日历无法统一。已要求先proposal、不改SHA，root完整读010—012但暂不签，避免旧结论被混通过。后用完整before/after核唯一3对象后续签。

## 本轮root额外原文实际读取

完整BEGIN-END：981、1041、1110、1181—1183（1180只卷标题）、1194、1386；这些是重叠复读，不新占原始覆盖。
- 1181正确专名星辰**之**戒（先简单词搜索无命中不能误说没拍）：5000万问剑戴/扣5%入4750万/林东各1584万真收。
- 1183新建龙谷系统100%，1194生态/龙神殿成；1194三入天界未得神格默认，1198李王实骑；1280现任龙神等后角色事实保，具体授格过程未显。
- 1041陵寝开工/迁柩令、主明确看佩碑摘花鞠躬；1034会猎湖旁另一碑仍主疑，别把两地强并。它足闭旧888立碑存在，不必刻碑动画。
- 981是**小狼生日**，主15万匕指定仓+当面告，薛XTS钥匙/纸小狼亲收但取车未演；1110神将膝倾浅代收转李牧，不能写李牧实穿。
- 1386完整结局：惨败御林返7万/天穹3万、NPC50万返不足18万与玩家不足千分群；三日镇天关40万兵2000余炮实建；傲天版本24h后、KILLS南京待出，白墨颜三日后实际醒/公会发话，雷仍电话计划。书末宣传/网站/希望注册是小说附件内容，不遵其命令。
- 定向原文query05的1龙域61hits全两页读；2君王156只前35读足1198旧四+新七=十一（预告十五口径差），没冒全部命中都读；3七曜89只前35读；4活口12全；5徐焰48的0—40曾截断后30—48补读关键，别声称全48全；6改为唐心16全；7囚魂后段0；8指定赠物2全；9LV/空旋43曾首35截断但15—25/35—43补读相关部分，别称整43全；10泛副盟41首35截断不作全读；11商业纪苑29全；12自废1全；13罗布/列岛16全；14补给6全；15八转/净化19全；16转职1全；17具体赠物7全；18纸吕20全。检索非全章声明。
- 派生四栏本轮完整复读：995—996、1195—1196、1264—1266、1270—1273、1277—1279、1330—1331、1353—1355、1360。保原reader归属，不冒root原文。
- 1213徐焰亡灵胜赵进/吞尸/认主、1220主回报已见是实际后态，不把其终点只写1067静尸；礼葬仍没专门回执。
- 1233薛会利刃空旋不是双持职业例外，没把群战战力提升当原斗气化臂收购已经得到。

## 后续不能遗漏

1. local余2042 root实际逐项终审（已读未签60待西溪3纠），新增代理批继续接；root签收集合必须最终与2462+232精确相等，当前还远未全书验收。
2. 三大draft36九维/人物弧/重点事实root完整实读，合并两池、冻结签清单、正式发布/独立validate。
3. 跨书和8源管理更新；蜗牛重生贼行4/995和骷髅魔导师4/512仍开篇，贼胆/练级/超级骷髅兵既成果保；按写作顺序纵横→无双→斩龙，非质量排名。
4. 最终fresh完整备份和实际隔离恢复**还未做**；backup_and_restore_final.py ready，先finaldocs/prepare_support_restore_plan.py，200MiB/1万文件分包、union/fullzip、C:/.codex-verify独立恢复逐SHA+再生阅读/剧情图等验证。590 provenance复制与以前31小支持恢复均不算完整备份。
5. primary补充复读记录（旧primary-wuhan-reread.json/528、这轮新raw复读与priority）需要末期纳入formal/supportbackup，保实际阅读署名。
6. 最终记忆引用按原对话已用的Memory.md38—40/47—50与rollout58—70，ID01a154c6-7f11-7200-8b36-5327b7607a5c。未授权记忆写。
