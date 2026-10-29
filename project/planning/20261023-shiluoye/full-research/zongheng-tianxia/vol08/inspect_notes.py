import json
from pathlib import Path
p=Path(__file__).parent
a=[json.loads(x) for x in (p/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines()]
for x in a[:20]:print(x['chapter_id'],x['title'],x['facts'][0][:120])
