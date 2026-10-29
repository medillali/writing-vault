import json, pathlib, hashlib,sys
sys.stdout.reconfigure(encoding='utf-8')
p=pathlib.Path(__file__).parent/'zhanlong/vol04'; b=p/'primary-delta/before'
for n in ['reader-state.json','handoff.md']:
 print(n,hashlib.sha256((b/n).read_bytes()).hexdigest(),hashlib.sha256((p/n).read_bytes()).hexdigest())
 if n.endswith('.json'):
  a=json.loads((b/n).read_text(encoding='utf-8'));z=json.loads((p/n).read_text(encoding='utf-8'))
  for k in set(a)|set(z):
   if a.get(k)!=z.get(k): print(k,json.dumps({'before':a.get(k),'after':z.get(k)},ensure_ascii=False))
