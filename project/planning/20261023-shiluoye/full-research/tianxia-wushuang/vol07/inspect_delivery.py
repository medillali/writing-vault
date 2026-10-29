import json,pathlib,sys
sys.stdout.reconfigure(encoding='utf-8')
H=pathlib.Path(__file__).resolve().parent
a=json.loads((H.parent/'vol05/analysis.json').read_text(encoding='utf-8'))
g=json.loads((H.parent/'vol05/graph.json').read_text(encoding='utf-8'))
print('ANALYSIS_KEYS',list(a))
for k in ['major_character_states','plotline_states','open_questions','unresolved_and_anomalies','reading_scope','transferable_mechanisms','literary_tradeoffs']:
 v=a.get(k);print(k,json.dumps(v[:1] if isinstance(v,list) else v,ensure_ascii=False))
print('SAMPLE_DIM',json.dumps(a['dimensions']['style'][0],ensure_ascii=False))
print('GRAPH',json.dumps({k:v[:2] if isinstance(v,list) else v for k,v in g.items()},ensure_ascii=False))
lines=(H.parent/'vol05/build_research.py').read_text(encoding='utf-8').splitlines()
print('\n'.join(str(i+1)+':'+s for i,s in enumerate(lines) if i>=270))
