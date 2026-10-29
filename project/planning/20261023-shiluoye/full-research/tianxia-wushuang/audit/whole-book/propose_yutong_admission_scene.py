import json,copy,hashlib
from audit_evidence import H,evidence
p=H/'character-arcs-part09.json';obj=json.loads(p.read_text(encoding='utf-8'));b=next(r for r in obj['characters'] if r['audit_id']=='character-arc-105');a=copy.deepcopy(b)
a['key_decisions']='888—889本人自愿去古剑；889陆发收入联盟申请、称以后为古剑人，她答谢并收靴，叙述搞定接收→943整批千法改不用归还换千骑月训→国战持续输出、1057被清风杀→1300血燕洞被血盟杀、1413仍为魔攻比较参照。'
a['terminal_state']='889已有具体入盟申请、双方接收话语与叙述搞定，不能只因未重播系统徽记把个人接收停作全未知；943整批不归还新约已成交。千骑实际训练与1262爱菲林杖具体交付仍无特定回执。'
a['evidence_boundaries']='千法唯一女自愿且本人已有接收场景，个人入会与943整批新约分阶段。手续未逐项重播不等缺入会行动；赠靴/招留不推恋爱，训练口约不当已完成。'
a['evidence']=evidence([int(e['chapter_id'][3:]) for e in b['evidence']]+[888,889,890])
x=dict(status='proposal_pending_primary_review_no_signed_group_modified',path=p.name,input_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),audit_id=b['audit_id'],before=b,after=a,changed_fields=[k for k in b if b[k]!=a[k]],source_layer='本人为核派生notes早已入说法BEGIN-END全文复读889 L73421—73508；L73499发收入联盟申请，73502—06当事接收话语和搞定叙述。未把缺系统徽记当缺全部入会动作。')
(H/'character-yutong-admission-scene-proposal.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(hashlib.sha256((H/'character-yutong-admission-scene-proposal.json').read_bytes()).hexdigest())
