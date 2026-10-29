from pathlib import Path
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')
P=Path(__file__).parent.parent
for d in ('l-a','l-b'):
 for f in sorted((P/d).glob('batch-*.json')):
  a=json.loads(f.read_text(encoding='utf-8'))
  for q in a.get('questions',[]):print(d,f.name,q.get('key'),q.get('status'),q.get('question'),q.get('answer'),sep=' | ')
