from pathlib import Path
import json,sys
sys.stdout.reconfigure(encoding='utf-8')
P=Path(__file__).parent
f=P/('terminal-question-map.json' if (P/'terminal-question-map.json').exists() else 'terminal-question-map.provisional.json')
for q in json.loads(f.read_text(encoding='utf-8'))['items']:
 if q['final_status']!='resolved':print(q['key'],q['final_status'],q['answer'])
