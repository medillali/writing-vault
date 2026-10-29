"""本卷待审稿交付编排与只读核验；无正式库写入。"""
import json,pathlib,sys,hashlib,collections,importlib.util
H=pathlib.Path(__file__).resolve().parent;sys.stdout.reconfigure(encoding='utf-8')
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
write=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
old='首2万?原首半血无我补数'
new='首局把神骨打至半血后击杀（无额外伤害数字）'
changes=[]
for p in [H/'batch-0933-0936.json',H/'chapter-notes.jsonl']:
 text=p.read_text(encoding='utf-8')
 if old in text:
  text=text.replace(old,new);p.write_text(text,encoding='utf-8');changes.append(p.name)
if changes:write(H/'note-corrections.json',dict(reason='去除草拟笔记中未依据原文的2万问号字样；正文L77083仅半血叙述，不变阅读覆盖/来源元数据。',chapter_id='ch-0933',changed_files=changes,claim_kind='synthesis',review_status='draft'))
a=read(H/'analysis.json');c=read(H/'cards.json');g=read(H/'graph.json');n=[json.loads(l) for l in (H/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines()]
N={x['chapter_id']:x for x in n}
def link(name,label=None):return f'[{label or name}]({(H/name).as_posix()})'
def refs(es):
 return '；'.join(f"[{e['chapter_id']} L{e['start_line']}—{e['end_line']}]({(H.parent/'source.json').as_posix()})" for e in es)
labels={'worldbuilding':'世界观与规则','characters':'人物','plot':'情节','style':'文风','narrative':'叙事','dialogue':'对话','pacing':'节奏','themes':'主题','continuity':'一致性'}
report=['# 《网游之天下无双》卷五全量九维研究（待主审）','', '实际全文阅读265正文、1卷标题，共266原片段：raw ch-0793—1058，原文印第787—1051章，L65981—86173。本读者 /root/zongheng_vol04_full 独立逐片读取BEGIN至END、每2—4片保存观察；没有以摘要/检索替代阅读。只亲读本卷，前四卷未重新全文；本卷包不使用卷六以后结论。全书覆盖仍为false。','', '最重要的阶段结果是：国内与世界WEL两冠、主正式世界MVP选天空王者之城；奥维亚取首任务完成而魂盒万魂释放未展示；苏菲通过母亲在场真相转银月，但卡兰斯已真死；国战系统宣布中国胜且紫葡萄荒废，陆尘紧接被取消CGL、剥夺中国玩家身份并通缉。五万生死谷守军归零，不能被最后胜利抵销。','', '阅读、分析与用户审美分开：本包全部draft；结构通过不代表用户已认可这些解释或愿用于原创。','']
for k,entries in a['dimensions'].items():
 report.extend(['## '+labels[k],''])
 for x in entries:
  report.extend([f"**{x['title']}。** 原文观察：{x['fact']} 研究判断：{x['inference']} 证据：{refs(x['evidence'])}",''])
report.extend(['## 人物与场景的取舍','', '46张独立人物卡保留目标、限制、关系方向、选择和卷末状态。陆尘不是完美统帅：白马毁约、借法私图不还、送爪少留以少己死、追入伏击，与勇气/救援/认责共同存在。何艺不被概括成花瓶或瞬间无敌：真实技术劳动、竞技败局、成长后的护连与调兵都有动作证。林逸欣保组织自主，北冥与连昕也有各自失误、学习及军团职责。','', '51张场景按状态变化挑选。机关/石化/盾印说明知识如何取得；白马父女/心然强剖龙心/剑圣未救把伦理代价留在奖励之外；WEL以每局信息变化而非只大比分讲能力；后半用普通骑/工匠和旧敌的真实贡献抵住单主英雄视角。','', '12张机制是研究抽象，均链接本卷场景卡：试错成本、威胁转资产、回归摩擦、胜负交错成长、NPC转盟有代价、任务与守诺分账、交付阶段、动态地图、兵种协同、旧敌到同袍、知情时间、胜利触发制度损失。每张写适用/失效及原创转换；不移植角色名、技能表、民族贬抑或物化套路。','', '## 卷末线索状态',''])
for t in g['threads']:
 report.extend([f"- **{t['title']}**：{t['status']}。{t['resolution_note']}"])
report.extend(['','## 仍未明确的事项','', '以下只断到卷五末，unknown/partial不代表作者全书遗忘，也不表示本卷还有正文没读。'])
for q in a['open_questions']:
 report.extend(['',f"- **{q['id']} {q['question']}**（{q['status']}）：{q['stage_assessment']} {refs(q['evidence'])}"])
report.extend(['','## 源文疑点与证据层','', '数值/误名/省略与剧情未明分开存。重要者有：青甲狼156/186、8级会5万/10万、阿扎尔万夜灵要求而蜈蚣结算、白马李杀柏丽而系统主杀郡主、苏斩奥首但系统北获杀、WEL120秒与多次超时、幽冥25/50%、资源仓算差与借偿币种、作者1049地理纠正、擒魂120秒与末段连用。龙盾0耐后可用仅说明修复过程省略，不能自造修理场；云取心后呼吸/生命波动是明确误认纠正，不能归同一类数字异常。','', f"完整25项见{link('analysis.json')}的unresolved_and_anomalies；逐章历史未解原记录保留time_scope，不被直接当卷末全仍open。",'', '## 交付与核验','',f"{link('chapter-notes.jsonl')}；{link('read-log.json')}；{link('reader-state.json')}；{link('analysis.json')}；{link('cards.json')}；{link('graph.json')}；{link('handoff.md')}；{link('validation.json')}。",'', '只写本隔离卷目录，没有正式库/Git/记忆操作。主代理负责文学审阅与串行入库；本读者随后继续已授权卷七。',''])
(H/'report.md').write_text('\n'.join(report),encoding='utf-8')
handoff=['# 卷五交接（全量已读，待主审）','', '范围：raw0793—1058，265正文+1标题；所有逐章笔记与reader-state已落。主代理可审，本代理按既定授权继续卷七raw1294—1504，不预读卷六补本卷末。前四卷未亲读，文内前史只按角色转述/系统引用。','', '## 卷末必须保住的事实','', '- 紫葡萄老王由烈焰红唇先打至残，三生让主，陆尘最后斩首并实际碎王徽。系统中国服务器胜/紫葡萄荒废/15日不可攻；没有选占领，具体本场MVP与物品奖没展开。','- 唐龙=虬龙/执剑盟主175，早宴承只指方向/不干具体战，末命还城；25%月营收方案只其自称谈妥、被毁徽中断未落地。鬼谷子杀其游戏角色不阻他官方介入。取消CGL、剥中国玩家身份、通缉是系统已实施，主名红/天空徽消。禁各会收留/否则逐是唐喊话，尚未见执行。不是现实中国国籍变化。','- 生死谷归零规则：被杀失所有经验/等级归零、包裹装备全爆、已装70%爆。李代主出征时主未知，张未事先说且未否隐瞒；主质张后亲去道歉/互跪承诺，李雨等此时已知仍留。不要把补知的愿留倒证当初充分知情。','- 系统李杀青霜/紫雷→红枫杀李→天堂雨杀红；北报古剑五万全归零，随后主看共享画面具体李投暗刃/魂返天空爆装、雨最后中国人含泪。晴空雪随队/归零群体覆盖，但没单独末杀死法。雪杉万、红唇十万等其他谷军命运不能自动由五万替掉。','- 清风最后是鬼撞救北、亚麻奶/林破碎压、主盾拦，主雷晕前投剑符印末杀；战神是未名刺客晕/十几人围后烛末杀。非主两次满血单挑独斩。烛战最终亲见破衣，自述迷路/荒漠近两千万杀，不把何麻将讽当实际不战。','', '## 人物、物品与资源','', '| 对象 | 本卷末可带走的状态 | 尚不等于 |','|---|---|---|','| 陆尘 | 紫郢、龙神盾、神武靴、九天离火腕已用；鬼神盾/盘龙回旋替换旧技；世界MVP选A天空 | 未得B暗月郡/C三寒武/天河资格；国战最终MVP/奖未知 |','| 何艺 | 七星枪/特兰盾、女神靴已用；1026第十一神将神斩刃，实护连调三路 | 世界队冠不等本赛所有大分胜；利润估值/合同总额不等入账 |','| 林逸欣 | 追月虎绑定、神泣新20码、女神甲已实穿；夔龙水陆实掩护 | 未与主何定多伴协议；0974藏事未知；未正式入古剑 |','| 北冥雪 | 七转、唯一追风全套/冰魄、神渊井与首骑射；指挥5000弓后损 | 格挡不免冻；井内不可伤目标，先魔免/领域可破；非每局全胜 |','| 连昕 | 转国籍/归国/绿名入会、后副职实指挥；雷杖已穿/法神握第十二飞升 | 不把全WEL提前写神将；归属不等林冲突完全无后续 |','| 李/雨/晴 | 五万古剑谷守军归零，李雨末战证据充足 | 不判现实死；恢复、赔偿和后去向未明 |','| 许阳/幽云/斗志 | 被清风/战神末段实际游戏杀；主旁核心也会死 | 不随便把未列名十三等补死 |','| 三生/千法 | 400万资源付款已达；0943改一月千骑换永久法 | 千骑尚无交付；禹瞳1057真被清风杀非全千法归原盟 |','| 神龙 | 血契幼龙1→27→83成长，国战无经验仍不到100不能骑；已有龙威 | 不能当主飞骑或已融合铠 |','| 暗月 | 国内MVP升10、复制/骑训/战鼓、1000骨龙金付巢建龙到主控 | 骨龙是城防NPC非个人坐骑；本卷国战未实测暗月受攻 |','| 龙曜 | 资源/每日500训限制；1005全会15000+铁5000+弓；野火/象/青兽连续递减 | 不用旧990弓当后全会总数；不把暂跑尸损永久除兵或敌域损当无代价 |','', '## NPC存死与历史','', '- 柏丽被李刺、奥力被主斩，父女真死；系统主杀郡主异常并列。主自承骗她，不能洗为守诺。狄5000劫宝逃西仍未追结。','- 云栈·玛法奥为神隐城国王第五子（0875面板简介），曾为卡琳珊好友由本人述；不是“王子玛法奥之子”。云栈先被主北误称死，仍呼吸/生命波动，心剖飞银小半心续命咳醒龙心骑士，飞银并未死且后来再现。回帝调七塞百万/光复特兰未落。迪奥斯真死，眼关闭未明确。','- 奥维亚0884苏斩首魂散/系统北奖；0885心带无头尸；0986明确净魂+战神血液复体成240无头骑，死后新阶段，非原没死。头卡琳说祭亡，不造接回。','- 卡兰斯0984被苏踢碎心明确死，心到未救及。苏寒刃告母火刑与卡隔离/烧盗否词分层，卡琳不知却信。母亡体修院存→相认→灵枯散/心阵救魂，反证烧母灰但不能全判卡旧史无罪。苏系统入银月、护善赎罪并拒帝国互战，只向白玫瑰附近林峡策应夜灵。','', '## 钱款、关系与行程','', '- 国内冠亚奖励实际到账与俱乐另200万/白马虚拟部800万申发未现场同等对待；李暗刃从拟售到0978持用有后证，20万欧付款未写。何1亿金币购1000骨龙实付实交，商业400亿总额不是收入。','- 主何有明确回应长吻/陪年，主林明爱牵手，乱强吻主不等主选她、主拒滚床。明/北的两女友及双收说法不是双方协定，没有本卷性生活证据。','- 主父只听首轮淘汰，读者知其没报名/七夜地铁；本书主母早亡多年，勿混纵横母离家。三生父送药与樱桃旧忆不等父亡。','- 世界赛赴洛杉矶/归上海苏州真成；后新疆扫乱姥墓真成，两房各住/表哥殴后乱求止；主诺国战稳定回苏首见林尚未行。不要以首个归国旅行替第二个返苏承诺。','', '## 交接问题和源疑点','']
for q in a['open_questions']:handoff.append(f"- {q['id']}（{q['status']}）{q['question']} {q['stage_assessment']} 证据："+','.join(e['chapter_id'] for e in q['evidence']))
handoff+=['', '主审定向修订：v05-e09井→石化边为echo，原标签保留；仅不同控制方法互照，不主张同物铺垫兑现。', '', '完整源异常保留在analysis：尤其1049作者纠方向、归属双层、擒魂CD/连续、8级会容量、仓算、WEL时长/概率/签证差。后卷研究可以追加后证，不回写本卷人物当时知道。','', '正式库仅主代理处理；未执行任何正式导入/Git/发布。九维与机制均待文学审阅，用户收藏/偏好/原创设定不自动填。','']
(H/'handoff.md').write_text('\n'.join(handoff),encoding='utf-8')
spec=importlib.util.spec_from_file_location('volume_check',H.parents[1]/'check_volume.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
result=module.load_and_check('tianxia-wushuang',5)[-1]
def scan(v):
 if isinstance(v,dict):
  if {'source_id','revision','chapter_id'}.issubset(v):assert v.get('claim_kind') in {'fact','inference','synthesis','plan'}
  for x in v.values():scan(x)
 elif isinstance(v,list):
  for x in v:scan(x)
for v in [a,c,g]:scan(v)
assert [x['chapter_id'] for x in n]==[f'ch-{i:04d}' for i in range(793,1059)]
assert not any('首2万?' in str(x) for x in n)
validation=dict(**result,review_status='draft',reader='/root/zongheng_vol04_full',chapter_notes_complete=True,unresolved_truncations=[],evidence_claim_kinds_checked=True,complete_book=False,formal_vault_written=False,literary_review='pending_primary',note='只读结构/章内定位/图闭包验证通过，不替代文学主审。')
write(H/'validation.json',validation)
files=['chapter-notes.jsonl','read-log.json','reader-state.json','analysis.json','cards.json','graph.json','report.md','handoff.md','validation.json','research-counts.json']
write(H/'delivery-freeze.json',dict(status='draft_ready_for_primary_review',source_id=a['source_id'],revision=a['revision'],body_units=265,raw_segments=266,files={f:sha(H/f) for f in files},note='输入与草稿已定；主审定向改动另记，不宣正式入库。'))
print(json.dumps(validation,ensure_ascii=False))
