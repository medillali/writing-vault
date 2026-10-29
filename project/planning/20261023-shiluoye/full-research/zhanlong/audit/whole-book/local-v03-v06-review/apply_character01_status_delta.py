"""按primary批准，仅修三人物行的schema状态并保存原字节。"""
from pathlib import Path
import json,hashlib,copy
H=Path(__file__).resolve().parent;A=H.parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=A/'character-arcs-part01.json';m=p.with_suffix('.md');v=A/'character-arcs-part01-validation.json'
assert sha(p)=='464201e36fee72f025fb77e01085a2dff4f595db6755ea51e4a8a6cc6b0f9358'
b=H/'corrections/character01-schema-status';b.mkdir(parents=True,exist_ok=False)
for old in [p,m,v]: (b/old.name).write_bytes(old.read_bytes())
before=json.loads(p.read_text(encoding='utf-8'));after=copy.deepcopy(before);changes=[]
for i,row in enumerate(after['characters']):
 assert row['review_status']=='draft_pending_primary'
 row['review_status']='draft'
 changes.append(dict(path=['characters',i,'review_status'],before='draft_pending_primary',after='draft'))
probe=copy.deepcopy(after)
for row in probe['characters']:row['review_status']='draft_pending_primary'
assert probe==before
dump(p,after)
assert m.read_bytes()==(b/m.name).read_bytes()
receipt=json.loads(v.read_text(encoding='utf-8'));receipt['json_sha256']=sha(p);receipt['schema_review_status']='draft';dump(v,receipt)
delta=dict(authorization='primary消息批准仅三row review_status修为draft；其他字段逐值不变',before_json_sha256=sha(b/p.name),after_json_sha256=sha(p),before_md_sha256=sha(b/m.name),after_md_sha256=sha(m),changes=changes,other_values_unchanged=probe==before,md_bytes_unchanged=True)
dump(A/'character-arcs-part01-schema-status-delta.json',delta)
print(json.dumps(delta,ensure_ascii=False,indent=2))
