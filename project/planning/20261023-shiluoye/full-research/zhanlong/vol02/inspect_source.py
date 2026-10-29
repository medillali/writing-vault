import json,pathlib,sys,hashlib
sys.stdout.reconfigure(encoding='utf-8')
V=pathlib.Path(__file__).resolve().parent;B=V.parent;R=V.parents[4]
s=json.loads((B/'source.json').read_text(encoding='utf-8'))
print('SOURCE',{k:v for k,v in s.items() if k not in ['chapters','volumes']})
for n in [2,5]:
 v=next(v for v in s['volumes'] if v['volume']==n)
 print('VOLUME',n,{k:val for k,val in v.items() if k!='units'})
 print('UNITS_COUNT',len(v['units']),'FIRST',v['units'][0],'LAST',v['units'][-1])
 print('NONSTANDARD_UNITS',[u for u in v['units'] if len(u['segments'])!=1 or u.get('kind') not in [None,'body']])
 print('SEGMENTS',[(u.get('unit_id'),u.get('kind'),[x['chapter_id'] for x in u['segments']]) for u in v['units'][:3]])
p=R/'writing-vault/library/reports/collection/reading-units.json';x=json.loads(p.read_text(encoding='utf-8'))
print('READING_UNITS_TOP',list(x) if isinstance(x,dict) else type(x).__name__)
def find(value,path):
 if isinstance(value,dict):
  if value.get('source_id')==s['source_id']:
   print('COLLECTION_MATCH',path,{k:v for k,v in value.items() if k not in ['units','volumes','chapters','reading_units']})
   print('COLLECTION_FIELDS',[(k,len(v) if isinstance(v,(list,dict)) else str(v)[:200]) for k,v in value.items()])
  for k,v in value.items():find(v,path+'/'+str(k))
 elif isinstance(value,list):
  for i,v in enumerate(value):find(v,path+'/'+str(i))
find(x,'')
print('HASHES',hashlib.sha256((B/'source.json').read_bytes()).hexdigest(),hashlib.sha256(p.read_bytes()).hexdigest())
