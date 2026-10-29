"""全文呈现限定范围的四栏研究笔记；这不是亲读原小说的声明。"""
from pathlib import Path
import json,sys
sys.stdout.reconfigure(encoding='utf-8')
B=Path(__file__).resolve().parent
book,leaf,a,b=sys.argv[1:];a,b=int(a),int(b)
assert Path(leaf).name==leaf and a<=b
rows=[json.loads(x) for x in (B/book/leaf/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
count=0
for r in rows:
    if a<=int(r['chapter_id'][3:])<=b:
        print(f"BEGIN NOTE {r['chapter_id']} {r['title']} L{r['start_line']}—{r['end_line']} reader={r.get('reader')}")
        for field in ['facts','inferences','state_changes','unresolved'] + (['source_anomalies'] if r.get('source_anomalies') else []):
            print(field+': '+json.dumps(r.get(field),ensure_ascii=False))
        print('END NOTE '+r['chapter_id']);count+=1
print('NOTES_COUNT='+str(count))
