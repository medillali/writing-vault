import json,pathlib,sys
sys.stdout.reconfigure(encoding='utf-8');H=pathlib.Path(__file__).resolve().parent;R=H.parents[5]
for v in range(1,9):
 a=json.loads((R/f'writing-vault/library/reports/tianxia-wushuang/vol{v:02d}-analysis.json').read_text(encoding='utf-8'));f=next(k for k in ['major_character_states','character_states','characters'] if k in a);rows=a[f]
 print(v,f,len(rows),[(i,x.get('name',x.get('title',x.get('character')))) for i,x in enumerate(rows)] if isinstance(rows,list) else list(rows))
