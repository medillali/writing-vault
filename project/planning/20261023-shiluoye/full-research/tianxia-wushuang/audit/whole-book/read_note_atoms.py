"""候选原notes已另实际读；此接口只列稳定新原子便于逐项配后证。"""
import json,pathlib,sys
sys.stdout.reconfigure(encoding='utf-8');H=pathlib.Path(__file__).resolve().parent
v=int(sys.argv[1]);lo=int(sys.argv[2]);hi=int(sys.argv[3])
rows=[x for x in json.loads((H/'local-question-pool.json').read_text(encoding='utf-8'))['candidates'] if x['volume']==v and x['original_field']=='notes-unresolved']
for i in range(lo,min(hi,len(rows))):
 x=rows[i];print(i,x['candidate_id'],','.join(e['chapter_id'] for e in x['original_evidence']),x['title'])
print('END_NOTE_ATOMS',v,lo,min(hi,len(rows)),'TOTAL',len(rows))
