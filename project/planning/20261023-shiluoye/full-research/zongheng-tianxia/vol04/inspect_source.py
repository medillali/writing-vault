import json
from pathlib import Path
import sys
sys.stdout.reconfigure(encoding='utf-8')
s=json.loads((Path(__file__).parent.parent/'source.json').read_text(encoding='utf-8'))
v=next(v for v in s['volumes'] if v['volume']==4)
print(json.dumps({k:s[k] for k in s if k not in ['chapters','volumes']},ensure_ascii=False))
print(json.dumps(v,ensure_ascii=False))
