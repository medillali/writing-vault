"""修正即时手写笔记的一处未清理草稿词，不更改阅读覆盖。"""
import json
from pathlib import Path
p=Path(__file__).parent
rows=[json.loads(x) for x in (p/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines()]
batch=json.loads((p/'batch020.json').read_text(encoding='utf-8'))
next(r for r in rows if r['chapter_id']=='ch-0081')['facts']=batch['notes'][-1]['facts']
(p/'chapter-notes.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows),encoding='utf-8')
print('ch0081 transcription cleaned; no coverage change')
