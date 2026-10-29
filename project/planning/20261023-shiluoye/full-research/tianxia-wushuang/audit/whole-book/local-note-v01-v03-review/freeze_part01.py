import json,hashlib,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');P=Path(__file__).parent
rows=json.loads((P/'adjudications-local-note-v01.json').read_text(encoding='utf-8'))
part=[r for r in rows if r['original_index']<24]
assert len(part)==107
p=P/'adjudications-local-note-v01-part01.json';assert not p.exists(),'already frozen, do not overwrite'
p.write_text(json.dumps(part,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'path':str(p),'rows':len(part),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()},ensure_ascii=False))
