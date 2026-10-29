import json
from audit_evidence import H,render_characters
p=H/'character-arcs-part08.json';x=json.loads(p.read_text(encoding='utf-8'))
for row in x['characters']:
 row['evidence_boundaries']=row['evidence_boundaries'].replace('婚姻 consummation','婚姻肉体关系已发生')
p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
render_characters('character-arcs-part08.md',x['characters'],x['title'])
import hashlib
print(hashlib.sha256(p.read_bytes()).hexdigest())
