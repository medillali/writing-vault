"""逐批定位/原题/证据结构核验，不产生语义阅读声明。"""
from check_volume import WORK,read
import sys,json
sys.stdout.reconfigure(encoding='utf-8')
P=WORK/'zhanlong/audit/whole-book';S=read(WORK/'zhanlong/source.json');C={r['chapter_id']:r for r in S['chapters']}
pool={r['candidate_id']:r for k in ['historical','local'] for r in read(P/f'{k}-question-pool.json')['candidates']};total=refs=0;ids=set()
for name in sys.argv[1:]:
 rows=read(P/name);assert isinstance(rows,list) and 0<len(rows)<=20,name
 for r in rows:
  cid=r['candidate_id'];assert cid in pool and cid not in ids,cid;ids.add(cid)
  if 'original_question' in r:assert r['original_question']==pool[cid]['title'],cid
  if 'original_record' in r:assert r['original_record']==pool[cid]['original_record'],cid
  assert r['status'] in ['answered','partial','unknown','unrecovered'] and r['rationale'] and r.get('actual_reviewer'),cid
  assert r['later_evidence'] and isinstance(r['later_chapters'],list),cid
  assert set(int(e['chapter_id'][3:]) for e in r['later_evidence'])<=set(r['later_chapters']),cid
  for e in r['later_evidence']:
   assert e['source_id']==S['source_id'] and e['revision']==S['revision'],cid
   c=C[e['chapter_id']];assert c['start_line']<=e['start_line']<=e['end_line']<=c['end_line'],(cid,e)
   assert e['claim_kind'] in ['fact','inference','synthesis','plan'],cid;refs+=1
  total+=1
print(json.dumps({'batches':len(sys.argv)-1,'candidates':total,'references':refs,'status':'structure-and-locators-passed','semantic_reading_created':False},ensure_ascii=False))
