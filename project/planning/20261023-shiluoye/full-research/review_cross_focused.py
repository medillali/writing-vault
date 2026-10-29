import json,sys,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent;R=B.parents[2];D=B/sys.argv[1]
a=json.loads((D/'cross-volume-focused-review.json').read_text(encoding='utf-8'))
sys.stdout.reconfigure(encoding='utf-8')
for row in a['findings']:
 print(json.dumps({k:v for k,v in row.items() if k not in ['source_locators','derived_refs']},ensure_ascii=False,separators=(',',':')))
for x in a.get('input_sha256_snapshot',[]):
 assert hashlib.sha256((R/x['path']).read_bytes()).hexdigest()==x['sha256'],x['path']
print('INPUT_SHA_VERIFIED',len(a.get('input_sha256_snapshot',[])))
