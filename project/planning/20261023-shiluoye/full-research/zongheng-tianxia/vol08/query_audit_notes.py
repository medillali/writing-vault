"""查询既有读者笔记，输出不是原文亲读记录。"""
import json,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
R=Path(__file__).parent
mode=sys.argv[1];query=sys.argv[2].split(',');lo=int(sys.argv[3]) if len(sys.argv)>3 else 0;hi=int(sys.argv[4]) if len(sys.argv)>4 else 9999
for v in range(1,9):
 p=R.parent/f'vol{v:02}'/'chapter-notes.jsonl'
 if not p.exists():continue
 for line in p.read_text(encoding='utf-8').splitlines():
  if not line.strip():continue
  n=json.loads(line);i=int(n['chapter_id'].split('-')[1])
  if not lo<=i<=hi:continue
  if mode=='chapters':
   if str(i) not in query:continue
   facts=n.get('facts',[])
  else:
   facts=[x for x in n.get('facts',[]) if any(t in str(x) for t in query)]
   if not facts:continue
  print(json.dumps(dict(volume=v,chapter_id=n['chapter_id'],facts=facts,uncertainties=n.get('uncertainties',n.get('unresolved_and_anomalies',[]))),ensure_ascii=False))
