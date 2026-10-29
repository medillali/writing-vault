import json,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');P=Path(__file__).parent
a=json.loads((P/'extended-seed-work.json').read_text(encoding='utf-8'))['dimensions']
for d in sys.argv[1:] or a:
 print('BEGIN',d)
 for i,r in enumerate(a[d]):print(json.dumps(dict(index=i,key=r['key'],title=r['title'],fact=r['fact'],claim=r['claim'],sources=r['sources']),ensure_ascii=False))
 print('END',d)
