import json, pathlib, collections

BASE=pathlib.Path(__file__).resolve().parent
SRC=json.loads((BASE.parent/'source.json').read_text(encoding='utf-8'))
SID=SRC['source_id']; REV=SRC['revision']
NOTES=[json.loads(x) for x in (BASE/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
NOTES.sort(key=lambda x:x['chapter_id'])
for n in NOTES:
    if n['chapter_id']=='ch-0529':
        n['state_changes']=[s.replace('达芙妮不可复生死亡','达芙妮截至本卷已死亡、未出现复活') for s in n['state_changes']]
    if n['chapter_id']=='ch-0508':
        n['facts']=[s.replace('书生鼓动玩家上前保不可复生NPC','书生称NPC死亡不能复生，鼓动玩家上前保护') for s in n['facts']]
(BASE/'chapter-notes.jsonl').write_text(''.join(json.dumps(n,ensure_ascii=False)+'\n' for n in NOTES),encoding='utf-8')
BY={int(x['chapter_id'].split('-')[1])-1:x for x in NOTES}
UNITS=next(x for x in SRC['volumes'] if x['volume']==5)['units']
SEGMENTS=[s for u in UNITS for s in u['segments']]
IDS=[s['chapter_id'] for s in SEGMENTS]
assert [x['chapter_id'] for x in NOTES]==IDS

def dump(name,data):
    (BASE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def evidence(*chapters,kind='fact'):
    return [dict(source_id=SID,revision=REV,chapter_id=BY[n]['chapter_id'],start_line=BY[n]['start_line'],end_line=BY[n]['end_line'],claim_kind=kind) for n in chapters]

def origin(t,key):return f'{SID}/full-20261025/vol05/{t}/{key}'

READ_LOG=dict(source_id=SID,revision=REV,volume=5,review_status='draft',complete_book=False,
    scope='原书第423—530章；108个阅读单元、108个原索引片段；不是全书完成声明',
    reader='/root/zongheng_vol05_full',method='以read_chapters.py每次1—2章输出带行号全文，逐次确认BEGIN/END；每2—4章写真实笔记及状态；压缩后从持久状态续读，未以摘要或索引替代剩余原文',
    chapter_count=len(IDS),first_line=NOTES[0]['start_line'],last_line=NOTES[-1]['end_line'],
    chapters=[dict(chapter_id=x['chapter_id'],start_line=x['start_line'],end_line=x['end_line'],full_text_read=True,original_chapter_number=int(x['chapter_id'].split('-')[1])-1,index_number=int(x['chapter_id'].split('-')[1])) for x in NOTES],
    reading_units=[dict(unit_number=i+1,chapter_ids=[s['chapter_id'] for s in u['segments']]) for i,u in enumerate(UNITS)],
    truncated_pending=[],anomalies=['源metadata与全部笔记展示曾有非正文输出截断，不计作正文阅读；所有正文逐批可见END，无正文待补读。','chapter_id数字比原书章号大1，分别保存。','未读卷三四全文；前史只采本卷明确回忆，待主代理跨卷核验。'],
    quality_boundary='覆盖校验只能证明研究定位与记录覆盖；解释仍待审阅，用户审美与收藏未填写。')
dump('read-log.json',READ_LOG)

DIMENSIONS={k:[] for k in ['worldbuilding','characters','plot','style','narrative','dialogue','pacing','themes','continuity']}
def obs(dim,key,fact,inference,chapters,question):
    DIMENSIONS[dim].append(dict(id=f'v05-{dim}-{key}',fact=dict(text=fact,claim_kind='fact',evidence=evidence(*chapters)),inference=dict(text=inference,claim_kind='inference',evidence=evidence(*chapters,kind='inference')),transfer_question=question,review_status='draft'))

obs('worldbuilding','honor','荣誉称号把NPC友好、合成、经验和爆率连成系统；艾兰高亲密提高强化成功率，量产又受原料耗尽限制。','声望资源不是装饰性排行榜，它改变生产路径，再把战斗、救助NPC和经济组合起来。',[426,428,439,440],'社会信用能否改变取得资源的方法，同时保留材料、时间或组织瓶颈？')
obs('worldbuilding','terrain','地狱图禁止回城且死亡原地掉级；血色战役中城墙高差可避鲁帝，后被飞行龙蛇破坏。','同一地图的出入、射程、仇恨与空地条件持续约束选择；地利不是一次找到后永久安全。',[445,446,511,512],'优势空间会被何种敌方能力有因果地拆解？')
obs('worldbuilding','manufacture','火龙弓需要图谱、筋、玄铁、暗金珠与金币声望；72%成功后才制成，艾兰是制甲师不能造弓。','生产专长、信息差、任务资源与概率风险共同构成制造链；新品即时解除旧弓不破防瓶颈。',[468,473,499,525,526],'一件关键工具能否经过不同类型行动取得，而不是连续同质刷怪？')
obs('worldbuilding','politics','人类贵族奴役精灵，女官承认贵族腐败仍守家园；菲雅动用联盟统帅令超越国王，将狮鹫调离人类内战。','光明阵营具有内部压迫和命令冲突；公共战争不自动让其制度无瑕，个人忠诚也有不同对象。',[464,465,475,513,520],'制度的腐败、家园的价值与具体人的选择能否同时存在？')

obs('characters','shusheng','书生为艾兰制暖瓶、迁居、治眼；为达芙妮护任务，后得她救命；联军分装前又私藏苍穹项链。','关怀、承诺、逐利和阵营偏私并存；研究应把有效领导与自我合理化分别记录。',[427,428,435,464,514,524,525],'能力成长能否同时暴露价值矛盾，而非把所有选择都包装成正确？')
obs('characters','sisters','凌月担心自己被当凌雪替代；凌雪教操作、替姐姐挡杀并让书生冲锋自己逃守尸；父亲冻结账户后姐妹一起留下。','相似外貌用记忆、战术贡献与共同抉择分化；双女友情节虽获主角幻想，仍有父亲和本人边界。',[434,435,448,469,508,527],'相似角色各自不可替代的行动、恐惧和拒绝是什么？')
obs('characters','qinyun','秦韵在地狱阶段已由兄长接离，线上继续治疗与战斗，现实拒报住址、拒返工作室晚饭，说希望有天醒来不再想书生。','维持合作不等接受关系安排；拒绝以地点与日常缺席持续生效，主角想挽回不等她已答应。',[450,457,471,495,515,524],'离开者如何通过可见选择保有能动性而不是只等主角追回？')
obs('characters','guilds','暗影随风为公共战斗冒死救书生，遭血饮质疑后还套退会；他拒雪月，接受天骄但不参与对雪月PK。','公义、尊严与自由优先于最强公会的吸引力；拒绝主角邀约让竞争组织仍有现实地位。',[518,521,522],'人才拒绝最强者时，有没有清晰价值与可支付的代价？')

obs('plot','npc-return','艾兰赠低值项链后被迁居、复明并成为制甲师；达芙妮被救后救主角，最终又为菲雅战死。','NPC不止发奖工具：回报、就业与不可逆损失改变任务成功的含义，关怀能有远期用途却不能保证不死。',[427,428,435,440,464,514,528],'任务结算后，人物的生活和风险是否还继续？')
obs('plot','gears-return','枫林任务掉追踪项链，主角雷霆护送时回城穿神谕后追踪归队，又在血色捡装时传回逃235仙BOSS。','奖励先建立规则，随后改变更高难冲突的解法；不是数值表中无后果的收藏。',[432,460,461,511],'早期工具能否在不同问题中改变因果链，而不只提高伤害？')
obs('plot','defeat-rematch','雪月核心被黑石长任务占住而错过首场，后备队决赛败给魂归，魂归国际败；核心回归第二次选拔、国际胜均系统结算。','延迟核心登场保留后备队尊严和代价，再把建设收益带入复仇；局部公开十战胜不能替代国际胜。',[480,481,482,483,484,488,498,505],'败局的结构原因与再战新增条件是否可对照？')
obs('plot','annie','安妮120分钟援军被系统预告为敌方压力，抵达后为护菲雅杀卡伦并离开，黑暗身份与姐妹关系同时确认。','威胁倒计时反成救援反转；名字、亲缘与阵营冲突有前置，但主角极限后的外力解围仍削弱玩家终结权。',[428,511,521,528,529],'转折是否既有可复查前置信息，又让先前行动确实创造它的可行条件？')

obs('style','interface','长段装备属性、技能效果和系统公告穿插战斗，随后用第一人称惊叹、俗语和夸张估价回应。','文风在规则清单与口语狂喜之间切换，把数值变成可期待的能力；高频夸赞会抹平珍稀品差异。',[439,455,515,525,526],'可调控制：规则展示中高，惊叹中；只展示将改变下次选择的数值。')
obs('style','violence-jokes','大规模血肉、断肢、焚魂和NPC死亡描写，与性笑话、现代品牌、口水骂战并列。','感官强度高、比喻现代口语化使阅读轻快，但可能削弱战争哀伤并把女性身体客体化；不等用户认可此审美。',[506,507,513,516,518,524,530],'可调控制：血腥中低、身体凝视低；严肃损失后保留反应时长再转轻喜。')
obs('style','short-turns','战斗高潮大量独立短段、拟声词、技能名与数字，艾兰和米拉段更多动作触感、停顿及景物。','句段颗粒随压力切换：击打以单次反馈推进，悲情靠物件和未尽动作延时。',[427,428,433,450,518],'可调控制：高压短段高、情感场景留白中高；不要全书恒定同速。')
obs('style','commentary','书生反复自嘲箭术、把私利称不抛弃或勤俭，插商业、足球、娱乐类比；现代语汇进入幻想战役。','叙述者的评价构成稳定喜剧声线，同时显自我辩护；类别或国籍的贬损会把人物机智变刻板偏见。',[499,502,511,520,524],'迁移叙述功能而非拷贝口头禅、品牌、羞辱对象与特征化措辞。')

obs('narrative','knowledge','艾兰起初误认书生是林克，读者与书生先知死讯；姐妹辨认段在书生离开后给出姐妹私下真相。','主观第一人称兼用焦点外补叙，形成读者领先；必须标谁知道，不能替所有人物同步更新。',[426,427,434,435],'读者的信息优势是由哪一场、哪位可知者提供，是否越过既定视角？')
obs('narrative','prediction','主角猜尘埃靠bug、猜卡伦等为末王、猜NPC有胜算；正文后续才分别展示或不证实这些判断。','自信口吻不等全知事实；不可靠性多来自知识有限和自利估计，而非系统性说谎。',[425,498,511,513,521,528],'在研究层显式分开观察、转述、猜测、后验确认。')
obs('narrative','information','系统公告展示实际任务结算与公共规则，官网/论坛解释预期，战场频道和盟友消息报道视野外损失。','多种信息界面承担群像远景，节省切视角成本，但消息来源、时间与可证程度不应合并为全知。',[426,445,480,510,513,528],'每项远景信息能否记录发布者与其知识边界？')
obs('narrative','reveal','末战先让玩家听卡伦称冰兰被困，后冰兰本人到场称击退奥丹；霜剑身份在姓名和亲情行为之后合并。','先敌方说法再有限核实制造被包围感；击退奥丹确认战果，不自动证实所有12圣龙细节。',[527,528,529],'一个反派解释需要多大独立证据，才可成为世界史？')

obs('dialogue','status','兄弟会抢怪争端中尘埃区分所见与同伴谎报，很萌致歉却也招走班长；合作攻卡伦时总指挥权与岗位分配需谈判。','对话在分配可信度、颜面和组织收益，赢口角或武斗不等政治全胜。',[441,442,443,444,521,522],'交谈结束后谁实际获得人、权、资源或退路？')
obs('dialogue','refusal','秦韵以不给住址、热剩菜和等自己不想他的说法拒归；冰之逸以反问拆穿保护话术并提出杭州请饭。','间接拒绝靠具体生活选择落地，直问则让主角目的受检验；许诺赴约尚未形成招募同意。',[495,515,524,529,530],'拒绝者的话是否改变下一行动，还是只作调情阻拦？')
obs('dialogue','command','第二龙蛇战明确数秒后哪组冲锋、封印失败后哪队弓手补；傲天令停止轮冲导致火龙三秒脱控。','命令可被验证，节奏、权限与后果绑定；对话本身制造成功和失误而非解释既成战果。',[512,523],'把空泛善指挥换成可执行的时序与失败备用方案。')
obs('dialogue','intimacy','凌月问是否替代品，书生以各自相遇和哭笑记忆区分；两人同寝调情仍反复表达当前拒绝。','同一对话从索要身份确认转到亲密幻想，前者有安慰效果，后者不能视为已同意；玩笑可能掩盖权力不对称。',[508,530],'亲密话语是在回应对方需要，还是将其拒绝当作可磨平的障碍？')

obs('pacing','braiding','守城胜紧接荣誉维护，艾兰静任务后进入枫林悲剧，再用驯宠和强化回到日常经营。','强战—安静承诺—失去—生产回报形成情绪起伏；安静段仍给长期工具，故不完全停滞。',[423,425,426,428,433,436,439],'缓冲段能否改变人物承诺或未来工具，而不只是休息闲聊？')
obs('pacing','grind','地狱前数门逐场展示，后数关用概述压缩；末奥克斯多次灭团、丢级拾装再恢复细写。','重复结构先教会读者再压缩，机制改变和损失显著时重新展开，避免每轮平均分配篇幅。',[445,446,447,448,449,450,451],'重复事件何时值得扩写，何时只记录不可逆变化？')
obs('pacing','construction','黑石训练四日、后续日常任务一周多用跳时与进度条；国战十分钟、战役数秒救人则展开多章。','感知速度由决策密度而非故事时间决定；长期积累以阶段结算可见，爆点保留小窗口。',[479,480,495,497,518,523],'用进度节点压缩劳动时，是否仍保留成本和误事的后果？')
obs('pacing','escalation','血色十波从玩家优势、登墙、飞行破地利、NPC接手、玩家再援，到首领与亲缘救援；波间分装备/饭食延缓。','升级层层改变参战资格和目标，不仅增加怪数；但连续濒死和及时援救密集会让危险贬值。',[507,509,511,512,513,516,520,528],'每一波是否改变解法？多少次外援后应由主角承担持久代价？')

obs('themes','loss','艾兰复明并就业却仍思林克；米拉死留婚纱披风，任务荣誉很多不能换她活；战役胜而达芙妮死、林丘断臂。','可计算成功不能抵消不可逆失去；物件保存死者关系，使奖励系统与哀悼形成张力。',[428,433,435,516,528],'当系统说成功，人的哪一项损失仍不被结算？')
obs('themes','public-private','暗影与尘埃跨敌会援，血饮前期拒公援却为妹妹挡卡伦；雪月号召集体但主角私藏联军掉落。','共同体道义与亲缘/阵营私利彼此竞争，小说不完全给同一种标准；研究保留矛盾而非帮主角判无罪。',[518,521,524,526],'人物用公共理由要求别人时，是否愿受相同约束？')
obs('themes','agency','林飘雨拒以报复为游戏目标另建会；暗影还装离会；冰之逸以自由为由拒招募并讥主角有用才保护。','对组织依附和游戏快乐有替代回答，角色可拒绝强者与既定阵营；主角施职业威胁又试其边界。',[425,426,521,529,530],'自由是否要付资源代价，强者好意是否允许被拒？')
obs('themes','care','月雪受骗仍说继续帮助；书生帮艾兰在系统任务完成后继续生活安置；秦韵线上关照但现实离开。','关怀不总等于占有、交易或关系和解；文本又常用回报奖励善行，因此需要审视其功利化倾向。',[428,440,506,515,524],'没有立刻回报或没有关系同意时，关怀行动还成立吗？')

obs('continuity','states','卷末书生182已装备火龙弓但尚未五转，接修伊任务未做；冰逸花火已祝福，仍无会，现实赴杭州尚在途中。','等级、资格、受任、装备持有和真正完成必须分开，避免用标题或主角计划填结果。',[526,528,529,530],'给每件任务记录已接/进行/系统完成/长期后果四个状态。')
obs('continuity','knowledge','苍穹项链先被主角空中私藏，只给凌雪看，未向联军公开；可飞骑是物品属性，200和最高称号门槛尚未达。','公开战利品清单不能推导所有角色都知圣器，未来使用受双重条件制约。',[524,525,528],'物品账本是否同时记录持有者、知情者、可用门槛和已使用证据？')
obs('continuity','contradictions','神谕结界初45秒后实25秒；战役规则称白银阵亡超50%败，后损90%以上仍胜；孤坟已死仍获未阵亡资格。','这是需跨卷/版本核验的文本矛盾，不自动解释为隐藏机制；不能为让剧情自洽自行发明例外。',[455,456,507,518,519,520,528],'异常能否保留两端证据并把自动修正与事实层隔开？')
obs('continuity','relationships','父亲冻结账户的双女友矛盾尚未明确解决；国战第二次赢但姐妹未返，秦韵持续未回；冰茶只吻脸并不等恋爱确立。','战斗胜利、调情、亲密动作和家庭许可是不同状态；合并会抹去下一卷关键压力。',[469,495,505,515,524,530],'所有关系转折是否有当事人明确行动支持，而非旁人愿望？')

ANALYSIS=dict(source_id=SID,revision=REV,volume=5,title='卷五：回报链、群体战争与无法结算的损失',review_status='draft',read_chapter_ids=IDS,complete_book=False,dimensions=DIMENSIONS,
    method_boundary='本代理逐章全文读取本卷108章；未读卷三四不补造前史；证据默认定位至完整章节区间，研究解释不是用户风格规则。',
    major_character_states=[],plot_threads=[],unresolved_and_anomalies=[],transferable_mechanisms=[],literary_tradeoffs=[])

CHARACTER_DATA=[
('shusheng','轻狂书生','155升至182，神谕套与火龙弓已用，苍穹圣器/龙盾有门槛未用；未五转，现实赴杭途中。','壮大雪月、挽回亲密共同生活、继续履约','高等级差、技能冷却、家庭许可、他人的拒绝','书生→凌雪：恋爱与相互战术信赖；→凌月：确认其独立身份；→秦韵：想留却未获归意；→冰兰：仰赖亦亲近','护NPC、转让盟主给月、组织跨会、私藏圣器、以职业资格威胁招募后称玩笑','由能独扛的核心变成公共战役中拖延/补控者，力量增长伴能动性天花板。',[423,428,455,509,518,524,528,530]),
('lingxue','凌雪／清风飞雪','本卷明确172后战役176；后续阵亡/奖励净等级未逐项列，卷末不补算。仍美国，雪羽天马、西西已用。','和书生团聚，护姐护队，证明三人共处可快乐','父亲冻结账户、同享恋爱边界、怪物差级','凌雪→书生：支持并主动承担位移目标眩晕；→姐姐：替挡穿刺','让旧剑珍藏、暗助寻龙、抽筋、复活点救书生','爱情靠行动与技能共同写成，但随父亲返国尚未兑现。',[434,438,469,501,510,518,525,527]),
('lingyue','凌月／清风揽月','重任雪月盟主；战役后在529章明说180；美国未回，地狱火戒腿待等级穿装逐件未叙。','经营雪月、争取爱情中的独立身份、与妹同进退','父亲与经济控制，害怕成为替代品','凌月→书生：要求被当独立者；→雪月成员：指挥/职业组织','拒班长使唤、建云梯、受袭仍愿助人、危机指挥','由经营与火力核心取得明确职务，也保留情感脆弱。',[441,469,506,508,509,512,529]),
('bingcha','冰茶','已转雷霆剑士，白虎之魄、龙龟、雷系控；地狱火靴180/8称号门槛未实穿；现实赴杭同行。','证明战力、维护伙伴与工作室日常','远古套防御偏弱，家庭信息未全揭','冰茶→书生：信任调侃、救场、吻脸；不推导正式恋爱；→凌雪：互让装备','回赠强化石、接秦韵现实空缺、用禁魔/雷晕救援','从输出辅助变扛局核心及现实同行者，私生活仍有未知。',[439,459,463,514,518,527,530]),
('qinyun','秦韵／紫韵儿','线上仍团队主疗，学战神祝福；现实已搬离且拒返；个人最终等级不反推。','爱与自我保护并存，尝试不再思念','主角感情多线、自己不愿接受安排；治疗受等级差压制','秦韵→书生：仍关怀但不等同关系同意；→姐妹/团队：继续合作','不报地址、不吃归家邀，危机反复治疗净化，声明离开是解决','离开真正生效，线上有贡献不消现实缺席。',[450,457,495,501,515,524]),
('linxiang','稻花香／林香','回工作室、腿能走仍恢复期；170为战役前后明确节点，卷末留家不能远行。','属于安全伙伴，帮书生与伙伴作战','现实身体恢复；封印高差目标大多miss','香→书生：信赖称哥哥，救援冒险；书生→香：保护，未写恋爱','首战败受火牢羞辱仍站立、强敌前再封印','软弱身体与强控制能力反差，仍有概率和等级限制。',[440,482,483,510,527,530]),
('ailan','艾兰','失明已治、迁王者之都，白银制甲师并能强化；仍怀念林克。','继续生活与保存林克记忆、学手艺','丧爱不可逆，职业只制甲不造弓','艾兰→书生：由误认林克到称哥哥的信赖，不等血缘','识瓶告别幻想、同意试药、学制甲','从被等待束住的NPC到有职业与回报能力的人，悲伤未被清空。',[426,427,428,435,440,525]),
('linqiu','林丘','240仙白银将领，米拉披风仍穿；战役断一臂和胸伤，卷末活着。','保家园、持续抗亡灵','妻已亡、断臂、首领差级','林丘→米拉：借遗物继续联系；→菲雅：忠诚与保护','绕路回乡面对妻、披遗物赴战、断臂仍战','私人哀恸成为公共承诺，但勇武付身体代价。',[430,433,513,516,528]),
('feya','菲雅','245传说、人类联盟第一军事统帅；战役重伤活，需重建血色；知姐姐安妮黑暗身份。','护白云与联盟、取得前沿堡垒，保存妹妹/姐姐联系','国王内战命令、兵力惨损、控制技与更强首领','菲雅→书生：信任、主动让经验；→安妮：依恋又困惑；→冰兰：尊敬并请守','承认腐败仍动员、焚魂、身先士卒、让杀利文经验、求冰兰不追姐','领袖从发任务者成承担失败与伤害者，胜后私人世界破裂。',[428,498,513,516,518,519,520,528,529]),
('daphne','达芙妮','曾被救、升235、反救主角；截至本卷已被卡伦斩首死亡，未出现复活，系统胜利不抵消此损失。','近卫护菲雅、完成使命','曾受敌围，最终实力差距','达芙妮→菲雅：赴死忠诚；→书生：感激后返救','带箱回城、救火龙险中书生、背刺卡伦','交互回报链截至本卷以真实死亡截断，系统胜利未恢复其生命。',[464,467,514,528]),
('annie','安妮／霜之剑刃','身份为旧人类女王、菲雅姐姐及黑暗军团第二BOSS；杀卡伦后离去。','表层黑暗领袖，明确护菲雅；其余动机未知','受明宇更高权威，黑暗转变原因未揭','安妮→菲雅：禁止任何人杀她；→卡伦：上级威压并灭口','确认军队尽没后杀卡伦，留下敌对宣言','身份揭示完成，阵营与亲情冲突未解决。',[428,511,521,528,529]),
('binglan','冰兰','龙域领袖击退奥丹的战果为本人陈述；留12龙骑守血色，带新人回域。','守龙域、对抗黑暗、培育继承力量','龙域牵制、龙骑阵亡；个人等级/极限未知','冰兰→书生：支持与亲近但牵手惊退；→菲雅：尊重守城需求','主动给血解神谕、允许同行，分配龙骑防务并发五转任务','超越玩家的权威仍有职责与亲密边界，不作万能即时救援。',[453,454,456,528,529,530]),
('suifeng','暗影随风','还凤翔离魂归，入天骄任军团长，拒对雪月PK；末战强制下线后本卷未再叙。','保尊严与行动自由，秉公合作','旧装备恩债、被质疑收买','暗影→血饮：由追随转决裂；→书生：相互认可但拒加盟；→红绫：接受低约束邀','冒死救敌对会、还整套、拒副盟主','不再让装备绑定人格，组织转变未归主角。',[518,521,522,527]),
('hongling','红绫舞','124出场后多次换装；仍魂归一员、替天骄带队挖人，恋/护王俊杰。','护王俊杰与重建天骄','与雪月能力差距，对王真相拒听','红绫→王：维护；→暗影：柔性资源招揽；→魂归：盟友兼挖角者','拒风流恶事仍追王仇，后招暗影','战斗屡败却通过组织关系取得实利，具体背景未揭。',[423,470,471,496,521,522]),
('xueyin','血饮天下','原血饮盟被解散，后魂归高层，失暗影；末战为护妹妹死。','权力、面子、妹妹安全','声誉与人才流失、强敌压制','血饮→暗影：把装备投入当控制债；→小蝶：保护优先','拒公共救援、辱暗影、最终挡卡伦护妹','公共自私与私人爱同时存在，不能洗成全恶或全善。',[423,483,518,521,526]),
('aotian','战魂傲天','魂归盟主，首战国际败、第二预选败；接受联军指挥，关键提前停轮控致灾。','保组织声望与领导权、获公共胜利','部下分裂、指挥执行失误','傲天→血饮/风流：需维护兄弟但逐渐抑冲；→书生：竞争兼临时受指挥','先犹豫救援后接受合作，分近战队却擅改命令','从霸权口气到公共妥协，能力与颜面仍冲突。',[484,498,519,521,522,523]),
('chenai','一粒尘埃','触荣誉/战场系统，曾降级转龙战士；138节点，末战救援死，最终等级未知。','对兄弟会尽责、坦荡竞技','低于核心等级、boss技能抗性','尘埃→同会：护同伴但拒偷袭；→书生：对手兼救援合作','分所见与谎报、拒霸王卑鄙、跨会赴险','用操作与原则支撑替代英雄形象，难度不足时也会死。',[425,426,442,443,480,518,523,527]),
('iceyi','冰之逸','已获神龙祝福，头衔见习龙骑士，公告龙战士；仍无会。','自由游戏并发展职业，检验招募诚意','250级才能骑巨龙；面临强者资源威胁','冰之逸→书生：警惕并拆穿功利保护话术；→流年花火：同行且替她防备','拒绝直接入会，提出杭州请饭面谈条件','奖励不直接兑换忠诚，卷末转现实承诺尚未回收。',[528,529,530]),
('fireflower','流年花火','已获神龙祝福，头衔见习龙骑士，公告龙战士；仍无会，与冰之逸同住杭州。','发展新职业、保持自由，愿见高手本人','250级骑龙门槛；伙伴共同决策','花火→书生：道谢并较倾向加盟，但未发入会同意；→冰之逸：亲近同行并劝其不必太凶','接受顺风龙骑、对午餐见面期待，未独自脱离伙伴','比冰之逸柔和不等没有个人意见，也不等已归主角组织。',[528,529,530])]

CARDS=[]
for key,name,summary,goal,limits,relations,decision,change,chapters in CHARACTER_DATA:
    card=dict(asset_type='character',scope='source-analysis',title=f'卷五人物｜{name}',origin_key=origin('character',key),tags=['作者:失落叶','作品:网游之纵横天下','卷:5','待审阅'],
        content=dict(summary=summary,goals=goal,constraints=limits,relationship_directions=relations,key_decisions=decision,stage_changes=change,claim_kind='synthesis',fact_scope='只概括本卷明确表现，人物动机解释为研究推断；无用户审美'),
        evidence=evidence(*chapters,kind='synthesis'),user_notes='',favorite=False,review_status='draft')
    CARDS.append(card)
    ANALYSIS['major_character_states'].append(dict(character_origin_key=card['origin_key'],name=name,fact=summary,inference=change,evidence=card['evidence']))

SCENE_DATA=[
('old-loyalty','给旧部十秒离场','守住领地并保持新部下忠诚','大剑师面对天骄旧部不忍','书生代做宽免并限定十秒','旧部得退路，剩余被剿','新忠诚不必靠立即弑旧友证明','把领导伦理变成有期限、可执行的让步','转会、旧阵营依恋与新组织规范冲突','若宽免没有战术成本或所有人齐声赞主角，会变廉价收买',[424]),
('moon-bottle','暖月光的承诺','把林克遗物交艾兰并面对死讯','盲女误认、月光不可装、法师索仙剑','告真相，承诺成败都回来，用月草与旧友附魔替代','制成百年光暖瓶，结算后仍迁居照料','任务结束后生活安置继续','先让小礼物确立情感价值，再用问题重构与信用解困','非武力问题、多种专长协作、承诺可追踪','若救助者只是为更大收益投资，会失去非功利余地',[426,427,428]),
('mila','米拉的婚纱与披风','林丘想确认妻子生死','妻变亡灵仍缝婚纱，认知与危险冲突','陪同回乡，危急出剑后听临终表达','米拉死，婚纱/披风成为遗物，林丘继续抗亡灵','奖励无法换回妻子，遗物延续关系','保留未完成家务，死者拥有具体等待而非抽象悲惨','任务成功与私人失败并存','若后续只用大量奖励替代哀悼，悲剧将变刷荣誉素材',[431,432,433,516]),
('taming','不求硬杀改驯雪羽','在魔法仙Boss前带队存活并获益','重甲被克、队友宠物死亡、驯服概率低','催眠回收、绕位冷却，反复一小时驯服','雪羽化仙骑给凌雪，白虎给冰茶；NPC返程仍伤亡','玩家工具获得不抹去任务队伍损失','转换目标从击杀改占有，控制与冷却撑重试','目标可替换且系统允许占有','若无限重试无丢级/队友代价，会消解战斗风险',[436,437,438]),
('craft-affection','绿链到强化信用','弥补强化失败并提升团队','连败五次、原料有限','求艾兰协助，利用亲密与称号提高成功率','强五并批量生产，交订单后材料耗尽','救助关系进入经济系统，不能无限量产','旧善行有制度接口，收益受资源上限','人际信用有可见影响但非万能','若NPC只剩免费工厂，人物关怀会彻底工具化',[427,435,439,440]),
('brotherhood','争怪中的有限证词','完成班长任务并救被杀队友','对方谎报恶意，尘埃仅见后段','先协商、被再袭后打，尘埃承认所见限制','很萌道歉却收班长势力，雪月退盾','武力胜利和组织收益分离','让证人不全知、领袖可道歉又求资源','多方争执、消息来源不同','若一方永远蠢坏且其他人全认可主角，政治张力消失',[441,442,443,444]),
('hell-loop','奥克斯的灭团学习','出七门地狱并取神谕套','禁回城、首领抗性、范围雷击，死亡掉级','以多次灭团测距离仇恨，轮控淬毒重试','多人总损31级后杀首传说，奖励回补，套后续解封','净收益正仍真实经历死亡与时间损失','反馈改变下一次参数而非原地意志更强','有可测规则与合理复位机制','若每败都被大奖全补且无长损，风险趋于仪式化',[445,446,447,448,449,450,451,452]),
('blood-consent','冰兰主动给血','在24小时内以冰兰血解神谕','导师实力高，强取不可能且有关系代价','主角说明求助，冰兰主动划腕于剑','完成血条件，圣疗互助，传承套可用门槛仍165','物品不是打败导师的证明','能力边界与关系许可共同解决武力不可解任务','老师/守护者资源可自愿给而非必须击败','若每次难关都无偿找导师，成长会寄生外援',[453,454,455,456]),
('thunder-escort','回城穿套再追踪归队','保护冰茶十小时转职路最后返城','魂归埋伏、任务不能回城、书生套尚仓','冰茶不杀防红名，书生回城换套用追踪回来担杀','护冰茶成功，后正式转雷霆剑士','早期传送物改变装配与护送的时间限制','让奖励以时空操作而非纯攻防回收','团队有不同限制、空间技能先立规则','若传送无冷却无绑定条件可处处消难，地图压力崩溃',[432,459,460,461,462,463]),
('dwarf','护女官遇见人类罪','护达芙妮与图谱回城','矮人既揭人类奴役又自身害人，主将杀工匠','主角带队守任务，女官承认己方腐败仍为家园战','女官存活、图谱交付；道德问题未因击杀全解','敌我不等善恶一一对应','对立各有可具体追查的伤害，个人选择仍紧迫','阵营战争中避免主角阵营天然无罪','若弱者控诉只铺完即被杀而无后续，会变装饰灰度',[464,465,466,467,468]),
('elf-prison','艾丽反过来提供解法','救半精灵公主和族群','兽人刑杀，地图不熟、伏兵与暴露风险','救艾丽并用其自制弓毒、向导能力，夜拆坐骑光声','放出吉安娜与众族，公主决定建国','受救者主动参与，后建设需训练','求援者带专长而不只是奖赏说明员','营救与文化专长/潜入互助','若受救者所有决策仍由主角包办，互助只是假象',[475,476,477,478,479]),
('missed-match','缺席核心的后备队','赢首轮50人选拔','主角队被黑石任务占，核心输出缺席','后备以远古套坐骑及战术尽力、复活牺牲','决赛败，稻花香受辱，伙伴安慰；后另择再战','败局不是后备无价值，积累不等当下必胜','让长任务占用时间产生机会成本','双线并行且角色有真实日程','若缺席只为制造主角回来即救世，配角尊严被削弱',[480,481,482,483]),
('korea','国际再战的针对准备','赢圆月队并改前周败局','韩法师强、凤凰虚幻、圆月多底牌','抗魔药、双线宠、分工、领域破虚幻，风烈暴击终结','系统中国胜，主角MVP；胜后承认人数与香威慑','全队资源回收，不是单人属性一剑结算','对照旧败局，提前准备针对性工具','再赛有新增策略和可信强敌','国别贬损、旗帜羞辱和性攻击不随有效战术迁移',[496,497,498,502,503,504,505]),
('benevolence','助人遭反咬仍不冷漠','劝低级队伍安全回城','受助者见仙装起贪袭凌月','先给回城卷，遭袭防卫反杀，事后仍称会再帮','五人死，主角团继续赴战','善意经失败压力测试而非只受好报','用具体再次选择检验道德宣言','角色有能力安全维持原则','若人人只为让主角占道德高地而恶，会扁平受助者',[506]),
('bridgehead','云梯与城墙桥头堡','获得更安全输出空间','地面四尾魔法大杀、城墙220弓手','建筑职业搭梯，主角让盟主给月再登墙开点','三人三宠清空地，远程上墙战士守梯口','生产/指挥/前锋各有岗位','空间目标取代无差别杀怪，资源转战术能力','攻城、地点可控且有后勤职业','若城防不随突破反应，桥头堡会成为永久刷怪漏洞',[509,510,511,512]),
('dragon-schedule','第二龙蛇的分秒控制','在一空敌持续屠杀时止损','首头靠盾手送命拖时，另一头仍喷火','分组冲锋、备用眩晕、失败补控、近战打一刀退','第二头十分钟近零损，经验装备让给参战团','组织学习可观察且福利抚恤跟上','同敌对照展示信息和组织的价值','规则允许控链而执行有协调成本','若所有boss都可无脑控满会令后续复制枯燥',[512,513]),
('pheya-delay','守住45秒并付掉级','保菲雅解除龙缚','利文高差碾压、队友控全miss','神谕无敌25秒、尘埃暗影合作，诸人轮流救','菲雅终于斩利文；主角诅咒真掉7，再获转交经验升8','成功是争取他人恢复，不是越级单杀','把胜利条件改为短时保护，人人贡献仍有限','有可计时解控窗口与非玩家决定性能力','若外援永不付代价而全奖给主角，会侵蚀协作可信度',[517,518,519]),
('suifeng-exit','还装备与拒绝最强邀约','暗影保存人格不受收买指控','老大把套装成本变恩债','当众还整套退会，拒雪月后选低约束天骄','天骄得将，附不对雪月PK；魂归失情意技协同','组织资源不等人格所有权','退还资源让价值选择付实物代价','组织忠诚与自由冲突，第三阵营有条件空间','若退会马上无成本换更强套，尊严牺牲会空转',[521,522]),
('fire-dragon','伤口—腐蚀—控链','打死重伤火龙并取材料','厚皮让腐蚀和眩晕都不能生效','三将拖时，魂殇沿剑痕开伤，主角送毒腐蚀','降防后集群控杀接近成功，擅停轮冲又招灾','技能依赖环有具体可突破接口','以跨专长步骤解决免疫，不是临时赠神技','目标防御有可被行动改变的结构','开口是否可定位及维持必须说清，避免万能弱点',[523,524]),
('mouth-counter','被衔入口成为攻击位置','从龙口活下并终结残血龙','被衔空中、25秒无敌后必死','刺眼不放手，在口内升龙与剑刃风暴','火龙死书180，公开分装前暗藏项链','强制近身危机转成极难主动取得的弱点位置','把危险位置与解法位置重合，已有无敌供时间','物理位置与技能效果可因果对接','若危机可随时开无敌离开，绝境名不副实；私藏须独立评价',[524,525]),
('annie-reversal','援军倒计时反成姐妹救援','保最后生存者与菲雅','卡伦近杀，达芙妮已死、安妮援至','安妮先核实部队尽没，卡伦杀菲雅时将其斩首','血色胜、姐姐身份揭开，但女官死和姐姐堕落不解','敌军终结权被私人关系打断','用同一到期事件逆转预期并保留敌方风险','有亲缘前置、秘密无人证可成立','外援若无前置且全面消损，将是机械降神；本例仍有终结权偏外力取舍',[521,527,528,529]),
('recruit-lunch','龙骑招募转现实午餐','招两新职业进雪月','两女厌约束、拒以名气换忠诚','主角先帮交通又威胁职业，冰逸拆穿并提请饭','实际赴杭，卷末未会未入会','下一行动由被招募者条件决定','将系统奖赏转成关系谈判并留下可核验约','招募需要双方价值与现实成本','职业威胁不应被洗成关怀；赴约不能写成招募完成',[529,530])]

for key,title,goal,obstacle,choice,consequence,state_change,why,applicability,failure,chapters in SCENE_DATA:
    CARDS.append(dict(asset_type='scene',scope='source-analysis',title=f'卷五场景｜{title}',origin_key=origin('scene',key),tags=['作者:失落叶','作品:网游之纵横天下','卷:5','待审阅'],content=dict(summary=f'{goal}；{choice}；{consequence}',goal=goal,obstacle=obstacle,choice=choice,consequence=consequence,state_change=state_change,why_it_works=why,applicability=applicability,failure_mode=failure,claim_kind='synthesis'),evidence=evidence(*chapters,kind='synthesis'),user_notes='',favorite=False,review_status='draft'))

PATTERN_DATA=[
('after-reward','任务结算后的生活继续',['moon-bottle','mila','craft-affection'],['先让求助者拥有具体劳动或未完日常','完成系统目标后再做一次无强制奖赏的选择','展示生活改变或持续哀伤','远期可回报也可遭新风险，不把成功设为免死'], '适合任务世界中恢复NPC主体性；需有结算后时间与生活空间','若所有善行必按更大奖兑换，照料会被解读为投资','更换求助关系、问题类型、职业与后果；保留结算后仍作选择的因果，不挪月光瓶、绿链、盲女和亡夫组合'),
('reward-affordance','奖励成为下一难题的动作工具',['thunder-escort','bridgehead','fire-dragon'],['先给出工具规则和限制','制造原战术无法解决的新障碍','把奖励能力嵌入空间、时序或协作步骤','留下冷却、材料或门槛，未来不能无限复用'],'适合长篇装备/法术成长；要让读者记得功能而非属性全文','临时改规则或全能工具替代每个问题会破坏可信度','将传送改为社会通行权/一次性改道等不同资源，保持行动选择变化，不复制物品名和技能链'),
('learn-loop','重复失败中的参数学习',['hell-loop','dragon-schedule'],['首轮暴露规则未知与真实损失','从死亡反馈提取距离、冷却或职责参数','缩写相同失败，只展开新信息','下一轮用备用分工验证修正并保留代价'],'适合可复位但有损失的游戏/试验叙事','反复重试只有口号，或损失必全补，会失真','另设可测变量与不可逆成本，如信誉或窗口，避免复制雷龙门阵和数值'),
('public-coalition','公共失败条件下的暂时联盟',['brotherhood','pheya-delay','suifeng-exit'],['建立所有派别都会承担的失败后果','让各自保有利益、颜面与忠诚障碍','谈定总指挥和专业子队权限','在执行中检验口头团结，按行动分配功劳与责'],'适合多组织危机，需要能清楚计算共同风险','把竞争者全写成蠢坏来衬主角，合作只会成归顺','改共同风险、代表权与授权结构；允许主角让权和被否决，不复制公会人名与国家羞辱'),
('objects-grief','遗物使私人损失跨线持续',['mila','pheya-delay','annie-reversal'],['先赋物件日常用途与双方愿望','不可逆失去后转为携带物','在非哀悼场景中再出现，改变行动或感受','不靠奖励或胜利取消失去'],'适合长篇跨任务保持人物记忆','遗物只被旁白点名，无行为变化会退成标签','换物件来源、关系和感官通道，保留用途转义；不复制婚纱披风和亡灵妻组合'),
('dependent-solution','解除技能依赖环',['fire-dragon','mouth-counter'],['说明必须用A破防却A本身不破防的闭环','引入不同专长B制造有限物理接口','让多人付出时间/位置代价维持接口','A成功后才使团队常规方法可用'],'适合读者熟悉规则后展示创造性解法','若接口临时出现且无位置持续条件，会成万能弱点','更换系统与专长，采用谈判权/证据/工艺等非战斗接口，不移植腐蚀箭和龙口设定'),
('agency-refusal','强者招募遭有价拒绝',['suifeng-exit','recruit-lunch'],['先表明人才与强组织的互需','让候选者提出独立价值和拒绝条件','若恩惠被转成控制，明确其代价并可退还','下一步由候选者选择可核验行动，而非默认加盟'],'适合团队扩张且要保留配角人格','胁迫被叙述成关爱，或一顿饭自动洗掉不平等，会破坏自主性','更换组织、资源与会面门槛；允许拒绝最终成立，不照搬龙骑资格威胁'),
('counter-position','危险位置也是解法位置',['mouth-counter','pheya-delay'],['把人物推到难以主动抵达的位置','已有能力只提供短时生存','从该位置观察新弱点或阻挡关键线路','选择承担后果完成不同胜利条件'],'适合空间清楚、能力有时限的高压场景','无限无敌或新能力突然救场会消解选择','换空间与胜利条件，比如证人席/封闭舱/公开演讲，不复制龙口、护罩、暴击'),
('cost-accounting','胜利账与损失账分开',['mila','missed-match','annie-reversal'],['给系统、组织和个人各自成功标准','逐项记录资源回报与不可逆伤害','让胜利仍改变未来而不抵消死伤','用未完成关系或任务牵向下一阶段'],'适合奖励密集长篇保持情感重量','净经验赚便宣称无损，会把牺牲降为领奖手续','更换评价体系与持久成本；保留多账本不互相抵销，不复制具体奖励数值')]
for key,title,froms,steps,app,fail,transform in PATTERN_DATA:
    derived=[origin('scene',x) for x in froms]
    ev=[]
    for c in CARDS:
        if c['origin_key'] in derived:
            for e in c['evidence']:
                if e not in ev:ev.append(e)
    ev=[dict(e,claim_kind='synthesis') for e in ev]
    CARDS.append(dict(asset_type='pattern',scope='reusable-pattern',title=title,origin_key=origin('pattern',key),tags=['作者:失落叶','作品:网游之纵横天下','卷:5','研究推断','待审阅'],content=dict(summary='；'.join(steps),causal_steps=steps,applicability=app,failure_mode=fail,originality_transform=transform,derived_from_origin_keys=derived,claim_kind='synthesis',not_user_style_rule=True),evidence=ev,user_notes='',favorite=False,review_status='draft'))
    ANALYSIS['transferable_mechanisms'].append(dict(origin_key=origin('pattern',key),title=title,causal_steps=steps,applicability=app,failure_mode=fail,originality_transform=transform,evidence=ev))
dump('cards.json',CARDS)

ANOMALIES=[
('honor-table','荣誉表最高称号括号数据缺项；不能自行填齐。',[426]),
('seal-count','雪羽驯服前封印石余量先多两枚后只剩一枚；后百白虎与另封火狼也有石头总量口径问题。',[437,438,458]),
('pet-duration','地狱中灵儿召唤时长/循环叙述与此前约十分钟时长口径需前卷核验；不是擅造无时限。',[445,446,447]),
('set-duration','神谕结界初始属性与实际使用先后有45秒/25秒差异；实际关键战按25秒记录。',[455,456,518,524]),
('ancient-set','远古套先总十套，冰茶与三元勋发装、后剩七套的分配算术不合；不补造第十一套来源。',[456,457]),
('map-payment','矮人图谱交付数量及每张荣誉、总荣誉算术不合，保留原叙增幅，不重算修正文。',[468]),
('elf-population','半精灵人口先族长述两万损失，后村庄十万口径变化；可能时空口径不同但未解释。',[475,478,479]),
('task-time','黑石长期任务此前72小时与后叙一周有不明时限口径；不能默认为延期机制。',[479,480,495]),
('battle-team','首战对手兄弟会法国/印度文字不一，后实际印度胜；系统荣誉5000与前预告1万口径不一。',[480,484,485,488]),
('npc-loss-rule','血色公告白银骑兵阵亡超50%即败，后写损失90%以上仍继续并胜。兵力先估10万后30万为估测修正可分开，败阈值仍无解释。',[507,513,517,519,528]),
('immune-death','龙魂顶着无敌仍被一剑秒杀；未提供破无敌属性，不能补设。',[527]),
('eligibility','系统龙骑资格称未阵亡普通战士，但孤坟前文明确两次死亡/下线，仍列入名单。',[520,528]),
('job-name','两女头衔见习龙骑士、系统转龙战士；250级骑龙门槛仍在，不等转职即能驾龙。',[529,530]),
('first-soul','卡伦战称破魂效果从未出现，但半精灵双王前已触发短控；数值效果也有情境差，按原文并存。',[477,527]),
('damage-digit','利文空手897638伤后书生仅险些被秒，与其血量量级冲突；保原值不改成89763。',[517]),
('typos','凌雪/月、冰茶/冰兰、技能灵魂星雨/陨石、火龙之匕/弦等局部名误；上下文可记录角色判断但不得改原文。',[496,506,511,525,528,529]),
('bottles-name','清瞳/青瞳泪腺异名；本卷试用结果已复明，原名不统一改写。',[432,435]),
('foreknowledge','早有安妮女性与姐妹名号，末战又集体惊讶霜剑为女性、合并身份，信息记忆衔接粗糙。',[428,511,528]),
('fort-size','血色要塞相对白云城面积先约四倍、后十倍，均主角描写而非正式测量，不合并精确地图。',[498,506]),
('timezone','北京九点姐妹在美国吃晚饭，时差日程未自洽；只记她们尚在国外。',[515])]
ANALYSIS['unresolved_and_anomalies']=[dict(id=key,text=txt,evidence=evidence(*chs),status='unknown',handling='保留两端说法；待跨卷/版本审计，不创设解释') for key,txt,chs in ANOMALIES]
ANALYSIS['literary_tradeoffs']=[
 dict(topic='高频回报的可读性与稀释',fact='套装、称号、强化、驯骑、制造与国战回报密集，频繁被即时用于下一冲突。',inference='满足连载升级期待，但大奖回补31级/7级损失使常规死亡趋程序性；达芙妮之死、林丘断臂与关系缺席承担持久成本。',evidence=evidence(450,451,455,495,519,526,528)),
 dict(topic='玩家能动性与史诗尺度',fact='玩家推动战役、保菲雅和减防，但卡伦最终死于安妮；冰兰抵达在战后。',inference='保强者等级和世界尺度，代价是高潮终结权外置；早期援军预告和身份前置可解释转折，不能自动消除机械解围感。',evidence=evidence(498,517,518,521,527,528)),
 dict(topic='多线亲密与拒绝边界',fact='姐妹当前限制与父亲反对持续；秦韵现实搬离，冰逸拒招却受职业威胁。',inference='文本能写温暖互助和个体脆弱，同时经常用玩笑和男主中心欲望软化拒绝；不将劝服成功或身体接触自动判成平等关系。',evidence=evidence(434,450,469,508,524,530)),
 dict(topic='群像尊严与主角偏袒',fact='尘埃暗影及后备队有贡献，血饮护妹，红绫招将成功；主角对己方与敌会采用不同宽容标准并私藏联军掉落。',inference='阵营内部有差异使群像不全扁平，但主角中心评语常把竞争者贬为笑柄；应保留行为证据和声音之间距离。',evidence=evidence(443,482,483,518,521,524,526)),
 dict(topic='幽默与客体化/偏见',fact='现代品牌、性笑话、外貌/国别贬损及道路骂战密集。',inference='口语轻快可迁移为语域参数，具体羞辱、刻板印象和危险驾驶不应升为用户风格；用户喜好本批留空。',evidence=evidence(501,502,503,520,530))]

ARC_DATA=[('hold-care','守城后：荣誉、遗物与家庭',423,440),('hell','跨会冲突与七门地狱',441,456),('escort','离别、转职与异族代价',457,478),('build-match','建国积累与两次竞技',479,505),('war','血色攻城：从优势到极限',506,527),('reveal-next','亲缘反转与新行程',528,530)]
NODES=[dict(id='v05-story',kind='story',parent_id=None,title='卷五 魂归战袍',claim_kind='fact',summary='108章本卷结构；不是全书结构',evidence=evidence(423,530))]
for key,title,a,b in ARC_DATA:
    NODES.append(dict(id='v05-arc-'+key,kind='arc',parent_id='v05-story',title=title,claim_kind='inference',evidence=evidence(a,b,kind='inference')))
def arc_for(ch):
    return next('v05-arc-'+key for key,_,a,b in ARC_DATA if a<=ch<=b)
SCENE_NODE={}
SCENE_CORE={'old-loyalty':424,'moon-bottle':426,'mila':431,'taming':436,'craft-affection':439,'brotherhood':441,'hell-loop':445,'blood-consent':453,'thunder-escort':459,'dwarf':464,'elf-prison':475,'missed-match':481,'korea':502,'benevolence':506,'bridgehead':509,'dragon-schedule':512,'pheya-delay':517,'suifeng-exit':521,'fire-dragon':523,'mouth-counter':524,'annie-reversal':528,'recruit-lunch':529}
for order,(key,title,goal,ob,choice,conseq,st,why,app,fail,chs) in enumerate(SCENE_DATA,1):
    nid='v05-scene-'+key; SCENE_NODE[key]=nid
    core=SCENE_CORE[key]
    NODES.append(dict(id=nid,kind='scene',parent_id=arc_for(core),title=title,narrative_order=core-422,core_original_chapter=core,claim_kind='fact',summary=f'{choice}；{conseq}',evidence=evidence(*chs),asset_origin_key=origin('scene',key),characters=[],knowledge=[]))
def node(key):return next(x for x in NODES if x['id']==SCENE_NODE[key])
def chars(key,*keys):node(key)['characters']=[origin('character',k) for k in keys]
def know(key,observer,state,belief,chapters):
    node(key)['knowledge'].append(dict(observer='reader' if observer=='reader' else origin('character',observer),state=state,belief=belief,evidence=evidence(*chapters,kind='inference')))
chars('moon-bottle','shusheng','ailan'); chars('mila','linqiu','shusheng','lingxue','lingyue')
chars('blood-consent','binglan','shusheng'); chars('thunder-escort','bingcha','shusheng','lingxue')
chars('dwarf','daphne','shusheng'); chars('missed-match','linxiang','aotian','xueyin')
chars('korea','shusheng','lingxue','lingyue','bingcha','qinyun','linxiang')
chars('bridgehead','lingyue','shusheng','lingxue','bingcha'); chars('pheya-delay','feya','shusheng','suifeng','chenai','bingcha')
chars('suifeng-exit','suifeng','xueyin','hongling','aotian'); chars('fire-dragon','shusheng','aotian','chenai')
chars('mouth-counter','shusheng','qinyun','lingxue'); chars('annie-reversal','annie','feya','daphne','binglan')
chars('recruit-lunch','iceyi','fireflower','bingcha','shusheng','binglan')
know('moon-bottle','ailan','misbelieves','初见误以书生为林克；触瓶与告死讯后更正，不延续到整卷。',[426,427])
know('moon-bottle','reader','knows','书生带死者遗物、正犹豫如何告知；领先艾兰。',[426])
know('craft-affection','ailan','knows','已复明且从事制甲；亲切称哥哥不证明血缘。',[435,440])
know('brotherhood','chenai','knows','只见自己到场后的反击，不能证明同会抢怪前史；他向盟主说明所见。',[442,443,444])
know('brotherhood','shusheng','suspects','兄弟会组织是否故意挑衅，在核问前不能一体归责。',[442,444])
know('mouth-counter','reader','knows','书生在公开分装前空中私藏项链，联军未公开知晓。',[524])
know('mouth-counter','lingxue','knows','随后获书生私下展示苍穹项链属性；不能扩散给全部队友。',[525])
know('annie-reversal','reader','knows','霜剑即安妮旧女王且护菲雅；黑暗转变原因未知。',[528])
know('annie-reversal','feya','suspects','以姐姐呼唤安妮，依恋并困惑；未得到她口头承认或转变解释。',[528])
know('annie-reversal','binglan','knows','战后听人告知霜剑来过，欲追；她此前不在战场，不能写成目睹杀卡伦。',[529])
know('recruit-lunch','iceyi','suspects','书生与冰兰关系能影响职业资格；只因威胁与导师回应形成判断，取消资格未被实际验证。',[530])

EDGES=[]
def edge(key,fr,to,kind,label,chs):
    EDGES.append(dict(id='v05-e-'+key,from_=SCENE_NODE[fr],to=SCENE_NODE[to],kind=kind,label=label,claim_kind='inference',evidence=evidence(*chs,kind='inference')))
edge('care-craft','moon-bottle','craft-affection','payoff','持续照料形成制甲/强化信用，但仍受材料限制',[427,435,439,440])
edge('grief-war','mila','annie-reversal','echo','披风贯穿战争，胜利仍有不可逆死亡；不是同一任务直接因果',[433,516,528])
edge('gear-escort','hell-loop','thunder-escort','payoff','神谕取得后在护送途中回城装备并传回',[451,455,460,461])
edge('blood-use','blood-consent','thunder-escort','cause','解封套装达到门槛，成为后续护送抗击打条件',[455,460,461])
edge('save-return','dwarf','pheya-delay','payoff','前救女官后由她救书生，再护菲雅；回报不保证女官免死',[467,514,517,528])
edge('elf-long','elf-prison','missed-match','cause','训练建设占住核心队时间，首场后备上阵',[479,480,481])
edge('failed-rematch','missed-match','korea','reversal','核心与长期技能回归后再预选并国际获胜',[483,495,498,505])
edge('pet-wall','taming','bridgehead','payoff','驯宠与升阶群法成为攻城桥头堡输出资源',[438,440,510])
edge('space-air','bridgehead','dragon-schedule','reversal','城高安全被空中龙蛇拆解，转为千人组织控制',[511,512])
edge('defense-timer','dragon-schedule','pheya-delay','setup','可控准Boss到不可控传说，目标从杀死改拖解缚时间',[512,517,518])
edge('public-split','pheya-delay','suifeng-exit','cause','暗影冒死公共救援和领袖私利差异，随后收买指控引退会',[518,519,521])
edge('cross-skill','suifeng-exit','fire-dragon','setup','退会不切断共同危机义务，跨会情意技仍可协作',[521,522,524])
edge('hole-control','fire-dragon','mouth-counter','reversal','轮控已成却误令停止，火龙再飞导致口中搏命',[523,524])
edge('manufacture-gap','mouth-counter','annie-reversal','setup','火龙筋促新弓制成、再战有效；仍无法由玩家终结卡伦',[525,526,527,528])
edge('private-reveal','pheya-delay','annie-reversal','reveal','菲雅须存活，安妮来援改杀己将保护她，揭姐妹身份',[517,521,528])
edge('war-next','annie-reversal','recruit-lunch','cause','龙域损失引新骑资格，转职奖励引发下卷现实招募',[528,529,530])
for e in EDGES:e['from']=e.pop('from_')

THREAD_DATA=[
('power','力量、组织与任务回报链','main','partial',['old-loyalty','moon-bottle','taming','craft-affection','hell-loop','blood-consent','thunder-escort','korea','bridgehead','fire-dragon','mouth-counter','annie-reversal','recruit-lunch'],['care-craft','gear-escort','blood-use','pet-wall','manufacture-gap','war-next'],'本卷神谕、雷霆、火龙弓、国战与血色已完成；五转、200级装备和新人入会未完成。',[455,463,505,526,528,529,530]),
('moon','艾兰的月光与生活','subplot','resolved',['moon-bottle','craft-affection'],['care-craft'],'装暖月光、迁居、复明和就业均有本卷兑现；林克之死没有复原，仅此限定目标闭合。',[428,435,440]),
('mila','米拉的等待与遗物','subplot','resolved',['mila'],[],'林丘见妻、妻死、披风承接誓言；见面目标收束而悲伤继续，不写成婚姻修复。',[433,516]),
('escort','冰茶雷霆转职','subplot','resolved',['blood-consent','thunder-escort'],['blood-use'],'护送后正式系统转职；称号声望损失尚在，但转职目标已结。',[463]),
('selection','竞技败局与国际再战','subplot','resolved',['missed-match','korea'],['failed-rematch'],'首轮败与后继选拔/国际胜均有结算；不等父亲已准返国。',[483,498,505]),
('fort','血色战役','main','resolved',['bridgehead','dragon-schedule','pheya-delay','fire-dragon','mouth-counter','annie-reversal'],['space-air','defense-timer','hole-control','manufacture-gap','private-reveal'],'系统确认胜与12%城防/NPC5级；卡伦死于安妮，女官死和军损不抵消。',[528]),
('annie','安妮的人类与黑暗身份','hidden','partial',['moon-bottle','pheya-delay','annie-reversal'],['private-reveal'],'身份和护妹行动已揭，堕落原因、与明宇关系和将来姐妹冲突仍开。',[428,528,529]),
('family','姐妹、父亲与秦韵的关系边界','subplot','open',['korea','mouth-counter','recruit-lunch'],[],'第二国战胜没有在本卷转成父亲明确许可；姐妹仍美、秦韵仍离居。',[469,495,505,515,524,530]),
('factions','暗影独立与魂归内裂','subplot','partial',['brotherhood','pheya-delay','suifeng-exit','fire-dragon'],['public-split','cross-skill'],'暗影退会加入天骄已成；对雪月不战条件明确，主角未来招揽尚期望。',[521,522]),
('new-riders','龙骑新人招募与杭州面谈','subplot','open',['annie-reversal','recruit-lunch'],['war-next'],'两女已转，未入会；书生冰茶在赴杭路，午餐未发生。',[528,529,530]),
('binglan','龙域受袭与导师亲近','hidden','partial',['blood-consent','annie-reversal','recruit-lunch'],[],'导师自述击退奥丹，具体12圣龙等仅卡伦说法；牵手惊退动机未揭。',[527,528,529]),
('ice-family','冰茶的家庭与赠靴对象','hidden','open',['taming','recruit-lunch'],[],'地狱火靴旁显生活费富裕，父卖电器为其说法；幽色靴转赠谁仍未知。',[508,514,530])]
THREADS=[]
for key,title,kind,status,nks,eks,note,chs in THREAD_DATA:
    THREADS.append(dict(id='v05-t-'+key,title=title,kind=kind,status=status,node_ids=[SCENE_NODE[k] for k in nks],edge_ids=['v05-e-'+k for k in eks],resolution_note=note,evidence=evidence(*chs)))
    ANALYSIS['plot_threads'].append(dict(id='v05-t-'+key,title=title,kind=kind,status=status,fact_status=note,evidence=evidence(*chs)))
GRAPH=dict(title='卷五 魂归战袍｜阶段树、因果边与认知差（待审阅）',review_status='draft',coverage=[dict(source_id=SID,revision=REV,chapter_ids=IDS,complete=False,scope='本卷108章完整覆盖，非全书')],nodes=NODES,edges=EDGES,threads=THREADS)
dump('graph.json',GRAPH)
for item in ANALYSIS['literary_tradeoffs']:
    item['evidence']=[dict(e,claim_kind='synthesis') for e in item['evidence']]
dump('analysis.json',ANALYSIS)

state=json.loads((BASE/'reader-state.json').read_text(encoding='utf-8'))
state.update(status='draft-artifacts-complete',review_status='draft',reader='/root/zongheng_vol05_full',currently_reading=None,artifacts=['read-log.json','chapter-notes.jsonl','analysis.json','cards.json','graph.json','report.md','handoff.md'],current_state=[x['state_changes'] for x in NOTES[-4:]],complete_book=False)
dump('reader-state.json',state)
print(json.dumps(dict(chapters=len(IDS),cards=dict(collections.Counter(x['asset_type'] for x in CARDS)),observations={k:len(v) for k,v in DIMENSIONS.items()},graph_nodes=len(NODES),graph_edges=len(EDGES),threads=len(THREADS)),ensure_ascii=False))
