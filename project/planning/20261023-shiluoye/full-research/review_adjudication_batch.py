"""折叠重复证据后读取全套原问题与终点语义，不替代正文阅读。"""
from pathlib import Path
import json,sys
def short(x):
 if isinstance(x,list):return [short(v) for v in x]
 if isinstance(x,dict):
  if {'source_id','revision','chapter_id'}.issubset(x):return x['chapter_id']
  return {k:short(v) for k,v in x.items() if k not in ['evidence','original_evidence','later_evidence','reviewer','review_status','original_path','node_ids','edge_ids','access_level','boundary','original_index','atomic_index','claim_kind']}
 return x
input_path=Path(sys.argv[1])
rows=json.loads(input_path.read_text(encoding='utf-8'))
rows=rows[int(sys.argv[2]):int(sys.argv[3])] if len(sys.argv)>2 else rows
pool={}
if any('original_record' not in row for row in rows):
 for ancestor in input_path.parents:
  found=False
  for pool_name in ['local-question-pool.json','historical-question-pool.json']:
   pool_path=ancestor/pool_name
   if pool_path.exists():
    pool.update({row['candidate_id']:row for row in json.loads(pool_path.read_text(encoding='utf-8'))['candidates']})
    found=True
  if found:break
sys.stdout.reconfigure(encoding='utf-8')
for row in rows:
 base=pool.get(row['candidate_id'],{})
 joined={k:base[k] for k in ['volume','original_field','original_record','title'] if k in base}
 joined.update(row)
 if '--atomic' in sys.argv and joined.get('original_field')=='notes-unresolved':
  joined={k:v for k,v in joined.items() if k not in ['original_notes_sha256','source_note_index','source_unresolved_index','source_subatomic_index']}
  joined['original_record']={k:v for k,v in joined.get('original_record',{}).items() if k in ['chapter_id','title','start_line','end_line']}
 print(json.dumps(short(joined),ensure_ascii=False,separators=(',',':')))
print('FULL_BATCH_ROWS_READ',len(rows))
