"""只应用root已批准的首项rationale时点更正，保全部其他值与旧签输入。"""
from pathlib import Path
import copy,hashlib,json,shutil,sys
sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;A=H.parent
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=read(H/'batch001-time-wording-proposal.json');f=A/p['file'];old_sha=sha(f)
assert old_sha==p['base_sha256']
old=read(f);new=copy.deepcopy(old)
i=next(i for i,r in enumerate(new) if r['candidate_id']==p['candidate_id'])
assert new[i]['rationale']==p['before']
B=H/'corrections/batch001-time';B.mkdir(parents=True,exist_ok=False)
shutil.copy2(f,B/'before.json');shutil.copy2(f.with_suffix('.md'),B/'before.md')
v=H/'adjudications-local-v03-batch001-validation.json';shutil.copy2(v,B/'before-validation.json')
new[i]['rationale']=p['proposed_after']
masked=copy.deepcopy(new);masked[i]['rationale']=old[i]['rationale']
assert masked==old and all(new[j]==old[j] for j in range(len(old)) if j!=i)
write(f,new)
md=f.with_suffix('.md').read_text(encoding='utf-8');assert md.count(p['before'])==1
f.with_suffix('.md').write_text(md.replace(p['before'],p['proposed_after']),encoding='utf-8')
auth=H/'authored-v03-batch001.json';a=read(auth);assert a[i]['rationale']==p['before']
shutil.copy2(auth,B/'before-authored.json');a[i]['rationale']=p['proposed_after'];write(auth,a)
delta=dict(status='root_approved_applied_pending_resign',file=p['file'],candidate_id=p['candidate_id'],field='rationale',
           before_sha256=old_sha,after_sha256=sha(f),before=p['before'],after=p['proposed_after'],
           proof=dict(other_19_objects_exactly_equal=True,all_other_fields_of_this_object_exactly_equal=True,original_record_and_evidence_unchanged=True),
           source_basis=[dict(source_id='src-20f2d16e3d1b472fa4b230ab0e1770c9',revision='61ab0b114c76446fda554abfafdac8c432cd88afaba7c2541f4473a3902134e3',chapter_id='ch-0528',start_line=42827,end_line=42836,claim_kind='fact')],
           sequence='L42827—29主死亡掉装；L42832系统还有4分钟才可上线；L42833四分钟过后主出现/60分钟无敌；L42836兄妹被护回且林、李牧复活。',
           actual_reviewer='zongheng_vol05_full',approval='primary明确批准只改本项rationale；旧批已签，需primary读delta重新签收。')
write(H/'batch001-time-wording-applied-delta.json',delta)
val=read(v);val['sha256']=sha(f);val['correction']='batch001-time-wording-applied-delta.json';val['only_approved_rationale_changed']=True;write(v,val)
print(json.dumps(dict(new_batch_sha256=sha(f),delta_sha256=sha(H/'batch001-time-wording-applied-delta.json'),unchanged_other_objects=19),ensure_ascii=False))
