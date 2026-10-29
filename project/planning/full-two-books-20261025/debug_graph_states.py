from pathlib import Path
import json,sys
sys.stdout.reconfigure(encoding='utf-8');P=Path(__file__).parent
for folder in ['l-a','l-b','z','z-b','z-c','z-d']:
 for f in sorted((P/folder).glob('batch-*.json')):
  b=json.loads(f.read_text(encoding='utf-8'))
  for t in b['threads']:
   if t.get('kind') not in ['main','subplot','hidden'] or t.get('status') not in ['open','partial','resolved','abandoned','unknown']:print(folder,f.name,t)
  for q in b['questions']:
   if q['status'] not in ['open','partial','resolved','abandoned','unknown']:print('QUESTION',folder,f.name,q)
