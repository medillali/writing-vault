"""整书终点审计草稿：亲读末卷+既有分卷研究，不是重新阅读全文。"""
import json
from pathlib import Path
R=Path(__file__).parent
S=json.loads((R.parent/'source.json').read_text(encoding='utf-8'))
cs={c['chapter_id']:c for c in S['chapters']}
def ref(cid,path,level='derived-research',a=None,b=None):
 c=cs[f'ch-{cid:04}'];return dict(source_id=S['source_id'],revision=S['revision'],chapter_id=c['chapter_id'],start_line=a or c['start_line'],end_line=b or c['end_line'],claim_kind='fact',access_level=level,research_path=path)
def own(i,a=None,b=None):return ref(i,'vol08/chapter-notes.jsonl','direct-reading-by-assigned-readers',a,b)
def old4(i):return ref(i,'vol04/chapter-notes.jsonl','direct-reading-by-this-agent-prior-volume')
def r5(i):return ref(i,'vol05/handoff.md')
def r6(i):return ref(i,'vol06/chapter-notes.jsonl')
def r7(i):return ref(i,'vol07/chapter-notes.jsonl')
def tail(i):return ref(i,'vol07-primary-tail/chapter-notes.jsonl')
F=[]
def finding(k,t,status,chain,result,boundary,ev):
 F.append(dict(key=k,title=t,audit_status=status,stage_chain=chain,terminal_result=result,boundary=boundary,evidence=ev,review_status='draft'))
finding('link-linqiu','林克与林丘明确分人','supported-vol07-draft-to-freeze',
 ['卷四林克盲锻/记忆权杖误认，铸甲后魂散。','卷五林丘是将领、妻米拉死/披斗篷、断一臂仍活。','卷七primary-tail菲雅述达尔弃林克/林丘为兄复仇，林丘被掏心再斩首。'],
 '林克先魂散；林丘在raw1035实际惨死。不能把后者当林克复死、也不能在卷八把旧神仆命名林丘当将领复活。',
 '兄弟关系为菲雅后述，现以卷七正式版本核定；卷八1091神仆名林丘纪念旧NPC不是叙述死者复活。',
 [old4(401),r5(434),r5(515),tail(1031),tail(1034),tail(1035),own(1091)] )
finding('aodan-life','奥丹：系统陨落、剧情存活、最后被杀','supported-vol07-draft-to-freeze',
 ['卷五冰兰自称击退奥丹，不等杀。','卷七raw1011冰兰剑贯胸，章内未判永久死；1012系统提示陨落/奖励，却保鲜红心、奥丹仍活。','1013净化成人但仍憎恨；1014—1015梦境看人类残酷与护人后愿入联盟；1016任第九军团统帅。','卷八明宇掷奥丹和巫师首级，并说明杀她/他，主冰兰反应与后文重复确认死亡。'],
 '奥丹到卷八raw1159才有明确最终被明宇杀的首证；不能回写卷七1012为已永死，也不能因曾净化推后来仍可无条件复生。',
 '卷七完整过程依primary-tail笔记，未由本代理亲读；任务完成/系统陨落与剧情生命要分账。',
 [r5(529),tail(1011),tail(1012),tail(1013),tail(1014),tail(1015),tail(1016),own(1159,124848,124858),own(1170,125814,125815)])
finding('wizard-death','大巫师的帮助、旧怨和实际死亡','supported',
 ['主为冰兰求巫，巫因冰兰昔杀其守护恶龙怀怨；知明宇/月哀风险后附条件借灵杖、要活祭。','主献等级、冰兰醒后与主共同跪歉，巫许未来合抗。','巫与奥丹佯攻地狱拖明宇，后来明宇掷其首级、斥本可安居南蛮却来自找死。'],
 '大巫师在卷八raw1159被杀明确，前期救冰兰与后来死亡应为独立人物弧；不能因当初巫有救神手段推自己已复活。',
 '救神格条件是本场具体交易，非无代价普遍复生公式；旧怨部分为巫证词。',
 [own(1133),own(1134),own(1135),own(1155),own(1159,124848,124858),own(1170,125814,125815)])
finding('purification-capacity','冰兰能否净化安妮：阶段与方法不可抹平','supported-with-causal-limit',
 ['卷七raw1013冰兰明确说安妮领域不逊自己，不能用同法净化。','卷八血吼识冰兰已成神；随后月哀碎神格，再经巫/活祭重建，实际醒。','猎安妮时冰兰仍未找到足抗月哀神器，捕获/寒潭/先除八成/斩龙牵引/雷鸣+主领域辅助是后来完整方法。','raw1170净化成功，安妮神格受伤需养；此时冰兰仍无法直接轻易战胜明宇。'],
 '“此前不能同法”与“后来新场景新方法成功”必须按时点保存；不能写冰兰始终随时可净化，也不能只凭成功删除此前限制。',
 '全书正式研究证据匹配已完成。阶段成长、神格重建、捕囚/圣光/斩龙/天雷是可比较差别，但未找到明说某一差别足以造成净化能力变化的说明，研究不替作者硬圆。',
 [tail(1013),own(1131),own(1132),own(1135),own(1155),own(1170,125767,125815)])
finding('annie-agency','安妮身份、受控与恢复后权位','supported',
 ['卷五霜之剑刃/旧女王/菲雅姐姐揭示，亲杀卡伦救妹后仍黑暗领袖。','卷八主潜听她护妹妹、拒替达尔报仇、惧明宇月哀；当面自述受欲控制。','活捕→修肢→雷鸣净化才实际恢复；再提供秘密寻镜、拒菲雅让王。'],
 '半年后菲雅王、安妮上将；安妮活且自主，没有再夺王，也非仍全受控。',
 '古史/月相/范围限制主要安妮证词，不把全体系均当系统实测；恢复不等她当时战力能敌明宇。',
 [r5(529),own(1157),own(1158),own(1159),own(1170),own(1172),own(1181,126744,126745)])
finding('mingyu-chain','明宇失踪判断与最后寂灭','supported-with-character-knowledge-boundary',
 ['卷七raw0915冰兰依据传承可签原认为导师死，却又感其气息；找到六尸而缺明宇/亚兰，任务独查。','raw0920亚兰自承杀六龙骑求力量，未交代明宇去向；0923系统杀亚兰/随后交任务不能自动证明明宇已死或复活。','卷八确认毁灭深渊明宇持月哀，害冰兰、杀巫奥丹、毁城；终战被冰兰碎心、黑暗灵魂及神格。'],
 '末明宇明确寂灭；其离疆力量减弱不等物理不能出界。初期“必死”是人物判断，不可和最终死亡合并为一条事实。',
 '月哀/入口联系来自安妮证词；圣者心和明宇神格是不同物，末分别处理。',
 [r7(915),r7(920),r7(923),own(1132),own(1159),own(1160),own(1170),own(1179),own(1180,126620,126623)])
finding('kallen','卡伦原死、复活与本次形魂俱灭','supported',
 ['卷五安妮亲杀卡伦解血色危。','卷八卡伦实再现285神，自述明宇用月哀复魂与力，先斩只是幻体。','冰兰龙缚本体再天雷，叙述明确身体元神俱碎。'],
 '本次形魂俱灭有文本依据，不能只因亡灵题材写任何死者皆可复活。',
 '圣者古史最初来自卡伦敌证，末仅部分力量与存在得到现场验证。',
 [r5(529),own(1175),own(1176,126283,126313)])
finding('soul','魂殇与烈魂召唤的不可逆结局','supported-vol06-formal',
 ['卷四魂殇化剑、烈魂召唤后来实战。','卷六raw0560系统魂殇永久毁灭、烈魂召唤特技永久消失。'],
 '卷四既有卡需保持当时可召；全书末不能仍列库存可召魂殇。',
 '魂散不自动等承诺复仇线圆满，要单独核其情感/敌人结果。',
 [old4(292),old4(294),r6(560)])
finding('linger-seals','灵儿三封印链与母史分开','supported-vol07-draft-to-freeze',
 ['卷三幻灵珠用途未明，卷四救援得灵儿、第一封印解除。','卷六raw0560灵儿归0后第二封印解，领幻神斩沉睡。','卷七raw0922 L103099系统第三即最后封解除/幻灵神格全面复苏，0923救主破镜；0963醒来确认最后封已解，展示0级裸装与持续气旋，随后重练到0985的228级战神。','卷八最后灵儿仍陪主问冰兰/爱。'],
 '三封印链已有关闭证据，不能列作全书“剩封印未收”。全书正式研究证据匹配已完成，未找到母系身世、与安妮旧识的完整独立终结说明，不以封印闭合代替全部身世闭合。',
 '0922解除宣布→沉睡→0963醒后状态是同一道第三/最后封的阶段链，不是新一道或第四次解除。母系身世仍按当前证据未知，不能由神格复苏推全史答完。',
 [old4(257),old4(387),r6(560),r7(922),r7(923),r7(963),r7(985),own(1181,126772,126779)])
finding('binglan-ending','冰兰终点：封冻、承爱与未知笑声','supported',
 ['卷四主不愿传承以导师死亡为代价。','卷八活祭救回后她仍欲独抗终局，最后称主最亲爱/托管龙域，生命禁咒封圣者并推出主。','半年后持首冰下静止，主每月来/明确答爱；听浅笑后再捕不得。'],
 '可写生命牺牲/长期封冻；不可写结尾确已复活，也不可把神格魂灭式永死加给她。',
 '主角体验是真实情感，但笑声可靠度未知；龙语者转正与接账是职责事实。',
 [old4(414),own(1135),own(1137),own(1180),own(1181,126740,126785)])
finding('qx-knowledge','秦月雪的性/亲密关系与知情不对称','supported-with-knowledge-limits',
 ['卷三秦韵仅未来期待/亲额，无性成立；卷五现实离开未归。','卷七raw0785雪拒同睡，提只爱她条件又不强婚；primary-tail raw1041书秦醉酒酒店当夜性关系明确。','raw1014夏误腿上凌月为雪，月顺认，夏未知；raw1056雪同床却拒性，主掩秦月齿痕/雪问后不追。','卷八raw1119秦忆第一次/愿留，主不舍；此夜吻后分房；雪后来提“我、姐、秦”仅证明意识多关系。'],
 '不能把雪不追问等同知道全部或许可；不能把秦回忆、月亲密、雪同床合成全员知情的性协议；卷末主雪无实际婚礼。',
 '已完成全书正式研究的逐场证据匹配，未找到秦月雪对全部亲密/性关系共同知情与认可的说明；不得按最终群聚反写早期选择。',
 [r5(451),r7(785),tail(1014),tail(1041),tail(1056),own(1119),own(1161,125070,125077),own(1181)])
finding('bingcha-health','冰茶病、身份与生命隐语','supported-vol06-formal-vol07-draft',
 ['卷四余生/生命坚强等隐语，当时无病名。','raw0774本人揭许冰/一年多前患血癌；许琳报告配对骨髓与约40%，清晨推入手术室。0775两日省略、名字消失及0777暗名都不能证明死。','raw0780本人上线报平安，说明上海手术未全成后转法国、以10%存活说幸存；0784电话仍法国休养。0811月估休养约三月，0849冰茶本人否认金发男友故事。','卷八回忆病重洗碗承诺、实际洗碗；许冰/许衡父女身份明确。'],
 '手术存死悬念已由本人后见/报平安回答，后来恢复相处明确；不能倒灌为卷四已确诊，也不能用疲累再次断言复发。',
 '40%为真堂姐许琳小说内转述/安慰、10%为后来剧情人物说法，均非现实医学统计。raw0774真堂姐与1093冰茶临时借许琳名自称分开，不把堂姐删成虚构。月的休养预估与返归实况分记；没有完整病历就不补治疗步骤。',
 [old4(415),r6(774),r6(775),r7(777),r7(780),r7(784),r7(811),r7(849),own(1086),own(1093),own(1167,125519,125528),own(1169,125662,125713)])
finding('marriage','婚约与婚礼分主体核兑现','supported',
 ['卷八凌天遗愿/股权条件有转述，秦称主雪未来两年后婚，非当时已婚。','冰茶说主雪正式一起将离/拒小三，后来返杭半年又再聚。','末随风雪见草上月北京婚已成；龙魂林霜婚礼后天，仍将赴。'],
 '只有随风雪见草本结尾明确已婚。主雪婚和龙魂林霜婚礼不可写为已经举行。',
 '许芳不反两侄女同在是其态度，非婚姻制度事实/双方新承诺。',
 [own(1107),own(1119),own(1150),own(1169),own(1181,126748,126750),own(1181,126827,126846)])
finding('travel-promises','赴美、回国、赴杭州的每次行程分开','supported',
 ['卷五姐妹美国/秦现实未归，末书冰赴杭尚路上；卷六raw0532实际面谈招两龙骑，0543正式建梦回/任军团长，不再只保路上。','卷七raw1042秦月实际取登机/离行、1056月短信确认抵美但专线未成、1058冰茶报已在线、1059主实际组五人队。','卷八1108月秦实际赶到凌天遗体；末又下月赴美工作计划。','半年后谈美国业务、末机场两女实际归，证明后一次也已出发并回。'],
 '不要把不同时段的赴美/返国合为一次长连续旅程；计划与抵达分别更新。',
 '两龙骑愿追随不等立刻加入旧雪月；独立结构梦回实际建立才更新。结尾“下月返”后“一周后到”保持跳接，不精算天数。',
 [r5(531),r6(532),r6(543),tail(1042),tail(1056),tail(1058),tail(1059),own(1092),own(1108),own(1180,126728,126736),own(1181,126795,126834)])
finding('business','经营/合同/股权与实际收款边界','supported',
 ['凌天分的是自己持股45/45/10；后主总7%以上口径可能不同。','蓝星月恒华东项目合同与运行在卷八实落地；许芳任九部门总监、冰茶为助理。','万达合作投入规模超3亿合同实签；后首单仍要雪签。','冰茶半年茶连锁/上海总店为结尾实见；S7单刷/股份收购等多为玩笑与判断。'],
 '可写经营与合作实际建立，不写三亿元已经全支付或所有预计估值已变现；龙域账单主接/指付，付款未展示。',
 '持股不补法律过户流程；主靠亲缘资源与人脉也要并记，不能全归纯技术。',
 [own(1107),own(1109),own(1115),own(1151),own(1168),own(1173),own(1181,126781,126785),own(1181,126817,126825)])
finding('xun-revenge','荀方结案分旧号、新号、组织、现实','supported',
 ['旧神算百计被压力实际删；后新神算千计147加入天下。','黄金灾毁后天下仍残余，1161主强制徽章退会/杀万余，未系统全解。','1174随风报追梦人倒戈/断魂谷全归零装爆，主自述荀破产、孤电话任职。'],
 '组织报复线可按报告结案，但荀现实活着任职；没有明确永久退游或司法结论。',
 '追梦人1125未答追求，1174实际交往不可提前；经济因果来自主自述，保强权伦理局限。',
 [own(1080),own(1112),own(1125),own(1160),own(1161),own(1174,126146,126161)])
finding('war-end','国战没有在终局永久结束','supported',
 ['疾风一时失王权/流亡，不等永久无国，后来复国报告。','兽魂破城后等民心维护纳中，野蛮当时退落炎。','末野蛮18出落炎夺曙光，七星移冰狼制衡；美仍英雄/闪光。'],
 '终点是主人公阶段退出，世界仍竞争；国家/公会失败不能写永久种族消失。',
 '民族贬抑是叙述立场，不转成研究者对现实人群评价。',
 [own(1096),own(1106),own(1167),own(1169),own(1181,126744,126751)])
finding('golden','黄金城不可算雪月攻占成果','supported',
 ['1114主毁厅后离，1115清风由友会已收回。','1154拟周末夺黄金，因主线改道延期。','1160末日深渊将黄金物理毁/天下流亡。'],
 '黄金的消失来自明宇灾毁；主利用结果不等亲自夺城、正式转属。',
 '系统公告1154误清风/旧名百计不应另建一战。',
 [own(1114),own(1115),own(1154),own(1160)])
finding('items','物品获得、可用、损毁与末持分开','supported',
 ['北冥/神舞剑先得但等级/天域未达；275后才用。','北冥MVP魂10实成；永恒活祭后六太古明确。','北冥1179连柄碎、北冥镜1177碎；1180月哀净化并绑定主。'],
 '末主不同时持完整北冥与月哀；镜不在库存。掉宝价估、基础属性概率与实际触发需分开。',
 '无全量幸运基线不自行加总末值；升级奖励两次+10已面板270，后来271/285另有时间节点。',
 [own(1068),own(1078),own(1085),own(1135),own(1150),own(1151),own(1172),own(1174),own(1177),own(1179),own(1180)])
finding('saint','圣者线关了入口危机，留下恶灵','supported',
 ['卡伦说遗物/圣者堕落史为敌证；系统终极任务要求10秒阻入口。','明宇修罗咒开门，多恶灵逃；冰兰杀明宇后圣者实际探头。','心碎/圣者断首与冰封；系统成功、新十王；半年佩妮娜新敌。'],
 '明宇及当前终极任务resolved；圣者封禁partial（截至半年持续）；恶灵和世界战争open。',
 '不要将任务成功等同十秒逐帧时钟证明，或给圣者续作剧情。',
 [own(1176),own(1178),own(1179),own(1180),own(1181)])
finding('guild-life','工作室解散、公会衰落、人生继续','supported',
 ['凌月正式宣布工作室解散/成员入蓝星/冰离意向。','半年亲友就业、学习、结婚，主雪很少上线，公会仍有十余分盟。','冰茶茶链重逢、月韵机场归，群体在商务车雨中同往苏州婚宴。'],
 '不能写雪月公会当场解散、所有人退游、生活彻底无战；团聚不等旧组织与角色职责原样复原。',
 '花火/冰之逸分别哪一会盟主句序未逐一配，不凭常识强配。',
 [own(1180,126728,126736),own(1181)])
finding('old-opening','早卷醉因/拒戒/旧弓等是否全回收','specific-detail-unknown-after-volume-research',
 ['卷一二研究保留醉倒/拒戒完整缘由未知；旧弓出售→实际交还，赠物不等可装备。','卷三手伤/亡姐回忆、卷四扫墓与情感展开，不等自动解释所有开篇醉因。','raw0779姐妹拜她们的母墓，主/香等拜亡姐墓；raw1037主自述童年母亲离家、仍活与否未知，不能用姐妹扫母墓证明主母已亡。'],
 '已完成全书正式研究证据匹配。旧弓回流明确，但未找到醉因/拒戒完整缘由的明确说明，不能凭后期温暖或身份披露宣全部resolved；这些是终点未知而非未执行的审计步骤。',
 '全卷问题/线程现已全收；仍未精确匹配这些细节的单一解释，不把未知判作作者遗忘，也不靠后期关系倒填。',
 [ref(101,'writing-vault/library/reports/zongheng-tianxia/vol02.md'),ref(102,'cross-volume-audit.md'),old4(248),ref(779,'cross-review-late.md / late-09','derived-independent-source-review',86162,86178),ref(1037,'cross-review-late.md / late-09','derived-independent-source-review',114240,114244)])
finding('wang','王俊杰、红绫和血饮现实案的不同信息来源','supported-with-testimony-limits',
 ['卷四336委托后345龙魂报告报复落实，第二批刻脸归凌天仍猜；卷五王仍天骄/月神关系与红绫保护。','卷七980围观妇女转述王被打死/红受多人暴力，981凌天电话确认被害却明说不知凶手、雪述王颈椎碎死/红住院精神创伤；月称鉴定未完。','982秦据仇怨与车活动推血饮；凌天报血饮尸13刀3心且归郑家为其说；主猜红亲刺/冰茶自有消息称血饮参与均非警方结论。','红后重建并收五旧部、冰蛋仍保，转雪盟友。'],
 '王现实死亡与红受害/重建、血饮后来报尸可分层记录；不能把早报复当未实施，也不能把凶手归因写成已侦破。',
 '涉及暴力/性羞辱，保信息来源、受害者后续能动性与权力伦理；不将传闻推断写司法事实。',
 [old4(336),old4(345),r5(471),r6(643),tail(979),tail(980),tail(981),tail(982),tail(983),tail(994),tail(1022)])
finding('npc-recovery','战时全灭、胜后军力恢复与个体死亡分账','supported-vol06-formal',
 ['卷六raw0669 L72568系统奖励恢复损失75%物资/军力；L72570书估十多万NPC至少复活七八万，两者为系统与人物估算不同层。','卷七raw1012守城后系统恢复80%死军并增50%数量；奥丹本身系统陨落后仍剧情活更说明结算与生命不能简单等同。','卷八终战地狱天灾覆NPC军团、 named人物明宇神格灭/巫奥丹首级等各有独立结果。'],
 '不能从战时全灭推卷六守都NPC全部永久损失，也不能以早规则盖后来恢复奖励。反过来，军力恢复比例不自动证明每个有名死者复活；需个体后续出现或明确说明。',
 '恢复是该战系统奖励而非所有NPC不死通规；卷八未见相同恢复就保“战时覆灭/未展示恢复”，不写跨全书一律不可复活。',
 [ref(669,'卷六正式审修/主代理raw0669独立复读',a=72568,b=72570),tail(1012),own(1159),own(1177)])
finding('ambiguities','源文内部异常与可解释口径分开','supported',
 ['活祭245/+5/250与255/降23冲突；永恒进化等级前后摇动；17殿名纠炼狱但末14/15未解。','迁沪后苏州异文、局部山鹰天域/三女圣域、晋32实16、人名/公告地名混。','股份个人份额与总比例、角色主观估值与现金是不同口径，不宜都称错。'],
 '保异常清单，不以强圆隐藏机制取代文本；能分口径的先分。',
 '证据定位有效不等设定自洽，文学审阅与用户审美另行。',
 [own(1084),own(1130),own(1135),own(1142),own(1146),own(1154),own(1163),own(1169),own(1173),own(1174)])
finding('protagonist-name','丁舒升、轻狂书生与丁书生不另造人','supported-by-targeted-source-check',
 ['raw0004 L166本人纠正凌雪：原名丁舒升，不是书生。','raw0966 L106934 CGL字幕明确轻狂书生原名丁舒升；丁书生见于房东/姐妹招呼与牌子，不能反定原名。'],
 '全书人物弧主名为丁舒升／轻狂书生；丁书生作为误称或招呼名互指同人，不建立另一个人物。',
 '本次仅定点复核这些原行，不把它增加成卷一/卷七全文亲读声明。',
 [ref(4,'原行定点复核','targeted-source-verification-not-full-chapter-reading',166,166),ref(966,'原行定点复核','targeted-source-verification-not-full-chapter-reading',106934,106934)])
finding('dragon-god-identity','龙神的物品旧史与血吼自述不能无证合案','identity-unknown-after-full-volume-inputs',
 ['raw1012 L111778—111790神骨之弦介绍，L111786称奥丹偷袭龙域杀龙神，取跖骨/筋制弓。','raw1131 L122308血吼自称捏碎昏庸老迈金龙龙神之心，并自称新龙神。'],
 '两来源并列保存：是否同一实体/同一事件未证；不选定称号承继，不强圆证词冲突，也不自动造两代龙神。末龙域责任转移与这个身份疑点分开。',
 '1012为物品介绍、1131为敌方自述；独立晚段复核来自卷三读者定向全文重读1012/1131，不宣其已亲读整卷八，本代理该旧史证据为派生复核。',
 [ref(1012,'cross-review-late.md / late-04（卷三读者定向全文复核）','derived-independent-source-review',111778,111790),own(1131,122308,122308),own(1180)])

snap=[]
for name in ['vol06','vol07','vol07-primary-tail']:
 p=R.parent/name/'chapter-notes.jsonl'
 ns=[json.loads(x) for x in p.read_text(encoding='utf-8').splitlines() if x.strip()]
 snap.append(dict(path=str(p.relative_to(R.parent)),count=len(ns),last_chapter_id=ns[-1]['chapter_id'],status='notes-consulted-for-derived-audit',duplicate_coverage=name=='vol07-primary-tail',ownership_note='primary-tail已并入vol07，不重复累计阅读覆盖' if name=='vol07-primary-tail' else '保留原读者归属'))
for f in F:
 f['audit_status']=f['audit_status'].replace('supported-vol07-draft-to-freeze','supported-formal-inputs').replace('supported-vol06-formal-vol07-draft','supported-formal-inputs')
A=dict(title='纵横全书终点人物/问题/伏笔审计草稿',source_id=S['source_id'],revision=S['revision'],review_status='draft',status='ready-for-primary-whole-book-review',method='以卷1—8正式分卷研究和本代理卷四/末卷亲读为基础逐项审计；其他卷资料查询不等本代理重新阅读全文。原行姓名定点复核单独标层级。',direct_reading_ownership=[dict(reader='zongheng_vol04_full',scope='vol04全部178；vol08 raw1081—1181共101'),dict(reader='primary',scope='vol08 raw1061—1080共20，保留原笔记')],consulted_research=[f'writing-vault/library/reports/zongheng-tianxia/vol{v:02}-analysis.json / vol{v:02}-graph.json / vol{v:02}-cards.json' for v in range(1,9)]+['cross-volume-audit.md','vol06/chapter-notes.jsonl（定向查证）','vol07/chapter-notes.jsonl（含primary-tail合并，定向查证）','full-research/review-vol06-vol07-bridge.md','full-research/review-vol08-ending.md','review-vol06.json','review-vol07.json','review-vol08.json'],research_snapshots=snap,findings=F,coverage_statement='各卷analysis.open_questions与graph.threads全收105条；混合未明/异常原子项404条逐条判定。穷尽这些输入字段不等穷尽正文所有潜在伏笔。',library_count_boundary='本轮八卷包426卡（150人物/205场景/71机制）；加原开篇6卡后全源432（153/207/72），不是本轮新增432。',remaining=['等待主代理整体文学审阅；用户审批/收藏仍未发生。','保留具体证据未知、来源异文和认知限制，不把unknown等同未读或作者遗忘。','不读天下无双，不写正式库/Git。'])
for f in F:
 for e in f['evidence']:
  c=cs[e['chapter_id']];assert c['start_line']<=e['start_line']<=e['end_line']<=c['end_line']
(R/'end-state-audit-draft.json').write_text(json.dumps(A,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lines=['# 《纵横》全书终点人物／问题／伏笔审计草稿','', '**状态：八卷正式输入齐备，待主代理整体审阅；不是重新全书阅读全文。**','',A['method'],'',A['coverage_statement'],'',A['library_count_boundary'],'','本代理亲读卷四178章与卷八续101单元；卷八首20由primary亲读并保持其原始归属。其他卷是正式研究与读者笔记的派生复核，不计本代理全文阅读；primary-tail已并卷七，不重复累计。','', '## 咨询过的读者笔记','']
for x in snap:lines.append(f"- `{x['path']}`：{x['count']}条，至`{x['last_chapter_id']}`；{x['ownership_note']}。")
lines+=['','## 本次最重要的修正','', '- 灵儿第三封印已有卷七raw0922系统证，不能把“剩余封印”列全书未收；母史终点未知另记。','- 奥丹卷七系统陨落仍剧情存活，净化/转立场/任军团长后，卷八才有被明宇首级确认的最终死。','- 林克、林丘为两人，后者为前者复兄仇；林丘raw1035斩首真死不是林克二次死。','- 冰兰此前不能同法净化安妮与后来不同方法成功需分阶段，不把阶段/方法差别当未经文本明言的万能解释。','- 秦月雪的知情、同床、性关系、婚约、婚礼分别记，末群聚不等全部知情许可。','']
for j,f in enumerate(F,1):
 lines +=[f"## {j}. {f['title']}",'',f"状态：`{f['audit_status']}`。",'']
 for x in f['stage_chain']:lines.append('- '+x)
 lines +=['',f"终点判定：{f['terminal_result']}",'',f"边界：{f['boundary']}",'','证据入口：']
 for e in f['evidence']:
  lines.append(f"- `{e['chapter_id']}` L{e['start_line']}—{e['end_line']}；{e['access_level']}；`{e['research_path']}`。")
 lines.append('')
lines+=['## 整体审阅入口','','- `historical-question-pool.json/.md` 保留所有原resolved与独立终点判断；`local-question-pool.json/.md` 展开混合字段，源异常不混为人物伏笔。','- `character-arc-audit-draft.json/.md` 提供初始比较阶段→决定→代价→终态，具体未知保留。','- `audit-validation.json` 只证明字段完整、证据章行有效及冻结卷八核心未变，不代替文学解释审阅。','- 本审计不直接导入正式图，不读取后续作品，不据群聚反写所有承诺已兑现。','']
(R/'end-state-audit-draft.md').write_text('\n'.join(lines),encoding='utf-8')
print(json.dumps(dict(findings=len(F),evidence=sum(len(x['evidence']) for x in F),status=A['status']),ensure_ascii=False))
