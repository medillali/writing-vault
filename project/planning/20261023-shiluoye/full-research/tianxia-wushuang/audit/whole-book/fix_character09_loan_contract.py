import json,copy,hashlib
from audit_evidence import H,evidence,render_characters
p=H/'character-arcs-part09.json';before=json.loads(p.read_text(encoding='utf-8'));after=copy.deepcopy(before);i=next(i for i,r in enumerate(after['characters']) if r['audit_id']=='character-arc-105');old=copy.deepcopy(after['characters'][i]);r=after['characters'][i]
r['key_decisions']='940参与借法合作并受陆帮助/招留，943整批千法从两周借约改为不用归还、交换一个月内训练一千龙曜的新约→978与1057国战输出、1057被清风击杀→1300许报血燕洞被杀者含她→1413月光回会后法攻超她次连。'
r['terminal_state']='943整批千法去留新约已成交，不能写整批去留仍全未知；训练一千骑的实际履行、禹瞳个人正式入会手续及1262爱菲林杖具体交付仍无特定回执，三者不混。'
r['evidence_boundaries']='千法男女概数不能抹唯一女例外；新约层面不归还法师已明确，个人手续未展示不否定整批约定。装备/招留不推恋爱，训练口约不当已完成。'
r['evidence']=evidence([int(e['chapter_id'][3:]) for e in old['evidence']]+[943])
assert all(a==b for n,(a,b) in enumerate(zip(before['characters'],after['characters'])) if n!=i)
(H/'reviewed-batches/character-arcs-part09-before-loan-contract.json').write_bytes(p.read_bytes());p.write_text(json.dumps(after,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');render_characters(p.with_suffix('.md').name,after['characters'],after['title'])
x=dict(status='draft_group_targeted_correction_pending_primary_signature',audit_id='character-arc-105',before=old,after=r,before_sha256=hashlib.sha256((H/'reviewed-batches/character-arcs-part09-before-loan-contract.json').read_bytes()).hexdigest(),after_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),other_11_objects_unchanged=True)
(H/'character09-loan-contract-delta.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(x['after_sha256'])
p=H/'character-arcs-part02.json';obj=json.loads(p.read_text(encoding='utf-8'));b=next(r for r in obj['characters'] if r['audit_id']=='character-arc-14');a=copy.deepcopy(b)
a['costs']='谷归零报告有全体覆盖却无其独立死法；主观战术预算一万不等最终确实死一万。早十三转述爱慕之后，1185晴空本人当面表明喜欢陆并拒李，仍不证明陆已接受。'
a['evidence_boundaries']='她与天堂雨不同人；爱慕从早转述到1185本人明说分时点，不推正式恋人成就。报告人数/预计代价不升级系统精确死簿，末端未知不等后卷未读。'
a['evidence']=evidence([int(e['chapter_id'][3:]) for e in b['evidence']]+[1185])
x=dict(status='proposal_pending_primary_review_no_signed_group_modified',path=p.name,input_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),audit_id=b['audit_id'],before=b,after=a,changed_fields=[k for k in b if b[k]!=a[k]],source_layer='本人完整阅读1185四栏派生笔记；root与v6原读者定向核原文L95482。')
(H/'character-qingkong-first-person-proposal.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
