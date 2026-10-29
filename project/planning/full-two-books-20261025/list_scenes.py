from pathlib import Path
import json,sys
sys.stdout.reconfigure(encoding='utf-8');P=Path(__file__).parent
for folder in (['l-a','l-b'] if sys.argv[1]=='l' else ['z','z-b','z-c','z-d']):
 for f in sorted((P/folder).glob('batch-*.json')):
  b=json.loads(f.read_text(encoding='utf-8'));print(folder,f.name,b['unit_start'],b['unit_end'])
  for s in b['scenes']:print(s['key'],s['title'])
