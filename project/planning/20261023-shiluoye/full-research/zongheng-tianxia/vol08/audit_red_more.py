import json,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');R=Path(__file__).parent
for vn in ['vol06','vol07','vol07-primary-tail']:
 a=[json.loads(x) for x in (R.parent/vn/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
 for n in a:
  hits=[x for x in n.get('facts',[]) if ('红' in str(x) or '沈' in str(x)) and any(t in str(x) for t in ['五','蛋','旧部','重建','调停','调解','自主','分盟','女友'])]
  if hits:print(vn,n['chapter_id'],n['start_line'],n['end_line'],json.dumps(hits,ensure_ascii=False))
