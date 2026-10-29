import json,pathlib,sys
sys.stdout.reconfigure(encoding='utf-8');H=pathlib.Path(__file__).resolve().parent
g=json.loads((H.parent/'vol05/graph.json').read_text(encoding='utf-8'))
print(json.dumps(g['nodes'][10],ensure_ascii=False))
lines=(H.parent/'vol05/build_research.py').read_text(encoding='utf-8').splitlines()
print('\n'.join(lines[245:271]))
