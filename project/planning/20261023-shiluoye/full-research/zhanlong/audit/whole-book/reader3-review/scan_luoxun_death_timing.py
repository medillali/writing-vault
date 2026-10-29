"""只定位受影响串，人工审读后才提出最小字段更正。"""
from character_arc_common import *
def walk(x,path=()):
 if isinstance(x,dict):
  for k,v in x.items():yield from walk(v,path+(k,))
 elif isinstance(x,list):
  for i,v in enumerate(x):yield from walk(v,path+(i,))
 elif isinstance(x,str):yield path,x
targets=[]
for base in [F,B/'vol05']:
 for p in base.iterdir():
  if p.is_file() and (p.name.endswith('.json') or p.suffix=='.md'):targets.append(p)
for p in [ROOT/'writing-vault/library/characters/chr-f2d8afcb79655bbb9b0f2314268e7810.json',ROOT/'writing-vault/library/views/chr-f2d8afcb79655bbb9b0f2314268e7810.md']:targets.append(p)
hits=[]
for p in dict.fromkeys(targets):
 if p.suffix=='.json':
  try:items=walk(json.loads(p.read_text(encoding='utf-8')))
  except Exception:continue
 else:items=((('line',i),s) for i,s in enumerate(p.read_text(encoding='utf-8').splitlines(),1))
 for pointer,value in items:
  if '999' in value and ('自刎' in value or '洛洵' in value):hits.append({'path':str(p.relative_to(ROOT)).replace('\\','/'),'sha256':sha(p),'field_path':list(pointer),'value':value})
dump(P/'luoxun-timing-string-hits.json',hits)
print('FIELDS',len(hits))
for i,x in enumerate(hits,1):print(i,json.dumps(x,ensure_ascii=False))
terminal=[]
for p in [A/'historical-question-pool.json',A/'local-question-pool.json']:
 a=json.loads(p.read_text(encoding='utf-8'))
 for c in a['candidates']:
  t=c.get('terminal_assessment',{});s=json.dumps(t,ensure_ascii=False)
  if '999' in s and ('自刎' in s or '洛洵' in s):terminal.append({'pool':p.name,'candidate_id':c['candidate_id'],'terminal':t})
dump(P/'luoxun-terminal-timing-candidate-hits.json',terminal)
print('TERMINALS',len(terminal))
for x in terminal:print(json.dumps(x,ensure_ascii=False))
