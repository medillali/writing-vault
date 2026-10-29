import json
from audit_evidence import H,render_characters
p=H/'character-arcs-part03.json';d=json.loads(p.read_text(encoding='utf-8'));x=next(x for x in d['characters'] if x['name']=='周小萌');x['terminal_state']='全书终点未展示特定签约/付款与现实见北；最稳终态是已脱该席并可继续活动，职业转会有谈妥转述而无独立合同回执。'
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');render_characters('character-arcs-part03.md',d['characters'],d['title'])
import hashlib;print(hashlib.sha256(p.read_bytes()).hexdigest())
