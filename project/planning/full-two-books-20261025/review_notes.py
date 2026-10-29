from pathlib import Path
import json,sys
sys.stdout.reconfigure(encoding='utf-8');P=Path(__file__).parent
key=sys.argv[1];start=int(sys.argv[2]) if len(sys.argv)>2 else 0;end=int(sys.argv[3]) if len(sys.argv)>3 else 999
for folder in (['z','z-b','z-c','z-c2','z-d'] if key=='z' else ['l-a','l-b']):
 for f in sorted((P/folder).glob('batch-*.json')):
  b=json.loads(f.read_text(encoding='utf-8'))
  if b['unit_start']>end or b['unit_end']<start:continue
  print(f'=== {folder}/{f.name} {b["unit_start"]}-{b["unit_end"]} {b["label"]} ===')
  if len(sys.argv)>4 and sys.argv[4]=='questions':print(json.dumps(b['questions'],ensure_ascii=False))
  else:
   for u in b['units']:print(u['ordinal'],u['title'],'；'.join(u['events']),'变化：'+'；'.join(u['state_changes']))
   if len(sys.argv)>4 and sys.argv[4]=='dimensions':print('九维：'+json.dumps(b['dimensions'],ensure_ascii=False))
