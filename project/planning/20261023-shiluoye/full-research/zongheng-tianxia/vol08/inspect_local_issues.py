import json,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
R=Path(__file__).parent;P=json.loads((R/'historical-question-pool.json').read_text(encoding='utf-8'))
for group in P['local_issue_records']:
 a=group['original_records'];print('V',group['volume'],group['field'],'type',type(a).__name__,'len',len(a))
 if a:print(json.dumps(a[0],ensure_ascii=False))
