"""只写修订提案与before，不修改已预审核心。"""
import json,hashlib,copy
from pathlib import Path
P=Path(__file__).parent;Q=P/'continuity-proposal';Q.mkdir(exist_ok=True)
raw=(P/'analysis.json').read_bytes();A=json.loads(raw)
assert not (Q/'analysis.before.json').exists(), '提案before已存在，禁止覆盖'
(Q/'analysis.before.json').write_bytes(raw)
OLD=A['dimensions']['continuity'];NEW=copy.deepcopy(OLD)
changes=[
 ('旧物后用与延迟交付让力量成长可被期待',
  OLD[0]['textual_fact'],
  '早得的盔、链和炮隔场才发挥作用，读者能从持有的资源期待下一次用途；重铸又使旧武器的积累延续。现实和游戏两把蝴蝶通过不同材料、价币、制作与试用分开，同名因此形成呼应而非同一物凭空跨界。',
  '先给物件可辨的取得与条件，让它在稍后一个真正需要的场景显效；过渡时间可以省略，但关键使用会重新唤起旧期待。同名物要以具体制作过程和作用对象分流，避免借名称偷换战绩。',
  '954丈八只是交一秒，不能像781紫链实用一样说已经发挥；酒10级仍缺仙人果，知识达到不等产物到手。968将无攻镇国刀作火神矛比较对象存在原称疑点，不能用呼应替它圆成镇岳。'),
 ('永久死亡、伤后归来与补员维持不同的损失重量',
  OLD[1]['textual_fact'],
  '死亡后有尸、棺、墓或空缺，后场不能轻易抹去读者已承受的失落；负伤者再出现则允许关系延续。大军后来补足人数只恢复组织规模，不能把唐麟、罗特等具体人的位置和记忆一起还原。',
  '让真死后留下葬礼、职缺和幸存者行为变化；让伤者归来保留可见余损，再以新人的不同身份恢复组织能力。个人生命和总兵力分开承受后果，战争的胜利便不会抵消全部哀痛。',
  '主842闭眼的濒死叙述随后843醒来，不能按真死亡制造复生；罗嗣断腕后可继续行动也不等断肢已恢复。百里伦861系统死后又现且885再斩，没有解释的重复不能擅当复活规则。'),
 ('身份揭晓重估旧关系，推测仍停在视角边界',
  '915抹茶夺城、亲杀旧友并显神话身份；916林小舞揭薛柔即小妖、林婉儿说明薛景亲缘，960明确堂姐妹，并非抹向主当面完整坦白。北辰风是问剑称；唐古挡剑与唐琦六爻是分人动作。林成活归为旧师，主亲生父母仍幼时失踪；裴涉案只有警方怀疑。',
  '读者在已付出信任和共同战斗之后获知另一身份，旧行动因此出现第二层意义；文本又让方的召回解释、主的怨与后来的修正并存，避免一项揭晓替所有未见动机下结论。',
  '先让读者看见会损害关系的行动，再由各知情者补身份与有限解释；让主能承认先前过推而不抹已发生伤害。新名字改变对旧关系的理解，却不能自动吞掉角色自己作的每个决定。',
  '946爱主只是方猜，956主承方未强逼交城，不能写本人告白或方逐步命夺。沈用凯瑞/裴用Andy是掩护接触，未证全部刑案；968白墨颜只有本书当前角色信息，不由同名获得别书履历。'),
 ('承诺在不同动作中兑现，也可以明确失败或仍向未来敞开',
  OLD[3]['textual_fact'],
  '兰馨的营救在系统完成处给即时释放，粮运则隔着袭粮危机直到报到才使前段担心回落；五千降俘处死让不杀诺以失败落地。神殿首批返军又把完成与未完成叠在同一结果里，使希望向后延伸而不假装全部团圆。',
  '为承诺安排性质相称的回声：护人以活返，运输以到达，长期训练以分批归队；在回收时保留之前的危险和代价。需要延长时先付出真实部分，让读者知道等待改变了什么，而非每次只推迟最后答复。',
  '879夏侯仁亲报粮到已能回应护运，不必重复卸粮镜；958两千返中仅200准骑/1800强普不能算余8000也回。960找薛柔和966仙人醉仍缺具体结果，不能用同类新成功替代。')]
for i,(title,fact,observation,mechanism,limits) in enumerate(changes):
 NEW[i].update(title=title,textual_fact=fact,observation=observation,mechanism=mechanism,limits_and_counterevidence=limits)
 assert NEW[i]['evidence']==OLD[i]['evidence'] and NEW[i]['interpretation_evidence']==OLD[i]['interpretation_evidence']
proposal={'status':'proposed-awaiting-primary','scope':'仅continuity四项五个文字字段；其他32项及证据不动','analysis_before_sha256':hashlib.sha256(raw).hexdigest(),'changes':[{'id':a['id'],'before':a,'after':b} for a,b in zip(OLD,NEW)]}
(Q/'before-after.json').write_text(json.dumps(proposal,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lines=['# 卷四连续性九维精确修订提案','','状态：待primary审核，核心analysis未改。before SHA：`'+proposal['analysis_before_sha256']+'`。原事实/证据保留，只有第3项事实按915行动/916揭晓/960亲缘澄清。','']
for x in proposal['changes']:
 lines+=['## '+x['id'],'']
 for k in ['title','textual_fact','observation','mechanism','limits_and_counterevidence']:
  lines+=['### '+k,'','旧：'+x['before'][k],'','拟：'+x['after'][k],'']
(Q/'before-after.md').write_text('\n'.join(lines),encoding='utf-8')
print(json.dumps({'before':proposal['analysis_before_sha256'],'proposal':hashlib.sha256((Q/'before-after.json').read_bytes()).hexdigest(),'path':str(Q)},ensure_ascii=False))
