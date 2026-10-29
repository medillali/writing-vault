"""只核验研究包及生成中文导读，不调用Vault、不写正式库。"""
import json,collections,hashlib
from pathlib import Path
P=Path(__file__).parent;BASE=P.resolve().as_posix()
def R(n):return json.loads((P/n).read_text(encoding='utf-8'))
def W(n,v):(P/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
A=R('analysis.json');C=R('cards.json');G=R('graph.json');ST=R('reader-state.json');LOG=R('read-log.json');S=R('../source.json')
SID,REV=S['source_id'],S['revision'];N=[json.loads(x) for x in (P/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
CH={c['origin_key'].rsplit('/',1)[1]:c for c in C if c['asset_type']=='character'}
# 关系方向写成有主体的阶段动作，避免仅凭同场就称普遍双向关系。
REL={
'lu':[('he','接受盟主授权管理虚产并实际出资；亲密不等独占伴侣'),('lin','独立盟友/竞争者，交换资源、共同作战与互吻'),('xin','由解主仆转兄妹，保护与依靠其力量并存'),('lubu','投资扇书但未买断其对零度的旧恩')],
'he':[('lu','授权其守产/倾向分装，表达情感并保职业自主'),('moon','共同筹新公司/长期互相照护'),('lin','竞城后仍联盟、分配王装与战术协力')],
'lin':[('lu','能胜他、拒他要求/议价，也主动救援与传图'),('he','同盟竞争后共分装备与守城，未正式归其会')],
'bei':[('lu','主动发现地形/指挥后排并在生活中打饭，非只受保护'),('gui','指出火马过时，独立弓系火力不服骑兵中心分配')],
'moon':[('he','共同离GGS与筹事业，负责杭州技术协议'),('lu','多次治疗救命/现实获救后吻，陆仍否认女友'),('yuelu','高阶牧互补而非同一实体')],
'gui':[('lu','作为独立统帅执行外线、提出风险，非只伴宠'),('youyun','骑神/飞将切换形成机动战术'),('rain','与新骑将协同掩护/分队')],
'li':[('lu','表达尊重信念、殿后牺牲，后谷战相互救援'),('zhu','旧女友事件含自述/当场承言，敌意曾使自己擅冲'),('dou','共同殿后与比赛，后教差0.2秒需要改进')],
'luanyue':[('lu','受让尾与书装后成为可救其同伴者，恋爱调侃未定约'),('dou','两次实救并追回无敌；卷末替其保管'),('lubu','带队培养其升级，报告已学紫龙但未征服其旧恩')],
'xu':[('he','旧日核心仍尽守护/分装支持'),('lu','现实被救、得到星空套，代分2500药'),('dou','同前线/技能联合，未合成一个菜鸟支持群体')],
'dou':[('li','以刚性换伤打法协同逼烛、共同殿后'),('luanyue','接受救援和回斧，不因此免除自己冒进后果')],
'youyun':[('gui','快速追近后切骑神输出，分工互补'),('lu','金龙尾刀与经验独立受益，非主角让尾')],
'lubu':[('zero','基于先前救命恩坚持留第八；拒转主盟'),('lu','接受资源/梦想认可且愿支援，但保旧归属'),('luanyue','由其强团带练，技能实学后仍未到主线')],
'xiaoman':[('lu','先接受援救却拒补与入会，后按条件取得庇护再入主盟'),('zero','清场受害方，拒绝在其第八部下'),('lin','向其女盟主形象看齐，但未自动拥有独立盟')],
'zero':[('lu','接受自治/名牌与保护后越界清场，被训仍留职'),('lubu','旧救命恩牵住人才，驳其转主盟'),('xiaoman','指使攻击/抢装造成信任破坏，未亲自道歉已见')],
'rain':[('gui','编其骑团、外线掩护杀临'),('lu','经同学同意受邀主盟；现实拜访未到')],
'zhan':[('lu','先代下属道歉、再赛场对赌，合作与敌对按事件分'),('gui','第三城外线被青虎压迫，未因此全会崩溃')],
'zhu':[('li','言语羞辱并控杀，非仅中立竞赛'),('lu','一阶段对手、竞逐王权/城权，九龙死后仍能攻紫百合')],
'xin':[('lu','解主仆为兄妹、主动替伤/回战，非受控宠工具'),('sophia','被其与雪薇优先保护，不等同夺卡琳珊城')],
'karin':[('lu','接受任务物并授系统奖励，未证明所有强敌主独杀'),('tiya','下令试炼/出征/治伤/侦察'),('sophia','同抗寒刃但互有政治边界')],
'sophia':[('xin','以军队来保她，承不觊城后实际撤'),('karin','不同政权有限合作，复国非吞并银月')],
'tiya':[('lu','先试炼授有限工具、后受其取血治疗'),('karin','五骑所属，奉令侦察九龙')],
'kaxiu':[('lu','以试炼换传承，追加脑浆后才治愈/授术')],
'yuelu':[('lu','插秒与卡片使其能活/能杀，辅助独立贡献'),('luanyue','在隐洞持续治与并获装，不是可删的背景'),('dou','谷战仍无法抵两次雷霆，治疗非无条件救命')]}
for key,rels in REL.items():CH[key]['content']['relationships']=[dict(target_origin_key=CH[t]['origin_key'],direction=text) for t,text in rels]
W('cards.json',C)
# 重复格式信息不修改原始逐章笔记与真实已读范围。
LOG['method']='本代理按read_chapters.py每次1—2原片逐行全文阅读，逐次核BEGIN/END；每2—4片立即写事实/推断/状态/未决笔记，共95批。未用检索或摘要代替全文。'
LOG['body_units_read']=376;LOG['indexed_segments_read']=378;LOG['complete_volume']=True;LOG['complete_book']=False;LOG['reader']='/root/zongheng_vol03_full'
LOG['unit_anomalies']=[{'chapter_id':'ch-0229','type':'volume_header','count_as_body':False},{'chapter_ids':['ch-0398','ch-0399'],'type':'split_body_continuation','count_as_body':1,'note':'两片都全文实读与记录；0399误识别第二回合GO不是新增章。'}]
W('read-log.json',LOG)
names={'worldbuilding':'世界观与规则','characters':'人物与关系','plot':'情节组织','style':'语言与文风','narrative':'叙事与知识差','dialogue':'对话','pacing':'节奏','themes':'主题与价值张力','continuity':'连续性与阶段边界'}
def link(n,label=None):return f'[{label or n}]({BASE}/{n})'
def cite(ev):return '、'.join(f"{e['chapter_id']} L{e['start_line']}—{e['end_line']}" for e in ev)
lines=['# 《网游之天下无双》卷三全量研究草稿','',
'本卷378个原始索引片段（raw0229—0606）均由 `/root/zongheng_vol03_full` 实际逐片全文阅读，合计376正文：卷标题一片不计正文，0398/0399为同一正文的两片。95批笔记已保存，截断待补为零。前二卷primary交接只作阶段参考，不计本代理亲读。以下为文学研究待审阅稿，未由用户批准为个人风格规则，也不表示全书已完成。','',
'本卷最可迁移的部分，是把能力成长放进组织分工与承诺结算：高阶装备需真实取得、具资格并使用；同伴会先失败再独立赢；公共胜利与个人伤亡不相互抵销。其局限同样明显：身体凝视、性羞辱、现实报复，以及主角谴圈地同时获利于封路等行为，必须保留价值张力。','',
f"资料入口：{link('analysis.json','九维分析')} · {link('cards.json',str(len(C))+'张卡')} · {link('graph.json',str(len(G['nodes']))+'节点/'+str(len(G['edges']))+'边/'+str(len(G['threads']))+'线')} · {link('chapter-notes.jsonl','378片逐章笔记')} · {link('read-log.json','阅读日志')} · {link('reader-state.json','检查点')} · {link('handoff.md','衔接状态')} · {link('validation.json','本地校验')}。",'']
for dim,title in names.items():
 lines+=['## '+title,'']
 for obs in A['dimensions'][dim]:
  lines+=['- **源事实：**'+obs['fact']+' **研究解释：**'+obs['inference']+'（'+cite(obs['evidence'])+'）','']
lines+=['## 人物不是战力附录','',
'23份独立人物卡保留目标、限制、选择与方向关系。陆尘的战术成长与治理失误并列；何艺不是单纯经济外挂，她主动承担创业专业工作；林逸欣赢比赛、保独立领地并持任务知识；北冥、明月、月露、乱月和李承风有不可删的具体贡献。鬼/斗的失冷静与冒进也有真实失败。新人物吕布衣守旧恩、小蛮拒绝坏组织，使招募不能只靠神装和赞美。','',
'| 人物 | 本卷阶段终态 |','|---|---|']
for c in CH.values():lines.append('|'+c['title']+'|'+c['content']['stage_change']+'|')
lines+=['','## 场景与可迁移机制','',
'32张场景按“目标—障碍—选择—后果—状态变化”组织。最重要的回收包括：镇魔剑封门；寒冰琼花实际交付；赤岩血煞与旧神怒在九龙反击；烈焰兽卡和可拆小洞；灼热扇/紫龙给吕；乱月掠夺回斗斧。它们连接的是同一工具的真实流转，不是只凭主题相似画因果。','']
for c in C:
 if c['asset_type']=='pattern':lines+=['- **'+c['title']+'**：'+c['content']['summary'].split('：',1)[-1]+'。失效条件：'+c['content']['failure_conditions']+'。原创转化：'+c['content']['originality_transform'],'']
lines+=['## 已结与尚未结','',
'紫罗兰复国、寒刃本次保城/职业交付、第二城系统归雪银、九龙九鳞最终任务、卡修救治都已有本卷回收证据。寒刃仍活逃、心然记忆/封力未全复；雨立方仍办手续且蓝星未正式签；第三城和暗月掠夺均未终判。卷末的悬念是具体五千幽灵铁骑刚出现，古剑约两千残军要继续挡，而不是笼统“下一卷还有敌人”。','',
'首俱乐部赛1:4败与李KOF一穿五不能合成“古剑从未输”。第三城赌约在598明确仍有效，外围截杀是陆利用文字边界干预战局，不能替他宣布没有道德争议。小蛮拒收的七件装备不能记作已赔偿；假死分身不能记作陆本体再触不死。','',
'## 原文疑点与研究限度','']
for x in A['source_anomalies']:lines+=['- '+x['issue']+'（'+cite(x['evidence'])+'）','']
lines+=['本地定位核验只验证来源身份、片段覆盖、区间、卡引用和图结构，不证明文学解释已获用户认可。正式库仅由主代理按卷序审阅、串行保存；本包仍是draft。','']
(P/'report.md').write_text('\n'.join(lines),encoding='utf-8')
HAND='''# 卷三交接：截止raw0606（印刷第601章）

378原片/376正文全部本代理亲读；raw0229卷标题、0398/0399合一正文均已逐片记。source_id为src-d8926e2a35f04bcf8139cff0ea516bbd，revision为d819f7d0ecf5a2004a0a434e987569bbe25015422d45e16676af913292346857。前卷primary信息仅背景，本交接不冒称亲读前两卷。全部产物待审。

## 人物/物品即时状态

- 成长时点复核：raw0363 L33274—33283是林捕寒冰狐后的共享经验使陆升100并触发武神；raw0367长耗紫域至杀王，raw0368 L33619明确100升105，L33663—33680偷天自带降需20后在105实穿，L33696—33701另以简易宝石降靴需求再穿。不能把两个经验来源合成同一升100时点。谁主沉浮决赛按古剑视角为1:2负雪银，半决赛2:1胜烛。
- 陆尘143（595明确并延续598），修罗王由579吸火种141才系统进化；501交导师才首五转白金。150骑乘/晋级新境界未到，名将不是圣域。青冥140已穿，赤岩甲、镇魂斗篷、惊涛靴、银龙戒/鬼影戒已用；鬼影75%属性不能加防御技能、下线死消/CD20分。旧偷天566被吕超245万买走/净2327500实到，不仍在陆包。青冥/青魂是源误称，不造另一剑。暗瞳自级+50看怪/50码隐、弱点几率，非对玩家必中。灵烹8；圣灵丹8实战回5000，十级只是预览未成。（502、563、566、579—581、584、593、596、598、606）
- 何艺最近136（575）、慕最近134（575），两人南京现实手续/签约，603明说头盔在家，本卷末未上线。何旋风/雪追已用；星焰135盾562已得，后来等级足但无明确换盾镜头。慕铁翼已孵为宠非骑；573获明镜35%治/瞬解负，能解鬼预是何推断未实测。车祸583医生额伤留观、584已出行，有司机；陆手缝两针，不是慕死亡又复活。
- 林逸欣592实140、倾国80上限，紫电135/皓月/冰镰/寒冰狐实用；593双飞140女辅助策略实学，首次不同步失败后合击112838。关系爱/喜欢/互吻有证，但不自动排他情侣、婚约或性关系；兄妹称呼有掩身份/调侃语境。
- 北冥最近136（575），烈影实用；130风行腿先得后等级足无明确穿镜头。卷末活，弓神150%攻60%速/高地后排指挥，与陆合杀百步穿肠（后误写穿杨）及嗜血神射，不是陆独杀两弓。弓主盟1500受扩骑挤压。（536、575、599、606）
- 鬼谷子最近135（575），彩虹九层丢/离拾、陆杀离追回→交风月委托→568已实持，归还已被后段实际动作确认。130地赤金盾536先存，后级足无本卷明确实换。幽云535尾黄金龙125成飞将，23码刀气尾刀，陆该王没经验；幽569实骑大地蜥，青虎后换。天堂雨577天风127第28名将骑将可重复、嘉兴学生、原七同学愿血佣仅口头，自己主盟已真入。鬼/幽/雨卷末仍外线，青虎3097实成、外战损500+，604限一小时无论果回暗月但606尚未返。
- 李承风最近135（575），迅雷/烈风剑/龙战士实用。560九层殿后真死，另一战571—572KOF一穿五，不把前死当永久。605谷被眩险死，月露/乱/陆救后掩陆退，末活。旧女友与烛事件含自述、烛当场恶言，不升级警方定案。
- 乱月549127掠夺；544四骨镰简易现场穿、546首碎石、549第五盔也实穿。555鬼预回城真死，未记精确掉级。卷末活；606斗真死爆卓越无敌敌刺先拾，乱掠夺杀刺追回塞包，未返斗/未复活斗。597送青山的普通非卓越无敌是另一同名装备，不能合并。
- 许阳=烈日，地下赛真实手臂伤/549仍石膏；游戏壁垒/星空套/铁背熊甲/撼岳实用，代分2500力量药。月露是独立高牧，生命潭属慕，月露送烈焰兽卡、插秒治疗/分区指挥，130月咏链已获未明确穿。
- 吕布衣133奇脉谋者（586/589），589策312含灼热扇50已拿上，紫龙135/策300/学降3级先未学；603乱月报告刚学约70%全属性，没明确此刻等级，不编135降132时间点。仍焚琴煮鹤第八副盟、未名将、未主盟/未到谷；零度救命旧恩为其亲述，拒转主盟有据。593陆自称能学紫龙与谋士专属冲突，不据此给陆技能。
- 零度仍第八盟主，588自治加入后5000满、5943000人清场/骚扰抢装由他指使，陆训而未踢；新收沉默者不全同罪。小蛮19/林21（598），八熟友无原行会；七赔装拒收，597敌盾与普通无敌实拾/青山实收，598八人真入主盟（非第八）。第九盟只想建，令未买/会未建。青山/青海为源称差，勿造双人。

## NPC与任务

- 心然解主仆为兄妹，古魂占身/封力与记忆未全解；寒冰琼花274实交才疗伤、复国302回归主伤。498四神骨活天术是操骨，四骨毁而非诸神真实复生。500心活、寒刃断腿逃，后神域修炼未来。（248—255、274、302、498—500）
- 卡丁被卡迪拉附身，救治短暂认女后真化灰，不能用任务成功写父存活。卡琳珊仍公主称号但500—501王座系统政权完成；寒刃战她伤未死，五龙骑重伤不是全死，500巫师治后又起飞毁杖。蒂雅552奉卡命骑绿龙入八层又离、非八王。索菲娅紫罗兰复国已成，援心承不觊浮冰而撤，不是夺城。
- 卡修千虎百牙577交后仍缺脑浆，580血颅165地王陆/狼长耗两小时杀且狼三死，581实交头系统任务结/灵烹实学/卡修抹药起身活跑。灵烹书写3000万声望但实际二三十万即学源冲突保原，不补豁免。
- 九龙金鳞古剑/木鳞烛抢林王/冰古剑/地古剑→鬼丢离→陆回/火离/飞十月/雷雪银/风吻月/星陆王。562林洛明协议交两鳞换各挑装备，九齐；563实际交公主→陆137至140幸33至38、暗月+1、青冥真穿。不是独杀九王或星龙直接掉天器，真正已完成。

## 城市、战争与未兑现事项

450首领地系统归古剑，陆受委托管理，NPC奥达尔代管不等私有。515第二城系统归雪银。末暗月6（575/598）仍古剑，诸侯令掠夺十小时须清城内守方才转权；宣战不等已夺。首次领地系统守8小时改5是源执行，第三城598守10。城市升级3→任务+1→实际5/传送2或3口径异常保留，不强补单独升级镜头。

568友谊赛赌第三城输方不争，570实际1:4负/陆没出场；572李KOF一穿五5:0且免战天跪，没有撤第三城赌。598明确原约有效，陆选择外围封截战天、拒改籍血佣；研究保字面规避与实质干预的张力。第三城本卷未占/君临未得。

598长生殿嗜血提交诸侯令联圣域玫瑰/问鼎掠暗月。十月唆使先乱猜、599凌雪殇称小道消息，非亲见游说。鬼3097青虎外线机动阻战天、陆主7000出青石谷争2—4小时、薛璐500弓/杜数百守传送。洛被烛攻不能来、三生已诺白帝攻城只五小时后条件援，本卷未到。青石谷先歼圣域二4000、问鼎两盟万、长生四分三万余退但自己419→近3000损→末约2000；606斗真死/斧乱保、陆北合杀双雷，近5000幽灵铁骑才出现，尚未冲锋/谷撤/回援或城守结局。不能把源估计各会总30万当已全部进入谷。

## 经济、合同与关系账

- 旧材料五万欠款（230）未见本卷清证；医疗十五万353真还，不用来清旧债。何500万电话承诺未见实付。拍卖实到/分配、收入表/旁白异算分开。
- 联想525四人年5100万合同当场签，526电脑实际送/ROSE到；工资没见首付。华硕525意向待签→568正式签约开业追述；苹果565五人签、林年2100万且590说按月。七候选526仍“一旦签约”，不真签。
- 地下500万赌未实收/未真付400万，528陆现实砸断百战臂腿非司法正防已判。550才实名互认。
- 584陆先1000万、售11血色及地煞/风雷后再1000万给何，总2000万实转；北500万仅据说。雨立方何50/陆慕北各10/余20募资、百亿估计不是现金。581蓝星只有合作意向未正式签；582腾龙先发已签且取回包，583注册派人/次日预计，584称成立/上午取照但未展示正式最终蓝星协议，末仍南京手续。何辞呈三天承诺未独立展示送达。
- 力量药58924592瓶制作/上架，590许2500杜500实交、林1500每3000共450万实交易；普通竞拍卖出具体总额未全结；不得用全库存×底价当已赚。灵烹8未10、青冥借林口头未实给。
- 多方亲密：何爱问/陆不知、林曾爱又说不爱及互吻、慕救命吻/陆仍否女友。没有本卷排他定约或性行为。诙谐所有女友/正妻/妹妹不是客观法律/血缘关系。

## 源异常与下一卷检查

重点核：赛事16/八强错奖作者自承；寒刃禁复中已死许斗杜薛后在场、九龙月光石535死后540/545施法未交代；冰旋CD20秒/20分/30秒；缚神502无敌可解却561离无敌不能脱；灵烹3000万望却学；踏破降防/攻击无视及比例、偷天/星空溅射异文；539套装合计九说八/589出五说三；577斗乘青虎后变幽且战士未150；606穿肠/穿杨与564青魂/青冥不要造新实体。未知与明确冲突分别保留，不自行修书。

下一卷先承606未开幽灵骑：确认谷战损失/撤退及青虎回城是否实发生、暗月十小时主权/第三城结算；追斗斧真正归还/复活、吕是否转主盟/名将与零度治理后果、明镜真正解除鬼预、蓝星正式签与雨立方手续、五万旧债是否交付。不要借后卷结果静默覆盖本卷阶段卡。
'''
(P/'handoff.md').write_text(HAND,encoding='utf-8')
# 本地结构检查，无Vault锁，不代主代理文学审阅。
spec=next(v for v in S['volumes'] if v['volume']==3);expected=[s['chapter_id'] for u in spec['units'] for s in u['segments']];src={s['chapter_id']:s for s in S['chapters']}
assert len(expected)==378 and len(set(expected))==378
assert [n['chapter_id'] for n in N]==expected
assert [n['chapter_id'] for n in LOG['chapters']]==expected
assert A['read_chapter_ids']==expected and ST['read_chapter_ids']==expected
assert ST['next_chapter_id'] is None and ST['complete_volume'] and not ST['complete_book']
assert not ST.get('pending_truncations') and not ST.get('pending_chapter_ids')
for n in N+LOG['chapters']:
 s=src[n['chapter_id']];assert n['full_text_read'] and (n['start_line'],n['end_line'])==(s['start_line'],s['end_line'])
refs=0
def walk(v):
 global refs
 if isinstance(v,dict):
  if {'source_id','revision','chapter_id'}.issubset(v):
   assert v['source_id']==SID and v['revision']==REV and v['chapter_id'] in expected
   s=src[v['chapter_id']];assert s['start_line']<=v['start_line']<=v['end_line']<=s['end_line'];assert v['claim_kind'] in {'fact','inference','synthesis','plan'};refs+=1
  for x in v.values():walk(x)
 elif isinstance(v,list):
  for x in v:walk(x)
for x in [A,C,G]:walk(x)
origins={c['origin_key'] for c in C};nodeids={n['id'] for n in G['nodes']};edgeids={e['id'] for e in G['edges']}
assert len(origins)==len(C) and len(nodeids)==len(G['nodes']) and len(edgeids)==len(G['edges'])
for c in C:
 assert c['review_status']=='draft' and not c['user_notes'] and c['favorite'] is False and c['content']['summary'] and c['evidence']
 for o in c['content'].get('derived_from_origin_keys',[]):assert o in origins
for n in G['nodes']:
 assert n.get('parent_id') is None or n['parent_id'] in nodeids
 for x in n.get('characters',[]):assert x in origins
 if 'asset_origin_key' in n:assert n['asset_origin_key'] in origins
 for x in n.get('knowledge',[]):
  assert x['state'] in {'knows','suspects','misbelieves','unknown'} and (x['observer']=='reader' or x['observer'] in origins)
  assert x['state']!='misbelieves' or x.get('belief')
for e in G['edges']:assert e['from'] in nodeids and e['to'] in nodeids and e['evidence']
for t in G['threads']:
 assert set(t['node_ids'])<=nodeids and set(t['edge_ids'])<=edgeids and t['status'] in {'open','partial','resolved','abandoned','unknown'}
 for eid in t['edge_ids']:
  e=next(e for e in G['edges'] if e['id']==eid)
  assert {e['from'],e['to']}<=set(t['node_ids']), (t['id'],eid)
 if t['status']=='resolved':assert t.get('resolution_note') and t.get('resolution_evidence')
assert [x for c in G['coverage'] for x in c['chapter_ids']]==expected and all(x['complete'] is False for x in G['coverage'])
counts=collections.Counter(c['asset_type'] for c in C);assert counts['character']>=8 and counts['scene']>=12 and counts['pattern']>=6
V=dict(book='tianxia-wushuang',volume=3,review_status='draft',indexed_segments_read=378,body_units_read=376,batches=95,reader='/root/zongheng_vol03_full',pending_truncations=0,dimensions={k:len(v) for k,v in A['dimensions'].items()},cards=dict(counts),nodes=len(G['nodes']),edges=len(G['edges']),threads=len(G['threads']),knowledge=sum(len(n.get('knowledge',[])) for n in G['nodes']),evidence_references_checked=refs,preflight='local_structure_passed',vault_validation='pending_primary_serial_check',literary_review='draft_pending_primary_and_user',checks=['片段/正文映射及完整覆盖一致','日志/笔记/状态索引无缺重','所有证据身份/修订/区间在本卷章内且自身带claim_kind','卡origin/派生源与图端点/人物引用有效','knowledge state/observer及resolved回收字段齐全','全书complete保持false'],limitations=['未在本脚本初始化Vault以避免并行锁；主代理可串行运行check_volume.py','定位结构通过不代表文学解释获批准'])
V['sha256']={n:hashlib.sha256((P/n).read_bytes()).hexdigest() for n in ['analysis.json','cards.json','graph.json','report.md','handoff.md','read-log.json','chapter-notes.jsonl','reader-state.json']};W('validation.json',V)
print(json.dumps({k:V[k] for k in ['preflight','indexed_segments_read','body_units_read','cards','nodes','edges','threads','evidence_references_checked']},ensure_ascii=False))
