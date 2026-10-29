import json,pathlib,sys
sys.stdout.reconfigure(encoding='utf-8')
b=pathlib.Path(__file__).parent/'zongheng-tianxia/vol08'
for name,key in [('character-arc-audit-draft.json','characters'),('end-state-audit-draft.json','findings'),('historical-question-pool.json','candidates'),('local-question-pool.json','candidates')]:
 a=json.loads((b/name).read_text(encoding='utf-8'))
 print(name,'ROOT',list(a),'COUNT',len(a[key]))
 print('FIRST',json.dumps(a[key][0],ensure_ascii=False))
 if name.startswith('historical'):
  print('THREAD',json.dumps(next(x for x in a[key] if 'thread' in str(x.get('entry_type',''))),ensure_ascii=False))
 if key=='characters':
  for x in a[key]:print('IDENTITY',json.dumps({k:x.get(k) for k in ['audit_id','name','title','identity_names','aliases','identity_boundary','identity_notes','character_assets'] if k in x},ensure_ascii=False))
