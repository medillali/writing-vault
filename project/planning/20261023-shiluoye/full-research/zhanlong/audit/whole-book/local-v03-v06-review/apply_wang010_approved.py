"""按primary已批准的两份提案受控修订010；不重建其他人物。"""
from pathlib import Path
import json, hashlib, copy

R=Path('C:/Users/Administrator/Documents/ChatGPT/Novel')
A=Path(__file__).resolve().parent.parent
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def dump(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def objsha(x): return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True).encode()).hexdigest()

p=A/'character-arcs-part03.json'; m=p.with_suffix('.md'); v=A/'character-arcs-part03-validation.json'
q=A/'priority-corrections-wang-identity-proposal.json'
e=A/'character-arcs-part03-wang-identity-evidence-material-proposal.json'
assert sha(q)=='584a5d0123215cc224a5deaf38d90c9fa1e6077220c370ebbf096a1077f261e8'
assert sha(e)=='0ce18016df724572490c1f04632a1cdc6e556a596290864068cb0eb9527f6e90'
proposal=load(q)['signed_character_changes']; ep=load(e)
assert sha(p)==ep['input_json_sha256'] and sha(m)==ep['input_md_sha256']
old=load(p); new=copy.deepcopy(old); oldmd=m.read_text(encoding='utf-8'); newmd=oldmd
before=A/'local-v03-v06-review/corrections/character03-approved-wang-identity'
assert not before.exists(); before.mkdir(parents=True)
ledger=A.parent.parent/'primary-research-group-review-progress.json'
assert ledger.exists()
snap={}
for f in [p,m,v,ledger]:
    (before/f.name).write_bytes(f.read_bytes()); snap[f.relative_to(R).as_posix()]=sha(f)
changes=[]
for ch in proposal['changes'][:4]:
    _,ix,k=ch['path']; assert ix==3 and new['characters'][ix][k]==ch['before']
    assert newmd.count(ch['before'])==1
    new['characters'][ix][k]=ch['proposed_after']
    newmd=newmd.replace(ch['before'],ch['proposed_after'],1)
    changes.append(dict(path=ch['path'],before=ch['before'],after=ch['proposed_after']))
oe=old['characters'][3]['evidence']; remove=ep['remove_exact_objects']
assert len(oe)==24 and len(remove)==1 and oe.count(remove[0])==1
retained=[x for x in oe if x!=remove[0]]
ne=retained+ep['append_exact_objects']; assert len(retained)==23 and len(ne)==27
for ref in ep['append_exact_objects']:
    assert ref['research_path']=='writing-vault/library/reports/zhanlong/audit/priority-corrections-wang-identity.json'
    assert sha(R/ref['research_path'])==ref['research_sha256']
new['characters'][3]['evidence']=ne
changes.append(dict(path=['characters',3,'evidence'],before=oe,after=ne))
def sourceline(refs): return '来源：'+'；'.join(f"raw{int(x['chapter_id'][3:])} L{x['start_line']}—{x['end_line']}" for x in refs)
assert newmd.count(sourceline(oe))==1
newmd=newmd.replace(sourceline(oe),sourceline(ne),1)
def diff(a,b,path=()):
    if a==b:return []
    if isinstance(a,dict) and isinstance(b,dict) and a.keys()==b.keys():
        return [d for k in a for d in diff(a[k],b[k],path+(k,))]
    if isinstance(a,list) and isinstance(b,list) and len(a)==len(b):
        return [d for i in range(len(a)) for d in diff(a[i],b[i],path+(i,))]
    return [list(path)]
assert diff(old,new)==[x['path'] for x in changes]
for i in range(7):
    if i!=3: assert old['characters'][i]==new['characters'][i]
assert {k:x for k,x in old.items() if k!='characters'}=={k:x for k,x in new.items() if k!='characters'}
dump(p,new); m.write_text(newmd,encoding='utf-8')
validation=load(v)
validation.update(json_sha256=sha(p),md_sha256=sha(m),evidence_count=sum(len(x['evidence']) for x in new['characters']))
validation['approved_correction_provenance']={
    'literary_proposal_sha256':sha(q),'evidence_material_proposal_sha256':sha(e),
    'scope':'仅010四文学字段及证据；其余六人、wrapper与010其他字段逐值不变；MD同四句及该行来源定位同步。',
    'primary_approval':'root消息批准584a四文学字段与0ce180证据材料补案；本回执不代替主审重签。'}
dump(v,validation)
delta=dict(status='applied_as_approved_pending_primary_independent_replay',actual_operator='zongheng_vol05_full',
    snapshotted_before_sha256=snap,proposal_sha256={'literary':sha(q),'evidence_material':sha(e)},
    changes=changes,json_sha256=sha(p),md_sha256=sha(m),validation_sha256=sha(v),
    assertions={'only_five_json_field_paths_changed':True,'other_six_characters_equal':True,
                'wrapper_equal':True,'retained_original_23_evidence_equal_and_ordered':True,
                'result_evidence_count_27':True,'md_only_four_sentences_and_one_source_line_changed':True,
                'original_freeze_and_formal_files_not_written':True,'ledger_copied_not_written':True},
    original_retained_evidence_objects_sha256=objsha(retained))
dump(A/'character-arcs-part03-approved-wang-identity-delta.json',delta)
print(json.dumps({k:delta[k] for k in ['json_sha256','md_sha256','validation_sha256','assertions']},ensure_ascii=False,indent=2))
