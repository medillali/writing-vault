import json,sys
from audit_evidence import H
sys.stdout.reconfigure(encoding='utf-8')
for p in list(H.glob('character-arcs-part*.json'))+list(H.glob('focused-findings-part*.json')):
 x=json.loads(p.read_text(encoding='utf-8'))
 for r in x.get('characters',x.get('findings',[])):
  for k,v in r.items():
   if isinstance(v,str) and any(s in v for s in ['未判','判刑','公审','终身监禁']):print(p.name,r.get('audit_id',r.get('key')),k,v)
   if isinstance(v,list) and k=='stage_chain':
    for s in v:
     if any(t in s for t in ['未判','判刑','公审','终身监禁']):print(p.name,r.get('key'),k,s)
