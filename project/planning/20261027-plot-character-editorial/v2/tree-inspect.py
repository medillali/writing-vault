from pathlib import Path
import json
from collections import Counter

base = Path(__file__).resolve().parents[3]
g = json.loads((base/'writing-vault/library/sources/src-2a13958390274509b2af019f6b12d981/plot-graph.json').read_text(encoding='utf-8'))
print('ROOT',list(g))
print('KINDS',Counter(n['kind'] for n in g['nodes']))
print('EDGEKINDS',Counter(e['kind'] for e in g['edges']))
ns={n['id']:n for n in g['nodes']}
print('SAMPLES',json.dumps(g['nodes'][:8],ensure_ascii=False))
print('EDITORIAL_THREADS',json.dumps([t for t in g['threads'] if t['id'].startswith('editorial')],ensure_ascii=False,indent=2))
print('GROUP_EDGE_ENDPOINTS',json.dumps([{k:e[k] for k in ['id','kind','from','to','label']} for e in g['edges'] if any(ns[e[k]]['kind'] not in ['event','scene'] for k in ['from','to'])],ensure_ascii=False))
print('ORDER_SAMPLE',[(n['id'],n.get('narrative_order'), min([e['chapter_id'] for e in n.get('evidence',[])],default='')) for n in g['nodes'] if n['kind'] in ['event','scene']][:30])
(base/'.planning/20261027-plot-character-editorial/v2/tree-source-summary.json').write_text(json.dumps({'events':[{k:n.get(k) for k in ['id','title','kind','narrative_order','parent_id']} for n in g['nodes'] if n['kind'] in ['event','scene']],'threads':g['threads'],'edges':[{k:e[k] for k in ['id','kind','from','to','label']} for e in g['edges']]},ensure_ascii=False,indent=2),encoding='utf-8')
guide='v1-poor,v1-team,v1-v1c12,v1-v1c39,v2-move,v2-zero,v2-return,v3-v03-token,v3-v03-reject_bet,v4-v04-exile,v4-v04-firstcity,v4-v04-hushou,v5-v05-scene-korea,v6-v06-scene-dragon-gate,v6-v06-scene-china-final,v6-v06-scene-defend-capital,v6-v06-scene-refuse-duke,v7-v07-relevel,v7-v07-qingfeng,v7-v07-split,v7-v07-destroy,v7-v07-industry,v7-v07-aryan,v7-v07-dal,v8-v08-father,v8-v08-bloodroar,v8-v08-sacrifice,v8-v08-wsl,v8-v08-cleanse,v8-v08-endbattle,v8-v08-after'.split(',')
print('GUIDE_CANDIDATES',json.dumps([{k:n.get(k) for k in ['id','title','narrative_order','evidence']} if (n:=ns.get(i)) else {'MISSING':i} for i in guide],ensure_ascii=False))
