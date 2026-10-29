"""按小批完整显示primary尾段四栏，不替代原文阅读或生成结论。"""
import json,sys
from pathlib import Path
P=Path(__file__).parent
rows=[json.loads(s) for s in (P.parent/'primary-vol01-tail/chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if s.strip()]
lo,hi=map(int,sys.argv[1:3])
picked=[r for r in rows if lo<=int(r['chapter_id'].split('-')[1])<=hi]
assert len(picked)==hi-lo+1
for r in picked:
 print('BEGIN NOTE',r['chapter_id'],r['title'],r['start_line'],r['end_line'],'reader='+r['reader'])
 for k in ('facts','inferences','state_changes','unresolved'):
  print(k+': '+json.dumps(r[k],ensure_ascii=False))
 print('END NOTE',r['chapter_id'])
