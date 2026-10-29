from pathlib import Path
import json,sys
sys.stdout.reconfigure(encoding='utf-8')
P=Path(__file__).parent
inv=json.loads((P/'integration-inventory.json').read_text(encoding='utf-8'))
mode=sys.argv[1] if len(sys.argv)>1 else 'threads'
for key,h in inv[mode].items():
 x=max(h,key=lambda x:x['through'])
 print(key,x.get('status',''),x.get('title',x.get('name','')),x.get('through'))
