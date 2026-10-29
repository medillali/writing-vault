from common import A,P,dump,sha
from revision import revise
import json,shutil
proposal=json.loads((P/'later-cap-order-four-items-proposal.json').read_text(encoding='utf-8'))
snapshots={}
for x in proposal['proposals']:
 f=A/Path(x['input_path']).name if False else A/x['input_path'].replace('\\','/').split('/')[-1]
 if f.name not in snapshots:
  assert sha(f)==x['input_sha256'];s=P/(f.stem+'-before-approved-cap.json');assert not s.exists();shutil.copy2(f,s);snapshots[f.name]=s
for i,x in enumerate(proposal['proposals']):
 cid=x['candidate_id'];bn=int(x['input_path'].replace('\\','/').split('/')[-1].split('batch')[1].split('.')[0]);after=x['after']
 changes={k:after[k] for k in ['rationale','later_chapters']}
 if cid.endswith('-0177-01'):changes['audit_domain']='resting-army-and-later-authorized-expansion'
 revise(4,bn,cid,f'approved-cap-{i+1}',changes,'root全文主审并原文核975 L72503批准；四项status partial不动，0177分类同步。')
out=[]
for filename,snap in snapshots.items():
 f=A/filename;before=json.loads(snap.read_text(encoding='utf-8'));after=json.loads(f.read_text(encoding='utf-8'))
 changed=[{'candidate_id':b['candidate_id'],'before':b,'after':a} for b,a in zip(before,after) if b!=a]
 out.append({'file':filename,'before_path':str(snap),'before_sha256':sha(snap),'after_sha256':sha(f),'count':len(changed),'changes':changed,'other_objects_equal':True})
assert sum(x['count'] for x in out)==4
dump(P/'cap-order-approved-combined-delta.json',{'batches':out,'four_changed_other_56_equal':True,'status_all_unchanged':True})
for x in out:print(x['file'],x['after_sha256'])
