from pathlib import Path
import json,hashlib,copy,sys
sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;A=H.parent;p=A/'character-arcs-part06.json';m=p.with_suffix('.md');v=A/'character-arcs-part06-validation.json';q=A/'character-arcs-part06-support-classification-proposal.json'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert sha(q)=='a6e3cf376b8d2ecf51a9c0214bee5ef0968edd0b10dda52beeea7a941830eecf';assert sha(p)=='1db6a17252d8e0fb164dd20c16ae3184077f7fc66ae6825c60dbcaa949e74714';before=json.loads(p.read_text(encoding='utf-8'));after=copy.deepcopy(before);key='.planning/20261023-shiluoye/full-research/zhanlong/audit/whole-book/local-question-pool.json';val=after['formal_input_sha256'].pop(key);assert 'additional_support_sha256' not in after;after['additional_support_sha256']={key:val}
b=H/'corrections/character06-approved-support-classification';b.mkdir(parents=True,exist_ok=False)
for x in [p,m,v]:(b/x.name).write_bytes(x.read_bytes())
probe=copy.deepcopy(after);assert probe.pop('additional_support_sha256')=={key:val};probe['formal_input_sha256'][key]=val;assert probe==before
dump(p,after);rec=json.loads(v.read_text(encoding='utf-8'));rec['json_sha256']=sha(p);dump(v,rec)
delta=dict(authorization='primary批准a6e3仅依赖迁分类',before_json_sha256=sha(b/p.name),after_json_sha256=sha(p),before_md_sha256=sha(b/m.name),after_md_sha256=sha(m),changes=[dict(operation='move_key_same_path_same_sha256',from_path=['formal_input_sha256',key],to_path=['additional_support_sha256',key],before=val,after=val)],characters_and_other_values_unchanged=probe==before,md_bytes_unchanged=m.read_bytes()==(b/m.name).read_bytes());dump(A/'character-arcs-part06-approved-support-delta.json',delta);print(json.dumps(delta,ensure_ascii=False,indent=2))
