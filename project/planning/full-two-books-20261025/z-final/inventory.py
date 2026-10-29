from pathlib import Path
import json,sys
sys.stdout.reconfigure(encoding='utf-8')
P=Path(__file__).parent.parent
for d in sys.argv[1:]:
 for f in sorted((P/d).glob('batch-*.json')):
  b=json.loads(f.read_text(encoding='utf-8'))
  print(f'{d}/{f.name}',b['unit_start'],b['unit_end'])
  for q in b['questions']:
   print(json.dumps(q,ensure_ascii=False,separators=(',',':')))
  print('THREADS',json.dumps(b['threads'],ensure_ascii=False,separators=(',',':')))
