"""仅在模型完整读完对应笔记输出后手动推进材料阅读游标。"""
import json,sys,hashlib
from pathlib import Path
P=Path(__file__).parent;n=int(sys.argv[1]);assert 1505<=n<=1572
p=P/'primary-material-state.json';s=json.loads(p.read_text(encoding='utf-8'));old=int(s['completed_note_chapter_ids'][-1][3:]);assert old<=n
s.update(completed_note_chapter_ids=[f'ch-{i:04d}' for i in range(1505,n+1)],next_note_chapter_id=f'ch-{n+1:04d}' if n<1572 else None,complete=(n==1572),source_notes_sha256=hashlib.sha256((P.parent/'vol08'/'chapter-notes.jsonl').read_bytes()).hexdigest())
p.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(len(s['completed_note_chapter_ids']))
