"""只列后证全部早于原场景的候选供人工核，不自动改判断。"""
import json,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');R=Path(__file__).parent
for fn in ['historical-question-pool.json','local-question-pool.json']:
 P=json.loads((R/fn).read_text(encoding='utf-8'))
 for x in P['candidates']:
  d=x['terminal_assessment'];o=x['original_evidence'];l=d['later_evidence']
  if not o or not l:continue
  earliest=min(int(e['chapter_id'][3:]) for e in o);latest=max(int(e['chapter_id'][3:]) for e in l)
  if latest<earliest and any(t in d['rationale'] for t in ['后来','后续','随后','后来','后有']):
   print(x['candidate_id'],earliest,latest,x['title'],d['rationale'])
