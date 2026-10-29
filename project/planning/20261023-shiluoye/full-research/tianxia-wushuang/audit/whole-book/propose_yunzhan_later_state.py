import json,copy,hashlib
from audit_evidence import H,evidence
p=H/'character-arcs-part07.json';obj=json.loads(p.read_text(encoding='utf-8'));before=next(x for x in obj['characters'] if x['audit_id']=='character-arc-81');after=copy.deepcopy(before)
after['terminal_state']='886植龙心咳醒时仍虚弱；1202官网明确云栈重建神隐帝国、受卡琳珊册封公爵、镇守神隐城，后态已越过仅续命阶段。原七塞百万军宣言与光复特兰没有特定行动回执，不能以重建神隐替代另一目标。'
after['evidence_boundaries']='玛法奥是云姓名组成，不误造名玛法奥的父；被植是龙的小半心而非整颗心，飞银后活另证。重建/册封/镇守为1202官网报道，非陆亲眼看完重建过程；特兰与神隐对象分开。'
after['evidence']=evidence([int(e['chapter_id'][3:]) for e in before['evidence']]+[1202])
out=dict(status='proposal_pending_primary_review_no_signed_group_modified',reason='1202官网有神隐重建/公爵/镇守明确后态，保七塞百万/特兰目标不同不互代。',input_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),path=p.name,audit_id=before['audit_id'],changed_fields=[k for k in before if before[k]!=after[k]],before=before,after=after)
(H/'character-yunzhan-later-state-proposal.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(out['input_sha256'])
