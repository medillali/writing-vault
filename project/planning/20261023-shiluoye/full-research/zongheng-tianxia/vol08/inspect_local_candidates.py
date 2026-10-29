import json,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');R=Path(__file__).parent
P=json.loads((R/'local-question-pool.json').read_text(encoding='utf-8'))
keys=set(sys.argv[1].split(','))
for x in P['candidates']:
 if x['candidate_id'] in keys:print(x['candidate_id'],x['title'],[e['chapter_id'] for e in x['original_evidence']])
