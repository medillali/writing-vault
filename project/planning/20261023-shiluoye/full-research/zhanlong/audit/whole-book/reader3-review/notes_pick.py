from common import B
import json,sys
ns={int(n) for n in sys.argv[1:]};found=set()
for p in sorted(B.glob('vol??/chapter-notes.jsonl')):
 for s in p.read_text(encoding='utf-8').splitlines():
  if not s.strip():continue
  r=json.loads(s);n=int(r['chapter_id'].split('-')[1])
  if n in ns:print(s);found.add(n)
assert found==ns,(ns-found)
