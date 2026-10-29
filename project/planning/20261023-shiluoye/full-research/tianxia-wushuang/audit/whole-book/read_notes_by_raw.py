import json,sys
from audit_evidence import B
sys.stdout.reconfigure(encoding='utf-8')
ids={f'ch-{int(i):04}' for i in sys.argv[1:]}
found=[]
for v in range(1,9):
 for i,l in enumerate((B/f'vol{v:02}/chapter-notes.jsonl').read_text(encoding='utf-8').splitlines()):
  if not l.strip():continue
  x=json.loads(l)
  cid=x.get('chapter_id') or x.get('chapter',{}).get('chapter_id')
  if cid in ids:
   print('BEGIN_NOTE',v,i,cid)
   print(json.dumps(x,ensure_ascii=False))
   print('END_NOTE',v,i,cid);found.append(cid)
print('REQUESTED',sorted(ids),'FOUND',sorted(found))
