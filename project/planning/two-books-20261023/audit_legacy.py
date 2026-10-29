from pathlib import Path
import json,collections,subprocess
R=Path(__file__).resolve().parents[2]
D=R.parent/'Chinese Novel/books/zeidan/distillation'
data=json.loads((D/'entities.json').read_text(encoding='utf-8'))
print('DEPTH',collections.Counter(x.get('maintenance_depth') for x in data))
for x in data:
    if '候选' in json.dumps(x,ensure_ascii=False) or '仅出场' in json.dumps(x,ensure_ascii=False):
        print('CANDIDATE',json.dumps(x,ensure_ascii=False)[:900]);break
graph=next((R/'writing-vault/library/sources').glob('*/plot-graph.json'))
g=json.loads(graph.read_text(encoding='utf-8'))
print('GRAPH_SAMPLE',json.dumps({'coverage':g.get('coverage'), 'nodes':g['nodes'][:3], 'edges':g['edges'][:1], 'threads':g['threads'][:1]},ensure_ascii=False)[:6500])
