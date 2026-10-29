from synthesis_common import *
q=json.loads((B.parent/'tianxia-wushuang/book-synthesis-draft.json').read_text(encoding='utf-8'))
print('SCHEMA TOP')
for k,v in q.items():
 if k not in ['dimensions','upstream_documents']:print(k,json.dumps(v,ensure_ascii=False))
print('SOURCE VOLUMES',json.dumps([{k:v for k,v in x.items() if k!='units'}|{'first_raw':x['units'][0]['segment_ids'][0],'last_raw':x['units'][-1]['segment_ids'][-1]} for x in S.get('volumes',[])],ensure_ascii=False))
print('LOG KEYS')
for n in range(1,7):
 p=F/f'vol{n:02d}-read-log.json';a=json.loads(p.read_text(encoding='utf-8'));print(n,type(a).__name__,list(a) if isinstance(a,dict) else len(a));print(json.dumps({k:v for k,v in a.items() if k not in ['chapters','entries','batches','read_entries']},ensure_ascii=False));print('FIRST',json.dumps(a['chapters'][0],ensure_ascii=False))
