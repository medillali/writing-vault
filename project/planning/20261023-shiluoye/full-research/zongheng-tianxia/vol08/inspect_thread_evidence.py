import json,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');R=Path(__file__).parent
P=json.loads((R/'historical-question-pool.json').read_text(encoding='utf-8'))
for x in P['candidates']:
 if x['volume']!=6:continue
 t=x['original_record'];e=t.get('resolution_evidence',x['original_evidence'])
 print(x['candidate_id'], sorted(set(i['chapter_id'] for i in e)))
