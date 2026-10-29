from common import A,P,dump,sha,evidence
import json,copy
changes=[
(16,'v04-local-chapter_unresolved_index-0170-01','931韩持牌申请军团二十万上限，918个人统兵上限不等申请已批。','931韩持牌申请的军团二十万上限后来975 L72503获浅林明确特赦，区别918个人统兵上限，原审批已有直接后证。'),
(17,'v04-local-chapter_unresolved_index-0171-01','931申请御林二十万建制未见同次批示，918个人统兵上限不偷替。','931申请的御林二十万建制后来975 L72503获浅林明确特赦允许扩充，关闭授权结果；不倒写成931当日已有二十万实兵。'),
(17,'v04-local-chapter_unresolved_index-0177-01','御林918个人二十万上限已生效，931另申请军团二十万未见批示；1374十四万实际出战证增长但不自动闭原建制审批二十万。','御林918个人二十万上限与931军团建制申请分开，975 L72503浅林真实特赦御林可扩二十万，授权已成；1374十四万实出是另实际人数，不以授权当已满编。'),
(18,'v04-local-chapter_unresolved_index-0198-01','原万兵剩余每批与930佣俘三万对应毕业、931二十万建制申请仍缺完整同批回执，不能拿持续新训合数冒原一万人全过关。','975 L72503浅林已明确特赦御林可扩二十万，原建制授权不再待；原万兵剩余每批及930三万佣俘对应毕业仍缺同批名单，不能拿持续新训合数冒原一万人全过关。')]
proposals=[]
for bn,cid,old,new in changes:
 f=A/f'adjudications-local-v04-batch{bn:03d}.json';rows=json.loads(f.read_text(encoding='utf-8'));before=next(x for x in rows if x['candidate_id']==cid);after=copy.deepcopy(before)
 assert old in after['rationale'];after['rationale']=after['rationale'].replace(old,new)
 after['later_chapters']=sorted(set(after['later_chapters']+[975]));after['later_evidence']=evidence(after['later_chapters'])
 proposals.append({'candidate_id':cid,'input_path':str(f),'input_sha256':sha(f),'before':before,'after':after})
out=P/'later-cap-order-four-items-proposal.json';assert not out.exists();dump(out,{'status':'proposal-not-applied','reason':'尾项读取后卷975完整四栏并定向L72491—72509，明确L72503后授二十万；只替缺后批示句，其他分题结论不变。','proposals':proposals})
print(sha(out))
