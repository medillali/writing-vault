from pathlib import Path
import json,hashlib,copy,sys
sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;A=H.parent;R=Path('C:/Users/Administrator/Documents/ChatGPT/Novel')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=A/'character-arcs-part06.json';v=A/'character-arcs-part06-validation.json';d=json.loads(p.read_text(encoding='utf-8'));old=copy.deepcopy(d);b=H/'corrections/character06-unsubmitted-input-addendum';b.mkdir(parents=True,exist_ok=False)
for x in [p,v]:(b/x.name).write_bytes(x.read_bytes())
extra={}
for x in [A/'local-question-pool.json',R/'writing-vault/library/reports/zhanlong/vol04-chapter-notes.jsonl']:
 extra[x.relative_to(R).as_posix()]=sha(x)
d['formal_input_sha256'].update(extra);dump(p,d);assert d['characters']==old['characters']
q=json.loads(v.read_text(encoding='utf-8'));q['json_sha256']=sha(p);q['additional_derived_input_sha256']=extra;dump(v,q)
receipt=dict(status='current_merged_terminal_and_actual_notes_read_not_full_pool_reread',actual_reviewer='zongheng_vol05_full',group=6,sha256=extra,reading_scope='实际完整读魏凡/欧阳川相关当前终评8条的全部理由/状态/后证章行；再完整读卷4 raw842/843/854/959四栏记录，原读者/root/zongheng_vol03_full归属保留；不是本人原文重读。',characters_unchanged=True,json_sha256=sha(p),md_sha256=sha(p.with_suffix('.md')));dump(A/'character-arc-input-addendum06.json',receipt);print(json.dumps(receipt,ensure_ascii=False,indent=2))
