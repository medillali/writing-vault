"""首次交付前收窄安吉拉知情，不以事件发生冒其逐招亲见。"""
from pathlib import Path
import copy,hashlib,json,shutil
H=Path(__file__).resolve().parent;A=H.parent;stem='adjudications-local-v03-batch011'
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=A/(stem+'.json');assert sha(p)=='129ebf2b5e96e78ebadad0ee29a46e7796a5742ae9d4da7d54a53b972e567c64'
before=load(p);after=copy.deepcopy(before);i=14
assert after[i]['candidate_id']=='v03-local-chapter_unresolved_index-0075-01'
old='587亲历他伤流霜献礼并由588系统确认叛；是否获知与何时信什么需分时'
new='587发生他伤流霜献礼、588系统确认叛，但事件发生不等安吉拉逐招亲见；是否获知与何时信什么需分时'
assert old in after[i]['rationale']
b=H/'corrections'/'batch011-knowledge';b.mkdir(parents=True,exist_ok=False)
shutil.copy2(p,b/p.name)
after[i]['rationale']=after[i]['rationale'].replace(old,new)
assert all(before[j]==after[j] for j in range(20) if j!=i)
assert {k:v for k,v in before[i].items() if k!='rationale'}=={k:v for k,v in after[i].items() if k!='rationale'}
dump(p,after)
for q in [A/(stem+'.md'),H/'authored-v03-batch011.json']:
    s=q.read_text(encoding='utf-8');assert s.count(old)==1;q.write_text(s.replace(old,new),encoding='utf-8')
receipt=load(H/(stem+'-validation.json'));receipt['sha256']=sha(p);receipt['first_handoff_narrowing']='0075-01仅收窄安吉拉知情，19项/其余字段不变';dump(H/(stem+'-validation.json'),receipt)
dump(H/'batch011-knowledge-narrowing.json',dict(before_sha256=sha(b/p.name),after_sha256=sha(p),candidate_id=after[i]['candidate_id'],before=before[i]['rationale'],after=after[i]['rationale'],other_values_unchanged=True,stage='before_first_handoff'))
print(sha(p))
