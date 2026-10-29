import json
from pathlib import Path
P=Path(__file__).parent;a=json.loads((P/'analysis.json').read_text(encoding='utf-8'))
r=next(r for r in a['dimensions']['continuity'] if r['id']=='v01-continuity-03')
print(json.dumps(r['evidence'][5],ensure_ascii=False,indent=2))
