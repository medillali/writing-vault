from pathlib import Path
import sys,json,collections
sys.stdout.reconfigure(encoding='utf-8');P=Path(__file__).parent
for folder in ['l-b','z-final']:
 p=P/folder/'terminal-question-map.json'
 if not p.exists():continue
 d=json.loads(p.read_text(encoding='utf-8'))['items'];bad=[x['key'] for x in d if not x.get('evidence') or not x.get('answer')];print(folder,len(d),dict(collections.Counter(x['final_status'] for x in d)),'empty',bad)
for p in sorted((P/'z-c2').glob('batch-*.json')):
 d=json.loads(p.read_text(encoding='utf-8'));print(p.name,d['unit_start'],d['unit_end'])
