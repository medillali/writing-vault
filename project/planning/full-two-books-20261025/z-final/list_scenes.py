from pathlib import Path
import json,sys
sys.stdout.reconfigure(encoding='utf-8')
P=Path(__file__).parent.parent
for d in sys.argv[1:]:
 for f in sorted((P/d).glob('batch-*.json')):
  b=json.loads(f.read_text(encoding='utf-8'))
  print(d,f.name,b['unit_start'],b['unit_end'])
  for x in b['scenes']:print(json.dumps({k:x.get(k) for k in ['key','title','summary','state_change','evidence']},ensure_ascii=False,separators=(',',':')))
