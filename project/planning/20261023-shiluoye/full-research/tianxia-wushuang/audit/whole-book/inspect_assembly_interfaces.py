import json,sys,hashlib,collections
from audit_evidence import H,B,R
sys.stdout.reconfigure(encoding='utf-8')
for name in ['primary-audit-review-progress.json','primary-research-group-review-progress.json','review-vol08.json']:
 p=B/name;x=json.loads(p.read_text(encoding='utf-8'));print(name,'KEYS',list(x))
 if 'batches' in x:
  print('BATCHES',len(x['batches']),'COUNT',sum(y['count'] for y in x['batches']),'FIRST',x['batches'][0],'LAST',x['batches'][-1])
  p2=H/x['batches'][0]['path'];y=json.loads(p2.read_text(encoding='utf-8'));print('SAMPLE_ROW',json.dumps(y[0],ensure_ascii=False)[:6000])
 if 'groups' in x:print('GROUPS',[(y['path'],y['count'],y['sha256']) for y in x['groups']])
 if name=='review-vol08.json':print(json.dumps(x,ensure_ascii=False)[:7000])
for name in ['historical-question-pool.json','local-question-pool.json']:
 x=json.loads((H/name).read_text(encoding='utf-8'));print(name,'KEYS',list(x),'ROWKEYS',list(x['candidates'][0]))
print('V8FILES',[p.name for p in (B/'vol08').iterdir() if p.is_file()])
