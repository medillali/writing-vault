from pathlib import Path
import json,sys
sys.stdout.reconfigure(encoding='utf-8')
for f in sorted(Path(__file__).parent.glob('batch-*.json')):
 a=json.loads(f.read_text(encoding='utf-8'))
 print('\n'+f.name)
 for u in a['units']:
  print(str(u['ordinal'])+' '+str(u['evidence'])+' '+'；'.join(u['events']+u['state_changes']))
