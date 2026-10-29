import json,copy,hashlib
from audit_evidence import H,evidence
p=H/'focused-findings-part02.json';before=json.loads(p.read_text(encoding='utf-8'));after=copy.deepcopy(before);changes=[]
for r in after['findings']:
 old=copy.deepcopy(r)
 if r['key']=='citizenship-and-restoration':
  r['stage_chain'][2]='1194天空城君主分离七日不可用、1202仍四日待入；1221系统卡琳珊九军已重返/城归中国，不能把待入阶段停留到终点。神隐重建/云栈册封另为官网报道。'
  r['evidence']=evidence([int(e['chapter_id'][3:]) for e in r['evidence']]+[1221])
 elif r['key']=='final-war-city-outcomes':
  r['stage_chain'][0]='1580林明说燕耳君主已杀并选择废城；林、清风破／林凡、小小猪等完成残局，陆到场时已结束，不将国战写成赛事或抹其他参战者。'
 elif r['key']=='organization-agreements-and-nonreceipts':
  r['stage_chain'][0]='888商议、889定千法两周借约、890四类资源各一百万实际交；943改不用归还换一个月内一千龙曜训练，新约已成交，不能沿旧两周必还。'
  r['evidence']=evidence([int(e['chapter_id'][3:]) for e in r['evidence']]+[888,889,890])
 if old!=r:changes.append(dict(key=r['key'],before=old,after=copy.deepcopy(r),changed_fields=[k for k in old if old[k]!=r[k]]))
assert len(changes)==3
assert all(a==b for a,b in zip(before['findings'],after['findings']) if a['key'] not in {c['key'] for c in changes})
(H/'reviewed-batches/focused-findings-part02-before-late-receipts.json').write_bytes(p.read_bytes());p.write_text(json.dumps(after,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lines=['# 无双终点重点第二组18项（待主审）','','依据八卷正式研究与必要派生接口；本代理亲读仅卷五/七，未个人重新阅读全文。','']
for x in after['findings']:
 lines+=['## '+x['key']+' '+x['title'],'','终点类型：'+x['terminal_status'],'']+[f'- {s}' for s in x['stage_chain']]+['','结论：'+x['conclusion'],'','限制与反证：'+x['limits_and_counterevidence'],'','证据raw：'+', '.join(e['chapter_id'][3:] for e in x['evidence']),'']
(H/'focused-findings-part02.md').write_text('\n'.join(lines),encoding='utf-8')
x=dict(status='draft_group_targeted_corrections_pending_primary_signature',changes=changes,before_sha256=hashlib.sha256((H/'reviewed-batches/focused-findings-part02-before-late-receipts.json').read_bytes()).hexdigest(),after_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),other_15_objects_unchanged=True)
(H/'focus02-late-receipts-and-stage-delta.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(x['after_sha256'])
