from save_batch import *
import sys
sys.stdout.reconfigure(encoding='utf-8')
idx={u['unit_id']:u for u in BOOK['units']}
errors=[]
def check(v,path):
 if isinstance(v,dict):
  if {'chapter_id','start_line','end_line'}<=v.keys():
   u=idx.get(v['chapter_id'])
   if not u or not (u['start_line']<=v['start_line']<=v['end_line']<=u['end_line']):errors.append((path,v,None if not u else [u['start_line'],u['end_line']]))
  for k,x in v.items():check(x,path+'/'+k)
 elif isinstance(v,list):
  for i,x in enumerate(v):check(x,path+'/'+str(i))
for f in P.glob('*.json'):check(json.loads(f.read_text(encoding='utf-8')),f.name)
print(json.dumps(errors,ensure_ascii=False,indent=2));print('errors',len(errors))
