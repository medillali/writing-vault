"""包装阅读者逐章阅读全文后选定的研究解释；不生成阅读声明，不改源文。"""
import json
from pathlib import Path
R=Path(__file__).parent
S=json.loads((R.parent/'source.json').read_text(encoding='utf-8'))
SID,REV=S['source_id'],S['revision']
N=[json.loads(x) for x in (R/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines()]
C={int(n['chapter_id'][3:]):n for n in N}
assert list(C)==list(range(246,424)) and all(n['full_text_read'] for n in N)
def E(i,a=None,b=None,kind='fact'):
    n=C[i]
    return dict(source_id=SID,revision=REV,chapter_id=n['chapter_id'],start_line=a or n['start_line'],end_line=b or n['end_line'],claim_kind=kind)
def es(*ids): return [E(i) for i in ids]
def W(f,v): (R/f).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def O(key,fact,inference,ids): return dict(key=key,fact=fact,inference=inference,evidence=es(*ids),review_status='draft')
D={
'worldbuilding':[
 O('costs-and-locks','隐藏职业多倍经验、仙宠孵化降20级且后续经验翻倍、主角融合要材料/10万声望/90%成功；收益伴随资格与损耗。','规则最有效时改变选择：秦韵因经验成本放弃仙龟，书生承担融合风险。不能把强者收益当无条件资源。',[246,372,409,410]),
 O('territory-as-process','首领地经历令牌争夺与10小时持有、资源劳力建设、升级城堡、传送收费、职业积分仓，再到正式掠夺攻城。','领地既是战利品也是制度容器；把一次夺宝拆为持有、维护、分配和再防守，持续产生情节。',[279,281,341,410,414,417]),
 O('pet-and-control-rules','灵儿初有变形和装备限制，第一封印解后保技成长；怪物免疫、反射、短控、技能冷却、预言守尸反复影响战斗。','战力不等输出数字；能否控、何时死、是否再杀、是否有续航和地形，构成多维门槛。设定异文须留账。',[287,294,344,387,405,408]),
 O('economic-asymmetry','秋风镇实际卖2000万人民币、神器鉴定消耗500万金币；雪见草会逐瓶捡中型药，甚至无钱买回城。','巨额奖励与普通成员生计并置，使组织分配有意义；若只保留天价面板，会丢掉资源差的叙事用途。',[383,409,416])],
'characters':[
 O('shusheng-protector-manager','书生拒凌天支票离队，又救月与香；后承认守护损失出于管理疏忽，实际给枪钱亲带，并建积分仓。','人物的主导价值是守护自己人，同时带有报复、占有与强者自信；成长不只等级，也从亲自救人转向组织补偿。',[258,285,297,411,414]),
 O('lingxue-agency','凌雪二转自己选冰霜剑士、校园公开男友、让圣盾给冰茶、最终实穿亚特套成前排主力；要求书生别为装备过度熬夜。','她既制造共同冒险也评判代价；恋人不是等待发奖的静态受益者，分配、让步、接力击杀都提供行动。',[247,340,406,408,417,423]),
 O('lingyue-and-qinyun','月在父权与婚姻压力中寻经济自主、表白并依靠书生；秦韵先安置离队者又持续留恋，花园中书生回应希望与她长在。','多人感情线由照护、回避和不完整答复递进；到卷末不能概括成书生只爱雪、韵单恋，也不能宣布三人关系已妥善协商。',[261,297,299,370,412]),
 O('fragility-and-competence','香现实腿伤噩梦未愈，游戏高血封印数次救团；弱输出雨与夏在古龟战主动牺牲保装备/挡击；紫月另组适配队成为主攻。','脆弱与能力可以同时存在。用角色不同任务的有效选择代替简单的强弱排位，才能让团体成员有存在感。',[286,287,393,404,408,411])],
'plot':[
 O('nested-gains','幻灵救援、领地争夺、古秦/赛事、守城、秋风反击、采药封印、亚特副本互相供给技能、经济和战力。','本卷不是单条升级曲线，而是资源跨任务转运：旧魂殇续召、毒剂后来毒龟、漩涡回到会战，奖励不断改变后续可选解法。',[257,294,335,369,384,387,408,421]),
 O('victory-with-debt','幻灵任务成功仍有队友掉级、百万补损；守城成功仍死大批人/NPC；古龟个人成功伴随团员退场、失联使守护受虐。','主线胜利保留人情、组织与身体欠账，让回报不抹平代价；补偿场景是战斗结果的一部分。',[257,367,369,408,410,411]),
 O('deception-and-property','秋风镇主角主动丢令让敌清NPC，利用一会不能两领及孤坟未知规则交镇收2000万；主承认围点打援做不到完全截断。','谋略有效来自信息差及调整，而非全知必胜。交易让不需的目标转为经济成果，同时暴露友盟关系中的利益计算。',[379,381,383]),
 O('unclosed-end','双战役已正式发起，主月冰雨及主冰茶一剑击溃中路；末暗影蝶已退、七星地龙死，但七星仍活，血2450未清、守城未结。','卷尾用压倒优势制造胜利预期，却把清隐刺与最终结算留到后卷；研究图必须open，不能用预期当结果。',[417,420,422,423])],
'style':[
 O('system-register-switch','长面板与系统铃声后频繁接第一人称感叹、粗口、英文缩写、夸张价值估算；融合/掉落处尤密。','文风控制可设数值密度高、口语高、感叹高。面板提供可比较承诺，口语即时翻译为情绪；重复惊叹过密会使稀有奖励同质化。',[335,409,410,415]),
 O('comic-deflation','深海仙怪被调侃为虾堡、坑塌双BOSS残血；巨型史王被敌称蓝色粪便却追不上人；火锅驾驶/吟诗穿插战斗。','高威胁后用日常食物与笨拙动作降压，保持轻快；笑点若依靠性羞辱或身材贬损，容易损害角色尊重与场面庄严。',[404,405,412,413,423]),
 O('sensory-focus','初雪、手冷、花将枯、红眼与端菜构成生活感；女性身体与衣着描写高频，常与角色初见或情感停顿绑定。','可迁移的是用具体温度/动作承载关心，不是复制凝视部位。将感官通道从单一视觉扩至触觉、疲劳和环境能保留情绪而减少物化。',[409,412,413]),
 O('lyrical-islands','墓园椰树、魂殇雪莉、林克盲锻、听雨称姐姐触亡姐回忆，把轻佻口语暂换为悲怆抒情。','短抒情岛依靠此前低调物件回收，形成情绪反差；不宜把每场都升格为誓言，需保留平静铺垫。',[248,291,292,401,417])],
'narrative':[
 O('limited-first-person','书生实时操作与内心判断支配视野；龙魂电话转述王伤、林傲重整与守护74死，视野外来源明确可辨。','“我”会猜测、炫耀与归因。研究应把转述、敌证、系统、现场分级，不把自信的因果说明误当上帝视角。',[345,359,404,410]),
 O('dramatic-irony','魂殇不知爱人已腐亡而读者看见；林克将记忆权杖认作安妮，主角与读者知道不是真人；书生不公布灵儿奔雷。','三类信息差分别制造悲悯、完成遗愿与战术伏笔。保持谁知道什么，比只写“揭密了”更能解释戏剧效果。',[291,292,401,403]),
 O('system-emotion-friction','冰兰回应愿为自己活，随后系统好感+100，主角反觉虚幻；风领域领悟公告后仍挡不住情意，主向月承认失败。','提示框既给成长确证又打断沉浸；作者让虚拟情感与系统奖励互相抵触，保留游戏小说特有的认知裂隙。',[414,422]),
 O('knowledge-not-outcome','读者见王报复从委托到龙魂报告落实；“凌天另一批”仍猜归因；冰茶多次余生/生命隐语未给病名。','有证据的发生、人物认为的原因与未来伏笔需分层。未知不等遗漏，也不等研究者可以补完。',[336,345,394,415])],
'dialogue':[
 O('negotiating-allocation','雪先让套件给冰茶，冰茶回让并坚持主角取者付钱原则；雨为弱自惭，众人表不弃后收宠；守护先拒枪再被“未来冲锋”说服。','分配对话让价格、尊严、信任显形。决定不是一句“大家同意”，而通过拒收、重申贡献、给未来角色实现。',[394,405,411]),
 O('evasion-with-consequences','韵问是否因姐妹看不见而不紧张，书生扶身换题；初雪韵花喻、雪离场后，书生转而明确也希望一直一起。','话题回避能延迟承诺，但后续必须改变答复强度；否则多人线只重复暧昧。此卷已有推进而未解决身份。',[406,412]),
 O('status-and-organization','书生允许盟友谈报酬、以秋风旧惠换帮助；大战守城指挥交孤坟，主场指令按职业与地形；龙魂对新牧荤话被秦韵制止。','短指令/玩笑/尊称在同一团队中切换，表现权威并非一味压服。制止玩笑是边界行动，应与笑点并读。',[417,420,421,416]),
 O('choice-before-fight','古龟称仙器可换最珍爱之人，书生护雪直接拒；冰兰谈传承旧代死亡，书生宁被清门户也不接受。','用二选一邀约让价值排序显形，再以战斗代价检验；不必复制特定誓词，保留选择结构即可。',[407,414])],
'pacing':[
 O('grind-compression','亚特前层多小时/天清怪被概述，首遇/BOSS/分配展开；坑塌五六层骤缩，古龟12小时却先展开安全距离试验再压缩循环。','真实耗时与文本节奏不同。只详细写改变方案的首次尝试、失败与转折，可避免重复劳动拖慢阅读。',[393,396,405,408]),
 O('cliffhanger-types','令牌属性先藏后揭、奔雷BOSS章末放大招未杀、卷末双剑落位未报命中、香遇寒风断在章尾。','奖励揭示、行动悬停、反制来袭轮换制造追读；每次悬停须在后文确切回收，不能用标题或下章预感替代。',[405,406,402,421,423]),
 O('breathers-carry-state','亚特归来饭菜红眼、补偿带练、初雪火锅看似休息，却分别改变承诺、组织关系和情感表达；外敌战报及时返回。','有效喘息不是暂停剧情，而是把战利品转换成关系与新任务；生活段可以低动作高状态变化。',[409,411,412,413]),
 O('escalation-with-failure','起初秒杀敌人，随后法弓集火迫退；情意对轰出现敌防御/新增技能，风领域新悟仍失败；最终再分兵清场。','增长后安排针对性威胁恢复悬念，新的技能不是一键取消旧风险；人数、控制与准备仍有效。',[418,419,422,423])],
'themes':[
 O('love-versus-instrument','魂殇被骗牺牲爱人；林克盲锻至终；龟取安妮爱情换圣剑，主角拒以雪换仙器；冰兰传承死亡也被拒。','力量是否必须消费亲密关系，是多次镜像问答。主角的答案是拒绝交换，但对敌复仇和多人占有仍使其守护伦理有局限。',[291,292,401,407,414]),
 O('loyalty-and-repayment','为幻灵死者补损、守护74死后亲带给枪、积分仓与雪见草资源扶持，把不弃同伴具体为资源和时间。','团体口号经兑现才有可信度。英雄不能只要求牺牲，需要承担管理疏忽并修补损失。',[257,410,411,414,416]),
 O('revenge-and-judgment','书生秋风战明说报复非正义，死亡挑战喊话也不谈正邪；同时私刑王身体损害被盟友庆笑，敌方温情却曾短暂展示。','文本会承认权力争夺，又用敌我标签宽宥己方暴力。研究可保留其热血动力，但不能把私刑/羞辱当普适正义或迁移规则。',[336,345,367,375,417]),
 O('virtual-life','冰兰对话因系统提示被拉回虚拟，仙宠具有陪伴承诺；初雪同看意义来自在场而非天气本身。','价值可由共同经历而来，即使世界有机制化评价。用角色对同一事件的不同意义解释，比笼统“现实虚拟融合”更具体。',[388,412,414])],
'continuity':[
 O('actual-versus-pending','王者城堡/烈魂融合/亚特奖励/150四转及雪穿套皆已完成；国王铸新甲、雪给同伴人民币、盲女月光任务、守护120掌骑均未见完成。','交接应按最后实际状态冻结，不能将价格、允诺或能力预测自动结算。',[403,410,414,415,417,420]),
 O('combat-state','主154黑龙剑士，风领域第二层首次脱力后恢复；雪150亚特套有复活与寂静但本卷寂静CD不足，主雪仍未悟情意。','同一物品包内/穿齐、同一角色上马/下马、每次预言是否重加影响结果；记录状态区间可避免把表面矛盾统修为一套规则。',[415,417,420,422,423]),
 O('textual-conflicts','神龙斩面板120秒旁白一分钟、终龟锁链百万跳与千万总血、回魂次数、人物名与层号误写等均在逐章unresolved中保留。','本研究不默改原文；可分类为数值/称谓/时间/规则疑点，由整书审计评估解释空间。',[335,336,407,408,417,422,423]),
 O('volume-boundary','本卷完整覆盖印245—422/raw246—423，卷三前史非本阅读者全文范围，卷末未读取卷五结果。','阶段研究必须允许未知；主代理可依后卷补收束边，但不得倒灌为本卷已完成。',[246,423])]
}

CHARS=[
 ('shusheng','轻狂书生','保护雪月与爱人、成为足以守护的强者','多倍经验、群控/魔法集火、管理盲区、非排他感情','对雪有正式恋人承诺；对月承认有情；对韵表达长在愿望；对冰兰拒传承死亡；对组织承担补偿','拒支票离队、救月/香、分派守城、亲补守护、拒龟交易','80二转到154四转；从个体打手扩展为领地与分配制度管理者；报复与占有仍在',[246,258,285,297,411,412,414,417,423]),
 ('lingxue','凌雪','自主选择职业与恋爱，和团队共同变强','父亲干预、经验门槛、装备依赖与控杀风险','对书生正式公开男友；接受姐姐在身边但未给多人制度授权；对冰茶以让书互惠','校园公开关系、先让圣盾、战中接力终杀暗影、关心熬夜代价','冰霜剑士二转到150四转，实穿七件亚特；从并肩高手进一步成为第一前排标志',[247,340,406,408,417,423]),
 ('lingyue','凌月','保雪月自主权、脱父权婚姻安排、留书生在身边','父亲资源控制、王的背叛、仙宠经验成本、爱情未获排他安排','对书生表白并依赖；对雪关爱兼有共享倾向；蓝星资源拥有者而非单纯雇员','拒婚、自主掌团队、复归工作室、用漩涡闪烁连击','冰雪法师150四转；已孵果果-20后练回；漩涡实学宗师，输出与战略地位更稳',[261,296,297,372,417,421]),
 ('qinyun','秦韵/紫韵儿','维系团队、以照护与自主选择留在书生身边','隐藏经验贵、治疗CD、面对姐妹的关系压力','对书生明确爱恋并盼长在，书生回应同愿；对新人牧有保护和规范作用','安置离队书生、专业治复、让仙宠、花园不弃愿望','神圣牧师142，核心治疗兼组织照护者；感情从含蓄转为互表愿望但未正式定义',[260,353,406,412,416,417]),
 ('bingcha','冰茶','共同进退、以自己的能力守团','家世/真名隐而不详、普通职业、生命隐语不能定病','对雪有让装互惠，对书生感谢和暧昧又称愿其照顾三女；不等确认恋人','坚持公平、获圣盾火龙剑、口述练仙龟、援飞火','悟一剑绝尘；最近明确145，末榜未列原因未本章展示；口述已练龟早于150资格存在时序疑点；140亚仙火龙实用',[337,344,347,394,406,409,413,415,417,423]),
 ('xiang','稻花香','摆脱控制、康复并作为雪月成员有尊严','现实腿伤/噩梦、封印MISS及等级差、灵魂星雨可打断','信赖书生与姐妹；与林家控制关系已断但风险在；与小蝴蝶战中有迟疑','假死不助敌、求救、接受护理、多次高血封锁救团','灵魂巫师144；现实仅报告腿稍能动和未来康复希望，未证痊愈/步行',[276,285,286,287,368,375,417,422]),
 ('linger','灵儿','陪伴保护书生，找回封印与身世','先天封印/变形装备限制，后仍受级差、群控与死亡降级','称书生哥哥、承诺除非被弃不离；母亲留封印/仙装；安妮熟识记忆未全','护泉、解第一封、坦怪、偷奔雷、斩地龙','第一封解取消变形保技、获仙装与奔雷；余二封未解；神级宠也会被古龟杀/人海控',[255,351,385,387,388,403,408,422,423]),
 ('binglan','冰兰','守护龙域与人类、培养龙语者','职责、传承旧代死亡说法、时间/冰封史','对书生多次救援与信任，好感增加；书生拒以她死换成长','负伤杀龙骨、斩卡伦臂使其遁、借斩龙剑、愿自私一次','仍活龙域，天神器255持有者；四转已授，神之领域示范成学生目标',[257,359,360,372,414,415,422]),
 ('qixing','七星灯','率血饮获胜、击败书生','技能弱期、驱散/控制、装备差与灵儿强度','对血饮有战友关系，非纯孤立反派；与九星死亡剑斩，对主为多轮竞争','赛事幽魂附体、守城战抵抗、挑战带侧翼，末无敌躲冲','145黑暗剑士；赛事败但未被永久消除；卷末地龙死、本人尚活正被两剑围攻',[335,347,367,382,417,422,423]),
 ('xueyin','血饮天下','扩高手集团、攻夺雪月领地','盟众士气、死亡挑战锁定、个人力弱于书生','护妹妹蝶，与随风有知遇与协作；组织上敌对雪月','招精英刷级、掠夺令先手、双情意防反、无敌逃','会长仍未在本卷确认终退；血饮2450人在场，行会未解散',[382,404,417,422,423]),
 ('suifeng','暗影随风','以操作挑战更强者并报血饮知遇','全敏容错、主装备与骑速、预判/硬控','对血饮感恩，不由主角猜卡伦弟子而确证；保护蝶协作','秋风单挑自迎刀、寒风断香、与蝶零度护众','143级敏剑；挑战中复活次数疑点，末被主杀后雪冰封玄冰终杀退场',[382,417,422,423]),
 ('hushou','剑火守护','守住雪月与成为有用骑将','被杀掉级爆装、缺金币、不会及时呼援','忠于雪月；寻梦态度趋近未证恋爱正式','反复复活守门、先拒贵枪后收、接受亲带','龙魂报74死降30，现场34；枪/100万/暗金实收，已带100可骑，120领骑仍计划',[395,410,411,412,420]),
 ('lin','林傲/傲世狂人','夺领地并压制雪月','资金及父信任波动，顶尖人才弱于血饮','控制香为幕后归因，与王/血饮联动；妹妹林飘雨同行','古战场围夺、买秋风被反清与卖镇、重整联盟','敌资助与联盟持续，肉身私刑王之第二批归凌天为推断不能套林；尚未彻底击溃',[267,286,375,381,383,404,417]),
 ('wang','王俊杰','借父权婚姻/敌资重建势力与报复','公开背叛月、被抓、私刑伤报告、搬住处','对月利用背叛；得林傲资助为龙魂报告；书生与龙魂参与报复委托','承认卖月、返游戏组天骄、续结盟','身体失性/育能力系龙魂报告已发生而非仍纯计划；第二批刻脸推凌天未证；天骄在围城盟',[297,321,336,345,367,404,417]),
 ('link','林克','履行给安妮铸甲与再见的承诺','死变盲亡灵、安妮不在现场、记忆权杖与真人不能辨','林克向安妮誓言延续到死后；对带权杖的玩家完成托付；关系互指独立安妮人物卡','为昔日突围牺牲、死后仍锻白金、完成战甲、抱权杖误认安妮后告别','本卷灵魂已消散，铸甲承诺已回收但未真重逢；瓶接月光少女仍open',[400,401,410]),
 ('annie','安妮','本卷回忆与任务叙史中为人类取王者圣剑；当前主动目标未知','未真人出场；记忆/物品简介/敌方及国王证词各有视野限制，当前生死与去向未完整确证','记忆中与林克有亲密与托付；国王称她女儿；古龟自称取她爱情，不能据单一证词补终局；关系互指林克独立卡','回忆里取圣剑并让林克铸甲；弃王位/牺牲等由国王说，完整动机仍待后文','仅由记忆、遗物与他人证词可见，未在本卷与林克真人重逢；女武神甲交国王，当前状态未知',[400,401,407,410]),
 ('soul','魂殇','为雪莉报仇、识破欺骗后托付遗愿','失明、受卡伦欺骗、临终方复明；召唤有时长与冷却','向雪莉的爱被公爵与黑暗者利用；对书生由敌转托付者；与冰雪女神影旧识','以极端杀戮回应献祭、临终见雪莉魂影知被骗、化剑助书生','人形敌已终结，作为可召死灵剑士保留在烈魂；卡伦仍逃，复仇未总清',[291,292,294,348,359,410]),
 ('xuecao','雪见草','节省药钱、帮助队伍并留雪月','110牧缺钱、被清场、职业消耗','信任盟主，主委龙魂培养为韵外替补；尚无恋爱关系','被救仍愿共退、捡全中药、收卷/2000金','从新加入未识盟主到被重点培养；替补实力成长尚待后文',[415,416])]

SCENES=[
 ('cemetery','墓园椰树与亡姐','理解书生强势之外的伤口','开心的工作室生活与祭亡并置','主角向冰茶讲亡姐并保留悲伤','保护欲有私人来路','亡姐成为反复回声','用椰树哭/笑与共同祭奠将抽象失去落为物件和动作','适合行动主角建立非胜负欲望','把伤口解释成所有暴力免责会过度简化',[248]),
 ('dragonbone','幻灵救援胜而补损','救幻灵并带同伴撤出','龙骨压倒玩家、众死、时间要求','求援冰兰并由玩家打一击获取任务；主补死者百万','主线完成仍掉级、导师负伤','灵儿入队与补偿责任同时形成','超规格救援限定在任务与好感，胜利保留团队债','有明确援助条件和不可逆损失的任务','把导师援助重复作无条件免死会失悬念',[256,257]),
 ('exile','撕支票离开雪月','保尊严与关系自主','凌天照片误判/五千万买离','书生撕票出走，秦韵提供住所、忠诚成员追随','经济资源与个人忠诚分离','组织分盟、感情压力转现实','让资源主人与情感中心分开，产生可见代价','团队分裂而未简单黑白清退','复制羞辱富父模板而无后续制度成本',[258,259,260]),
 ('firstcity','首领地最后持令','夺首领地','令17易手、多方联盟/十小时门槛','与孤坟立约、守末、集援、正式持领主令','领地终于建成并需建设','从战斗奖励变长期组织资产','多方竞价+盟约把单场PK扩成外交和物流','资源目标有持有期/转移权','预喊胜利不等系统完成；不能忽略其他会外援',[271,277,278,279]),
 ('rescuexiang','上海救香与护理','把求救者带离控制','现实行动危险、腿伤、隐私与证据冲突','伪快递入内救人、毁录像、送医付20万安置','身体与噩梦未立即治愈','从敌方工具转受照护同伴','让营救后的医疗、空间和信任继续发生','创伤角色拥有后续自主和游戏作用','把破坏证据/殴打直接神化，或救出即痊愈',[285,286,287,290]),
 ('soul','魂殇临终复明','理解亡灵为何追杀','被骗献祭爱人而不自知','临终见雪莉魂影、请求复仇并化剑','旧敌转可召伙伴','仇杀重解释并留下武器承诺','读者早知/角色晚知令战斗转为悲悯，战利品带人格','有前置认知差与遗愿的敌人转化','用装备价值盖过死者故事会消耗悲剧',[291,292,294]),
 ('hotel','月获救与回家','救被出卖的月并重建安全','王下药、父权婚姻与误解','书生拒乘危、接月，月表爱；再迁回别墅','安全与亲密增加，雪知识不等全部在场','关系由雇佣/合作进一步转恋爱压力','危机场景通过克制选择而非仅武力显价值','尊重受害者后续行动与未公开信息','将药理处置当真实医疗指南或把救命变爱情债',[297,298,299]),
 ('ancientqin','古秦多人接力杀帝王魂','过高难副本','鬼神降、召物、预言与香血限','香/宠/众人接力扛、召魂殇、主升龙收','书生110、月悟情意，雪未悟','人际期待与可用技能出现差','用资源轮转让全队强弱互补','技能冷却/代价清楚的团战','一次爆发就删掉所有前置风险',[317,318,319,320]),
 ('tournament','决赛血狂逆七星','赢竞技冠军','七星虚幻/预言/幽魂附体，双召被压','先试探失败再背刺暴击，保留操作与爆发配合','首冠、神龙斩与成长奖励','竞技声望与战力进入领地战','公开赛把技能揭示和围观评价合并','规则固定且胜负可验证的竞技','旁白回述伤害不一致需列异常，勿强修',[333,334,335,336]),
 ('campus','校园公开男友','确认现实关系自主','同学炫资辱劳动者、家与校园舆论','雪公开称男友并吻；主回击后仍主动动手','恋爱身份公开，冲突可能延后','恋人关系从暗示变实际称谓','用第三方见证让状态变化可证','关系需要公共确认的节点','肢体反击与后续家教报复不宜当普适成熟',[340]),
 ('kallen','逐风翼中护恋人与导师救援','拖住毁城风并完成驯坐骑','全MISS、灵儿死、卡伦压制','让雪用6秒无敌抵风眼，冰兰救后斩臂、主驯马','卡伦逃未死、仙马到手但未119不能骑','未来机动战力与未死强敌并存','把免死短窗变协作条件，而非无成本拖时','任务与灾变合并的高危段','驯获不等可骑；重伤逃走不等永久清除',[357,358,359,360]),
 ('citydefense','守城成功的巨额损失','守白云不失城','多波兵、空地分流、终黑龙超规格','主香利用背/体内盲点、魂殇剖体、死后复起续战','系统守成+3双倍，但联军/NPC大损','仙蛋/剑刃风暴与人情债并出','胜利条件只保城，过程损失不被结算抹平','集体任务有不同层次的成败判据','不能将主角5000一击等同独力无损守成',[366,367,368,369]),
 ('autumn','主动丢令、再卖秋风镇','报复林傲并利用已夺资源','NPC先攻成本与不能二领','丢令诱敌清NPC，末抢回；利用规则卖孤坟','实际2000万到账、分奖、镇归似水','仇敌损耗与现金收益替代重复领地','知道不需目标且有出售窗口才使诱饵成立','资产可转让、有真买方/规则差的谋略','把所有敌人写傻、谋略无执行风险',[378,379,381,382,383]),
 ('spring','魔泉误以失去灵儿','脱兽皇保灵儿','水域不能骑、宠栏缺失、主误判','灵儿护主入泉、醒后解一封，母印消','实力改变、其余封印未解','宠物陪伴承诺与身世后续并存','先让系统栏误导，再用行动/规则变化澄清','信息界面不能完整描述生命式角色的场景','凭主角恐慌宣布契约已解会错读',[385,386,387,388]),
 ('linkforge','盲亡灵最后铸甲','履安妮旧约','死亡、失明、千年等待与安妮不在','林克仍锻白金，抱记忆权杖误认恋人后告别','女武神战甲完成，魂散，众人无喜','任务转月光少女未完成','物件触发记忆与误认重逢，给玩家奖励却改变情绪','跨时承诺有实体劳动遗迹','把幻影当真人重逢、把旧诺直接当全史可靠',[400,401]),
 ('pit','引坑意外打穿两层','化解虾强震退','正攻受阻、队友真退场','月提坑主实施，塌层砸怪；香封残BOSS、雪大招收','五六层清但无小怪经验/额外装备少','重复刷层被一次环境连锁压缩','意外必须有连锁后果与机会成本','可破坏环境且已铺结构空间','当作任何游戏都可复制的逃课技巧',[404,405]),
 ('turtle','拒交换后十二小时毒龟','保最珍爱者并完成任务','团灭、装备爆出、无破防与级差','拒龟交易，雨夏牺牲捡回，主试54码隐退、止回毒/柱/宠接力','龟真死，主145红灯，团队掉级；后战利品补强','亚特装备与漩涡取得，玩家身体付价','多条件组合逐步验证，环境优势还会断裂','敌回血/距离/地形/持续操作有明确约束','把熬夜当健康建议或毒瓶无条件杀任意BOSS',[407,408,409]),
 ('hushou','给枪与亲带补守护','修补忠诚者惨重损失','74死报告、34级现场、缺钱、拒收','盟主承疏忽后赋未来骑将任务，实给枪钱装并带练','守护100可骑，120主骑仍约定；寻梦态度转近','组织承诺以稀缺资源和时间兑现','礼物包含被需要的未来身份，受助者保尊严','团队过度牺牲后必须补偿的情节','只赞忠诚不修管理，或拿估值当真现金',[410,411,412,420]),
 ('snow','初雪共同观看与韵花喻','共享生活并表达未了感情','冷、多人关系与含蓄退让','姐妹挽臂、雪先离、韵明示坚持；主回应也盼长在','情感向共同愿望推进，身份仍未定义','喘息段实际改关系状态','天气意义来自谁一起看，花喻后用答复强度结算','长战后的关系承接场景','把暧昧当全员同意或疾病确诊',[412]),
 ('doublewar','五盟守城、主盟入死亡挑战','抵御夺城同时消灭核心敌会','两战同10小时、有限盟友位与敌退会锁','先10分钟公告留退出机会，再实交令，孤坟总守城','双战同时启动，结果本卷未结','空间分工与制度规则成战略','两个规则相互咬合使外交与主线战力都必要','盟友有明确任务、通信和失败边界','只看竞技优势就宣布领地也守成',[417,420]),
 ('domainfail','风领域失败与情意对轰','救前排并反击','敌攻防情意、我套寂静不可用','主悟领域却脱力，转冰雨面积压零度再一剑打聚众','至少2000己方死，敌更大损，龙鬼另线死','新能力不完整、远端代价仍存','先给有限救援再承失败，连招利用对手防御选择','升级/援助不应取消损失的高潮','系统领悟即默写完全成功，或把寂静写已释放',[422]),
 ('volend','优势围杀却未结算','清敌赢挑战','暗影蝶/地龙强点、藏匿刺客、七星无敌','主雪终杀暗影蝶，灵儿斩龙，分队搜隐，围七星','场内血2450，末剑气未报中死','卷末仍开放，需后卷系统证据','把胜利条件具体到最后一人，优势不等完成','有限清场条件适合悬念收束','跨卷倒灌结算或误读最后动作',[423])]

PATS=[
 ('reward-redeployment','奖励跨任务再部署',['先在旧战中痛感缺口','获稀缺工具并说明限制','在不同类型冲突中试用/反制','改变后续可选择方案而非只加分'],['奖励有可演示功能与限制','新冲突改变用途'],['新奖励无条件覆盖所有问题','旧队友贡献被工具吞没'],'更换世界规则、工具来源和代价，让旧体验提出新问题；不要移植技能名、参数或场景顺序',['soul','citydefense','spring','turtle','domainfail']),
 ('win-debt','胜利后必须偿付的组织债',['区分系统胜利与个体损失','具体记录谁因集体目标受损','领导承认疏漏/分担资源','用时间或制度兑现而非口号'],['组织目标和成员成本可分离','补偿会影响未来资源'],['牺牲被一次升级自动抹掉','奖励只是领袖施恩无责任反思'],'原创时设计独特组织责任、成员拒收理由与补偿流程，不复用反复被杀次数/神枪',[ 'dragonbone','citydefense','hushou']),
 ('misrecognition','读者知真相的误认告别',['给读者足够物件/身份信息','让角色在有缺陷感知中投射愿望','允许情绪完成而不篡改事实','后续行动携带遗愿与未解决部分'],['误认符合伤口/感知限制','对象真实状态保持可辨'],['研究或叙述当作真重逢','只为催泪临时造身份'],'可用非亡灵非恋爱关系、不同感知缺陷与未发出的承诺；不用同一盲锻/权杖组合',['soul','linkforge','spring']),
 ('distribution-dialogue','以分配谈判塑造团队',['稀缺战果产生冲突','让人明确说出需要或羞愧','以贡献/未来作用/自选成本谈判','接受/让出后在后场景验证作用'],['人物有不同成本函数','结果实际发生并可回访'],['全员一律谦让无真实欲望','价格估算替代人物选择'],'设计新的分配制度和需求差：数据权限、维修工时或风险额度；保留拒收到接受的心理因果',['linkforge','pit','hushou','turtle']),
 ('terrain-probe','把不可能战斗改为验证循环',['明确正攻为何失败','测一条可见边界并接受失败可能','组合移动/距离/状态/地形','让环境优势耗尽或敌改行动','坚持操作并付时间/身体或资源成本'],['边界可实测','组合条件缺一会变结果'],['BOSS无理由停机','脱战与回血规则被随意改'],'以原创地形、感知和恢复规则设计安全循环，保留试验过程，不照搬54码/毒龟',['kallen','autumn','turtle']),
 ('breather-state','低动作喘息仍改变状态',['让大战产物进入日常','用小动作引出未说的需求','答复比前一次更明确或更回避','把新关系/责任带回下一战'],['人物有累积未结话题','日常物件与身体状态具体'],['仅重复身材赞美与插科','人物每次又回到原关系'],'采用原创日常习惯、天气/器物和不同话语权，让停顿结算一个小状态而不是套火锅初雪',['exile','hushou','snow']),
 ('incomplete-awakening','关键领悟先部分失败',['危机提出旧能力无法满足的需求','人物主动尝试新用法','系统/行动确证层级上升','效果只保局部并产生新消耗','换方案处理剩余损失'],['新能力有成长空间','失败后不虚构无损'],['临战悟技立刻解决一切','角色没有承担尝试代价'],'把觉醒机制改为技能训练、装备实验或协作默契，具体保留被救者与没救到者差别',['domainfail','citydefense']),
 ('two-front-rules','规则交叉生成两线战略',['清楚说明两种战役的时点和胜负条件','对手先承诺一种行动','己方用另一规则锁定关键力量','盟友/制度承担原战场','分别追踪结果和通信盲区'],['盟友利益和资格可解释','两战均有失败空间'],['一线胜利自动当另一线胜利','盟友成为无成本工具'],'创造新的时窗、责任边界与交易，不使用相同令牌/会名/固定人数结构',['firstcity','autumn','doublewar','volend'])]

cards=[]
def key(t,k):return f'{SID}/full-20261025/vol04/{t}/{k}'
base=dict(tags=['作者:失落叶','作品:网游之纵横天下','卷:四','状态:待审阅'],user_notes='',favorite=False,review_status='draft')
for k,t,g,l,rel,de,change,ids in CHARS:
    cards.append(dict(base,asset_type='character',scope='source-analysis',title=t,origin_key=key('character',k),content=dict(summary=change,goal=g,limitations=l,relationships_directional=rel,decisions=de,change=change,boundary='仅卷四阶段；非全书人物终局。'),evidence=es(*ids)))
for c in cards:
    if c['origin_key']==key('character','link'):c['content']['related_origin_keys']=[key('character','annie')]
    if c['origin_key']==key('character','annie'):c['content']['related_origin_keys']=[key('character','link')]
for k,t,g,o,ch,co,st,why,app,fail,ids in SCENES:
    cards.append(dict(base,asset_type='scene',scope='source-analysis',title=t,origin_key=key('scene',k),content=dict(summary=f'{ch}；{st}',goal=g,obstacle=o,choice=ch,consequence=co,state_change=st,why_it_works=why,applicability=app,failure_mode=fail),evidence=es(*ids)))
scene_by={x[0]:x for x in SCENES}
for k,t,steps,conds,fails,transform,derived in PATS:
    ids=sorted(set(i for d in derived for i in scene_by[d][-1]))
    cards.append(dict(base,asset_type='pattern',scope='reusable-pattern',title=t,origin_key=key('pattern',k),content=dict(summary=t+'；研究性机制，不是用户审美规则。',causal_steps=steps,applicability=conds,failure_mode=fails,originality_transform=transform,derived_from_origin_keys=[key('scene',d) for d in derived]),evidence=es(*ids)))
W('cards.json',cards)

anomalies=[dict(chapter_id=n['chapter_id'],issues=n['unresolved'],evidence=[E(int(n['chapter_id'][3:]))]) for n in N if n['unresolved']]
A=dict(source_id=SID,revision=REV,volume=4,title='卷四乱世称雄：全量九维研究草稿',review_status='draft',read_chapter_ids=[n['chapter_id'] for n in N],coverage=dict(body_units=178,raw_range=['ch-0246','ch-0423'],printed_range=[245,422],complete_volume=True,complete_book=False),dimensions=D,characters=[dict(origin_key=key('character',c[0]),name=c[1],stage_state=c[6],evidence=es(*c[-1])) for c in CHARS],threads=[
 dict(key='guild-rise',kind='main',status='partial',state='王者之都已城堡并开仓收费；双战役已开但本卷守城/死亡挑战无结算。',evidence=es(410,414,417,423)),
 dict(key='atlantis',kind='main',status='resolved',state='上古龟死且回国王系统完成亚特；国王铸新甲与月光少女另属未决。',evidence=es(408,410)),
 dict(key='relationships',kind='subplot',status='partial',state='雪正式女友；月表白/依恋；韵获主角同盼长在的明确回应；尚未解决多人安排。',evidence=es(340,412)),
 dict(key='seals',kind='hidden',status='partial',state='灵儿第一封解，母印三符，后两封/身世待后续；安妮熟识尚未全解。',evidence=es(351,385,387,388)),
 dict(key='revenge-wang',kind='subplot',status='partial',state='报复已由委托推进至龙魂报告致伤；第二批刻脸与凌天归因不确定；王仍组织天骄。',evidence=es(336,345,404)),
 dict(key='bingcha-identity',kind='hidden',status='open',state='真名借号/家世/生命隐语未揭；不能推疾病/终局。',evidence=es(337,394,403,415)),
 dict(key='binglan-legacy',kind='hidden',status='open',state='冰兰仍活，称新代强需旧代死，被主角拒；斩龙剑已归还，未传。',evidence=es(414,415)),
 dict(key='moonlight',kind='subplot',status='open',state='林克瓶接月光少女，回城后本卷无交任务证据。',evidence=es(401,410))],unresolved_and_anomalies=anomalies,transferable_mechanisms=[dict(origin_key=key('pattern',p[0]),summary=p[1]) for p in PATS],literary_tradeoffs=[dict(claim_kind='inference',observation='面板与连续重奖强化可比成长，也出现数值膨胀、概率/称谓错漏，结构校验不能替文学连贯性背书。',evidence=es(335,407,410)),dict(claim_kind='inference',observation='团体不弃与救助有感染力；性羞辱、身材贬称、以敌我定义可施暴与女性被救后围绕主角的惯例，限制可迁移部分。',evidence=es(345,411,413,419)),dict(claim_kind='inference',observation='敌方护妹/知遇/临败互勉使反派局部有关系厚度，但敌方群体经常以菜鸟化服务碾压爽点。',evidence=es(367,382,422,423))],boundary_notes=['未由本阅读者全文阅读卷三，前史依赖待主代理衔接。','未把卷五结果倒灌；死亡挑战status open。','全部为研究待审阅草稿，不代表用户收藏/审美认可；原创机制须结构变换与来源隔离。'])
W('analysis.json',A)

root='v04-story'
nodes=[dict(id=root,title='卷四：守护、领地与强者成本',kind='story',parent_id=None,claim_kind='synthesis',summary='由个人成长扩至组织资产与两线战争，本卷结局尚开放。',evidence=es(246,423))]
arcs=[('awakening','幻灵与离队',246,260),('territory','首领地与香救援',261,290),('qin','魂殇古秦与归家',291,320),('contest','竞技冠军与关系公开',321,340),('mount','冰雪神殿与骑乘',341,356),('defense','卡伦与白云守城',357,374),('autumn','秋风复仇与魔泉封印',375,388),('atlantis','海底之城与跨时承诺',389,410),('restitution','补偿、初雪与150',411,416),('challenge','两线战争未结',417,423)]
for k,t,a,b in arcs:nodes.append(dict(id='v04-arc-'+k,title=t,kind='arc',parent_id=root,claim_kind='synthesis',evidence=es(a,b)))
scene_arc={'cemetery':'awakening','dragonbone':'awakening','exile':'awakening','firstcity':'territory','rescuexiang':'territory','soul':'qin','hotel':'qin','ancientqin':'qin','tournament':'contest','campus':'contest','kallen':'defense','citydefense':'defense','autumn':'autumn','spring':'autumn','linkforge':'atlantis','pit':'atlantis','turtle':'atlantis','hushou':'restitution','snow':'restitution','doublewar':'challenge','domainfail':'challenge','volend':'challenge'}
event_landing={'cemetery':248,'dragonbone':257,'exile':258,'firstcity':279,'rescuexiang':286,'soul':292,'hotel':297,'ancientqin':320,'tournament':335,'campus':340,'kallen':359,'citydefense':369,'autumn':383,'spring':387,'linkforge':401,'pit':405,'turtle':408,'hushou':411,'snow':412,'doublewar':417,'domainfail':422,'volend':423}
participants={'cemetery':['shusheng','bingcha'],'dragonbone':['shusheng','lingxue','binglan','linger'],'exile':['shusheng','lingyue','qinyun'],'firstcity':['shusheng','lingyue','lingxue'],'rescuexiang':['shusheng','xiang','qinyun'],'soul':['shusheng','soul'],'hotel':['shusheng','lingyue','wang'],'ancientqin':['shusheng','lingyue','xiang','linger','qinyun'],'tournament':['shusheng','qixing','soul','linger'],'campus':['shusheng','lingxue'],'kallen':['shusheng','lingxue','binglan','linger'],'citydefense':['shusheng','xiang','soul'],'autumn':['shusheng','lin','suifeng'],'spring':['shusheng','linger'],'linkforge':['link','annie','shusheng'],'pit':['lingyue','lingxue','shusheng','xiang'],'turtle':['shusheng','lingxue','linger'],'hushou':['shusheng','hushou'],'snow':['shusheng','lingxue','lingyue','qinyun','bingcha'],'doublewar':['shusheng','lingxue','lingyue','xueyin'],'domainfail':['shusheng','lingyue','bingcha','xueyin','suifeng'],'volend':['shusheng','lingxue','qixing','suifeng','linger']}
for order,x in enumerate(SCENES,1):
    k,t,g,o,ch,co,st,why,app,fail,ids=x
    node=dict(id='v04-'+k,title=t,kind='scene',parent_id='v04-arc-'+scene_arc[k],narrative_order=event_landing[k],claim_kind='fact',asset_origin_key=key('scene',k),summary=f'{ch}；{co}。阶段变化：{st}',evidence=es(*ids),characters=[key('character',p) for p in participants[k]])
    if k=='soul':node['knowledge']=[dict(observer='reader',state='knows',belief='读者先见雪莉已腐亡/魂影，魂殇仍在被骗的认知中'),dict(observer=key('character','soul'),state='misbelieves',belief='前半仍相信所追求的承诺，临终复明才知受骗')]
    if k=='linkforge':node['knowledge']=[dict(observer='reader',state='knows',belief='来的是记忆权杖而非安妮真人'),dict(observer=key('character','link'),state='misbelieves',belief='把权杖的气息当作安妮到来')]
    if k=='spring':node['knowledge']=[dict(observer=key('character','shusheng'),state='suspects',belief='宠栏不见灵儿，恐怕已失契约；随后被醒来/解印澄清'),dict(observer='reader',state='knows',belief='截至本场后段灵儿仍在且第一封印已解')]
    if k=='volend':node['knowledge']=[dict(observer='reader',state='knows',belief='七星未报死，系统仍血2450；任何必胜陈述都是人物预期')]
    nodes.append(node)
edges=[]
def edge(a,b,kind,label,ids):
    eid=f'v04-e{len(edges)+1:02}'
    edges.append(dict(id=eid,**{'from':'v04-'+a,'to':'v04-'+b},kind=kind,label=label,claim_kind='inference',evidence=es(*ids)))
    return eid
edge('cemetery','snow','echo','伤口与共同生活并置，主角关心的私人来源',[248,412])
edge('dragonbone','spring','setup','灵儿的获取通向封印成长与陪伴承诺',[257,387,388])
edge('exile','hotel','reversal','被驱离之后又由救月与迁回重建团队',[258,297,299])
edge('exile','firstcity','cause','组织分裂后的联盟与忠诚进入领地争夺',[259,271,279])
edge('firstcity','autumn','echo','不能二领与领地转让使第二领地成为交易',[279,383])
edge('firstcity','doublewar','setup','首领地发展成城堡，随后被掠夺挑战',[279,410,417])
edge('rescuexiang','citydefense','payoff','受救者以高血封锁成为守城终战关键',[287,368,369])
edge('soul','ancientqin','payoff','魂殇化剑召唤在古秦实战',[294,317,319])
edge('soul','linkforge','echo','两种跨时爱情与误认/欺骗，结局不同',[292,401])
edge('hotel','snow','setup','月爱与秦韵照护累积至初雪共同愿望',[297,299,412])
edge('ancientqin','tournament','setup','情意/技能与装备成长转入公开竞技',[320,335])
edge('tournament','kallen','echo','力量层级对照：竞技冠军成长后仍面对逐风者全MISS，导师层级重置目标',[335,358,359])
edge('campus','snow','payoff','正式女友身份在日常共同观看中被承接',[340,412])
edge('kallen','citydefense','cause','卡伦灾变与敌军攻城相连，仙马改变空地调度',[357,360,366])
edge('citydefense','hushou','echo','成功不能抹除集体付出，需要后来补偿',[367,369,410,411])
edge('autumn','doublewar','cause','敌失镇仍重整，冲突升级为两线规则战',[383,404,417])
edge('spring','turtle','payoff','为采毒材进泉解封，所得止回毒成为终龟解法',[384,385,387,408])
edge('linkforge','turtle','reveal','林克为爱守诺后，古龟提出以爱换力的敌方说辞',[401,407])
edge('pit','turtle','setup','前层套装与团队价值累积，团灭时必须保住',[405,408])
edge('turtle','hushou','cause','关聊专注导致领地受袭不知，归城发现守护损失',[408,410,411])
edge('turtle','domainfail','payoff','漩涡掉书在会战实用是兑现；同场风领域失败是独立能力限制，并非漩涡造成',[407,409,421,422])
edge('hushou','doublewar','payoff','守护被带至100能参与战，领骑120仍未来',[420])
edge('snow','doublewar','echo','日常亲密与敌夺爱挑衅并置，私愿转组织动员',[412,417])
edge('doublewar','domainfail','cause','死亡挑战锁定双方，准备不足遇敌双情意',[417,422])
edge('domainfail','volend','reversal','损失后反击分兵压敌，优势仍未达最后清场条件',[422,423])
edge('turtle','doublewar','payoff','挑战令出海底、雪150实套与月漩涡使挑战可发动',[406,417])
edge('exile','snow','echo','失去与重新选择同伴，关系逐步从雇佣转共同生活',[258,299,412])
def thread(k,t,kind,status,ns,eidx,note,ids):return dict(id='v04-thread-'+k,title=t,kind=kind,status=status,claim_kind='inference',node_ids=['v04-'+n for n in ns],edge_ids=[f'v04-e{i:02}' for i in eidx],resolution_note=note,evidence=es(*ids))
threads=[
 thread('guild','雪月领地与两线战争','main','partial',['exile','firstcity','autumn','hushou','doublewar','domainfail','volend'],[4,5,6,16,24,25],'领地已城堡/制度成，死亡挑战和守城未结。',[410,414,417,423]),
 thread('atlantis','亚特兰蒂斯主任务','main','resolved',['linkforge','pit','turtle'],[18,19],'上古龙龟已死，国王接任务物，系统明确亚特完成；不涵盖月光少女支任务。',[408,410]),
 thread('love','雪月韵与主角关系','subplot','partial',['exile','hotel','campus','snow'],[3,10,13,27],'雪正式女友；月表白，韵获同盼；多人安排未定。',[340,412]),
 thread('seals','灵儿母印与身世','hidden','partial',['dragonbone','spring','turtle'],[2,17],'仅第一封印解，仍两封与安妮旧识待解。',[351,385,387,388]),
 thread('loyalty','不弃同伴的补偿','subplot','partial',['dragonbone','rescuexiang','citydefense','turtle','hushou'],[7,15,20],'百万补损、护理和守护枪钱时间已实付；守护120统骑仍计划。',[257,287,411,420]),
 thread('memory','跨时恋人遗愿','subplot','partial',['soul','linkforge','turtle'],[9,18],'林克铸甲/魂散已回收但并非真人重逢；盲女月光后续仍open，魂殇复仇也未总清。',[292,401,410]),
 thread('newpower','新力量与限制','main','partial',['tournament','kallen','spring','turtle','domainfail','volend'],[12,17,21,25],'四转/烈魂/套装已获，风领域首次局部失败，寂静CD不足；无全书终局。',[414,415,422,423])]
G=dict(title='卷四乱世称雄：因果树与未结线索（待审阅）',source_id=SID,revision=REV,review_status='draft',nodes=nodes,edges=edges,threads=threads,coverage=[dict(source_id=SID,revision=REV,chapter_ids=[n['chapter_id'] for n in N],complete=False,complete_volume=True,volume=4)],boundary='仅本卷，未倒灌后卷结算；人物origin_key待主代理映射正式卡。')
W('graph.json',G)

state=json.loads((R/'reader-state.json').read_text(encoding='utf-8'))
state.update(status='artifacts-ready-for-review',complete_volume=True,complete_book=False,current_volume_state=['死亡挑战在场雪月27408/血饮2450；暗影/蝶已终退、地龙死，七星灯末尚活。','守城由孤坟五盟负责，未有本卷结算。','书生154黑龙剑士；雪/月150四转；雪实穿亚特，月实学宗师漩涡；寂静本卷CD不足。','领地城堡/烈魂融合/亚特任务奖励实成；月光少女、国王铸甲、雪现金分配、守护120领骑尚未证完成。'])
W('reader-state.json',state)
log=json.loads((R/'read-log.json').read_text(encoding='utf-8'))
log.update(complete_volume=True,complete_book=False,printed_range=[245,422],raw_range=['ch-0246','ch-0423'],body_units=178,total_segments=178,truncated_pending=[],anomalies=['原文疑点逐章写入chapter-notes.unresolved并汇入analysis；未默改原文。','中途仅metadata inspect曾输出截断；所有正文read_chapters调用均核END完整。'])
W('read-log.json',log)
print(json.dumps(dict(notes=len(N),dimension_observations={k:len(v) for k,v in D.items()},cards={t:sum(x['asset_type']==t for x in cards) for t in ['character','scene','pattern']},nodes=len(nodes),edges=len(edges),threads=len(threads)),ensure_ascii=False))
