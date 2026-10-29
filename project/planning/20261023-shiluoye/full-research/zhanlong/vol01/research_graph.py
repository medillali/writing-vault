for _key in ('duelwenjian','firsttoken'):
 if origin('character','wenjian') not in SCENES[_key]['content']['characters_origin_keys']:
  SCENES[_key]['content']['characters_origin_keys'].append(origin('character','wenjian'))
ARCS=[
 ('start','起步：能力与规则重新磨合',['employment','bear','falseaid','biketail','letter','classchange','combo','duel']),
 ('mutual','合同、首令与旧友重召',['longwind','firsttoken','oldfriends','gaodi','tombwar']),
 ('team','五人、后勤与现实权力',['implant','fushui','darknotes','teachbusiness','admitmocha','butterflyqueen','cliffpet','police']),
 ('relic','荒陵十人合作与古魂复生',['prisonkey','oldman','yaoxing','murong','kingreborn','duelwenjian']),
 ('guild','组织失败、重建与有限和解',['compensation','forestwar','phantom','yangwei','rebuild','foundguild','enrollenemy','truce','stone','ally']),
 ('legacy','龙庙传承与资源矿战',['exile','templeentry','thunder','fire','cold','inheritance','wangcontrast','counterhunt','qinsword','minewar'])]
NODES=[{'id':'v01-root','title':'卷一 从零开始｜个人与组织的不同结算','kind':'volume','parent_id':None,'claim_kind':'synthesis','summary':'raw0002—0251共同全文覆盖；前150片agent3、后100片primary。卷尾矿战未结，研究待审。'}]
assert set(k for _,_,ks in ARCS for k in ks)==set(SCENES)
for ai,(arc,title,keys) in enumerate(ARCS,1):
 NODES.append({'id':'a-'+arc,'title':title,'kind':'arc','parent_id':'v01-root','claim_kind':'synthesis','narrative_order':ai})
 for key in keys:
  c=SCENES[key];NODES.append({'id':'s-'+key,'title':c['title'],'kind':'scene','parent_id':'a-'+arc,'narrative_order':min(int(e['chapter_id'].split('-')[1]) for e in c['evidence']),'claim_kind':'inference','summary':c['content']['summary'],'state_change':c['content']['state_change'],'asset_origin_key':c['origin_key'],'character_origin_keys':c['content']['characters_origin_keys'],'evidence':c['evidence'],'knowledge':[]})
NL={n['id']:n for n in NODES}
def know(scene,observer,state,content,nums,belief=None,kind='fact'):
 row={'observer':'reader' if observer=='reader' else origin('character',observer),'state':state,'content':content,'claim_kind':kind,'evidence':ev(nums,kind)}
 if belief:row['belief']=belief
 NL['s-'+scene]['knowledge'].append(row)
know('duel','reader','knows','主一死一胜，第二借三鼠仇恨而非已正面全面超越。',[62,63])
know('duel','waner','knows','看完两段录像后为主画十二战术图；此前未亲见那两战。',[65])
know('longwind','fushui','misbelieves','旧阶段更倾向剑的说法，至135看原约才改判。',[133,135],belief='主为一把紫剑无理杀她崇拜的盟主；尚未看全原无品阶优先条款。',kind='inference')
know('fushui','fushui','knows','135看认证录像后确认剑黑主剑，承认当时起死剑伤主并道歉。',[135])
know('gaodi','jianfeng','suspects','124从匿名SSS榜与林拆招推读心属她，林公开没有承认。',[124],kind='inference')
know('gaodi','xiaoyao','knows','124林私信确认游戏SSS读心；102已现实亲承读心。',[102,124])
know('implant','reader','knows','性交场面为植入后的主幻境，现实回餐桌，主女事前不知。',[132])
know('implant','lintian','unknown','知道已植入/自信忠守功效，但不知具体幻境内容；永久控制不能据此证成。',[132],kind='inference')
know('admitmocha','reader','knows','薛柔本人自报23/草莓抹茶27剑，理论好与0杀7死并存。',[147,148])
know('police','xiaoyao','suspects','155按14点能量猜至少御气，156尸体退毛后仍未知改造具体来源。',[155,156,168],kind='inference')
know('murong','reader','knows','复活链成功但省蓝叫停余五，龙牙石卡位实际失败。',[175,176])
know('kingreborn','reader','knows','冉闵NPC已复身而非仅许诺，罗林发忠誓但未来忠诚尚未检验。',[178,179])
know('yangwei','reader','knows','个人17杀MVP与一门忠烈系统解散同时成立。',[196])
know('truce','xiaoyao','suspects','206不信刘终身誓，仅同意当前止守离谷；243实止手提供有限后证。',[206,243],kind='inference')
know('exile','reader','unknown','卡尔控罗林故害子，流霜说军令牺牲；本卷无独立裁定。',[211],kind='inference')
know('templeentry','reader','knows','SSS明确上限9/固定九人，后十人文字不新添未名人物。',[212,214,215])
know('cold','reader','knows','假老人是寒岩，真正云辰灵念在地下；另八死时主仍活。',[228,229,230])
know('inheritance','xiaoyao','knows','五卷已学，青龙/紫雷等级不足，前三也要神兵符；242才兵解有材。',[233,241,242])
know('wangcontrast','xiaoyao','knows','亲见汪私场暴力/征服林意图，且实际阻止。',[222,223])
know('wangcontrast','dongcheng','unknown','当时只获同学/医疗九伤消息，未得主隐瞒的私场见闻。',[224],kind='inference')
know('qinsword','xiaoyao','knows','魂100%为半成品，须双十级工艺与100麒麟铁，当前兄9采妹9铸分开。',[244,245,247])

EDGES=[]
def edge(key,a,b,kind,label,nums):
 EDGES.append({'id':'e-'+key,'from':'s-'+a,'to':'s-'+b,'kind':kind,'label':label,'claim_kind':'inference','evidence':ev(nums,'inference')})
edge('profession','classchange','combo','cause','任务与新技能提供五动作正式组合的条件，不是现实招式直接自带系统连招。',[50,55,56,59])
edge('enemy-teacher','duel','darknotes','payoff','主从剑锋寒拆一骑学来的后翻，在142被王偷招时用于解自己末两击。',[62,63,142])
edge('contract-video','longwind','fushui','reveal','无品阶优先原录像135使囡修正对主的误判。',[83,87,89,135])
edge('token-ally','firsttoken','tombwar','setup','首令/3000G助忠烈成立，使后来以真实行会发布公主坟并邀主。',[98,99,125,126])
edge('resource-flow','tombwar','oldfriends','echo','主128收还佣4万、130其中3万运营，使重召不止一次买盔。',[100,103,128,130])
edge('five-person','fushui','darknotes','cause','新增稳定奶补齐笔记最高5共享，五人实际执行S。',[135,136,142])
edge('ring-service','darknotes','teachbusiness','cause','任务五枚洛戒与可带人条款是收费服务的实际通行工具。',[143,144,145])
edge('labor-newcomer','teachbusiness','admitmocha','setup','带学收益后讨论工作室基本生活与招工，不把钱自动变已签合同。',[146,147])
edge('knowledge-axis','admitmocha','butterflyqueen','payoff','面试战术判断在测CD/报岗中实际贡献，拙操仍留。',[147,148,150])
edge('eggs','butterflyqueen','cliffpet','payoff','151收七虫卵原食材、154烤时意外孵幻蝶交抹绑定。',[150,151,154])
edge('key-entry','prisonkey','oldman','setup','造钥/入墓后才能发现被困百炼，进入条件不等预知其在内。',[159,162,163])
edge('repair','oldman','murong','setup','被救者提供多次实际修装，十人长副本可续；不称其直接杀终王。',[163,165,170,174,175])
edge('illusion-control','cliffpet','yaoxing','payoff','154抹得幻蝶，166该宠缠绕实际断穹熊后续击。',[154,163,166])
edge('head-body','murong','kingreborn','cause','终王死/177取头只是新阶段，带至龙城才能完成身魂复生。',[176,177,178])
edge('reserve-militia','kingreborn','exile','setup','冉闵实留城，209卡尔报其斩矮人将；该战为转述，不抹流霜受伤。',[178,179,209,210])
edge('good-faith','compensation','rebuild','payoff','一抹先获紫胸/求荐，197已成忠烈核心表追随，后来随营入斩龙。',[185,197,200,205])
edge('certificate','forestwar','phantom','cause','李牧因协作将实得转职证明交主，189抹完成任务消耗。',[188,189])
edge('new-tank','phantom','templeentry','payoff','已转幻影骑士和实学技，让九人配置有双T/分身接怪。',[189,190,212,216])
edge('loss-rebuild','yangwei','rebuild','cause','忠烈被系统解散迫使旧核心寻找新承载，198给保营自治方案。',[196,197,198])
edge('stealth-token','yangwei','rebuild','payoff','失败MVP书197实学草丛，199用来伏交易后沐天取令。',[196,197,199])
edge('promise-register','rebuild','foundguild','payoff','饭局两营/加盟口约在200令币系统成立后才分岗位接人。',[198,199,200,201])
edge('coalition-capacity','foundguild','enrollenemy','setup','真实行会两营与管理给纳入旧敌提供权限，需主处理成员报复。',[200,201,203,205])
edge('battle-to-talk','enrollenemy','truce','cause','多轮守尸形成对方求停压力；不是千阳一入队自动和平。',[204,205,206])
edge('limited-enactment','truce','qinsword','payoff','243刘/小猪实止部下攻击，允许主采青木，验证有限止战。',[206,242,243])
edge('master-change','exile','templeentry','cause','逐师后接受龙墓试炼，新任务和九人出发依该资格。',[211,212,214,215])
edge('apprentice','exile','inheritance','payoff','流霜许活出收徒在221中途三转已先兑现，234SSS结不同层。',[211,221,233,234])
edge('massdeath','fire','cold','echo','两场均把控制全MISS后的施救/承伤边界写清，寒岩仍升级到另八死。',[226,229,230])
edge('star-break','stone','cold','payoff','207七星可破建筑，230按云辰天权玉衡星位实际碎两柱放机关虎。',[207,230,231])
edge('tiger','cold','inheritance','payoff','机关虎被吞后蛋出现并绑定孵化；具体血认主转蛋是与子解释非系统因果全证。',[231,232,233])
edge('pet-power','inheritance','counterhunt','payoff','新神虎实际练级后以踏火/吼/嗜血协同主反猎，仍被剑浮生杀。',[233,235,236,238,239,241])
edge('rune-supply','inheritance','qinsword','setup','233五卷消耗符、241缺符，242兵解低银得15，另开收购循环。',[233,241,242])
edge('soul-barrier','qinsword','minewar','cause','醒魂半品还需高工艺/麒麟铁，南宫采矿升级被赤金封锁，推动五会矿争。',[244,245,246,247])
edge('allied-aid','ally','minewar','payoff','209系统盟后247血色实际到矿援战。',[209,247])

THREADS=[]
def thread(key,title,kind,status,members,edges,stage,nums,resolution=None):
 row={'id':'t-'+key,'title':title,'kind':kind,'status':status,'node_ids':['s-'+s for s in members],'edge_ids':['e-'+s for s in edges],'stage_note':stage,'evidence':ev(nums)}
 if resolution:row.update(resolution_note=resolution,resolution_evidence=ev(nums))
 THREADS.append(row)
thread('growth','规则学习与职业/技能成长','main','partial',
 ['employment','classchange','combo','duel','darknotes','exile','templeentry','inheritance','qinsword'],['profession','enemy-teacher','master-change','apprentice','rune-supply'],
 '转剑/二转/三转、反弹与前三墨家资格已得；墨家后两未到级，秦王仍半品。',[50,82,143,211,221,233,242,245])
thread('guild','斩龙从重召到正式行会','main','partial',
 ['oldfriends','firsttoken','tombwar','teachbusiness','admitmocha','yangwei','rebuild','foundguild','enrollenemy','minewar'],['token-ally','resource-flow','labor-newcomer','loss-rebuild','stealth-token','promise-register','coalition-capacity'],
 '实体重建与200正式建成均已成，201满300/245报972；前十和卷尾矿权尚未结。',[103,146,147,196,198,200,201,245,251])
thread('contract','天策违约与囡信念更新','subplot','resolved',
 ['longwind','fushui'],['contract-video'],
 '装备归剑未追回，但承诺真相在囡个人认知中得到明确回收；长期敌对另开。',[83,87,89,135],
 '135囡看认证录像后承剑黑剑/道歉并正式离开，解决她对原事件的错误认知。')
thread('waner','暗护、亲近与自主权','main','partial',
 ['employment','duel','gaodi','implant','duelwenjian','wangcontrast','qinsword'],[],
 '主现实护卫持续/有亲近行为，仍未正式恋人；记忆保留、父商约/实习/汪威胁未解决；双女仍英雄冢。',[7,65,124,132,180,182,213,223,234,244])
thread('mocha','理论强与动作弱的培养线','subplot','partial',
 ['admitmocha','butterflyqueen','cliffpet','yaoxing','phantom','templeentry','minewar'],['knowledge-axis','eggs','illusion-control','new-tank'],
 '已招/30/紫宠/幻骑/55枪实用/统战授权，仍249打歪；合同细项与58圣魂盾实穿未明。',[147,148,150,154,166,189,216,221,247,249])
thread('finance','运营资金、分账与供给','subplot','partial',
 ['oldfriends','tombwar','teachbusiness','admitmocha','kingreborn','inheritance','qinsword'],['resource-flow'],
 '还款4万/运营3万、教学5万G与囡1000、枪十份/宠九份均各有后证；另工资/500/佣金/售扇等未全结。',[102,128,130,146,179,228,242])
thread('hunger-npc','百炼受救与反哺维修','subplot','resolved',
 ['prisonkey','oldman','murong','kingreborn'],['key-entry','repair'],
 '解毒局部A/图内实修/177离墓分别回收，未把早奖误作早已出墓。',[162,163,165,170,177],
 '177十人步行出墓时百炼实际救出，早带出承诺已兑现。')
thread('reincarnation','冉闵魂救与有条件留守','subplot','partial',
 ['prisonkey','murong','kingreborn','exile'],['head-body','reserve-militia'],
 '任务救魂与NPC复生已成，罗林忠誓/冉闵条件需后续行动检验，不记终身已定。',[158,176,177,178,179,209])
thread('frost-karl','卡尔失子、流霜与换师','hidden','partial',
 ['letter','classchange','exile','templeentry','inheritance'],['master-change','apprentice'],
 '逐师与新师承已系统确证，卡特死因双方说法仍争，卡尔未释怀；地龙前流霜七炎预援保留。',[82,209,210,211,221,234])
thread('loyal','忠烈组织败与核心再承载','subplot','resolved',
 ['firsttoken','tombwar','compensation','forestwar','yangwei','rebuild','foundguild'],['token-ally','good-faith','loss-rebuild','promise-register'],
 '旧会确败解，不重建同名；核心通过忠烈营纳入新会，李牧长老/自治权限。',[99,196,197,198,200,201],
 '200—201新会真实成立并扩容量接人，解决核心去向；不改写196旧会败。')
thread('territory','练级地、有限停战与矿权','main','open',
 ['gaodi','enrollenemy','truce','counterhunt','qinsword','minewar'],['battle-to-talk','limited-enactment','soul-barrier'],
 '霜枫当场退让/雄霸一场止战已证；赤金五会战至251简首闪未死、开放条件未结。',[124,205,206,241,243,247,251])
thread('stela','血契背碑到建筑破坏实用','subplot','resolved',
 ['stone','cold'],['star-break'],
 '207融合/系统技能得，230按星位破柱实际援战；碎月/碎岳源异另记。',[81,207,230,231],
 '长携物成本已结成SS七星，并有破柱实际用途。')
thread('mohist','云辰、机关虎与受限传承','subplot','partial',
 ['templeentry','cold','inheritance','counterhunt','qinsword'],['tiger','pet-power','rune-supply'],
 '真云辰已传五卷后消散、虎已孵归主并战；符刚15/高阶技未到级，不能称全墨家可用。',[214,230,231,232,233,241,242])
thread('mutant','黑兽、血联与改造体线','hidden','open',
 ['police','wangcontrast'],[],
 '黑兽斩后退人形/针孔与DNA异常研究所转述已见；汪保镖异常未证与其同种或同幕后。',[155,156,168,222,223,224])
thread('publicface','汪公私形象与林信息差','hidden','partial',
 ['employment','implant','wangcontrast','templeentry'],[],
 '主亲见私场威胁并实干预，却未告林；实习/午饭及公司真实影响未回收，不补全暗杀阴谋。',[213,214,222,223,224,234])
thread('external','不转会也可合作的外部关系','subplot','partial',
 ['ally','templeentry','thunder','inheritance','qinsword','minewar'],['allied-aid'],
 '血色系统盟/实援、与子留青瓷合作、南宫拒转而许铸；新合作结果各自未全成。',[209,212,217,228,247,251])

GRAPH={'title':'斩龙卷一｜成长、组织与不完全胜利','owner':{'kind':'source','id':SID},'nodes':NODES,'edges':EDGES,'threads':THREADS,'coverage':[{'source_id':SID,'revision':REV,'chapter_ids':IDS,'complete':False}],'notes':'分卷共同全文覆盖不是全书完成；图边均为显式工具/条件/选择关联，echo只作结构比较。知识存节点，人物用origin待正式导入映射。','review_status':'draft'}
ANOMALIES=[]
def anomaly(key,description,boundary,nums):ANOMALIES.append({'id':'v01-a-'+key,'description':description,'handling':boundary,'claim_kind':'inference','status':'unknown','audit_domain':'source-anomaly','evidence':ev(nums)})
anomaly('ch28-split','原索引ch0030为印28章开头，ch0031误识别正文片，实际同章合一。','两个segments全部亲读，正文仅计一个，卷题另不计正文。',[30,31])
anomaly('charisma-early','早期魅奖励合计与21界面5/22后7等不全齐。','保界面及奖各次记录，不重算补遗漏行为。',[18,21,22])
anomaly('skill-name','54食人妖称寒霜，与常见流霜近名但未足另立同一能力者。','原名保存，人物卡仍流霜证实身份不静默改源。',[54,82])
anomaly('skill-wind','巽风早.2秒/108叙2秒前摇，而124又.2。','按各场文本，不自行称升级速度变化。',[55,56,108,124])
anomaly('friend-visibility','104规则等级差10好友例外，但已加友三友看主仍问号。','保规则与场景差，不编未加友。',[103,104])
anomaly('retire-years','旧师跟练与退役年数有五年/107自称四年等口径。','不硬凑公历或给不存在履历。',[103,107,132,169])
anomaly('gun-tier','138黑暗火焰之吻黄金面板，139叙投出称白银。','按原面板黄金与实穿事实，保白银异写。',[138,139])
anomaly('laok-gun','142冉闵退场文字拖火焰之吻，与其斧/狐枪归属冲突。','不据此移枪给冉，物主用139实穿狐。',[139,142])
anomaly('seal-payment','143两魂1000G/每人200与五人含自己和其前持金527等缺明细。','承认买石/实强成功失败，不造新转金镜头或精算资金清账。',[136,143])
anomaly('reflect-level','144攻击反弹面板需40而宣传10级可学。','两层保，实际已学者本段都40以上不证10可学。',[143,144])
anomaly('ring-life','143得洛戒/144说明24h，146同晚9即称寿尽，同时5000额满。','额满可证停学，时长解释未知，不替作者说只次数限制。',[143,144,145,146])
anomaly('salary-mo','146招稿3000而147抹说4000起，应与血色告示4000分别。','保工资未签付具体细则，不能直接认主已改薪4千。',[146,147])
anomaly('mo-level','149抹30，150王连升2应32，151称死掉回32/主疑多杀。','154明确32升36；不补151前隐藏35。',[149,150,151,154])
anomaly('combo-cd','早一骑共30秒CD，150抹按60与藤约50讨论。','各章口径存，未见明确改版解释，不据数学称每轮都可破所有藤。',[59,63,150])
anomaly('hero-promise','99三月不离英雄冢，157至少一月，180再三月，232至少一月/再20天。','承诺尚未履满/两女未转可证，期限差不强裁统一。',[99,157,180,232])
anomaly('twenty-party','183职业总20/另1发烧没来，宋一度说两个20人团。','按实际20，不扩40。',[182,183,184])
anomaly('war-ending','196中途仅剩飞龙说法与系统终5活有跳省。','终系统5:0/主死亡忠烈败优先，不补杀光全敌。',[195,196])
anomaly('seven-count','190斩龙临入一门一度6后明7。','140雷入、147抹入的独立成员链与后队七合核，不删一人。',[140,147,190])
anomaly('star-name','207系统七星碎月斩而技能列表/后文碎岳斩。','保同次破壳两称，不造两次独立学习。',[207,230])
anomaly('star-area','208口述七星30×3又约72平米。','长度/面积为角色估，算术差留不补新宽。',[207,208])
anomaly('temple-nine','SSS明确9人/名单9，之后多处写十人。','原名单全保，不造未名第10人。',[212,214,215,223,234])
anomaly('tiger-heal','233嗜血击说明100%，2394238回2119、2412578回1289为50%。','保技能描述与两次实测双层，不把所有伤害当100%吸血。',[233,239,241])
anomaly('reward-gold','234系统2万G，后口语1万G。','系统记奖2万，同时保口语异文，免20%抽成是实际决策。',[234])
anomaly('elite-kill','241原28剩剑/浮生即26死，242朋友/林夸绝杀27。','原战实际优先、后言为转述夸词。',[238,239,240,241,242])
anomaly('iron-grade','245十级麒麟铁、246口述100级。','工艺材料分级异写不擅改已知配方。',[245,246])
anomaly('reinforcements','248李报6000余/北极自称7000及七团口径差。','按报告主体存，不强精确唯一参战总数。',[247,248,250,251])

END_QUESTIONS=[]
def question(key,q,boundary,nums):END_QUESTIONS.append({'id':'v01-q-'+key,'question':q,'status':'open','claim_kind':'inference','stage_boundary':boundary,'evidence':ev(nums)})
question('mine','五会矿战是否胜、矿区是否开放、简是否被追杀？','251只若叶死/简首闪，未谈条约。',[247,248,249,250,251])
question('qin','秦王正式重铸/两10级工艺及100麒麟铁何时完成？','魂已100%但半品不可穿，南宫决9采/灵9铸尚未到10。',[244,245,246,247])
question('herojoin','双女英雄冢留期最终按何口径/何时实入斩龙？','三月/一月/20天异写，251未入，不把519剑援当转会。',[99,180,190,232,244])
question('mutant','人形黑兽、针孔、DNA异常及血联/幕后关联后证？','尸体/警方转述已有，汪保异常不能自动认同一改造链。',[155,156,168,222,223,224])
question('wang','汪次日午餐/林实习/校园与游戏关系后果？','校报名已见；游戏入仅小猪言/ID未知，不把自述CEO等同所有行为已证。',[213,214,222,223,224,242])
question('karl','卡特死亡两种说法、卡尔怨恨会如何变化？','逐师真实/221新师真实，但234仍敌意未释。',[82,209,210,211,221,234])
question('rolin','罗林忠誓及冉闵有条件留守经何事检验？','NPC实复生与誓言分开，无本卷终身忠诚结论。',[178,179,209])
question('compensations','阿雷让装/倾浅同位刺客戒等补偿是否具体兑现？','173主许补阿雷；220主许同位补倾浅，227靴/匕新分不自动等同戒偿。',[167,173,220,227])
question('money','仍未见独立收付的早佣、500饭借、工资/合同与代售细账如何后续？','128原3000G借与当次佣已闭，不能拿其还款泛闭83旧佣；102500未独证还、120次月5万未付，抹年约/薪差未结，空虚扇235交狐无分款。',[79,83,102,120,128,147,217,235,242])
question('rune','墨家符供给与前三项后续实际施用、高级两技解锁？','五卷已学，242兵解15符/狐受5000收银；241之前缺符不能用，80/100门槛未达。',[233,241,242])
question('shield','抹茶58圣魂盾资格/明确装备与冰壶等分装？','221只交盾待58；后未有明确实穿镜，不能拿圣盾技能代盾装备。',[150,151,216,221,229,232])
question('reforms','小猪副盟/积分制度和三高手是否真正实施招到？','243仅允诺与当场止攻，不能一个守约回执打包闭改革。',[243])
question('imprint','主保留烙印记忆的后续效力/是否真正清除？','132实植，182主自说可清却不舍/未行动；长期强制效果仍未独证。',[132,182])
question('friend-invitations','问剑洛阳邀请、湿地出游等明确生活邀约有何后证？','181邀请/数次湿地延期本卷未全见成，不把随口调笑都造契约。',[83,125,180,181])
question('territory-growth','斩龙前十/更高会级、外部盟友合作何时兑现？','200建/201二级/245三级972已分别成；前十和半月四级仍目标。',[200,201,209,245,247])
