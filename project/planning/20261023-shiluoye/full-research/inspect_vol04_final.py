import json, pathlib, sys
sys.stdout.reconfigure(encoding='utf-8')
p=pathlib.Path(__file__).parent/'zhanlong/vol04'
for name in ['primary-delta/application-receipt.json','primary-delta/equipment-edge-delta.json','primary-extra-proposal.json','continuity-proposal/before-after.json']:
 o=json.loads((p/name).read_text(encoding='utf-8'))
 print(name, 'keys', list(o))
 for key in ['deltas','changes']:
  if key in o:
   for r in o[key]:print(key, {k:(list(v) if isinstance(v,dict) else len(v) if isinstance(v,list) else str(v)[:200]) for k,v in r.items()})
print('before', [q.name for q in (p/'primary-delta/before').iterdir()])
o=json.loads((p.parent/'vol04-primary-review-progress.json').read_text(encoding='utf-8'))
print('progress',o.keys())
for r in o['batches']:print(r)
