"""只读已主审终评中指定名字的实际终评字段，检索不等原文覆盖。"""
from pathlib import Path
import json,sys
sys.stdout.reconfigure(encoding='utf-8')
A=Path(__file__).resolve().parent.parent;args=sys.argv[1:];s=next((x.split('=',1)[1] for x in args if x.startswith('--slice=')),None);lo,hi=map(int,s.split(':')) if s else (1,100000);terms=[x for x in args if not x.startswith('--slice=')];count=0
for file in ['historical-question-pool.json','local-question-pool.json']:
 p=A/file
 if not p.exists():continue
 d=json.loads(p.read_text(encoding='utf-8'));rows=d.get('candidates',d.get('questions',[]))
 for c in rows:
  title=c.get('title',c.get('question',''))
  if not any(t in title for t in terms):continue
  count+=1
  if not lo<=count<=hi:continue
  t=c.get('terminal_assessment') or {};out={k:v for k,v in t.items() if k!='later_evidence'};out['later_evidence_bounds_fixed_sidrev']=[[e.get('chapter_id'),e.get('start_line'),e.get('end_line')] for e in t.get('later_evidence',[])]
  print(json.dumps(dict(match_index=count,pool=file,candidate_id=c.get('candidate_id'),title=title,terminal_assessment=out),ensure_ascii=False,separators=(',',':')))
print('END matched terminal rows '+str(count)+'; not original-text coverage')
