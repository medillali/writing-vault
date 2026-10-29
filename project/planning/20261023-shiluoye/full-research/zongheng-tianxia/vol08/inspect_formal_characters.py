import json,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');R=Path(__file__).parent;F=R.parents[4]/'writing-vault/library/reports/zongheng-tianxia'
v=int(sys.argv[1]);terms=sys.argv[2].split(',')
A=json.loads((F/f'vol{v:02}-cards.json').read_text(encoding='utf-8'));A=A.get('cards',[]) if isinstance(A,dict) else A
for x in A:
 if x.get('asset_type')=='character' and any(t in x['title'] for t in terms):
  print(x['title']);print(json.dumps(x['content'],ensure_ascii=False));print('EVIDENCE',sorted(set(e['chapter_id'] for e in x['evidence'])))
