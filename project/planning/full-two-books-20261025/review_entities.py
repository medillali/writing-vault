from pathlib import Path
import json,sys,collections
sys.stdout.reconfigure(encoding='utf-8');P=Path(__file__).parent
for key,folders in [('z',['z','z-b','z-c','z-d']),('l',['l-a','l-b'])]:
 names=collections.defaultdict(list)
 for folder in folders:
  for f in sorted((P/folder).glob('batch-*.json')):
   b=json.loads(f.read_text(encoding='utf-8'))
   for c in b['characters']:names[c['name']].append({'key':c['key'],'units':[b['unit_start'],b['unit_end']],'aliases':c.get('aliases',[])})
 print(key,json.dumps(names,ensure_ascii=False))
