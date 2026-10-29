"""完整显示每个原题、判定及后证；重复归属说明只显示一次。"""
from check_volume import WORK,read
import sys,json
sys.stdout.reconfigure(encoding='utf-8')
audit=WORK/'zhanlong/audit/whole-book'
pool={r['candidate_id']:r for kind in ['local','historical'] for r in read(audit/f'{kind}-question-pool.json')['candidates']}
def compact(x):
 if isinstance(x,list):return [compact(v) for v in x]
 if isinstance(x,dict):
  if {'source_id','revision','chapter_id'}.issubset(x):return x['chapter_id']+f" L{x.get('start_line')}—{x.get('end_line')}"
  return {k:compact(v) for k,v in x.items()}
 return x
for argument in sys.argv[1:]:
 name,sep,span=argument.partition('@')
 rows=read(audit/name)
 if sep:
  a,z=map(int,span.split(':'));rows=rows[a:z]
 print('BEGIN_BATCH',argument,len(rows));seen=set()
 for row in rows:
  base=pool[row['candidate_id']]
  if 'original_question' in row:assert row['original_question']==base['title'],row['candidate_id']
  view={k:v for k,v in row.items() if k not in ['original_record','original_question','original_location','source_attribution','provenance','reading_attribution','volume','entry_type','original_path','original_field','original_index','atomic_index','title','original_evidence','original_record_sha256','reviewed_at','source_candidate_pool_sha256','review_status']}
  view={'original_question':base['title'],**view}
  origin=row.get('source_attribution',row.get('provenance',row.get('reading_attribution')))
  if origin is not None:
   key=json.dumps(origin,ensure_ascii=False,sort_keys=True)
   if key not in seen:print('ATTRIBUTION',key);seen.add(key)
  print(json.dumps(compact(view),ensure_ascii=False,separators=(',',':')))
 print('END_BATCH',name,len(rows))
