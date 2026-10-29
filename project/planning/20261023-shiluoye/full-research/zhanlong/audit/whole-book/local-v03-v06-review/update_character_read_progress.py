from pathlib import Path
import json
H=Path(__file__).resolve().parent;A=H.parent;p=A/'character-arc-reading-progress.json'
d=json.loads(p.read_text(encoding='utf-8'))
for x in d['read_scope']:
 if x['path'].endswith('vol04-cards.json'):x['scope']='全部45人物卡完整content及全部证据，1—5/6—14/15—23/24—32/33—39/40—45，无截断'
 if x['path'].endswith('vol05-cards.json'):x['scope']='全部56人物卡完整content及全部证据，1—4/5—13/14—22/23—32/33—42/43—50/51—56，无截断；后三组compactcards仅去排版空白而无字段删减'
 if x['path'].endswith('vol06-cards.json'):x['scope']='全部32人物卡完整content及全部证据，本轮1—3/4—12/13—22/23—32再接读，无截断；本人原始全卷实读另保'
d['groups_delivered'].append(dict(path='character-arcs-part02.json',ids=['character-arc-004','character-arc-005','character-arc-006'],json_sha256='1beb29e39d3e3de9a4a6168fa3c1a89217af561c2c479f03854bae7ce0a0922c',status='stable_draft_delivered_pending_primary'))
d['observations'] += ['卷三全部50与卷四45/卷五56/卷六32人物已完整接读。罗林833问剑系统末刀、霜1174归功回顾分；NPC落海与洛克林、玩家/NPC冉闵、傅雷/弗雷、龙忠/龙硎、百里若风/百里伦分实体。','王翦734已称星痕男友，不能停在500秦雨暂拒；狐早刘庸/后慕天需保姓名源差不任一方覆盖。纸与方1358已明确交往/副盟，自述渠道不能仍只写卷五未任。','卷六机关、军务与终点分层：子舒右臂1360实再生，龙硎1380臂骨折非截肢；佩魂复苏/西瓦娜借体分意志，沧吞魂链按石报和主后沿用，不作希本人亲承。']
d['pending']='全部六卷271张人物卡已接读；继续阶段states/正式优先层及必要定向源，覆盖近名/军政/现实组织后分稳定组交付，总稿最后逐值装配。'
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
