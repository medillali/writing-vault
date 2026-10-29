import json,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');P=Path(__file__).parent;A=P.parent;B=P.parents[2]
pool=json.loads((A/'local-question-pool.json').read_text(encoding='utf-8'))
v,lo,hi=map(int,sys.argv[1:4])
notes=[json.loads(x) for x in (B/f'vol{v:02d}'/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
for ix in range(lo-1,hi):
 a=[x for x in pool['candidates'] if x['volume']==v and x.get('original_field')=='notes-unresolved' and x['original_index']==ix]
 if not a:continue
 print('BEGIN GROUP',ix+1)
 n=notes[a[0]['source_note_index']]
 print(json.dumps(n,ensure_ascii=False))
 for x in a:print(json.dumps({'id':x['candidate_id'],'atom':x['title'],'unresolved_index':x['source_unresolved_index']},ensure_ascii=False))
 print('END GROUP',ix+1)
