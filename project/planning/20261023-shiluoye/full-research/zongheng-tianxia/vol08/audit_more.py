import json,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
R=Path(__file__).parent
for name in ['vol06','vol07','vol07-primary-tail']:
 p=R.parent/name/'chapter-notes.jsonl'
 ns=[json.loads(x) for x in p.read_text(encoding='utf-8').splitlines() if x.strip()]
 for n in ns:
  hits=[x for x in n.get('facts',[]) if ('灵儿' in str(x) and any(t in str(x) for t in ['封印','母亲','母印'])) or any(t in str(x) for t in ['患病','病重','重病','骨髓','白血','病情','求婚','婚约','婚礼','知情'])]
  if hits:print(json.dumps(dict(path=name,chapter_id=n['chapter_id'],start_line=n['start_line'],end_line=n['end_line'],facts=hits),ensure_ascii=False))
