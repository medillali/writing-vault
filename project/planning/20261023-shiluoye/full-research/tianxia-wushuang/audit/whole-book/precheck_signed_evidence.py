"""最终写入前只读探查证据元数据；不裁定任何文学问题。"""
import json,hashlib,collections
from audit_evidence import H,B,source
cs={c['chapter_id']:c for c in source['chapters']};issues=[];nullable=[];count=collections.Counter()
def visit(x,where,allow_null=False):
 if isinstance(x,dict):
  if {'source_id','revision','chapter_id','start_line','end_line'}.issubset(x) or (allow_null and {'chapter_id','start_line','end_line'}.issubset(x)):
   count['reference_shapes']+=1;c=cs.get(x['chapter_id'])
   if c is None or not isinstance(x['start_line'],int) or not isinstance(x['end_line'],int) or not c['start_line']<=x['start_line']<=x['end_line']<=c['end_line']:issues.append([where,'range',x])
   for key,value in [('source_id',source['source_id']),('revision',source['revision'])]:
    if x.get(key) is None and allow_null:nullable.append(dict(path=where,key=key,before=x.get(key)))
    elif x.get(key)!=value:issues.append([where,key,x.get(key)])
   if x.get('claim_kind') not in ['fact','inference','synthesis','plan']:issues.append([where,'claim_kind',x.get('claim_kind')])
  for k,v in x.items():visit(v,where+'/'+k,allow_null)
 elif isinstance(x,list):
  for i,v in enumerate(x):visit(v,where+'/'+str(i),allow_null)
for kind in ['historical','local']:
 x=json.loads((H/f'{kind}-question-pool.json').read_text(encoding='utf-8'))
 for row in x['candidates']:visit({k:v for k,v in row.items() if k!='terminal_assessment'},row['candidate_id']+'/original',False)
p=json.loads((B/'primary-audit-review-progress.json').read_text(encoding='utf-8'))
for g in p['batches']:
 path=H/g['path'];actual=hashlib.sha256(path.read_bytes()).hexdigest()
 if actual!=g['sha256']:issues.append([g['path'],'signed_sha256_changed']);continue
 for row in json.loads(path.read_text(encoding='utf-8')):
  refs=row.get('later_evidence')
  if refs is not None:
   visit(refs,row['candidate_id']+'/later_evidence',True)
   if sorted({int(e['chapter_id'][3:]) for e in refs})!=sorted(set(row['later_chapters'])):issues.append([row['candidate_id'],'later_chapters_set'])
  else:count['references_to_build_from_signed_chapter_lists']+=len(set(row['later_chapters']))
result=dict(status='passed_metadata_precheck' if not issues else 'failed',signed_candidates=p['distinct_reviewed_candidates'],counts=dict(count),source_metadata_null_fields_to_enrich=len(nullable),metadata_null_locations=nullable,issues=issues,no_writes_to_signed_groups_or_pools=True)
(H/'preassembly-evidence-metadata-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in result.items() if k not in ['metadata_null_locations','issues']}|dict(issue_count=len(issues),issue_sample=issues[:3]),ensure_ascii=False))
