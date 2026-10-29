from common import A,P,dump,sha,evidence
import json,copy
f=A/'adjudications-local-v04-batch016.json'
rows=json.loads(f.read_text(encoding='utf-8'));proposals=[]
texts={
'v04-local-chapter_unresolved_index-0163-01':('925矿工实际开两矿/城基本修成，926池兄妹任领主/特色兵已出，927亲见矿车运龙晶金及熔炉铸浅林像金币，934炮弹充足。938罗嗣亲说火神矿一半上交帝国且火斧已分得两千余龙晶弹，给出上缴实际发生的直接后证，原题各项已回收；不据此宣全期逐批金额数量均已核清。',[923,924,925,926,927,934,938]),
'v04-local-chapter_unresolved_index-0164-01':('925六天城基本重建、92610级城正式池领主/玉清次领及特色兵，965建设90%以上继续给进度；938罗嗣明说矿一半已交帝国且火斧获分配，半矿实交已有明确后证，不应只停在批准比例或铸币。关闭原题具体建设任命/上缴是否有执行，不额外声称全城每屋竣工和全期逐笔账齐。',[924,925,926,938,965])}
for cid,(rationale,nums) in texts.items():
 before=next(x for x in rows if x['candidate_id']==cid);after=copy.deepcopy(before)
 after.update(status='answered',rationale=rationale,later_chapters=nums,later_evidence=evidence(nums))
 proposals.append({'candidate_id':cid,'input_path':str(f).replace('\\','/'),'input_sha256':sha(f),'reason':'938直接上缴/分配后证此前未纳入；原题问实际执行，并非全期逐笔对账。','before':before,'after':after})
out=P/'halfmine-two-items-proposal.json';assert not out.exists();dump(out,{'status':'proposal-not-applied','proposals':proposals})
print(sha(out))
