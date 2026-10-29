"""只读分卷成果形成全书九维派生草稿，不声称整合者个人重读全书。"""
import json,pathlib,hashlib,collections,sys,re,functools
sys.stdout.reconfigure(encoding='utf-8')
B=pathlib.Path(__file__).resolve().parent
ROOT=B.parents[3]
FORMAL=ROOT/'writing-vault/library/reports/zongheng-tianxia'
S=json.loads((B/'source.json').read_text(encoding='utf-8'))
SID=S['source_id'];REV=S['revision']
CH={c['chapter_id']:c for c in S['chapters']}
DIM_NAMES={'worldbuilding':'世界观','characters':'人物设计','plot':'情节组织','style':'文风','narrative':'叙事','dialogue':'对话','pacing':'节奏','themes':'主题','continuity':'连续性与证据'}
UP={};DOC=[];LOGS=[];CARD_COUNTS=[]
for v in range(1,9):
 # 正式版已存在即优先，避免引用冻结前已经被审修的旧草稿。
 p=FORMAL/f'vol{v:02d}-analysis.json'
 if not p.exists():p=B/f'vol{v:02d}/analysis.json'
 a=json.loads(p.read_text(encoding='utf-8'));assert a['source_id']==SID and a['revision']==REV
 UP[v]=a
 log=FORMAL/f'vol{v:02d}-read-log.json'
 if not log.exists():log=B/f'vol{v:02d}/read-log.json'
 l=json.loads(log.read_text(encoding='utf-8')); assert all(c['full_text_read'] for c in l['chapters'])
 LOGS.append((v,l))
 report=FORMAL/f'vol{v:02d}.md'
 if not report.exists():report=B/f'vol{v:02d}/report.md'
 hand=FORMAL/f'vol{v:02d}-handoff.md'
 if not hand.exists():hand=B/f'vol{v:02d}/handoff.md'
 docs=[]
 for kind,fp in [('analysis',p),('read-log',log),('report',report),('handoff',hand)]:
  docs.append(dict(kind=kind,path=fp.relative_to(ROOT).as_posix(),exists=fp.exists(),sha256=hashlib.sha256(fp.read_bytes()).hexdigest() if fp.exists() else None))
 DOC.append(dict(volume=v,documents=docs,read_record_count=len(l['chapters']),read_first=l['chapters'][0]['chapter_id'],read_last=l['chapters'][-1]['chapter_id']))
 cp=FORMAL/f'vol{v:02d}-cards.json'
 if not cp.exists():cp=B/f'vol{v:02d}/cards.json'
 cs=json.loads(cp.read_text(encoding='utf-8'));cs=cs['cards'] if isinstance(cs,dict) else cs
 CARD_COUNTS.append(dict(volume=v,counts=dict(collections.Counter(x['asset_type'] for x in cs)),count=len(cs),document=cp.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(cp.read_bytes()).hexdigest()))

def original_obs(v,d,i):
 x=UP[v]['dimensions'][d]
 x=x if isinstance(x,list) else x['observations']
 return x[i]
def textof(x):
 if isinstance(x,str):return x
 if isinstance(x,dict):return x.get('text',x.get('statement',x.get('claim','')))
 return ''
def reported(x):
 f=x.get('fact',x.get('claim',x.get('statement','')))
 return textof(f), (f.get('claim_kind','fact') if isinstance(f,dict) else ('fact' if 'fact' in x else x.get('claim_kind','inference')))
def source_ev(x):
 if 'fact_evidence' in x:return x['fact_evidence']
 if isinstance(x.get('fact'),dict) and x['fact'].get('evidence'):return x['fact']['evidence']
 return x['evidence']
def ref(v,d,i):return (v,d,i)
T=[]
def add(d,k,title,claim,refs,mechanism,limits,transform):T.append((d,k,title,claim,refs,mechanism,limits,transform))

add('worldbuilding','gated-power','把强大拆成取得、资格与使用',
 '早期装备等级/鉴定，中期声望购店与仙宠经验成本，后期圣域/天域及北冥等级门槛，反复让已获得的财富或力量暂不能直接使用。升级的有效意义是改变可选行动，而不只是把数字放大。',
 [ref(1,'worldbuilding',1),ref(3,'worldbuilding',0),ref(4,'worldbuilding',0),ref(6,'worldbuilding',1),ref(8,'worldbuilding',0)],
 '给获得即时回报→另列真正使用条件→角色选择付成本或另找方法→后来确实使用/被拒一次。',
 '资格有越级或临时改口的源疑；已使用是发生事实，不能反推缺失条件一定被合理补足。不要一概把所有限制都说成严密游戏引擎。',
 '在原创题材中重设资格与成本来源，例如信誉、维护、法律或资源约束，避免照搬等级、职业及装备组合。')
add('worldbuilding','resource-maintenance','资源从生计转成组织维护',
 '早期药费与兑币牵动房租，中期声望进入商业资格、领地变收费与分配制度，后期城池补给和龙域账单构成持续责任。经济越来越重要的部分是维护谁的生活，而不是估值越来越高。',
 [ref(1,'worldbuilding',0),ref(2,'worldbuilding',1),ref(3,'worldbuilding',0),ref(4,'worldbuilding',3),ref(7,'worldbuilding',1),ref(8,'worldbuilding',3)],
 '战果转资源→资源换组织能力→组织产生持续开支→开支反过来迫使分工和选择。',
 '估价、营业额、净利、账户、借贷、代付和实际到账必须分栏；小说巨额收入的作者说明不是现实经济证据。',
 '另设可验证的资源流和受益者，给普通成员的成本以场景，不保留原作天价与公司名。')
add('worldbuilding','territory-process','空间资产需要持有、治理与再防守',
 '领地从令牌和计时，发展到资源劳力、传送、积分仓、分阶段攻守及灾后重建。破墙、杀王、民心、名义城主、系统归属和实际交通是不同状态；后期大力量甚至会造坑、毁路而要求别人补完。',
 [ref(4,'worldbuilding',1),ref(6,'worldbuilding',3),ref(7,'worldbuilding',3),ref(8,'worldbuilding',2)],
 '先建完成层级→每次胜利只改一层→新层带维护与反攻→最终主权独立结算。',
 '同类城战有不同阶段规则，不宜归为全世界固定一套公式；毁城尤其不等主角占领。',
 '可改造为船队、城镇、研究设施或政治联盟，重建持有责任和交通条件。')
add('worldbuilding','rules-as-obstacles','旧强招要遇到具体而可读的反例',
 '早期从群拉改单体，中期控场、地形、复活受益间隔，后期魔免、禁骑禁组、资源判定与天域对象差异，持续阻止一个最强技能解释全部胜负。',
 [ref(1,'worldbuilding',2),ref(2,'worldbuilding',2),ref(4,'worldbuilding',2),ref(6,'plot',2),ref(7,'worldbuilding',2),ref(8,'worldbuilding',1)],
 '先示强与用途→用不同约束使其失效→让已有其他专长介入→新解法保留边界。',
 '100%箭被纯变速躲、五人绑定后换队等未解释冲突不能美化成反例教学；特殊75%战后军力恢复也须明确写为奖励例外。',
 '重设约束组合和失败原因，别复制同一技能名、控场链和胜负顺序。')

add('characters','power-and-responsibility','能力增长也扩大了能伤害他人的权力',
 '书生从受同伴支援的谋生者，变为补偿组织失误、主持分配和领地战争的领袖，最终接无法轻易拒绝的职责。护短与真切照料一直存在，私藏、强制、报复及自我辩护也随权力扩大；不宜整理成无瑕英雄。',
 [ref(1,'characters',0),ref(3,'characters',0),ref(4,'characters',0),ref(5,'characters',0),ref(7,'characters',0),ref(8,'characters',0)],
 '受助→兑现回报→承担管理错误→掌更大权→让被影响者或后果质询权力。',
 '这是人物设计的跨期结构解释，不替代独立人物弧台账，也不把胜利当伦理证明。',
 '为原创主人公另设利益、错误与问责者，让同一优点在不同权力规模下显出阴影。')
add('characters','distributed-competence','用任务适配分配群像价值',
 '凌雪的提案与救援、秦韵幕后劳动/反弹、香的高血控场、雨夏保装与紫月换队/争出场，显示强弱依任务而变。后期经营、审合同、工匠药商与NPC也参与共同体运作，主角不能替所有角色工作。',
 [ref(2,'characters',1),ref(3,'characters',1),ref(3,'characters',3),ref(4,'characters',3),ref(6,'themes',3),ref(7,'themes',0),ref(8,'characters',1)],
 '先给不足与独立需要→环境改任务→已有专长变关键→贡献有可见结果与承认。',
 '承认仍常经男主视角，受赠和被救本身不等自主；不能只让配角付出身体/死亡去启蒙主人公。',
 '给角色能拒绝的职责、休息和不依主角存在的目标，改写工作分工与贡献形式。')
add('characters','agency-in-relationships','亲近、同住与正式承诺必须分速推进',
 '关系常由馈赠、照料、搬入、离开、返归和拒绝推进；姐妹外貌相同却有不同记忆和决定。后期再聚也没有自动完成所有身份协议。研究应记录行动与标签各自的时点，而非从温情倒推全员同意。',
 [ref(1,'characters',1),ref(2,'dialogue',1),ref(3,'dialogue',2),ref(4,'characters',2),ref(5,'dialogue',3),ref(6,'continuity',5),ref(7,'dialogue',1),ref(8,'dialogue',0)],
 '具体亲密动作→索要定义/提出限制→对方答复或回避→行为后果继续检验承诺范围。',
 '醉后带回与后来同意分开；身体接触、长辈同意、单方愿望不能代替每位当事人同意。',
 '原创时改变人物关系结构并明确互相承诺，避免复刻姐妹/多角配置和相同暧昧节点。')
add('characters','opponents-with-ties','对手的尊严、旧恩与家园使阵营可移动',
 '亡灵可助战，敌会成员会公共救援，人才会拒主角，旧部有重建目标，反派转向须经事件与选择。阵营标签不能独自解释行动；仍需保留欺瞒、羞辱和犯罪报道的来源边界。',
 [ref(3,'worldbuilding',3),ref(5,'characters',3),ref(6,'characters',4),ref(7,'characters',2),ref(7,'characters',3),ref(8,'characters',2)],
 '给予独立承诺→让其与组织命令冲突→作有代价的选择→新归属不自动清掉旧债。',
 '救赎不等无罪，主角的敌意也不能单独否定对手所有合理需求；不以晚来自述倒灌早章全知。',
 '重建不同承诺网络与可支付代价，不复制投名、特定背叛或原反派转善路线。')

add('plot','nested-resources','长线靠成果转用途，而非相似事件相邻',
 '卷初现金与赠物改变现实/战术，重练到建会买店，任务奖再投领地、副本、竞技、国战，后期材料、证与装备回到终战。明确物件和决定的转运，是长篇连续性的主要连接。',
 [ref(1,'plot',0),ref(1,'plot',2),ref(3,'plot',0),ref(4,'plot',0),ref(5,'plot',1),ref(8,'plot',0)],
 '本段收益必须改变下一段的可选方法、资格或责任，关键转移写一次可见行动。',
 '共同主题、相似掉物、先后出现都不够证明因果；没有后用证据的库存仍保库存。',
 '设计自有资源依赖图，换掉物品/职业/任务组合，保留转换逻辑。')
add('plot','multiple-ledgers','胜利、回滚与私人愿望各自结算',
 '早期杀王得物却任务失败，转职成功却归零，中期守胜与关系伤口并存；75%NPC军力奖励是真实回滚例外；终战任务成功却导师封冻。成功不是统一字段，失去也不必全部不可逆。',
 [ref(1,'continuity',1),ref(2,'plot',2),ref(4,'plot',1),ref(6,'plot',1),ref(7,'continuity',2),ref(8,'plot',1)],
 '分别列制度目标、存活/物品、关系/愿望、补偿与未恢复部分，在实际结算时各自更新。',
 '不能用NPC战时全灭宣战后全部永久损，也不能因部分恢复回写全程无损；系统陨落与在场生命有时不同通道。',
 '给原创世界自己的损失与恢复权限，不照搬归零、永久毁技能或封冻组合。')
add('plot','failure-to-reframing','失败更有用时会改变问题本身',
 '鬼将柱战成功后寒冰王削柱，阿瓦隆堵门也被冲开，国战从制空失败改水攻/拆塔，后期耗胜与填坑说明蛮力之外还有胜利指标。升级不必靠永远新增更大招。',
 [ref(3,'plot',1),ref(6,'plot',2),ref(6,'pacing',1),ref(7,'plot',1),ref(8,'worldbuilding',1),ref(8,'worldbuilding',2)],
 '保留失败信息→改目标或条件→跨用已知工具→让新选择承担代价。',
 '偶然安全位和导师外力能救场但削弱自力解题；不能事后伪造主角预知。',
 '以不同媒介和能力重新设计问题，不复刻柱战、水淹、诅咒和同一填坑步骤。')
add('plot','bounded-ending','阶段可闭合，世界不必终止',
 '前几卷末多留任务/战场未结，后期跨线结算也会再开新资格与责任。最终结束的是主人公征服阶段与工作室阶段，仍保世界竞争、重要缺席和未确定协议；终点不等全部线程resolved。',
 [ref(1,'plot',3),ref(3,'plot',3),ref(4,'plot',3),ref(6,'plot',4),ref(7,'pacing',3),ref(8,'plot',3)],
 '完成本阶段明确目标→清点真实改变→保留有边界的延期或未知→给人物生活重心变化。',
 '开放结局不能作为漏结算借口；人物终点与问题池由独立卷八读者/主代理核对，本综合不替其结案。',
 '为原创故事确定什么阶段确实结束，以新生活行为而非消灭一切矛盾收束。')

add('style','panel-reaction','数值块与口语反应形成稳定双语域',
 '各卷都让装备、公告和伤害后接自嘲、估价、惊叹、分配或新动作：清单给确定性，群体反应把强度翻成地位。它是可配置表现手段，不是独有台词库。',
 [ref(1,'style',1),ref(3,'style',0),ref(4,'style',0),ref(6,'style',0),ref(7,'style',0),ref(8,'style',0)],
 '展示会用的数值→立即给情感/社交解释→下场验证用途。',
 '未量化统计句长或比例；极品、巨额和惊叹连续过密会通胀，不能把任意面板堆砌当可读性。',
 '数值密度中高、惊叹中低、用途反馈高；更换叙述声音和评价词，不模仿口头禅。')
add('style','sentence-distance','短击打与长概述按决策密度切换',
 '近景战斗用短动作、拟声、技能与数字颗粒推进，稳定重复用时间概述，群战又借规模数字拉远。相同速度写所有场合，会抹平情绪和决策。',
 [ref(1,'style',3),ref(2,'style',0),ref(4,'pacing',0),ref(5,'style',2),ref(6,'style',1),ref(8,'pacing',0)],
 '靠近动作时拆细单次反馈，方案稳定后拉远，首次失效再回近景。',
 '这是操作描述，不宣称全书有未经统计的平均句长、短段比例或固定段落公式。',
 '将可调项设为动作颗粒、反馈延迟和概述跨度，按原创场景压力选择。')
add('style','objects-change-function','抒情依靠同一物件改变用途',
 '馈赠、死者遗物、手冷端菜、茶杯包子洗碗，到末段龙域账单，普通物能从用途转为关系、缺席或责任。情感重量来自先前共同行动，不只形容词和誓言。',
 [ref(1,'plot',2),ref(4,'style',2),ref(4,'style',3),ref(5,'themes',0),ref(6,'themes',4),ref(8,'style',3)],
 '先写普通用途→让人物共同使用/承诺→情境改变→同物产生新责任或失去的触感。',
 '艾兰复明就业与林克、米拉、达芙妮死亡分别记录；后者终态以独立审计为准，不能凭相似意象自动算回收。',
 '选择自有生活习惯与物件，重建共同经历，避免保留同样洗碗/账单/遗物组合和句式。')
add('style','humor-with-limits','轻快声音的收益与贬损成本同时可见',
 '粗口、缩写、谐音、现代类比和现实游戏化持续统一职业玩家声音，强威胁后降格笑料也能减压。但女体凝视、性别与国籍概括、危险行为笑谈经常压缩他人的主体性。',
 [ref(1,'style',0),ref(1,'style',2),ref(3,'style',1),ref(3,'style',2),ref(5,'style',3),ref(7,'style',2),ref(8,'style',1)],
 '保语域落差与自我拆台，让笑点对准困境和误判，而非固定弱者。',
 '不能从文本频繁出现推定用户喜好，也不能用“幽默”免除对场景庄严和角色尊重的影响。',
 '口语高、自嘲中高、身体凝视低、群体贬损不用；由原创角色经历生成自己的幽默资源。')

add('narrative','mediated-panorama','限知第一人称用媒介取得远景',
 '书生内心是主聚焦，榜单、系统、录像、频道、电话和论坛连接他未在场的世界；另有少量第三人称密谋、同伴独处与战场切面。范围扩大不等主角同步知道一切。',
 [ref(1,'narrative',1),ref(2,'narrative',0),ref(4,'narrative',0),ref(5,'narrative',2),ref(7,'narrative',0),ref(8,'narrative',0)],
 '每条远景写清获得媒介、发布者、时间与接受者，焦点外场面只增加读者知识。',
 '系统公告也只确认对应目标，不能覆盖在场人物生命/实际主权；匿名或敌方战报不自动独立确证。',
 '选择原创作品可用的信息网络，并为延迟、误报与保密设成本。')
add('narrative','knowledge-gaps','认知差分别服务喜剧、悲悯与策略',
 '身份误认、敌以为主角死、魂殇和林克的误认、私藏战利品、善意虚报净化希望等，让读者与不同人物处在不同位置。认知差的功能取决于谁受损、谁能行动。',
 [ref(1,'narrative',2),ref(2,'narrative',1),ref(3,'narrative',1),ref(4,'narrative',1),ref(5,'continuity',1),ref(8,'narrative',1)],
 '同时记录可知事实/角色信念/读者领先来源，让揭示真实改变选择或感情。',
 '不能将研究者已知等于所有人物已知；善意说法和实际成功不证明此前概率真实。',
 '重设每位观察者的利益与可见范围，不复制姐妹误认或具体假概率揭密。')
add('narrative','belief-correction','自信的叙述需要允许被纠正',
 '品阶误判、领域解释、雪被埋认死、冰病猜测、秦同居误会、女娲满血错觉等说明观察、情绪与成因分属不同层。新证据更新当前状态，不能覆盖先前真实无知。',
 [ref(2,'narrative',2),ref(5,'narrative',1),ref(6,'narrative',1),ref(6,'narrative',3),ref(7,'narrative',1),ref(8,'narrative',2)],
 '先保可见现象→标角色猜因→给独立新证→只更新获得新证之后。',
 '不把不可靠概括成一直说谎；有些是知识不足，有些是自利辩护，有些源文确有矛盾。',
 '为原创叙述者设计具体盲点与纠错证据，避免用同样假死/疾病作为捷径。')
add('narrative','time-and-reveal','回忆、前瞻与当前动作分别排序',
 '开篇先果后因，亡姐信息分层回忆，人物未来成长偶有预叙，卷七印刷错序夹回叙，结尾跳时压缩结果。叙述顺序、事件时序和证据最早铺垫不是同一个顺序。',
 [ref(1,'narrative',0),ref(3,'narrative',2),ref(3,'narrative',3),ref(6,'narrative',4),ref(7,'continuity',0),ref(8,'pacing',2)],
 '为当前事件定首次实际展开点，回忆/预告另标时间关系，不把前瞻写成当前成就。',
 '时间手法能制造期待，也可能掩盖不清时间账；不能为了图连续而重排源顺序或合并不同分片。',
 '用原创人物的记忆缺口与未来代价决定揭示时点，不照搬亡姐片影与相同章末。')

add('dialogue','negotiation','报价、拒收与分权使关系可执行',
 '早期赠物/还钱争清账，中期战利品按贡献喜好谈判，后期人才拒绝迫使分盟、工资、权位与补偿条款变化。好对话留下谁得到什么、欠什么、还有什么可拒绝。',
 [ref(1,'dialogue',1),ref(2,'dialogue',1),ref(4,'dialogue',0),ref(6,'dialogue',1),ref(7,'dialogue',2),ref(7,'dialogue',3)],
 '提出资源/身份方案→对方指出不能接受项→改实质条款→用交付或行动验证。',
 '口头同意、实际付钱、转会、迁移分别记；拒收不是必然谦虚，也不只是抬价。',
 '在原创关系中重新设计交换物与不愿交换的价值，不复刻神弓买人或同样赠戒。')
add('dialogue','command-as-action','命令与约定能直接改变战局',
 '佯恐诱敌、让全队停手睡宠、轮控数秒、分路拆塔、引捕接力和等待NPC计划，都让短句成为行动条件；错误停控或武器约定被利用也有可见后果。',
 [ref(3,'dialogue',0),ref(3,'dialogue',3),ref(5,'dialogue',2),ref(6,'dialogue',2),ref(8,'dialogue',2)],
 '给谁/何时/何种条件/失败后谁补位，不只喊冲或事后解释聪明。',
 '违约胜并不自动值得赞扬；对手也须有理解与回应能力，不能靠旁白剥夺其已知信息。',
 '用原创协作任务生成简短可执行语言，重设失败备用方案。')
add('dialogue','refusal-and-subtext','回避可以延迟承诺，但拒绝须有后果',
 '不报住址、不同意标签、转移话题、拒陪床、只养不包、拒正式盟等，通过具体生活或组织行为限制主角。私下洗碗愿望与诀别托责又以未尽话表达关系需要。',
 [ref(3,'dialogue',2),ref(4,'dialogue',1),ref(5,'dialogue',1),ref(6,'dialogue',3),ref(6,'dialogue',4),ref(7,'dialogue',1),ref(8,'dialogue',3)],
 '表层话题与实际需要分开→角色答应有限范围→下一行动尊重或暴露未被尊重的边界。',
 '调情、身体接触、后来返回都不自动推翻此前拒绝；原696愿伴秦/拒留书须记主宾。',
 '用原创人物的特殊生活与话语习惯写潜台词，避免编一套万能暧昧句。')
add('dialogue','dissent','同伴异议检验主角的自我说明',
 '父亲狼道与拒赌，夏天问是否因无用被舍，月质疑随风偿恩，秦质问杀戮与复仇短暂，香最终亲口拒形式孝道，都提供不由主角包办的价值声音。',
 [ref(3,'dialogue',1),ref(6,'dialogue',0),ref(6,'themes',1),ref(7,'dialogue',0),ref(8,'dialogue',1)],
 '给异议者具体损失/替代方案→主角回应或回避→保留采纳与否的结果。',
 '出现异议不等作者已批判或解决问题；若异议之后不改变任何行为，可能只是装饰性自省。',
 '为原创反对者保有自主行动与后果，不让其只作提问后被说服的工具。')

add('pacing','variation-density','重复稳定后压缩，方法改变时展开',
 '练级数小时常概述，首次规则验证、失控、返尸、分配和新解法细写；从早期古刹到古龟、阿瓦隆、后期女娲与赛事，此分配持续成立。感知速度依新增决策，不依故事经过时长。',
 [ref(1,'pacing',1),ref(2,'pacing',0),ref(4,'pacing',0),ref(6,'pacing',0),ref(7,'pacing',1),ref(8,'pacing',0)],
 '先让读者学会循环→压缩稳定执行→在失效/不可逆变化处恢复现场。',
 '不得编造全文时长或句长统计；每一场都先败后胜也会模板化。',
 '给原创重复任务不同的失效变量，按决策差安排篇幅。')
add('pacing','breathers','日常段在结算另一种状态',
 '吃饭睡觉、修理转账、带练补偿、现实谈判、创业与迁居、最终再聚，接住战果的人际与经济后果。现实也会中断游戏：停练、灾难、病情和公司责任使两边不能任意兼顾。',
 [ref(1,'pacing',2),ref(2,'pacing',1),ref(3,'pacing',1),ref(4,'pacing',2),ref(6,'pacing',3),ref(7,'themes',2),ref(8,'pacing',3)],
 '高压结果→低动作场兑现或改变承诺→现实约束反馈下个行动。',
 '并非所有吃饭闲聊都有效；须有状态改变，照料也不应被固定给同一性别或弱角。',
 '安排原创角色自己的工作和休息需求，让缓冲有不同参与者与代价。')
add('pacing','rotating-horizons','章末悬念轮换目标层级',
 '怪物异变、奖励待揭、交付受阻、身份未明、伙伴去向、近满级中断与新本入场不断轮换，较少只重复能否击杀。个人、组织、国家空间交替换主目标，旧资源和关系保持连续。',
 [ref(1,'pacing',0),ref(2,'pacing',2),ref(3,'pacing',2),ref(4,'pacing',1),ref(6,'pacing',4),ref(7,'plot',0)],
 '完成一个短闭环→揭其未解决的另一条件→切入不同类型可行动问题。',
 '不以未揭标题/预感当已完成；连续只隐瞒结果而无新行动会成为拖延。',
 '为原创长篇设计不同尺度目标和信息缺口，不复制相同奖励/假死切章点。')
add('pacing','long-tail','结尾的代价也要获得时间',
 '中段情感出走分次拒返/南归，赛事强局逐回合试错；终战反转依次消耗工具并改变目标，随后一月与半年跳时让就业、组织衰退和再聚显出长期后果。',
 [ref(6,'pacing',2),ref(7,'pacing',2),ref(7,'pacing',3),ref(8,'pacing',1),ref(8,'pacing',2)],
 '在高压前建立工具/承诺→高潮逐项真实改变→战后给可见时间验证改变。',
 '密集反转会透支惊讶，跳时又可能把重要结案压成转述；既要留余韵，也应标哪些结果只来自报道。',
 '用自有社会与人生进程检验结尾，避免只堆更大牺牲和同款半年后重聚。')

add('themes','care-autonomy','照料的检验是成本与自主权',
 '归属从馈赠、回援、重练劳动发展到组织补偿和现实守候。它有效时意味着替人承担资源与时间，也允许被照料者拒绝；若只按有用性分配或把返回当归属证明，温情就带占有阴影。',
 [ref(1,'themes',1),ref(2,'themes',1),ref(4,'themes',1),ref(5,'themes',3),ref(6,'themes',0),ref(8,'dialogue',1)],
 '以相反选择反复测试同一承诺，给受影响者自述和决定权。',
 '不是所有帮助都无私，拒绝者也不必被证明错；作者的回报善行可能使关怀功利化。',
 '原创时重设照料的对象、边界与机会成本，不把女性过度劳动当爱情必要条件。')
add('themes','community-power','共同体既保护也排斥',
 '反欺凌、同伴保护与资源独占、守尸报复、强制转会、资本压制并存；守家园敌人也能获片刻尊严。系统合法、公共口号、私人利益和伦理判断始终不能互换。',
 [ref(1,'themes',3),ref(2,'themes',2),ref(3,'themes',2),ref(4,'themes',2),ref(5,'themes',1),ref(6,'themes',2),ref(7,'themes',1),ref(8,'themes',0)],
 '让同样手段在敌我和不同权力位置接受可比较检验，而非只换称谓。',
 '出现反思不自动消除后续民族/性别双标；犯罪与死亡转述也不能被综合稿净化为司法结案。',
 '为原创权力建立可问责的后果和对方声音，不把私刑与羞辱当必要爽点。')
add('themes','unpriced-loss','可计算成就不能定价全部经验',
 '系统能宣布任务、好感、排名与奖励，人物却会为提示反觉虚幻、为遗物与缺席悲伤。常规死亡可补、部分NPC军力可奖励恢复，但魂殇永久毁、亲人逝去或生命封冻须按各自证据处理。',
 [ref(4,'narrative',2),ref(5,'themes',0),ref(6,'plot',1),ref(7,'themes',3),ref(8,'themes',1),ref(8,'themes',2)],
 '并置制度成功和体验代价，让生活行为继续显示哪些尚不可替代。',
 '不能推成NPC一律不可复、现实一律无法救；每次实际恢复/封禁/死亡都有独立条件。',
 '在原创题材中重设制度指标与人物愿望之间的差距，避免同样人物牺牲结构。')
add('themes','stage-ending','成长也包括接受共同生活改变形式',
 '开篇行动余地靠收入和朋友，中段为共同生活争家族/组织自主，后段反复离开和回归，终局有人经营、学习、结婚、间歇上线并接长期职责。结束征服阶段可以与世界继续竞争并存。',
 [ref(1,'themes',0),ref(1,'themes',2),ref(3,'themes',1),ref(7,'themes',2),ref(8,'themes',3),ref(8,'plot',3)],
 '把最后价值从永远下一件更强改为愿意承担与不再强求的事情。',
 '不是人人退游、所有关系解决或世界永久和平；终点具体归属由独立终点池核验。',
 '为原创角色设计不同生活目标，不复制工作室解散、茶厅与机场的同一收束顺序。')

add('continuity','state-ledger','状态链比单个终值更可靠',
 '取得、鉴定、绑定、等级/资格、实穿、转赠、损毁、恢复各有时点；任务接受/杀死/交付也不同。相同字面装备或人物在不同状态下会有不同结果，不能用末态抹去过程。',
 [ref(1,'continuity',0),ref(2,'continuity',0),ref(3,'continuity',0),ref(4,'continuity',0),ref(5,'continuity',0),ref(7,'continuity',1),ref(8,'continuity',0)],
 '事件驱动更新，保前后值、触发证据与尚未完成条件；未知不填计算值。',
 '算术推定不等面板，估价不等实际交易，未来资格不等已达门槛；活祭冲突不强算降级总数。',
 '原创资料库采用带时点的状态变化记录，别只存角色最终面板。')
add('continuity','unit-map','正文阅读单元、章号与时序分开',
 '卷六689/690各分两单元，卷七还有同印号不同正文、错序夹回叙；全书1180正文单元并不等于1173个不同原章号。覆盖必须依真实raw与行段，另加书首片段，不能凭号差认跳读。',
 [ref(4,'continuity',3),ref(6,'continuity',0),ref(7,'continuity',0)],
 '保原索引与全部片段→保存原题→另标阅读单元与时序→在源修订下核覆盖。',
 '本综合不新增全文阅读；项目记录的覆盖与整合者亲读范围分开，原始片段不擅合并。',
 '原创和研究都保身份稳定键与版本映射，避免以展示标题替代真实对象。')
add('continuity','uncertainty','先分类不确定性，再判断源错',
 '名字/数值异文、口径分母、角色误认、未知动机、规则边界和后来奖励例外不是同一类。神谕时长、埋骨换队、NPC75%恢复、净化希望与冰下笑声需要不同处理，不能统一圆成隐藏规则。',
 [ref(1,'continuity',2),ref(3,'continuity',3),ref(5,'continuity',2),ref(6,'continuity',2),ref(6,'continuity',3),ref(8,'continuity',1),ref(8,'continuity',2),ref(8,'continuity',3)],
 '先保各说法和来源→核分母/时点/对象→可解释则限域说明→仍冲突则不裁判。',
 '不以对作者有利或不利的预设选值；未解不等已证矛盾，定位合法也不等解释正确。',
 '原创可从这一分类反推连续性审查清单，用冲突驱动修订而非用它作临时解围借口。')
add('continuity','derived-evidence','合作阅读与派生研究分别署名',
 '本综合只读既有分卷成果，不新增个人全书通读声明。前两卷既有主任务、卷三/四各阅读者、卷五本代理、卷六44+200、卷七175+110、卷八20+101的原记录分别存在；主代理交叉复读是审查，不能重复加覆盖数。',
 [ref(4,'continuity',3),ref(6,'continuity',0),ref(7,'continuity',0),ref(8,'continuity',3)],
 '每条综合保上游文件hash、维度/条目索引、原观察层次与原证据；审修后刷新并核对，用户偏好继续留空。',
 '证据覆盖不能替代文学审查；本综合不替代人物全弧、问答或终点池，不把源事实写进原创正典。',
 '原创学习系统用来源事实、研究机制、用户评价、原创设计四层，试写后另记效果而非自动采用。')

DIM={d:[] for d in DIM_NAMES}
all_refs=[]
for d,k,title,claim,refs,mechanism,limits,transform in T:
 support=[];evidence=[];seen=set()
 for v,sd,i in refs:
  x=original_obs(v,sd,i);txt,kind=reported(x)
  support.append(dict(volume=v,dimension=sd,index_zero_based=i,observation_id=x.get('id',x.get('key')),reported_observation=txt,upstream_claim_kind=kind,reported_interpretation=textof(x.get('inference',''))))
  for e in source_ev(x):
   e=dict(e);e['claim_kind']='synthesis'
   ek=(e['chapter_id'],e['start_line'],e['end_line'])
   if ek not in seen:seen.add(ek);evidence.append(e)
  all_refs.append((v,sd,i))
 DIM[d].append(dict(id='book-'+d+'-'+k,title=title,claim=claim,claim_kind='synthesis',supporting_observations=support,mechanism=mechanism,limits_and_counterevidence=limits,originality_transform=transform,evidence=evidence,review_status='draft'))

body=[c for _,l in LOGS for c in l['chapters']]
body_ids=[c['chapter_id'] for c in body]
assert len(body_ids)==1180 and len(set(body_ids))==1180
supp=json.loads((B/'supplementary-read-log.json').read_text(encoding='utf-8'))
all_ids=set(body_ids)|{c['chapter_id'] for c in supp['chapters'] if c['full_text_read']}
assert all_ids==set(CH)
ownership=[dict(volume=1,reader='既有卷一主任务全文记录',count=49),dict(volume=2,reader='既有卷二主任务全文记录',count=51),dict(volume=3,reader='zongheng_vol03_full',count=144),dict(volume=4,reader='zongheng_vol04_full',count=178),dict(volume=5,reader='/root/zongheng_vol05_full',count=108),dict(volume=6,reader='primary',count=44),dict(volume=6,reader='/root/zongheng_vol05_full',count=200),dict(volume=7,reader='zongheng_vol03_full',count=175),dict(volume=7,reader='primary',count=110),dict(volume=8,reader='primary',count=20),dict(volume=8,reader='zongheng_vol04_full',count=101)]
interfaces=[]
for v in range(1,8):
 a=next(x for x in DOC if x['volume']==v);z=next(x for x in DOC if x['volume']==v+1)
 assert int(z['read_first'].split('-')[1])==int(a['read_last'].split('-')[1])+1
 interfaces.append(dict(from_volume=v,to_volume=v+1,last_raw=a['read_last'],next_raw=z['read_first'],index_contiguous=True,meaning_boundary='索引连续只证明无覆盖间隙，语义接口依主代理桥接复读与各卷交接。'))
ready7=all(x['exists'] for x in DOC[6]['documents'])
semantic_interfaces=[
 dict(id='v06-v07',claim_kind='synthesis',basis='卷六终点与卷七正式报告/交接的阶段对照，未新增整合者原文阅读。',
  claim='卷六末书254、赤霄已绑不可用、清风破口未最终结算、冰手术未知；卷七保卫战中才先短时满装圣域体验后归零，清风raw0799才按该卷记录回收，冰后续生还与自述另更新，不回填卷六已知。',
  upstream_documents=['writing-vault/library/reports/zongheng-tianxia/vol06-handoff.md','writing-vault/library/reports/zongheng-tianxia/vol07.md','writing-vault/library/reports/zongheng-tianxia/vol07-handoff.md'],
  evidence=[dict(source_id=SID,revision=REV,chapter_id=cid,start_line=CH[cid]['start_line'],end_line=CH[cid]['end_line'],claim_kind='synthesis') for cid in ['ch-0773','ch-0774','ch-0775','ch-0778','ch-0779','ch-0799']]),
 dict(id='v07-v08',claim_kind='synthesis',basis='卷七正式终点与卷八正式报告/交接的阶段对照，未新增整合者原文阅读。',
  claim='卷七raw1060只清S6首层小怪、10火魄在袋，首王未开；北冥在仓须275未用。卷八材料/装备与天域推进、275后可用由该卷实际读者分时更新，不把结局或首通回写卷七。',
  upstream_documents=['writing-vault/library/reports/zongheng-tianxia/vol07-handoff.md','writing-vault/library/reports/zongheng-tianxia/vol08.md','writing-vault/library/reports/zongheng-tianxia/vol08-analysis.json'],
  evidence=[dict(source_id=SID,revision=REV,chapter_id=cid,start_line=CH[cid]['start_line'],end_line=CH[cid]['end_line'],claim_kind='synthesis') for cid in ['ch-1036','ch-1055','ch-1060','ch-1067','ch-1068','ch-1085']])
]
revision_audit= B/'vol07/review-changes.md'
upstream_revision_checks=dict(document=revision_audit.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(revision_audit.read_bytes()).hexdigest(),method='复核正式卷七report/handoff、九维对应条目及审修记录，不把旧草稿哈希作最终依据。',
 checks=['玩家圣域重置与灵儿封印/神格复苏分开；保卫战中归零，不写守城已败后才归零。','灵儿raw0922第三即最后封解除，raw0963醒后展示，非第四封；本综合只取两套成长规则的区别。','刑天母亲重病时嘱托不移给龙魂，不升级为已死亡或正式遗嘱；本综合未建立该人物终弧。','奥丹雨露峡谷建令未证完成；本综合只取反派转向的选择结构，不复刻错地名。','萨格隆/盾证据与S4一牧已由正式修版处理，本综合不继承旧场景错证据或双牧说。','曙光要塞据点不是曙光城；200万元已转与次日让点计划分开。','送花未奖白银匕、通缉内得匕，未继承被删除的跨节点因果边。'])
inventory=collections.Counter()
for x in CARD_COUNTS:inventory.update(x['counts'])
assert sum(x['count'] for x in CARD_COUNTS)==426
assert dict(inventory)=={'character':150,'scene':205,'pattern':71}
identity_guard=dict(claim_kind='fact',reported_fact='主角原名丁舒升；丁书生为源文误称/牌上称呼，不当原名。',basis='主代理独立回读raw0004 L166与raw0966 L106934后通知；本代理此次不新增这两单元个人全文阅读。',evidence=[dict(source_id=SID,revision=REV,chapter_id=cid,start_line=line,end_line=line,claim_kind='fact') for cid,line in [('ch-0004',166),('ch-0966',106934)]])
O=dict(schema_version=1,artifact_type='derived-book-synthesis',source_id=SID,revision=REV,author='失落叶',work_title='网游之纵横天下',title='全书九维综合｜合作阅读后的派生研究草稿',review_status='draft',claim_kind='synthesis',
 status='draft-ready-for-review' if ready7 else 'draft-awaiting-final-vol07-interface',
 scope=dict(volumes=list(range(1,9)),project_body_units_with_fulltext_records=1180,project_frontmatter_segments_with_fulltext_records=1,project_indexed_segments_with_fulltext_records=len(all_ids),source_indexed_segments=len(CH),distinct_printed_body_chapters=len({int(m.group(1)) for cid,c in CH.items() if cid in body_ids and (m:=re.search(r'第(\d+)章',c['title']))}),project_read_record_union_complete=True,new_fulltext_reads_by_this_synthesis=0,personal_complete_book_read=False),
 derivation_boundary='本代理亲读卷五108与卷六后200；本文件经各卷成果派生，不冒称个人独读全书。不是新的阅读日志/正式卡片/人物全弧/问答/终点池；不读取无双或斩龙。',
 upstream_reader_attribution=ownership,upstream_documents=DOC,raw_interfaces=interfaces,semantic_interface_checks=semantic_interfaces,upstream_revision_checks=upstream_revision_checks,identity_guard=identity_guard,
 inventory_boundary=dict(volume_packages=CARD_COUNTS,volume_package_totals=dict(inventory),volume_package_card_count=sum(x['count'] for x in CARD_COUNTS),source_asset_total_reported_by_primary=432,retained_opening_cards_reported_by_primary=6,note='八卷分卷包426卡与全源432卡分开，另保旧开篇6。不是432张本轮新增。'),
 evidence_policy='综合条目均为synthesis；supporting_observations保上游事实/解释及其层次。证据从对应上游条目原样定位继承，claim_kind按综合用途标synthesis，不宣整合者重新通读每一原文证据。',
 dimensions=DIM,user_evaluation=None,user_taste=None,original_project_settings=None,
 pending_acceptance=['主代理对全书综合的语义审阅','卷七最终修版后刷新上游哈希与对应条目核对'] if not ready7 else ['主代理对全书综合的语义审阅'],
 cross_volume_guards=['卷五本卷未复活/未见复活不升级全世界绝对不可复活。','卷六649惩戒当章清，不写已掉十级；NPC战时全灭后有75%军力特殊恢复，书估可复七八万。','卷六末手术/清风未结只保存当时未知，下卷结果另更新；初获火龙60分钟不能覆盖后文新时长。','灵儿封印解开/神格复苏与玩家圣域晋阶是两套规则，不把系统陨落等同必然生命消灭。','明宇明确毁与圣者封禁、冰兰半年未明确醒、主雪未实婚分别保存；仅作综合边界，不重写终点池。','已存在的其他作者全书任务状态不由本文件推断；本综合只讨论本书。'])

e_count=0
for ds in DIM.values():
 assert len(ds)==4
 for item in ds:
  for e in item['evidence']:
   c=CH[e['chapter_id']]
   assert e['source_id']==SID and e['revision']==REV and c['start_line']<=e['start_line']<=e['end_line']<=c['end_line'] and e['claim_kind']=='synthesis'
   e_count+=1
O['validation']=dict(observations=sum(map(len,DIM.values())),dimensions=len(DIM),inherited_evidence_references_checked=e_count,upstream_observation_references=len(all_refs),unique_upstream_observations=len(set(all_refs)),body_coverage_union=1180,frontmatter_coverage_union=1,raw_interfaces_checked=7,result='passed-source-locators-and-derivation-structure',boundary='通过只证明继承定位/覆盖/上游条目可解析，不等文学解释或正式验收。')
for x in semantic_interfaces:
 for e in x['evidence']:
  c=CH[e['chapter_id']];assert c['start_line']<=e['start_line']<=e['end_line']<=c['end_line']
O['validation']['additional_semantic_interface_evidence_checked']=sum(len(x['evidence']) for x in semantic_interfaces)
O['validation']['all_eight_analysis_inputs_are_formal_versions']=all(d['documents'][0]['path'].startswith('writing-vault/library/reports/zongheng-tianxia/') for d in DOC)
sys.path.insert(0,str(ROOT/'distill-novels/scripts'))
from fictionlib.vault import Vault
vault=Vault(ROOT/'writing-vault')
vault._source=functools.lru_cache(maxsize=None)(vault._source)
for ds in DIM.values():
 for x in ds:vault.validate_evidence(x['evidence'])
for x in semantic_interfaces:vault.validate_evidence(x['evidence'])
vault.validate_evidence(identity_guard['evidence'])
for group in DOC:
 for fp in group['documents']:
  if fp['exists']:assert hashlib.sha256((ROOT/fp['path']).read_bytes()).hexdigest()==fp['sha256']
O['validation']['identity_evidence_checked']=2
O['validation']['vault_evidence_references_checked']=e_count+sum(len(x['evidence']) for x in semantic_interfaces)+2
O['validation']['input_sha256_rechecked']=True
(B/'book-synthesis-draft.json').write_text(json.dumps(O,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

lines=['# 《网游之纵横天下》全书九维综合（待审阅派生草稿）','',
 '这部书可学习的核心，是让资源、关系、责任在一轮轮任务之间转换：强者取得更多行动余地，也承担更大的维护与伤害能力；系统能结算胜利，却不能替人物解决全部关系与缺席。全书并非只有更高面板，而是多次让旧优势遇新条件，再把结果带回共同生活。','',
 '本文件综合八卷已有研究，未新增整合者个人全文阅读。本代理实际亲读卷五108单元及卷六后200单元；其余按原阅读者归属复用。项目记录并集覆盖1180正文阅读单元与1书首片段，共1181原索引片段；不同原章号为1—1173，分片不擅合。本综合不是新的全书个人通读声明，也不替代人物全弧、问答或终点池。','',
 '下列36条全是研究综合（synthesis），事实底座与原解释分别在 [book-synthesis-draft.json](book-synthesis-draft.json) 中保留上游卷/维度/条目索引、文件哈希和原证据定位。它们不是用户已认可的审美规则，更不是原创项目正典。','',
 '## 阅读归属与取材','',
 '| 卷 | 全文阅读记录归属 | 单元 |','|---|---|---|',
 '| 一 | 既有卷一主任务 | 49 |','| 二 | 既有卷二主任务 | 51 |','| 三 | zongheng_vol03_full | 144 |','| 四 | zongheng_vol04_full | 178 |','| 五 | /root/zongheng_vol05_full | 108 |','| 六 | primary 44 + /root/zongheng_vol05_full 200 | 244 |','| 七 | zongheng_vol03_full 175 + primary 110 | 285 |','| 八 | primary 20 + zongheng_vol04_full 101 | 121 |','',
 '书首14行另由主代理完整读取。主代理的跨卷复读与审查不重复加覆盖数。八卷分卷包合计426卡（150人物、205场景、71机制）；全源432含另保旧开篇6，不能称432张本轮新增。原名丁舒升由主代理回读raw0004 L166、raw0966 L106934确认；丁书生为误称/牌上称呼，不当原名。正式入库状态与阅读完成分别由主任务维护，本文件不推断其他作者任务状态。','']
if not ready7:lines+=['当前卷七analysis/全文记录已齐，报告与交接仍待最终修版；本稿状态为待刷新卷七接口，不冻结旧稿错误。','']
for d,name in DIM_NAMES.items():
 lines+=['## '+name,'']
 for x in DIM[d]:
  vols=sorted({s['volume'] for s in x['supporting_observations']})
  lines+=['### '+x['title'],'',x['claim']+'（比较范围：卷'+ '、'.join(map(str,vols))+'；逐条出处见JSON `'+x['id']+'`。）','',
   '可迁移动作：'+x['mechanism'],'','边界：'+x['limits_and_counterevidence'],'','原创变换：'+x['originality_transform'],'']
lines+=['## 使用这份综合的方式','',
 '优先选择一个机制做小规模试写：先说明要改变的读者体验，再列约束、角色选择和结果。以原创材料重建因果，试写后记录哪些条件有效、哪里失效；未获用户反馈前不要自动写成个人风格规范。最适合先试的是奖励分层、重复任务变策、群像专长互补、胜利多账、喘息改状态和物件用途转情感。','',
 '应主动改造或舍弃的部分包括：连续极品/巨伤通胀、主角自辩被当伦理裁判、以女体或群体贬损代替个性、操控后以结果顺利倒推同意、以女性牺牲单向启蒙男主。保留文本的价值张力，不替它抹平，也不替用户选择喜恶。','',
 '## 接口与验证','',
 '七处卷间raw索引连续，244卷六与285卷七等分片完整保留；连续只证明没有覆盖空隙。语义另核：六末未入圣/手术未知/清风仅破口，七卷才分时更新圣域重置、清风回收与冰生还；七末S6首王未开和北冥未用，八卷成果不能回写。全八卷分析、报告与交接以正式版本刷新哈希。','',
 '卷七审修另核玩家圣域与灵儿封印分开、922开最后封/963醒后展示、刑天母嘱归属、奥丹雨露峡谷建令未证成、萨格隆/盾证据、S4一牧、曙光要塞据点与送花/白银匕因果。综合不继承旧稿相应误读。原文数值异文、人物猜测、特殊奖励和最终未知分层保存：卷六NPC全灭后有75%物资军力特殊恢复，不能当永久全损；初获火龙时限不覆盖后段新值。','',
 f'本稿有9维、36条跨卷综合，继承并检查{e_count}处证据定位、{len(all_refs)}个上游观察引用，另核12处六七/七八语义接口与2处姓名定位，共{e_count+14}处经Vault证据接口通过；正文记录并集1180、书首1，七处接口索引通过。此检查不等文学解释通过，尚需主代理审阅；每条源观察与综合解释可以各自修订。','',
 '终点具体人物、物品、关系与线索结案请使用卷八读者和主代理的终点池；本稿只保留防误读边界。未读《天下无双》或《斩龙》，不做后续作品比较。','']
(B/'book-synthesis-draft.md').write_text('\n'.join(lines),encoding='utf-8')
print(json.dumps(dict(status=O['status'],validation=O['validation'],card_packages=dict(inventory),vol07_analysis_sha256=DOC[6]['documents'][0]['sha256'],outputs={name:hashlib.sha256((B/name).read_bytes()).hexdigest() for name in ['book-synthesis-draft.json','book-synthesis-draft.md']}),ensure_ascii=False))
