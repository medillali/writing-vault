import json,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');P=Path(__file__).parent;B=P.parents[2]
notes=[]
for v in range(1,9):
 for line in (B/f'vol{v:02d}'/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines():
  if line.strip():
   n=json.loads(line);n['_volume']=v;notes.append(n)
mode=sys.argv[1]
if mode=='find':
 for term in sys.argv[2:]:
  matches=[n for n in notes if term in json.dumps(n,ensure_ascii=False)]
  print(json.dumps(dict(term=term,count=len(matches),matches=[dict(chapter_id=n['chapter_id'],title=n.get('title')) for n in matches]),ensure_ascii=False))
elif mode=='get':
 ids=set()
 for arg in sys.argv[2:]:
  if '-' in arg:a,b=map(int,arg.split('-'));ids.update(range(a,b+1))
  else:ids.add(int(arg))
 for n in notes:
  if int(n['chapter_id'][3:]) in ids:print(json.dumps(n,ensure_ascii=False))
