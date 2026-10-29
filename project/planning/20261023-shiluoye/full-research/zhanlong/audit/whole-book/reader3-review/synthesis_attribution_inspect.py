from synthesis_common import *
from collections import Counter
for n in range(1,7):
 p=F/f'vol{n:02d}-read-log.json';a=json.loads(p.read_text(encoding='utf-8'));counts=Counter(x.get('reader',a.get('reader','not-in-log')) for x in a['chapters']);print('READLOG',n,len(a['chapters']),dict(counts))
 np=F/f'vol{n:02d}-chapter-notes.jsonl';ns=[json.loads(x) for x in np.read_text(encoding='utf-8').splitlines() if x.strip()];print('NOTES',n,len(ns),dict(Counter(x.get('reader','missing') for x in ns)))
v=json.loads((F/'audit/full-reading-validation.json').read_text(encoding='utf-8'));print('FULLVALIDATION KEYS',list(v));print(json.dumps({k:x for k,x in v.items() if k not in ['formal_input_sha256','volumes','read_log_checks','checks','files']},ensure_ascii=False)[:4500])
p=B/'primary-synthesis-dimension-reviews.json'
if p.exists():
 a=json.loads(p.read_text(encoding='utf-8'));print('PRIMARY DIM RECEIPT KEYS',list(a));print(json.dumps(a,ensure_ascii=False)[:3000])
