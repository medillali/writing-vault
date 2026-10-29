import json,sys,re
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');R=Path(__file__).parent
for fn in ['historical-question-pool.json','local-question-pool.json']:
 P=json.loads((R/fn).read_text(encoding='utf-8'))
 for x in P['candidates']:
  d=x['terminal_assessment'];s=d['rationale']
  if d.get('audit_domain')!='source_anomaly' and re.search('待核|待.*正式|待.*整合|待.*验证|须.*核|需.*(?:证|核|对照|逐名)|未精|未.*匹配|未.*定位',s):
   print(fn,x['candidate_id'],s)
