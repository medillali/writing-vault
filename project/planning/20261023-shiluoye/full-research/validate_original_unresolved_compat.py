"""用实际原章笔记核对两种索引字段；空记录保留但不能伪造问题。"""
import json,sys
from check_volume import WORK,read
sys.stdout.reconfigure(encoding='utf-8')
results=[]
for vol in range(1,7):
 p=WORK/'zhanlong'/f'vol{vol:02d}';ap=p/'analysis.json'
 if not ap.exists():continue
 a=read(ap);notes=[json.loads(s) for s in (p/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if s]
 expected={n['chapter_id']:(n['reader'],n['unresolved']) for n in notes if n.get('unresolved')}
 indexed={};empty=[]
 for i,row in enumerate(a['chapter_unresolved_index']):
  values=row.get('unresolved',row.get('original_unresolved'))
  assert isinstance(values,list),(vol,i,'索引须明确原数组')
  if not values:empty.append(i);continue
  assert row['chapter_id'] not in indexed
  indexed[row['chapter_id']]=(row['reader'],values)
 assert expected==indexed,(vol,'索引丢失/改字/改读者')
 for i in empty:
  row=a['chapter_unresolved_index'][i]
  assert next(n for n in notes if n['chapter_id']==row['chapter_id'])['unresolved']==[]
 results.append({'volume':vol,'nonempty_original_rows':len(expected),'explicit_empty_records':empty,'original_strings_and_reader_equal':True})
print(json.dumps({'status':'passed','volumes':results,'semantic_judgments_created':0},ensure_ascii=False))
