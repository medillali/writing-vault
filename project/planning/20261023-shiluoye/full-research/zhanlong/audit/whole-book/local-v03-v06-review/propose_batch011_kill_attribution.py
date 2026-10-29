"""只生成主审要求的单项提案，不修改已签批。"""
from pathlib import Path
import copy,datetime,hashlib,json,sys
sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;A=H.parent
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
batch=A/'adjudications-local-v03-batch011.json'
before=next(r for r in read(batch) if r['candidate_id']=='v03-local-chapter_unresolved_index-0078-01')
after=copy.deepcopy(before)
after['rationale']=before['rationale'].replace('后606复苏、1174再回指她亲杀罗林，决裂有后证却不倒写584已完全信主。','后606复苏；1174主回顾“罗林是她一手杀掉的”并叙她杀旧友留下阴影，只保为后文归功与心理描写，833系统实际公告末刀为问剑、青萝等亦参与压血，不据回顾改写击杀链或认单人击杀。587遇害、606复苏与后来旧友已死可证决裂代价，却不倒写584已完全信主。')
ref=copy.deepcopy(before['later_evidence'][0]);ref.update(chapter_id='ch-0833',start_line=63809,end_line=63820,claim_kind='fact')
after['later_evidence']=before['later_evidence']+[ref]
after['later_chapters']=list(dict.fromkeys(before['later_chapters']+[833]))
proposal=dict(status='proposal_only_pending_primary',created_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),actual_reviewer='zongheng_vol05_full',input_batch=str(batch.relative_to(A)),input_batch_sha256=sha(batch),candidate_id=before['candidate_id'],allowed_fields=['rationale','later_chapters','later_evidence'],before=before,proposed_after=after,other_19_unchanged=True,source_check=dict(actual_reader='zongheng_vol05_full',kind='targeted_source_ranges_not_new_whole_chapter_coverage',ranges=[{'raw':833,'start_line':63805,'end_line':63820},{'raw':1174,'start_line':85720,'end_line':85728}]),boundary='不修改原notes、冻结分卷、正式库、已签批；待root批准精确应用。')
target=A/'batch011-rolin-kill-attribution-proposal.json'
if target.exists():
    archive=H/'unsubmitted-batch011-rolin-proposal-before-narrowing.json'
    assert not archive.exists()
    archive.write_bytes(target.read_bytes())
target.write_text(json.dumps(proposal,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(A/'batch011-rolin-kill-attribution-proposal.md').write_text('# 0078-01 罗林击杀归属最小提案\n\n原批SHA：'+sha(batch)+'\n\n仅拟改理由并补raw833 L63809—63820；status/domain与其余19项不改。\n\n原理由：'+before['rationale']+'\n\n拟改理由：'+after['rationale']+'\n\n实际定向源核：833 L63805—63820；1174 L85720—85728。未宣重读整章，不改变原阅读归属。\n',encoding='utf-8')
print(json.dumps(dict(before_rationale=before['rationale'],proposed_rationale=after['rationale'],proposal_sha256=sha(target)),ensure_ascii=False))
