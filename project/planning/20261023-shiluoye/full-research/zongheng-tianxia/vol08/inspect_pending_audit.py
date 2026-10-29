import json,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
R=Path(__file__).parent
P=json.loads((R/'local-question-pool.json').read_text(encoding='utf-8'))
for x in P['candidates']:
 d=x['terminal_assessment']
 if x['volume'] in [3,4] and d.get('review_progress')!='reviewed-draft' and d.get('audit_domain')!='source_anomaly':
  print(x['candidate_id'],x['title'],'CH',[e.get('chapter_id') for e in x['original_evidence']])
