from pathlib import Path
import json,sys
sys.stdout.reconfigure(encoding='utf-8')
root=Path(__file__).parent.parent
for arg in sys.argv[1:]:
 p=root/arg;b=json.loads(p.read_text(encoding='utf-8'))
 print('\nBATCH',arg,b['unit_start'],b['unit_end'],b['label'])
 print('UNITS',json.dumps(b['units'],ensure_ascii=False,separators=(',',':')))
 print('DIMENSIONS',json.dumps(b['dimensions'],ensure_ascii=False,separators=(',',':')))
 print('CHARACTERS',json.dumps(b['characters'],ensure_ascii=False,separators=(',',':')))
 print('THREADS',json.dumps(b['threads'],ensure_ascii=False,separators=(',',':')))
 print('QUESTIONS',json.dumps(b['questions'],ensure_ascii=False,separators=(',',':')))
