import pathlib,json,sys
sys.stdout.reconfigure(encoding='utf-8')
root=pathlib.Path('writing-vault')
print('root',root.resolve(),root.exists())
print('children',[x.name for x in root.iterdir()])
for p in root.rglob('*.json'):
 if '.git' in p.parts or 'private-sources' in p.parts: continue
 try: d=json.loads(p.read_text(encoding='utf-8-sig'))
 except Exception: continue
 if isinstance(d,dict) and (d.get('owner_id')=='src-2a13958390274509b2af019f6b12d981' or ('nodes' in d and '2a139583' in str(d))):
  print('GRAPH',str(p),json.dumps(d,ensure_ascii=False))
PY=pathlib.Path('distill-novels/scripts/library.py').read_text(encoding='utf-8').splitlines()
for i,l in enumerate(PY):
 if 'def validate_graph' in l or 'ASSET_TYPES' in l or 'GRAPH_' in l: print(i+1,l)
