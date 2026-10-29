from build import ROOT,BOOK
import json
ns={55,92,93,94,95,102,120,129,117,112,128,77,90,65,138,97,51,61,126,130,110,139,140,37}
for p in sorted(ROOT.glob('batch-*.json')):
 d=json.loads(p.read_text(encoding='utf-8'))
 for u in d['units']:
  if u['ordinal'] in ns:print(json.dumps(u,ensure_ascii=False))
