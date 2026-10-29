from pathlib import Path
import json
from build import BOOK,ROOT
U={x['unit_id']:x for x in BOOK['units']}
errors=[];ords=[];counts={k:0 for k in ['units','characters','scenes','patterns','threads','questions']}
allowed_q={'promise','misbelief','rule','anomaly','unresolved'}
def walk(x,loc):
 if isinstance(x,dict):
  if {'chapter_id','start_line','end_line'}<=x.keys():
   u=U.get(x['chapter_id'])
   if not u or not(u['start_line']<=x['start_line']<=x['end_line']<=u['end_line']):errors.append([loc,x,u])
  for k,v in x.items():walk(v,loc+'/'+k)
 elif isinstance(x,list):
  for i,v in enumerate(x):walk(v,loc+f'/{i}')
for p in sorted(ROOT.glob('batch-*.json')):
 d=json.loads(p.read_text(encoding='utf-8'));walk(d,p.name)
 for k in counts:counts[k]+=len(d[k])
 ords.extend(x['ordinal'] for x in d['units'])
 assert all(x['events'] and x['evidence'] for x in d['units'])
 assert set(d['dimensions'])==set('worldbuilding characters plot style narrative dialogue pacing themes continuity'.split())
 assert all(d['dimensions'][k] and all(x['evidence'] for x in d['dimensions'][k]) for k in d['dimensions'])
 assert all(x['evidence'] for k in ['characters','scenes','patterns','threads'] for x in d[k])
 for q in d['questions']:
  if q['kind'] not in allowed_q:errors.append([p.name,q['key'],'invalid question kind',q['kind']])
 assert len(d['scenes'])>=3 and len(d['patterns'])>=2
 assert all(s['goal'] and s['obstacle'] and s['choice'] and s['consequence'] and s['state_change'] and s['why_it_works'] and s['applicability'] and s['failure_mode'] for s in d['scenes'])
assert ords==list(range(1,194)),ords
hp=ROOT/'handoff-to-second-half.json'
if hp.exists():walk(json.loads(hp.read_text(encoding='utf-8')),hp.name)
report={'source_id':BOOK['source_id'],'expected_range':[1,193],'saved_ordinals':ords,'counts':counts,'evidence_errors':errors,'status':'pass' if not errors else 'fail','scope':'结构与证据行界审计，不声称自动证明研究解释正确'}
(ROOT/'audit-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'counts':counts,'errors':errors,'metadata':{k:BOOK[k] for k in ['source_id','revision','normalized_path']},'boundary_units':BOOK['units'][192:194]},ensure_ascii=False))
