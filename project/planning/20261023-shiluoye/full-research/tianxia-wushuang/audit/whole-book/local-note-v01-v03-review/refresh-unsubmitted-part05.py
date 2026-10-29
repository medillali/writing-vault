import json,hashlib
from pathlib import Path
P=Path(__file__).parent
p=P/'adjudications-local-note-v03-part05.json'
assert hashlib.sha256(p.read_bytes()).hexdigest()=='90be2b29bcf928bcc6e25b212064d8566c1408eef83c0b2233fd0e6a1b40759d'
before=p.read_bytes();rows=json.loads((P/'adjudications-local-note-v03.json').read_text(encoding='utf-8'))
out=[r for r in rows if 168<=r['original_index']<216]
old=json.loads(before);assert len(out)==len(old)==93
diff=[a['candidate_id'] for a,b in zip(old,out) if a!=b]
assert diff==['v03-local-notes-unresolved-213-03'],diff
s=P/'unsubmitted-snapshots';s.mkdir(exist_ok=True)
(s/'part05-before-self-anchor-correction.json').write_bytes(before)
p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(hashlib.sha256(p.read_bytes()).hexdigest())
