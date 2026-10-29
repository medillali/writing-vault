import json,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
R=Path(__file__).parent
ns=[json.loads(x) for x in (R.parent/'vol07-primary-tail/chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
for n in ns:
 i=int(n['chapter_id'][3:])
 if 974<=i<=984 or i in [1042,1056,1058,1059]:
  print(n['chapter_id'],n['start_line'],n['end_line'],json.dumps(n['facts'],ensure_ascii=False))
