import json,pathlib,sys
sys.stdout.reconfigure(encoding='utf-8');H=pathlib.Path(__file__).resolve().parent
for p in list(H.glob('adjudications*.json'))+list(H.glob('character-arcs*.json')):
 d=json.loads(p.read_text(encoding='utf-8'));rows=d if isinstance(d,list) else d.get('characters',[])
 for x in rows:
  for k,v in x.items():
   if isinstance(v,str) and any(t in v for t in ['母离开','母亲离开','母亲离家','陆母','扫母墓']):print(p.name,x.get('candidate_id',x.get('audit_id')),k,v)
