"""读取全套历史原题语义，证据折叠为章行，未作终点评判。"""
from check_volume import WORK,read
import json,sys
sys.stdout.reconfigure(encoding='utf-8')
def compact(x):
 if isinstance(x,list):return [compact(v) for v in x]
 if isinstance(x,dict):
  if {'source_id','revision','chapter_id'}.issubset(x):return x['chapter_id']+f" L{x.get('start_line')}—{x.get('end_line')}"
  return {k:compact(v) for k,v in x.items() if k not in ['node_ids','edge_ids','original_path']}
 return x
a,z=map(int,sys.argv[1:3]);rows=read(WORK/'zhanlong/audit/whole-book/historical-question-pool.json')['candidates']
for i,r in enumerate(rows[a:z],a):
 print(i,json.dumps(compact({k:r[k] for k in ['candidate_id','volume','title','original_stage_status','original_record','original_evidence']}),ensure_ascii=False,separators=(',',':')))
print('READ_COMPLETE',a,z,len(rows[a:z]))
