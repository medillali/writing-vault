import json,hashlib
from audit_evidence import H,evidence
p=H/'character-wenhen-leadership-proposal.json';x=json.loads(p.read_text(encoding='utf-8'));a=x['after']
a['evidence_boundaries']='1098官方同名吻痕三项明确区分：中国165刺客所属公会名谁与争锋、美国192战属英雄联盟、无籍199荷兰战士；1209巴西212剑师的角色ID为谁与争锋，是公会名与角色ID同名，不能混字段/人物。1199陆仍盟主到1219她已任职为两个时点，不编交接或全体恢复中国籍。'
a['evidence']=evidence([int(e['chapter_id'][3:]) for e in a['evidence']]+[1209])
x['changed_fields']=[k for k in x['before'] if x['before'][k]!=a[k]]
x['source_layer']='本人完整读1098/1199/1209/1219派生notes；root BEGIN-END全文1098/1209核字段：三同ID属于吻痕，不属于巴西角色谁与争锋。'
p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(hashlib.sha256(p.read_bytes()).hexdigest())
