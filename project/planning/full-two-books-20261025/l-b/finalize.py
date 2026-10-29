from save_batch import *
import sys
sys.stdout.reconfigure(encoding='utf-8')
B=[json.loads(f.read_text(encoding='utf-8')) for f in sorted(P.glob('batch-*.json'))]
A=[json.loads(f.read_text(encoding='utf-8')) for f in sorted((P.parent/'l-a').glob('batch-*.json'))]
assert [u['ordinal'] for b in B for u in b['units']]==list(range(194,388))
def write(name,data): (P/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
def end(status,answer,*e):return {'final_status':status,'answer':answer,'evidence':list(e)}
Q={}
for b in A+B:
 for q in b.get('questions',[]):
  status={'resolved':'resolved','partial':'partial','open':'unknown','unknown':'unknown'}.get(q['status'],'unknown')
  Q[q['key']]={'key':q['key'],**end(status,q['answer'],*(q.get('resolution_evidence') or q.get('setup_evidence') or []))}
overrides={
'titan-identification':end('resolved','220得泰坦图与导师，320拆开篇旧钟取泰坦心并实际制造恩特；鉴定费6251本身未写支付。',ev(221,9206,9256),ev(321,14743,14765)),
'warlock-exile':end('partial','后文王室政争及跨阵营和解展示布拉卡达地位；未对开篇逐术士历史给唯一完整真相，不应把后事追认为当时官方已错。',ev(330,15457,15542)),
'name-anomaly':end('partial','早期萧寒疑误写仍保留；终章父亲实际实名萧寒，不意味着早期每处混名都另增父亲在场。',ev(9,272,318),ev(388,23217,23229)),
'old-warlock-motive':end('partial','后段马尔都克/旧鉴定师政争及戒附件回收；未把最初雇佣的每项隐意独立解释完。',ev(294,13098,13147),ev(295,13148,13193),ev(296,13195,13235)),
'being-watched':end('unknown','该次罗格眼被注视感未见后文具名揭晓；不把莫雷卡托或后续敌人倒填为观察者。',ev(78,2846,2885)),
'ore-compatibility':end('resolved','后段混材按设计规则制泰坦/水晶，水晶胸四肢用红岩、翼腰用梦菲斯并吸雷，实际完成。',ev(367,20255,20282),ev(367,20289,20306)),
'soul-fragment':end('unknown','欧斯林克所得一级灵魂碎片未见明确消耗或用途；不能与莫雷卡托灵魂结晶、血羽心合并。',ev(98,3536,3564)),
'timos-identity':end('partial','前半已揭偷阿卡德项链、诱塔进院行为；镇长之子身份在后半未新增直接确认。',ev(148,5834,5838)),
'curse-trigger':end('partial','诅咒事件前半实际解除；旧鉴定师后为马尔都克且政变被王杀，戒附件获交，但不逐项解释早触发全部意图。',ev(295,13148,13193),ev(296,13195,13235)),
'artifact-misrecognition':end('resolved','当时希莱尔仍史诗，后295合可升级亚神器魔神戒，371才升真神器，区分时间。',ev(296,13216,13235),ev(372,21034,21044)),
'ring-round-mark':end('partial','后文卡尔洛斯解释封印成戒灵并融合魔神戒；早先圆图的每项具体效用未独立说明。',ev(277,12230,12271),ev(278,12272,12309),ev(296,13216,13235)),
'low-task-choice':end('resolved','该转职不安全迅速，流程曾加难，但前半到193已完成机械主转；不是后半英雄或60二转同一任务。',ev(175,7031,7045),ev(187,7572,7586)),
'hua-detection':end('unknown','花舞感知周围玩家方式后半未明示机制；不能等同萧翎恶瞳或双胞探隐。',ev(162,6513,6516)),
'moon-crystal':end('unknown','拟给月落的月亮晶石用途/实际交付未明确回收；与无岚无羽给六枚月光宝石造起搏器名称近似不能自动合一。',ev(151,5941,5943),ev(334,15826,15935),ev(335,15936,16048)),
'gargoyle-transfer':end('partial','后文明确可用神炼和转灵魂保原意识，水晶完成仍同伙伴；这解决人物延续但不抹掉早44拆毁规则与后规则差异。',ev(45,1667,1690),ev(243,10384,10485),ev(367,20292,20306)),
'holkad-aura':end('partial','恶魔气原因与三传承交付前半已解；霍尔拟受审之后判决、神赦、死亡都未写。',ev(194,7881,7909),ev(195,7912,7960)),
'night-luo-master':end('resolved','195两天升宗师，217承担军药义务；338五戒合药王戒至大宗师，专家药供应全团但不是无限供所有盟团。',ev(196,7962,8000),ev(218,9002,9084),ev(339,16492,16613),ev(356,18920,18930)),
'guest-security':end('resolved','不保证安全：随后狂龙挖角围杀及内线打压确发生；天狂213风险投资并234续长期合作，最终正式竞技击败狂龙。',ev(214,8723,8734),ev(235,9864,9925),ev(381,22390,22410)),
'q-horadric':end('resolved','330夜落用药学四过程精灵语解红生命树；334七符文开库取得魔盒并全团共享。',ev(331,15543,15625),ev(335,15936,16048)),
'q-dynamic-mission':end('resolved','已给动态战况导致任务升SSS的规则解释，守援并完成85%结算；没有人为设局确证。',ev(203,8265,8293),ev(217,8912,9001)),
'q-independent-contract':end('partial','后续已接受追加五千万长期合作且实际竞技胜狂龙；原一个月3000万/违约金合同未逐条审计精确期限与清算，不写全部原条款结清。',ev(234,9830,9863),ev(235,9864,9925),ev(381,22390,22410)),
'q-xiaoyu-id':end('unknown','本书明确同名亡灵贼和相似跨书事件；仅本书未直接声明等于另一小说主角。跨书对应另交联合研究核，不自动合实体。',ev(200,8127,8129),ev(387,23116,23117)),
'q-spy':end('resolved','黑蛇盐磷定位匡飞天骑；前者逐出后者留反间，天骑承认钱与暗恋林菲，完成围狂龙后逐。',ev(245,10564,10642),ev(246,10643,10745),ev(292,12985,13047),ev(297,13238,13283)),
'q-rings-count':end('partial','最后实际五戒合亚神器药王戒、夜落大宗师；早两/三/四数量跳变无补齐解释。',ev(225,9400,9453),ev(339,16492,16613)),
'q-wuloves':end('resolved','两女身份与救命动因已明；终章邮件称三人在商务公司上班且同居，未写婚姻或确定排他关系。',ev(233,9774,9829),ev(388,23233,23235)),
'q-general':end('resolved','旧20万将军套目标后来被50万荣耀准帅套实际超越，公爵是功勋另轴，不能混为同任务。',ev(349,17816,17999),ev(374,21601,21613)),
'q-double-rings':end('resolved','七功勋遗物同源，三附件组成魔神戒；伊克斯最终由王赠后合成，异界钥匙传说仍未直接打开异界。',ev(277,12230,12271),ev(296,13216,13235)),
'q-engineering20':end('resolved','欧斯特雷神银20块已给，312七八天大宗师，320取泰坦心制恩特；不把目标20天写成耗足20天。',ev(301,13468,13489),ev(313,14100,14108),ev(321,14743,14765)),
'q-capitalfall':end('resolved','圣光城先系统沦陷-10%，外交保居民撤离敌三天退；黄昏又遭外敌毁城，二战别合一次。',ev(331,15543,15625),ev(336,16049,16145),ev(383,22603,22612)),
'q-arland':end('resolved','328认父，329确认天下股东扮维护NPC，终章父亲萧寒安排重逢。',ev(329,15350,15456),ev(330,15457,15542),ev(388,23217,23229)),
'arland-debt':end('resolved','父子关系在328/329明示，亏欠与关爱由后续公爵奖及现实重逢深化；不倒填每句当时心理。',ev(329,15350,15456),ev(374,21561,21583),ev(388,23217,23229)),
'ring-exp':end('unknown','295/304经验比例冲突未被解释，371神器新属性另为+200%戒吸50%，只更新阶段不抹旧冲突。',ev(296,13223,13228),ev(305,13648,13659),ev(372,21038,21044)),
'vanity-secret':end('unknown','净化后虚荣戒古怪未见进一步说明；林菲后续用刺客技能不等于戒余谜已解。',ev(313,14075,14083)),
'who-made-puppet':end('partial','最终资料说沃顿掌握包括伊森得的强大存在，建立隶属；泥人制作人未直接具名，不能说沃顿亲手烧陶。',ev(364,19851,19854),ev(382,22520,22522)),
'second-transfer':end('resolved','382接60级二转光之引导，383全军团最终完成；神格与众神让力为随后任务临时强化。',ev(383,22643,22662),ev(384,22723,22729),ev(387,23123,23124)),
'duke-fairness':end('unknown','主脑接受与父违背规则的叙述措辞冲突未获澄清。',ev(374,21565,21570)),
'arena-kuanglong':end('unknown','365称狂龙也参加1v1、373改未参，后决赛实际天龙，不能据后状态抹前矛盾。',ev(366,20165,20168),ev(374,21498,21498),ev(375,21814,21815)),
'post-landing':end('partial','现实伙伴工作婚恋与四女团聚有终章直接后日谈；游戏是否继续运营未明确。',ev(388,23232,23260),ev(387,23150,23152)),
'tomb-count':end('unknown','王室墓穴七与总九前后不一，任务实际完成不修正墓数。',ev(353,18452,18673),ev(354,18674,18831)),
}
for k,v in overrides.items():assert k in Q,k;Q[k]={'key':k,**v}
write('terminal-question-map.json',{'source_key':'l','coverage':[1,387],'method':'前半handoff与全部阶段问题逐项终态核对；unknown不等于abandoned，源矛盾保留。','items':list(Q.values())})
H=json.loads((P.parent/'l-a'/'handoff-to-second-half.json').read_text(encoding='utf-8'))
cross={
'titan-heart':overrides['titan-identification'],
'goblin-map':end('resolved','339花舞同行开始主藏宝图路线，经西瘟疫入机械城，347爆城脱险并保装备刻刀材料，水晶伙伴366实造。不是前半罗格眼小宝藏。',ev(340,16614,16722),ev(344,17101,17242),ev(348,17669,17815),ev(367,20292,20306)),
'five-ring':overrides['night-luo-master'],
'soul-fragment':overrides['soul-fragment'],
'akad-set':end('unknown','阿卡德荣耀项链在前半入队，后半未见四件完整套装与共鸣回收；不能因别套集齐算本套完成。',ev(148,5834,5838)),
'gems':end('partial','242五符文换五暗黑宝石并重造转魂、243全团镶嵌附魔兑现升级；前半每枚翡翠/湛蓝采购及找盾图造新盾未逐笔点明。',ev(243,10384,10485),ev(244,10486,10563)),
'moon-crystal':overrides['moon-crystal'],
'marduk':end('resolved','旧鉴定师确认马尔都克，索主角效忠后出城恶魔化，王已防政变并实际杀死，伊克斯戒由学徒交出；女学徒是否间谍仍主角猜。',ev(293,13048,13097),ev(294,13098,13147),ev(295,13148,13193),ev(296,13195,13235)),
'frontline':end('resolved','196至圣光城，197接军务，攻守迪菲利亚至援军来，215任务成216得85%奖励；付团员与石像鬼险死代价。',ev(197,8003,8041),ev(198,8042,8071),ev(215,8767,8837),ev(217,8912,9001)),
'rivals':end('unknown','早期猎杀者/猎头者及无实名亡灵法师未见后半身份一一再确认；不与萧御或其他亡灵角色合并。',ev(13,461,496),ev(52,1904,1936)),
'reality':end('resolved','父亲揭天下主脑维护和移民航船框架，终章营养仓醒实际新星登陆；序章冰棺人生由宇航休眠现实框架收束，但梵天之梦哲学不被实验论证。',ev(330,15457,15542),ev(372,20990,20995),ev(388,23156,23161),ev(388,23217,23229)),
'female-pilots':end('resolved','216批准无炎两女友入团，后229/230双胞无岚无羽现身探隐，232救命经历明；终章三人同居上班。',ev(217,8912,9001),ev(231,9663,9722),ev(233,9774,9829),ev(388,23233,23235)),
'perfect-fire-crystal':end('partial','三传承后段实际被牧野引用并沿用父爱主题，完美火晶具体镶嵌去向未再明确；不编分配。',ev(194,7905,7906),ev(374,21567,21568)),
'ring-max-not-stack':end('resolved','后续魔神戒保三系能力并升神器；没有由四职业相乘推数值，最终强度来自独立明确神器/引导增幅。',ev(296,13216,13235),ev(372,21038,21044)),
'aggro-wall':end('resolved','门锁伊森得仍需仇恨，光柱等条件使前提变化；沃顿明示智慧不受仇恨约束转身体卡位，没有取消全游戏仇恨系统。',ev(362,19591,19600),ev(386,22965,22979)),
'gargoyle-continuity':overrides['gargoyle-transfer'],
'rogue-eye':end('partial','217罗格眼险毁，后用石像鬼换视而非凭罗格传声；500码/无声不因换载体取消。未重写宝藏造眼者全貌。',ev(218,9002,9084),ev(348,17669,17815),ev(385,22845,22849)),
'mana-spring':end('resolved','火魔战明说连拥有源泉的主角仍耗空，牧师靠神圣恢复和专家药CD，非源泉无限/给牧师同效。',ev(373,21257,21281)),
'god-oath':end('resolved','伊特斯互誓通过只不杀不等于不囚保留空隙，等死真神誓保密才放开水晶；誓约仍需按措辞和主体记录。',ev(348,17669,17815),ev(370,20662,20668)),
'xiao-ling':end('resolved','46榜376推进到联盟等级第一、68后二转全成；个人双人及团队夺冠，主神力为临时，现实四女团聚；最终精确等级未再固定。20技能栏后遗失书可替换使用。',ev(326,15148,15199),ev(370,20583,20598),ev(383,22642,22662),ev(388,23239,23260)),
'tian-kuang':overrides['guest-security'],
'wu-yan':end('resolved','主盾与教官延续，军团前锋并三/五赛冠；现实与双胞同居工作。',ev(380,22186,22186),ev(385,22825,22831),ev(388,23233,23235)),
'ye-luo':end('resolved','宗师、大宗师、五戒及有限强药兑现，最终第三、现实与月落婚。',ev(339,16492,16613),ev(375,21685,21705),ev(388,23232,23232)),
'mu-lin':end('resolved','原女友延续至现实重逢，但371性关系叙述有激烈反抗，不把多人结局反向宣称全过程自愿。',ev(372,21177,21178),ev(388,23208,23223)),
'fei-yu':end('resolved','亚神器套实际分配、终局四伴侣之一现实重逢；没有直接写她独立宣誓接受多人婚姻。',ev(364,19906,19908),ev(388,23214,23223)),
'bath-shadow':end('resolved','浴血德鲁伊分指挥，乱影侦察及三盗互救；现实本城各工作浴血恋爱。',ev(381,22342,22345),ev(385,22870,22878),ev(388,23238,23238)),
'hua-wu-liu-shang':end('resolved','花舞324自由契约脱狂龙330入团340同意恋人342亲密，最终现实重逢；流觞随团单人第六、现实雨蝶恋成。花舞探玩家机制仍未知。',ev(325,15095,15147),ev(331,15543,15625),ev(343,16938,17100),ev(388,23238,23260)),
'holkad':end('partial','三件传承已交及父爱话语后来引用；受审判决、宽恕和死亡未直接写，保持未知。',ev(194,7881,7909),ev(374,21567,21568))
}
cross_items=[]
for section in ('core_characters','rules','open_and_recheck'):
 for item in H[section]:
  assert item['key'] in cross,item['key']
  v=cross[item['key']]
  cross_items.append({'key':item['key'],'handoff_section':section,'setup_state':item['state'],'setup_evidence':item['evidence'],**v,'status':v['final_status']})
cross_items.append({'key':'oslinlan-late-reunion','handoff_section':'resolved_do_not_reopen',**end('resolved','原任务前半已解；后383额外见奥斯林兰塔布雷特在神之境幸福相拥，不倒改此前牺牲过程。',ev(384,22757,22771))})
write('cross-half-audit.json',{'source_key':'l','source_id':BOOK['source_id'],'handoff_file':'l-a/handoff-to-second-half.json','read_coverage':[194,387],'items':cross_items,'no_abandoned_inference':True})

hist={}
for b in B:
 for c in b['characters']:hist.setdefault(c['key'],[]).append({'stage':[b['unit_start'],b['unit_end']],'record':c})
# 只有终章及明确终战事实会成为书末状态；其余保留最后实见点和未写明项。
chars=[]
for k,hh in hist.items():
 last=hh[-1]['record'];last_stage=hh[-1]['stage']; terminal=last_stage==[374,387]
 chars.append({'key':k,'name':last['name'],'last_explicit_state':last['summary'],'last_explicit_evidence':last['evidence'],'final_state':last['summary'] if terminal else '结尾未专门交代此实体；最后实见状态见last_explicit_state。','unknown_at_ending':[] if terminal else ['最终去向/生死/现实生活若无直接终点，不据缺席判死亡或弃线。'],'stage_history':hh})
write('characters-final.json',{'source_key':'l','coverage':[194,387],'scope':'后半全部阶段角色记录；同名旧key不强合，父王/父萧寒关系另见cross-half-audit。','characters':chars,'ending_limits':['萧翎神格为任务临时态，结尾已撤，不说现实成神。','四女现实相聚，无主角婚礼/法律婚姻、职业和子女叙述。','无炎双胞同居不等于三人结婚。','火舞未写成为第五伴侣。','爱丽丝、黑伍德、霍尔卡德未明示死亡或审判。']})
threads={}
for b in B:
 for t in b['threads']:threads.setdefault(t['key'],[]).append(t)
thread_terminal={
'horadric-riddle':end('resolved','330解谜334得魔盒。',ev(331,15543,15625),ev(335,15936,16048)),
'difeiliya':end('resolved','守到援军任务85%实结。',ev(217,8912,9001)),
'dragon-rivalry':end('resolved','正式团队赛胜，狂龙团圣殿解散；原合同清算未逐条写。',ev(381,22390,22410),ev(381,22473,22491)),
'xiao-yu-l':end('partial','萧御独立毁神格；末次PK胜负明说不讲。',ev(387,23116,23117),ev(387,23139,23145)),
'romance-l':end('resolved','四女现实相聚，个体同意边界另审，不把结局反推过程。',ev(388,23217,23260)),
'arland-identity':overrides['q-arland'],
'engineering-titan':overrides['q-engineering20'],
'vanity-ring':overrides['vanity-secret'],
'crazy-dragon':end('resolved','狂龙团解散，与天龙风龙同行。',ev(381,22467,22491)),
'father':end('resolved','现实父亲与母亲出现，安排四女与伙伴消息。',ev(388,23217,23229)),
'demon-ring':end('partial','魔神戒已真神器可升级；七勋异界钥匙传说未直接开启。',ev(372,21038,21044)),
'relationships':end('resolved','四女现实相聚，过程同意疑点仍保留。',ev(388,23217,23260)),
}
out=[]
for k,hh in threads.items():
 last=hh[-1]
 v=thread_terminal.get(k,end(last['status'] if last['status'] in ('resolved','partial','unknown') else 'unknown',last['state'],*last['evidence']))
 out.append({'key':k,'title':last['title'],'kind':last['kind'],'status':v['final_status'],'state':v['answer'],'evidence':v['evidence'],'history':hh})
write('threads.json',{'source_key':'l','items':out,'note':'不同阶段同题异key保留，终态可核question-map；未知不标abandoned。'})
write('ending-audit.json',{'source_key':'l','coverage':[194,387],'ending_unit':387,'ending_chapter_id':'ch-0388','actual_ending':[
 end('resolved','竞技五规格天狂阵营夺冠；单人22分主角第一、帝焰第二夜落第三天龙第四流觞六，含同盟积分协助。',ev(380,22141,22186),ev(381,22390,22410)),
 end('resolved','狂龙放队员带装，团队解散；圣殿之火发遣散费解散。狂龙天龙风龙仍同行，未写现实命运。',ev(381,22467,22491)),
 end('resolved','乌服诺斯沃顿是侵略主宰；万人神战由萧翎等杀躯体、萧御毁本命神格，系统确认完整成功。',ev(382,22514,22523),ev(387,23105,23118)),
 end('resolved','众神未永久死，重现为凡人；玩家引导神力消失，主角不再参反攻。',ev(387,23121,23125)),
 end('resolved','三日旅行海滩告别、出营养仓新星登陆；父安排四女重逢，花舞最后实际接机。',ev(387,23131,23152),ev(388,23156,23168),ev(388,23217,23260)),
 end('resolved','前半悲恋塔布雷特奥斯林兰神之境相拥；夜落月落现实结婚、无炎双胞工作同居，天狂林菲科技公司，其他成员现实就业创业恋爱。',ev(384,22757,22771),ev(388,23232,23238))],
'unwritten_or_deliberately_open':[
 end('unknown','末次萧翎对萧御PK胜负作者经主角明确不公布。',ev(387,23139,23145)),
 end('unknown','游戏靠岸后是否继续运营、原机械伙伴随后命运、卡尔洛斯戒灵最后去向均未交代。',ev(387,23150,23152),ev(388,23156,23157)),
 end('unknown','爱丽丝、黑伍德有死志或断后爆炸但无直接死亡确认；霍尔审判未写。',ev(327,15200,15249),ev(329,15350,15456),ev(194,7881,7909)),
 end('unknown','虚荣戒余谜、一级灵魂碎片、月亮晶石、阿卡德全套、早期罗格注视者无明确终态回收。',ev(313,14075,14083),ev(98,3536,3564),ev(151,5941,5943),ev(148,5834,5838)),
 end('partial','七功勋遗物作异界钥匙的传说未直接开启；魔神戒升级完成不等于整个钥匙承诺完成。',ev(277,12230,12271),ev(372,21038,21044)),
 end('unknown','给主角唯一神级药半小时五倍未见明确喝下；不能把夜落自己T半成品或其他终极药当同一瓶。',ev(340,16614,16722),ev(375,21688,21690)),
 end('partial','纳德主神被沃顿掌握只是天狂我想，安东尼克确为叛者但纳德复生/解封未直接演出。',ev(327,15200,15249),ev(382,22520,22522))],
'source_anomalies':[c for b in B for c in b['dimensions']['continuity']],
'interpretation_limits':['本审计按作者实际写出结果；不以研究认为应圆满的结局补齐未知。','四女现实重逢有证，不等于此前每个亲密行为自由同意；牧琳反抗和可爱橘子十七八岁遭骚扰威胁的笑料保留批判观察。','神力引导只是任务临时升级，结局未保留全队主神身份。','前半已解决任务不因后半不再提而重开；逐项见cross-half-audit。']})
print('saved',len(Q),'terminal questions;',len(cross_items),'cross-half items;',len(chars),'character keys;',len(out),'thread keys')
