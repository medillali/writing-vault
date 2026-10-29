import json,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
R=Path(__file__).parent
P=json.loads((R/'historical-question-pool.json').read_text(encoding='utf-8'));D=json.loads((R/'local-terminal-decisions.json').read_text(encoding='utf-8')) if (R/'local-terminal-decisions.json').exists() else {}
out=[]
v7_atomic={
1:['805/806、938/939、940/941、946/947、957/958是独立正文，章号/片段计数不得机械换算。','941/944结算末行敌名误写魂。','894花火/冰之逸的气旋与龙错称。'],
2:['冰之逸220被写已穿225战神。','淬火750万资格在书旧633万面板后未交代增量而实际戴。','1055声望1275050低于达尔1200万奖励，不擅补位。'],
3:['遗迹2小时与两天王刷新口径不同。','零度皮胸拟给雨后给紫月。','灵恸项链披风后称靴。','剑飞扬本战死后仍受令。','围城损失每秒3与每小时3。'],
4:['现实七名涉案人是否全死：无确证的三人只是失踪。','红绫亲自刺杀血饮只是书生推测。','郑家主使报复为凌天归因，非警方结案。','孤坟带荀方是否意在政治压雪只有书生猜测。'],
5:['金窟静刃头尚未见明确交矿工任务。','青云2000万元报酬实付并入领地资产，逐人分配未展示。','梦回让黄金级据点曙光要塞的200万元补偿到凌月，尚未展示逐人到账及次日弃点。','天域凭证275门槛，卷七末未用。']}
for g in P['local_issue_records']:
 for ri,r in enumerate(g['original_records']):
  issues=r.get('issues',[r.get('text',r.get('issue',r.get('note',r.get('fact_or_boundary',''))))])
  if g['volume']==7:issues=v7_atomic[ri+1]
  for j,t in enumerate(issues):
   if not t:continue
   k=f"v{g['volume']:02}-local-{ri+1:03}-{j+1:02}"
   out.append(dict(candidate_id=k,volume=g['volume'],original_path=g['path'],original_field=g['field'],original_index=ri,atomic_index=j,original_record=r,title=t,original_evidence=r.get('evidence',[]),terminal_assessment=D.get(k,dict(status='unknown',review_progress='pending-manual-adjudication',rationale='待逐条核，不能据未查判未回收',later_evidence=[],depends_on_volumes=[]))))
(R/'local-question-pool.json').write_text(json.dumps(dict(status='draft',scope='各卷混合未决/异常字段逐条展平，人物/任务问与纯源异文分开评',candidates=out),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lines=['# 地方未明问题与源异常逐项审计（草稿）','','本表逐项保留八卷正式研究的混合字段，不将它们一概沿用为终点open。source_anomaly只是源文异常处置，不代表剧情漏收；unknown须按audit_domain及具体判断区分证据/认知边界，不等整卷未读。','','| ID | 原问题 | 类型 | 终点判断 | 依据/待核 |','|---|---|---|---|---|']
for n in out:
 d=n['terminal_assessment'];lines.append('| '+' | '.join(str(x).replace('|','／') for x in [n['candidate_id'],n['title'],d.get('audit_domain','pending'),d['status'],d['rationale']])+' |')
(R/'local-question-pool.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
a=int(sys.argv[1]) if len(sys.argv)>1 else 0;b=int(sys.argv[2]) if len(sys.argv)>2 else len(out)
print('total',len(out))
for n in out[a:b]:print(n['candidate_id'],n['title'])
