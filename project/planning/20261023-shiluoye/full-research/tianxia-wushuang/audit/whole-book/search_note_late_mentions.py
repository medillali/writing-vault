import json,sys
from audit_evidence import B
sys.stdout.reconfigure(encoding='utf-8')
terms=sys.argv[1:]
for term in terms:
 out=[]
 for v in range(1,9):
  for l in (B/f'vol{v:02}/chapter-notes.jsonl').read_text(encoding='utf-8').splitlines():
   x=json.loads(l)
   if term in json.dumps(x,ensure_ascii=False):out.append((v,x))
 print('TERM',term,'TOTAL_MATCHING_NOTES',len(out))
 for v,x in out[-3:]:
  print('BEGIN_NOTE',v,x['chapter_id']);print(json.dumps(x,ensure_ascii=False));print('END_NOTE',v,x['chapter_id'])
