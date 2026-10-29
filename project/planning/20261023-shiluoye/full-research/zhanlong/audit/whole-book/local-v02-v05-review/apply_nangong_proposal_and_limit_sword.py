from save_manual_batch import P,read,write,sha
import copy
p=read(P/'nangong-membership-and-sword-growth-proposal.json');ch=p['changes'][0];f=P/ch['path'];assert sha(f)==ch['input_sha256'];rows=read(f);hist=P/'history';hist.mkdir(exist_ok=True)
snap=hist/'batch003-before-nangong-membership.json';assert not snap.exists();snap.write_bytes(f.read_bytes())
i=next(i for i,x in enumerate(rows) if x['candidate_id']==ch['candidate_id']);assert rows[i]==ch['before'];rows[i]=ch['after'];write(f,rows)
md=f.with_suffix('.md');s=md.read_text(encoding='utf-8');s=s.replace(ch['before']['rationale'],ch['after']['rationale']).replace(f"**{ch['candidate_id']}** · partial",f"**{ch['candidate_id']}** · answered");s=s.replace('证据raw：258, 298, 921, 922, 926；','证据raw：258, 921, 922, 957, 1266；');md.write_text(s,encoding='utf-8')
delta=dict(status='applied-exact-approved-one-object-awaiting-primary-resign',primary_approval='root消息批准南宫第一条；不是用户品味/用户批准',proposal_sha256=sha(P/'nangong-membership-and-sword-growth-proposal.json'),batch_before_sha256=ch['input_sha256'],batch_after_sha256=sha(f),before_snapshot=str(snap.relative_to(P)).replace('\\','/'),change=ch,other_objects_equal=True)
write(P/'nangong-membership-merged-delta.json',delta)
state=read(P/'reader-state.json')
for b in state['submitted_batches']:
 if b['path']==f.name:b.update(sha256=sha(f),primary_review='pending-primary-delta-resign')
write(P/'reader-state.json',state)
second=copy.deepcopy(p['changes'][1]);second['after']['status']='partial';second['after']['rationale']='309补丁面板真生效，443秦王进化龙池；633以圣天融合升鬼阶且面板仍可进化1，957旧龙池加罗鼎神晶/定海石重铸五星游戏蝴蝶并实装，撤回587崩残等于后续成长未成的旧判断。补丁、后成长和千阳309亲拒旧恋/310对方撤离均已答；但633仍可进化1而957明确为重铸，原协商第二进化额度是否以何机制实际消费未独立说明，不将面板可能性当故事保证或作者遗忘。'
q=P/'sword-growth-quota-limited-proposal.json';assert not q.exists();write(q,dict(status='proposal-pending-primary-review-not-applied',previous_proposal_sha256=sha(P/'nangong-membership-and-sword-growth-proposal.json'),change=second,limited_delta_from_previous_after=dict(status_before='answered',status_after='partial',rationale_before=p['changes'][1]['after']['rationale'],rationale_after=second['after']['rationale']),meaning='仅第二条after的status/rationale收窄，其余字段包括后证逐值不动；batch007尚未应用。'))
print('batch003',sha(f));print('delta',sha(P/'nangong-membership-merged-delta.json'));print('sword-proposal',sha(q))
