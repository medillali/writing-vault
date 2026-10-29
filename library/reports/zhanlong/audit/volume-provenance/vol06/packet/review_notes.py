"""打印本卷已经实际读存的人工笔记；不代替原文阅读。"""
from pathlib import Path
import json,sys
sys.stdout.reconfigure(encoding='utf-8')
rows=[json.loads(x) for x in (Path(__file__).parent/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines()]
lo=int(sys.argv[1]);hi=int(sys.argv[2]) if len(sys.argv)>2 else lo
for r in rows:
    n=int(r['chapter_id'][3:])
    if lo<=n<=hi:
        print('NOTE-BEGIN',r['chapter_id'],r['title'],r['start_line'],r['end_line'],r['reader'])
        for k in ['facts','inferences','state_changes','unresolved']:
            print(k, json.dumps(r[k],ensure_ascii=False))
        print('NOTE-END',r['chapter_id'])
