import json,sys
from audit_evidence import R
sys.stdout.reconfigure(encoding='utf-8')
terms=sys.argv[1:]
for v in range(1,9):
 a=json.loads((R/f'writing-vault/library/reports/tianxia-wushuang/vol{v:02d}-analysis.json').read_text(encoding='utf-8'))
 rows=next((a[k] for k in ['major_character_states','character_states','characters'] if k in a),[])
 for i,x in enumerate(rows):
  if any(t in str(x.get('title',x.get('name',''))) for t in terms):
   y={k:([e.get('chapter_id') for e in val] if k=='evidence' else val) for k,val in x.items()}
   print(v,i,json.dumps(y,ensure_ascii=False))
