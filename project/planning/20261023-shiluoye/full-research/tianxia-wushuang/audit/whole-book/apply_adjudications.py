"""只将逐项人工判断应用至保全候选，不按关键词或默认unknown冒充已审。"""
import json,pathlib,sys,collections
sys.stdout.reconfigure(encoding='utf-8');H=pathlib.Path(__file__).resolve().parent;B=H.parents[1]
read=lambda p:json.loads(p.read_text(encoding='utf-8'));source=read(B/'source.json');S={int(c['chapter_id'][3:]):c for c in source['chapters']}
def write(n,v):(H/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def E(ids):
 es=[]
 for i in sorted(set(ids)):
  c=S[i];v=c.get('volume') or next(x['volume'] for x in source['volumes'] if any(s['chapter_id']==c['chapter_id'] for u in x['units'] for s in u['segments']))
  es.append(dict(source_id=source['source_id'],revision=source['revision'],chapter_id=c['chapter_id'],start_line=c['start_line'],end_line=c['end_line'],claim_kind='fact',access_level='direct-reading-by-this-agent' if v in [5,7] else 'derived-volume-research',research_path=f'writing-vault/library/reports/tianxia-wushuang/vol{v:02d}-analysis.json'))
 return es
progress={}
for pool in ['historical','local']:
 filename='historical-question-pool.json' if pool=='historical' else 'local-question-pool.json';d=read(H/filename);lookup={r['candidate_id']:r for r in d['candidates']};seen=set()
 for batch in sorted(H.glob('adjudications-'+('history' if pool=='historical' else 'local')+'-*.json')):
  for x in read(batch):
   cid=x['candidate_id'];assert cid in lookup and cid not in seen,(batch,cid);seen.add(cid)
   assert x['status'] in ['answered','partial','unrecovered','unknown']
   lookup[cid]['terminal_assessment']=dict(status=x['status'],audit_domain=x['audit_domain'],review_progress='reviewed-draft',rationale=x['rationale'],later_evidence=E(x['later_chapters']),source_scope='本读者亲读卷五/七；其他后证来自已交付正式分卷接口，未个人重读整书。',evidence_matching_status='specific-formal-research-evidence-matched')
 d['status']='partially_adjudicated_draft' if len(seen)<len(lookup) else 'all_candidates_adjudicated_draft_pending_primary_review';write(filename,d)
 progress[pool]=dict(total=len(lookup),adjudicated=len(seen),pending=len(lookup)-len(seen),reviewed_ids=sorted(seen),statuses=dict(collections.Counter(lookup[i]['terminal_assessment']['status'] for i in seen)))
write('adjudication-progress.json',dict(status='in_progress_not_complete',pools=progress))
rows=[x for x in read(H/'historical-question-pool.json')['candidates'] if x['volume']==8]
md=['# 卷八历史线程终点评定（可先主审，待全书总审）','','只基于卷八正式人物状态/线程接口和来源定位；本读者未亲读卷八正文。其他卷全部问题正在逐项继续，尚未完成全书审计。','']
for x in rows:
 t=x['terminal_assessment'];md += [f"## {x['candidate_id']} {x['title']}",'',f"原阶段：{x['original_stage_status']}；终点：{t['status']}。{t['rationale']}",'','后证：'+', '.join(e['chapter_id'] for e in t['later_evidence']),'']
(H/'historical-reviewed-vol08.md').write_text('\n'.join(md),encoding='utf-8')
print(json.dumps({k:{kk:vv for kk,vv in v.items() if kk!='reviewed_ids'} for k,v in progress.items()},ensure_ascii=False))
