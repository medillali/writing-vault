"""首次交付前补747击杀撼梁证据；只增该项两证据字段。"""
from pathlib import Path
import copy, hashlib, json, shutil
H=Path(__file__).resolve().parent; A=H.parent
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
stem='adjudications-local-v03-batch004'; p=A/(stem+'.json')
assert sha(p)=='be7d7fa761c1a4510120cc7ccfed60cbee95fd5a2be67fede3fb27bb9d882b43'
before=load(p); after=copy.deepcopy(before); i=10
assert after[i]['candidate_id']=='v03-local-unresolved_and_anomalies-0030-02'
backup=H/'corrections'/'batch004-evidence';backup.mkdir(parents=True,exist_ok=False)
for f in [p,A/(stem+'.md'),H/(stem+'-validation.json'),H/'authored-v03-batch004.json']:
    shutil.copy2(f,backup/f.name)
e=copy.deepcopy(after[i]['later_evidence'][1]); e.update(chapter_id='ch-0747',start_line=58408,end_line=58461)
after[i]['later_evidence'].insert(2,e);after[i]['later_chapters'].insert(2,747)
for j in range(20):
    if j!=i: assert before[j]==after[j]
    else:
        assert {k:v for k,v in before[j].items() if k not in ['later_chapters','later_evidence']}=={k:v for k,v in after[j].items() if k not in ['later_chapters','later_evidence']}
auth=load(H/'authored-v03-batch004.json');auth[i]['refs'].insert(2,[747,58408,58461]);dump(H/'authored-v03-batch004.json',auth)
dump(p,after)
md=(A/(stem+'.md')).read_text(encoding='utf-8'); section='## '+after[i]['candidate_id']
start=md.index(section); end=md.index('\n## ',start+3)
chunk=md[start:end]; old='raw746 L58346—58407 (fact)；raw748'; new='raw746 L58346—58407 (fact)；raw747 L58408—58461 (fact)；raw748'
assert old in chunk
md=md[:start]+chunk.replace(old,new,1)+md[end:];(A/(stem+'.md')).write_text(md,encoding='utf-8')
receipt=load(H/(stem+'-validation.json'));receipt['sha256']=sha(p);receipt['first_handoff_evidence_supplement']='仅0030-02补747证据，其余字段/19项不变';dump(H/(stem+'-validation.json'),receipt)
dump(H/'batch004-evidence-supplement.json',dict(status='applied_before_first_handoff',before_sha256=sha(backup/p.name),after_sha256=sha(p),candidate_id=after[i]['candidate_id'],changed_fields=['later_chapters','later_evidence'],before={k:before[i][k] for k in ['later_chapters','later_evidence']},after={k:after[i][k] for k in ['later_chapters','later_evidence']},other_values_unchanged=True,original_reader='primary',current_action='本裁定者完整派生读取747原行，未重计该章原文覆盖'))
checks=load(H/'source-checks.json');assert not any(r['id']=='local03-batch004-stage-and-priority-correction' for r in checks['checks'])
checks['checks'].append(dict(id='local03-batch004-stage-and-priority-correction',actual_full_text_rereads=[dict(raw=740,start_line=57910,end_line=57980,begin_end_verified=True),dict(raw=743,start_line=58114,end_line=58186,begin_end_verified=True)],actual_targeted_source_ranges=[[68856,68885],[58222,58245],[58187,58221],[42825,42840],[62970,62979],[92748,92760]],complete_derived_notes_rows_read={'volume3':[506,507,509,527,528,529,711,729,732,740,743,744,745,746,747,748,749],'volume4':[841,842,915,916]},candidate_records_read='卷3稳定顺序61—80完整原记录与每个原子题；无截断。',findings='公告是十小时内而非后，撤研究误读；743临时交盾使用与749最终保有分阶段。霜林初韩后746日本澄清、747林杀撼梁与748主杀霜林分开。916明确失城后解除NPC领地军限制。818四倍与1282黑夜换算补早期时距边界。',attribution='原740/743等尾段reader=primary，本轮本裁定者实际全文复核740/743；其他列明派生行保原reader。定向段落不宣整章重读；不替代或覆盖冻结原notes。'))
dump(H/'source-checks.json',checks)
print(json.dumps(receipt,ensure_ascii=False))
