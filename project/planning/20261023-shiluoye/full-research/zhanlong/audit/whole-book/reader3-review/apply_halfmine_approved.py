from common import A,P,dump,sha
from revision import revise
import json,shutil
f=A/'adjudications-local-v04-batch016.json';snap=P/'v04-batch016-before-approved-halfmine-e70.json'
assert sha(f)=='e70a117e4cbb0379b12dcda81212705148b671e473d834d833a3f7e4fa7eb0eb'
assert not snap.exists();shutil.copy2(f,snap)
proposal=json.loads((P/'halfmine-two-items-proposal.json').read_text(encoding='utf-8'))
for i,x in enumerate(proposal['proposals']):
 after=x['after'];reason=after['rationale'].replace('两千余龙晶弹','2000多枚龙晶炮（语境为炮弹）').replace('火斧获分配','火斧已分得源称2000多枚龙晶炮（语境为炮弹）')
 nums=after['later_chapters']
 if i==1:nums=[924,925,926,927,938,965]
 revise(4,16,x['candidate_id'],f'approved-halfmine-{i+1}',{'status':after['status'],'rationale':reason,'later_chapters':nums},'root已完整读938并批准；第二项保927/仅补938；源炮名不静改。')
before=json.loads(snap.read_text(encoding='utf-8'));after=json.loads(f.read_text(encoding='utf-8'))
changed=[{'candidate_id':b['candidate_id'],'before':b,'after':a} for b,a in zip(before,after) if b!=a]
assert len(changed)==2
dump(P/'halfmine-approved-combined-delta.json',{'before_path':str(snap),'before_sha256':sha(snap),'after_path':str(f),'after_sha256':sha(f),'changes':changed,'other_18_equal':True})
print('FINAL',sha(f))
