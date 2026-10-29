"""应用root批准的0078-01最小更正，保留原签版本。"""
from pathlib import Path
import collections,copy,hashlib,json,sys
sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;A=H.parent
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=A/'adjudications-local-v03-batch011.json';m=p.with_suffix('.md');proposal=read(A/'batch011-rolin-kill-attribution-proposal.json')
assert sha(p)==proposal['input_batch_sha256']
before=read(p);after=copy.deepcopy(before);idx=next(i for i,r in enumerate(before) if r['candidate_id']==proposal['candidate_id'])
assert before[idx]==proposal['before']
after[idx]=proposal['proposed_after']
fields=proposal['allowed_fields'];assert fields==['rationale','later_chapters','later_evidence']
assert all(a==b for i,(a,b) in enumerate(zip(before,after)) if i!=idx)
assert {k:v for k,v in before[idx].items() if k not in fields}=={k:v for k,v in after[idx].items() if k not in fields}
out=H/'corrections/batch011-approved-kill-attribution';out.mkdir(parents=True,exist_ok=False)
for f in [p,m,H/'adjudications-local-v03-batch011-validation.json']:(out/f.name).write_bytes(f.read_bytes())
oldmd=m.read_text(encoding='utf-8');assert oldmd.count(before[idx]['rationale'])==1
dump(p,after);newmd=oldmd.replace(before[idx]['rationale'],after[idx]['rationale'])
oldref='证据：'+'；'.join(f"raw{int(e['chapter_id'][3:])} L{e['start_line']}—{e['end_line']} ({e['claim_kind']})" for e in before[idx]['later_evidence'])
newref='证据：'+'；'.join(f"raw{int(e['chapter_id'][3:])} L{e['start_line']}—{e['end_line']} ({e['claim_kind']})" for e in after[idx]['later_evidence'])
assert newmd.count(oldref)==1;m.write_text(newmd.replace(oldref,newref),encoding='utf-8')
delta=dict(candidate_id=proposal['candidate_id'],approval='root明确批准仅该条理由及新增833证据；保status/domain及其他19',before_batch_sha256=proposal['input_batch_sha256'],after_batch_sha256=sha(p),before=before[idx],after=after[idx],changed_fields=fields,other_19_exactly_equal=True,unlisted_fields_exactly_equal=True,source_ranges_checked=[[833,63805,63820],[1174,85720,85728]],frozen_volume_untouched=True)
dump(A/'batch011-rolin-kill-attribution-applied-delta.json',delta)
receipt=read(H/'adjudications-local-v03-batch011-validation.json');receipt.update(sha256=sha(p),approved_delta='batch011-rolin-kill-attribution-applied-delta.json',previous_validation_preserved=str(out.relative_to(A)))
dump(H/'adjudications-local-v03-batch011-validation.json',receipt)
print(json.dumps(dict(batch_sha256=sha(p),delta_sha256=sha(A/'batch011-rolin-kill-attribution-applied-delta.json'),other_19_exactly_equal=True),ensure_ascii=False))
