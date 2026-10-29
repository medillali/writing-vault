import json,hashlib,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');P=Path(__file__).parent
v,part,lo,hi,expected=map(int,sys.argv[1:]);rows=json.loads((P/f'adjudications-local-note-v{v:02d}.json').read_text(encoding='utf-8'))
subset=[r for r in rows if lo-1<=r['original_index']<hi];assert len(subset)==expected
p=P/f'adjudications-local-note-v{v:02d}-part{part:02d}.json';assert not p.exists(),'frozen block exists'
p.write_text(json.dumps(subset,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'path':str(p),'count':len(subset),'groups':[lo,hi],'sha256':hashlib.sha256(p.read_bytes()).hexdigest()},ensure_ascii=False))
