from pathlib import Path
import json
from build import BOOK,ROOT
U={x['unit_id']:x for x in BOOK['units']}
errors=[]; ords=[]; counts={k:0 for k in ['units','characters','scenes','patterns','threads','questions']}
def walk(x,loc):
 if isinstance(x,dict):
  if {'chapter_id','start_line','end_line'}<=x.keys():
   u=U.get(x['chapter_id'])
   if not u or not(u['start_line']<=x['start_line']<=x['end_line']<=u['end_line']):errors.append({'location':loc,'evidence':x,'unit_bounds':None if not u else [u['start_line'],u['end_line']]})
  for k,v in x.items():walk(v,loc+'/'+k)
 elif isinstance(x,list):
  for i,v in enumerate(x):walk(v,loc+f'/{i}')
for p in sorted(ROOT.glob('batch-*.json')):
 d=json.loads(p.read_text(encoding='utf-8'));walk(d,p.name)
 for k in counts:counts[k]+=len(d[k])
 ords.extend(x['ordinal'] for x in d['units'])
 if [x['ordinal'] for x in d['units']]!=list(range(d['unit_start'],d['unit_end']+1)):errors.append([p.name,'unit order'])
 if not all(x['events'] and x['evidence'] for x in d['units']):errors.append([p.name,'unit records missing'])
 if set(d['dimensions'])!=set('worldbuilding characters plot style narrative dialogue pacing themes continuity'.split()):errors.append([p.name,'nine dimensions'])
 if not all(d['dimensions'][k] and all(x['evidence'] for x in d['dimensions'][k]) for k in d['dimensions']):errors.append([p.name,'dimension evidence'])
 if not all(x['evidence'] for k in ['characters','scenes','patterns','threads'] for x in d[k]):errors.append([p.name,'card evidence'])
 for q in d['questions']:
  if q['kind'] not in {'promise','misbelief','rule','anomaly','unresolved'}:errors.append([p.name,q['key'],'invalid question kind',q['kind']])
  if q['status'] not in {'open','partial','resolved','unknown','abandoned'}:errors.append([p.name,q['key'],'invalid question status',q['status']])
 if len(d['scenes'])<3 or len(d['patterns'])<2:errors.append([p.name,'scene or pattern count'])
 if not all(s['goal'] and s['obstacle'] and s['choice'] and s['consequence'] and s['state_change'] and s['why_it_works'] and s['applicability'] and s['failure_mode'] for s in d['scenes']):errors.append([p.name,'scene fields'])
if ords!=list(range(391,464)):errors.append(['coverage',ords])
for name in ['ending-audit.json','read-coverage.json']:
 p=ROOT/name
 if p.exists():walk(json.loads(p.read_text(encoding='utf-8')),name)
report={'source_id':BOOK['source_id'],'expected_range':[391,463],'saved_ordinals':ords,'counts':counts,'evidence_errors':errors,'status':'pass' if not errors else 'fail','scope':'结构、问题枚举与证据章节行界审计；不声称自动证明研究解释正确'}
(ROOT/'audit-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'status':report['status'],'counts':counts,'evidence_errors':errors,'metadata':{k:BOOK[k] for k in ['source_id','revision','normalized_path']}},ensure_ascii=False))
