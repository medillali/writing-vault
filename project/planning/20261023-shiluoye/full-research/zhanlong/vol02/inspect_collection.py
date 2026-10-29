import json,pathlib,sys
sys.stdout.reconfigure(encoding='utf-8');V=pathlib.Path(__file__).resolve().parent;R=V.parents[4]
x=json.loads((R/'writing-vault/library/reports/collection/reading-units.json').read_text(encoding='utf-8'))['src-20f2d16e3d1b472fa4b230ab0e1770c9']
print('ENTRY',type(x).__name__)
if isinstance(x,dict):
 print('FIELDS',[(k,len(v) if isinstance(v,(dict,list)) else v) for k,v in x.items()])
 for k,v in x.items():
  if isinstance(v,list):print(k,'FIRST',v[:2],'NON_SINGLE',[u for u in v if isinstance(u,dict) and len(u.get('segments',[]))>1])
elif isinstance(x,list):print('COUNT',len(x),'FIRST',x[:2],'NON_SINGLE',[u for u in x if isinstance(u,dict) and len(u.get('segments',[]))>1])
