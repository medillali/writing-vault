import pathlib,json,sys
sys.stdout.reconfigure(encoding='utf-8')
b=pathlib.Path(__file__).parent/'zongheng-tianxia/vol08'
def compact(x):
 if isinstance(x,list):return [compact(i) for i in x]
 if isinstance(x,dict):
  if {'source_id','revision','chapter_id'}.issubset(x):return x['chapter_id']+':'+str(x.get('start_line'))
  return {k:compact(v) for k,v in x.items()}
 return x
for name,key in [('character-arc-audit-draft.json','characters'),('end-state-audit-draft.json','findings'),('historical-question-pool.json','candidates'),('local-question-pool.json','candidates')]:
 a=json.loads((b/name).read_text(encoding='utf-8'))
 for x in a[key]:
  if any(t in json.dumps(x,ensure_ascii=False) for t in ['邱华','龙神','CGL']):
   print(name,json.dumps(compact(x),ensure_ascii=False))
