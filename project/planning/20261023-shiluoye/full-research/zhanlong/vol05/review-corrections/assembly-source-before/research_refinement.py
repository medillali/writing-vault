"""初稿手写后的逐项章界/适用条件复核；只改本卷尚未冻结研究，不改原逐章笔记。"""
REPLACEMENTS={
 '北辰观28?本卷明27岁':'北辰观27岁',
 '三十?本次霜带五十':'本次霜带五十',
 '1127系统死':'1125系统死',
 '雷丁首1128':'雷丁首1126',
 '1128回交霜':'1126回交霜',
 '1040印总胜':'1039印总胜',
 '艾尔莎1040交东':'艾尔莎1039交东',
 '1040系统':'1039系统',
 '1040交东':'1039交东',
 '1040印胜':'1039印胜',
}
def textfix(x):
 if isinstance(x,dict):
  for k,v in x.items():x[k]=textfix(v)
 elif isinstance(x,list):
  for i,v in enumerate(x):x[i]=textfix(v)
 elif isinstance(x,str):
  for a,b in REPLACEMENTS.items():x=x.replace(a,b)
 return x
for x in [CARDS,dimensions,GRAPH,QUESTIONS,ANOMALIES,LIFE_STATES]:textfix(x)
def refs(obj,nums):obj['evidence']=ev(nums)
crefs={
 'xiaoyao':[978,999,1005,1006,1022,1048,1074,1089,1138,1160,1165,1178],
 'waner':[1006,1047,1082,1103,1121,1142,1156,1166,1177,1179],
 'rou':[1086,1087,1091,1109,1110,1134,1141,1156,1157,1179],
 'li':[984,985,1016,1079,1110,1149,1154,1156,1171],
 'wang':[1014,1015,1016,1033,1078,1079,1149,1154,1171],
 'rannpc':[1108,1109,1127,1138],
 'song':[981,1095,1121,1141,1161,1171],
 'xiaowu':[1090,1097,1120,1150,1152,1171],
 'qian':[1078,1079,1080,1110,1151,1172],
 'paper':[1006,1111,1126,1179],
 'milk':[1006,1079,1080,1081,1141,1148,1149],
 'yelai':[1126,1153,1155],
 'fre':[1134,1135,1136,1137,1155],
 'lerding':[1124,1125,1126],
}
for k,ns in crefs.items():refs(CHARACTERS[k],ns)
CHARACTERS['lerding']['content']['stage_change']='1125系统死，雷首1126实际交霜完成任务；不再当卷末活敌。'
CHARACTERS['rannpc']['content']['stage_change']='百酒交易升王戒后，再三魂精晶与1000魅500万金换霸王全五星已成；两次交易分开。'
srefs={
 'mine':([970,971,972,973,974],974),
 'rescue':([982,983,984,985,986,993,994,995],995),
 'arena':([1002,1003,1004,1005,1006],1006),
 'firelion':([1019,1020,1038,1039,1040,1056],1040),
 'lake':([1031,1032,1033,1034,1035],1034),
 'huntaward':([1037,1038,1039,1041,1060],1039),
 'lastfan':([1078,1079,1080,1081],1080),
 'capital':([1083,1084,1085,1088,1089],1089),
 'warreward':([1089,1090,1091,1094],1094),
 'ring':([1108,1109],1109),
 'copy':([1109,1110,1126,1134,1138],1134),
 'regiment':([1111,1112,1113,1114],1111),
 'stealth':([1119,1120,1121],1121),
 'thunder':([1124,1125,1126],1126),
 'work':([1129,1130,1139,1140,1141],1141),
 'freeze':([1134,1135,1136,1137],1137),
}
for k,(ns,n) in srefs.items():refs(SCENES[k],ns);SCENES[k]['content']['narrative_order']=n
SCENES['rescue']['content']['summary']='救龙硎千兵/敌BOSS周海被杀后SSS闭；后来抗三君王仍有甲士与未名龙骑真死。'
SCENES['huntaward']['content']['summary']='1039系统印度以22006分差获胜并得临海；主个人MVP，四星匕交林/艾尔莎交东且1060实冰。'
SCENES['huntaward']['content']['consequence']='国家印胜/主个人MVP，林东各实得物，主未赢阵营城权。'
SCENES['mine']['content']['applicability']='当军事行动可成功、收益分配却受王朝军制和第三方命令限制时。'
conditions={
 'molten':'新坐骑产地将被毁、封印晶与等级有门槛，而主队又要及时回防留空的驻军。',
 'north':'军队被上级命令迁走且运输/掩护不足，救援者能挡部分火力但不能回到炮响之前。',
 'rescue':'任务同时要求具名受困者活着和敌首交回，战场奖励不能替代救人回执。',
 'coup':'政治冲突中有多个具名对象，威逼者的目标和各自生死/军权可分开核实。',
 'arena':'角色平时依装备/成长领先，赛事却统一等级装备并允许职业/加点选择。',
 'gonggong':'大团有采购耐性装的资金、职业互补和分装规则，但群控/治疗并发仍限制无伤。',
 'seven':'新技能有明确学习门槛与练习对象，强后用会反过来使主弱化、依赖队友。',
 'prison':'角色既要保大多数囚命又不能公然违命，但替死对象和被放者行为都会产生责任。',
 'firelion':'敌可用合法诏令改变阵营颜色，部将又可能因欲望违令并让别人承担军损。',
 'lake':'水军受炮与地貌牵制，可改变地形但施术后有不能再自保的冷却弱期。',
 'huntaward':'同一活动分别核阵营总分、个人积分和奖物去向，玩家有可能一败一胜。',
 'office':'新职有形式授予而强部将尚未服威，双方能先约一个有限、可验的比试目标。',
 'emperor':'多服争一个最终城权，主队可重创最大敌却被第三方取得最后系统条件。',
 'release':'敌将有回到守军的机会，主希望以生还传恐惧而非只增加击杀，但盟友情报不全。',
 'fan':'守城不是一击失陷，设施、运输、具名伤亡会逐轮逼近换战略的临界点。',
 'borrow':'解围所需外力属于价值冲突的敌方，交易能成但主不能完全控制其军队行为。',
 'moon':'夺另一城能牵动部分敌军但联盟各方目标不同，还要面对盟军对平民越界。',
 'forced':'新城缺人口而被救者有自己去处，保护者必须在资源需求与拒绝权间作选择。',
 'queen':'迁来者已有女王和组织，可以在获得定居地与对帝国的臣属之间协商。',
 'lastfan':'高端敌需极短控制窗口，伙伴能创造窗口但会真死/掉级，不能无限白给。',
 'capital':'救另一城与眼前兄弟安全冲突，条件随援军到达而变化，主需真正改令付成本。',
 'return':'当事人跨会/跨服且有旧伤，道歉、临时作战权与正式职位不会同时自动生效。',
 'warreward':'奖励领域不一致，经验、设施、兵数增益和具名人物生死必须分条验收。',
 'boost':'威胁跨地域同时发生，现场主胜并不能覆盖远处警员和平民伤亡。',
 'lan':'潜入队伍小且目标需活带回，视野、治疗、伪装与路径信息不可被主单攻替代。',
 'ring':'商谈有可替代的特殊对价，朋友拥有取得稀缺物的技能，但仍要亲交后升级。',
 'copy':'系统允许把一个效果转到套装但会使原物失效，且转赠后可能缺资格或实收。',
 'regiment':'跨会协作有固定人数/职业配比和付费申请，熟人申请不等全部入选。',
 'corpse':'副本阻止直飞末层且Boss有多命，长战需要恢复资源与分次真正终结。',
 'stealth':'对手高机动潜杀导致分队搜寻反受害，队伍有能留下短暂标记的非主角技能。',
 'thunder':'主想要的机制尚在Boss掉落物里，当前战只能付普通死亡成本把物打出来。',
 'souls':'升级材料分散在战利品、交易对象和活人融合魂中，每件需不同取得方式。',
 'work':'角色有家庭启动资源与专业设计师，但经营要经过执照、采购、合同和首批验货。',
 'freeze':'个人成长材料位于条约伙伴的活将身上，夺取行为会触发明确外交反问和底线。',
 'clue':'嫌疑公司有公开合法身份，现场样本只能证明局部异常，侦查需新渠道而非即刻定罪。',
 'cannon':'新武器只有少量材料与庞大运输负担，试炮、弹源与量产需求必须分开满足。',
 'coast':'不同部队补充和复活条件不一，若继续守点会失去更难重建的炮与NPC军。',
 'revive':'角色已有付一级的原地重生机制，且先逼掉敌无敌、仍留反攻所需怒与技能。',
 'lamp':'隐身敌到来前有可识迹象，撤退目的地具当地人掌握的持续显形设施。',
 'bomb':'攻击面板极低却以死亡/近群触爆，另有护送单位与城墙破坏目标。',
 'bones':'内墙有与友军混战的精英、外面有密集人海，同一炮只能安全打其中一方。',
 'revenge':'公共活动已经结算，私人报酬另有明确对象和价格，可由讨价再下单回扣。',
 'assault':'主有很强防御但多方向力量分配不足，既想保命又需要活口才能继续调查。',
 'heart':'奖励道具具不止一种用途，而另一角色有长期未完成的具体救亲愿望。',
 'blood':'订契者神智和信息不对等，母/导师认可与被绑定者本人知情同意可以区分。',
 'training':'已有战斗失败揭示技能短板，师者能控制火力并提供量化与动作的双反馈。',
 'fly':'契约伙伴有强体质也有自己的玩耍意愿，系统解锁要求实际共同操作而非只收名。',
 'diplomacy':'一方缺补给通道，另一方用贸易资源换军事从属，拒绝会迫使寻找新资源来源。',
 'sea':'远征需王准/运载/侦图，己方射程占优而劝降也可能先损人员。',
 'land':'岛内地形可埋伏且远征有粮期，攻后又须保耕地、任官/留军与供给制度。',
 'dragons':'表面夺蛋有更大迁族目标，队伍预备捕索却仍要应对火焚/龙息与主体抵抗。',
 'kill':'两名首领与群体并战，主伤害远低NPC但有控制/末刀机会，贡献与归属须分。',
 'auction':'多人共有高值物且内部赠谁都可能偏袒，公开市场仍有手续费和未落槌风险。',
}
assert set(conditions)|{'mine'}==set(SCENES)
for k,v in conditions.items():SCENES[k]['content']['applicability']=v
# 逐项复核早段章号：比赛终局1006，会猎阵营/个人结算1039，雷丁死1125/铠与首交1126。
obsrefs={
 ('worldbuilding',2):[1023,1067,1083,1089,1090,1091,1094,1126],
 ('characters',2):[1006,1047,1082,1098,1104,1142,1156,1177,1179],
 ('plot',1):[1005,1006,1039,1071,1077,1089,1154,1157],
 ('plot',4):[1109,1110,1126,1127,1129,1133,1137,1138,1151],
 ('pacing',1):[1039,1060,1095,1114,1126,1157,1173],
 ('continuity',1):[1006,1086,1108,1109,1110,1131,1134,1149],
 ('continuity',2):[981,1110,1126,1178,1179],
 ('continuity',3):[1053,1067,1105,1107,1125,1126,1160,1177,1178],
}
dimensions['continuity'][1]['textual_fact']='宋寒生日匕寄存/纸钥匙收未提车、雷丁首交任务完成、旧膝月代送李未独收、龙牙1179直接实装。'
for (d,i),ns in obsrefs.items():
 o=dimensions[d][i-1];o['evidence']=ev(ns);o['interpretation_evidence']=ev(ns,'inference')
# 修订先前误称“韩生日”为宋寒生日；不改原notes。
for x in [CARDS,dimensions,GRAPH,QUESTIONS]:
 def correct_birthday(y):
  if isinstance(y,dict):
   for k,v in y.items():y[k]=correct_birthday(v)
  elif isinstance(y,list):
   for i,v in enumerate(y):y[i]=correct_birthday(v)
  elif isinstance(y,str):y=y.replace('韩生日','宋寒生日')
  return y
 correct_birthday(x)
# 同步场景节点，确保叙述顺序落在实交/实杀/实装，不以晚章回述代主落点。
for k,c in SCENES.items():
 n=NL['v05-s-'+k];n.update(title=c['title'],summary=c['content']['summary'],state_change=c['content']['state_change'],narrative_order=c['content']['narrative_order'],evidence=c['evidence'])
edge_refs={'coworklevel':[1016,1017],'lakeaward':[1034,1039],'weaponuse':[1039,1060,1089],'lootgift':[1090,1110],'ringuse':[1109,1150,1151,1156],'recruitlayers':[1111,1112,1115],'finallayer':[1121,1122,1124,1125,1126],'setdeath':[1126,1151,1152],'needmaterials':[1126,1127,1138],'supplycannon':[1133,1134,1145]}
for e in EDGES:
 k=e['id'].replace('v05-e-','')
 if k in edge_refs:e['evidence']=ev(edge_refs[k],'inference')
for t in THREADS:
 k=t['id'].replace('v05-t-','')
 if k=='arena':t['evidence']=ev([1005,1006]);t['resolution_evidence']=ev([1006])
 if k=='hunt':t['evidence']=ev([1017,1034,1039,1060]);t['resolution_evidence']=ev([1039,1060])
 if k=='hundred':t['evidence']=ev([1111,1116,1121,1125,1126]);t['resolution_evidence']=ev([1125,1126])
 if k=='set':t['evidence']=ev([1110,1126,1137,1138,1151,1152]);t['resolution_evidence']=ev([1138,1151,1152])
for n in NODES:
 for item in n.get('knowledge',[]):
  if '雷丁战时' in item['content']:item['evidence']=ev([1125,1126])
  if '旧铠给薛' in item['content']:item['evidence']=ev([1126,1134,1138])
# 保留原问题索引，精确高级药链/赏物位置。
for q in QUESTIONS:
 if q['id']=='v05-q-delivery':q['evidence']=ev([981,1110])
 if q['id']=='v05-q-tangxin':q['evidence']=ev([995,996])
for c in CARDS:
 assert c['content']['summary']
assert len({c['content']['applicability'] for c in SCENES.values()})==len(SCENES)
