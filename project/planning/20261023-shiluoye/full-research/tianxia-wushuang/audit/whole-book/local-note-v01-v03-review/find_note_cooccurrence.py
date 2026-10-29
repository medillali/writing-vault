import json,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
B=Path(__file__).resolve().parents[3]
for v in range(1,9):
 for s in (B/f'vol{v:02d}'/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines():
  if not s.strip():continue
  n=json.loads(s)
  hits=[x for k in ('facts','state_changes','inferences','unresolved') for x in n.get(k,[]) if all(t in x for t in sys.argv[1:])]
  if hits:print(json.dumps({'chapter_id':n['chapter_id'],'matches':hits},ensure_ascii=False))
