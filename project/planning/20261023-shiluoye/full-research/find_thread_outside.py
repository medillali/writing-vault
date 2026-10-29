import json,sys
from pathlib import Path
d=Path(__file__).parent/sys.argv[1]/f'vol{int(sys.argv[2]):02d}'
g=json.loads((d/'graph.json').read_text(encoding='utf-8'));E={e['id']:e for e in g['edges']}
sys.stdout.reconfigure(encoding='utf-8')
for t in g['threads']:
 for eid in t.get('edge_ids',[]):
  e=E[eid]
  if not {e['from'],e['to']}.issubset(t['node_ids']):print(json.dumps(dict(thread=t['id'],edge=eid,endpoints=[e['from'],e['to']],members=t['node_ids']),ensure_ascii=False))
