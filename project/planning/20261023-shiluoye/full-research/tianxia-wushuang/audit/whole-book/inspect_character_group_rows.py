import json,sys
from audit_evidence import H
sys.stdout.reconfigure(encoding='utf-8')
ids=set(sys.argv[1:])
for p in sorted(H.glob('character-arcs-part*.json')):
 for x in json.loads(p.read_text(encoding='utf-8'))['characters']:
  if x['audit_id'] in ids:
   y={k:([e['chapter_id'] for e in val] if k=='evidence' else val) for k,val in x.items()}
   print(json.dumps(y,ensure_ascii=False))
