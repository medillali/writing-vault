from pathlib import Path
import json,hashlib,copy,sys
sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;A=H.parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
q=A/'character-arcs-part02-time-correction-proposal.json';assert sha(q)=='d7bfccb9a15446257cbfefc9750c0a7b2ba7ce1c5446e0555e66d2f1add8fa91';prop=json.loads(q.read_text(encoding='utf-8'));p=A/'character-arcs-part02.json';m=p.with_suffix('.md');v=A/'character-arcs-part02-validation.json'
assert sha(p)==prop['input_sha256'][p.name];assert sha(m)==prop['input_sha256'][m.name]
b=H/'corrections/character02-approved-time';b.mkdir(parents=True,exist_ok=False)
for x in [p,m,v]:(b/x.name).write_bytes(x.read_bytes())
before=json.loads(p.read_text(encoding='utf-8'));after=copy.deepcopy(before);change=prop['changes'][0];assert after['characters'][1]['terminal_state']==change['before'];after['characters'][1]['terminal_state']=change['proposed_after']
probe=copy.deepcopy(after);probe['characters'][1]['terminal_state']=change['before'];assert probe==before
oldmd=m.read_text(encoding='utf-8');assert oldmd.count(change['before'])==1;newmd=oldmd.replace(change['before'],change['proposed_after']);assert newmd.replace(change['proposed_after'],change['before'])==oldmd
dump(p,after);m.write_text(newmd,encoding='utf-8');receipt=json.loads(v.read_text(encoding='utf-8'));receipt['json_sha256']=sha(p);receipt['md_sha256']=sha(m);dump(v,receipt)
delta=dict(authorization='primary批准d7bf最小提案，仅一文学字段两raw数互换',before_json_sha256=sha(b/p.name),after_json_sha256=sha(p),before_md_sha256=sha(b/m.name),after_md_sha256=sha(m),changes=[change],all_other_values_unchanged=probe==before,md_only_same_sentence_replaced=True,source_check=prop['source_check'])
dump(A/'character-arcs-part02-approved-time-delta.json',delta);print(json.dumps(delta,ensure_ascii=False,indent=2))
