from pathlib import Path
import json,sys
sys.stdout.reconfigure(encoding='utf-8')
root=Path('.verify/tree-maps-20261025/library/reports/two-books-full-20261025')
for folder in ('zeidan','leveling'):
    g=json.loads((root/folder/'plot/graph.json').read_text(encoding='utf-8'))
    print(folder,list(g))
    print(json.dumps(next(n for n in g['nodes'] if n['kind']=='scene'),ensure_ascii=False,indent=2))
    print(json.dumps(next(n for n in g['nodes'] if n['kind']=='arc'),ensure_ascii=False,indent=2)[:1000])
print((root/'sources.json').read_text(encoding='utf-8')[:1800])
