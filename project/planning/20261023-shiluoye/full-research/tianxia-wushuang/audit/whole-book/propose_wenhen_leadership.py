import json,copy,hashlib
from audit_evidence import H,evidence
p=H/'character-arcs-part09.json';obj=json.loads(p.read_text(encoding='utf-8'));b=next(r for r in obj['characters'] if r['audit_id']=='character-arc-107');a=copy.deepcopy(b)
a['key_decisions']='与斩神/保护伞共同求生，1199陆仍盟主、黑海驻地互保方案进行；1219明确吻痕已任保护伞盟主、驻地成暗月卫星，交接过程未专写→留守不随偷日落→1382亲看阳等S5供情报、1397被报帝君末杀→1572指出换命会全损，陆实际调兵。'
a['terminal_state']='已任保护伞盟主/驻地互保后持续独立支援，末战仍提出战术意见，不是仅早期受救者；没有个人末死/永久退游确证。'
a['evidence_boundaries']='1098官方同ID三项明确区分：中国165刺谁与争锋、美国192战英雄联盟、无籍199荷兰战士；不混入巴西同ID剑师。1199陆仍盟主到1219她已任职是两个时点，不编交接镜头或全体恢复中国籍。'
a['evidence']=evidence([int(e['chapter_id'][3:]) for e in b['evidence']]+[1098,1199])
x=dict(status='proposal_pending_primary_review_no_signed_group_modified',path=p.name,input_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),audit_id=b['audit_id'],before=b,after=a,changed_fields=[k for k in b if b[k]!=a[k]],source_layer='本人完整阅读1098/1199/1219派生notes；root及v6原读者核原文locator。')
(H/'character-wenhen-leadership-proposal.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(x['input_sha256'])
