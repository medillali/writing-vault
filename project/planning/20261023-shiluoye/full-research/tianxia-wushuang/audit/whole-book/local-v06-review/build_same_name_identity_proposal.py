"""为两个已签裁定创建独立proposal，不应用任何变更。"""
from pathlib import Path
from copy import deepcopy
import hashlib
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')
HERE=Path(__file__).resolve().parent
WS=next(p for p in HERE.parents if (p/'writing-vault').is_dir())
SID='src-d8926e2a35f04bcf8139cff0ea516bbd'
REV='d819f7d0ecf5a2004a0a434e987569bbe25015422d45e16676af913292346857'
SOURCE=WS/'writing-vault/private-sources/normalized/sources'/SID/(REV+'.txt')
lines=SOURCE.read_text(encoding='utf-8-sig').splitlines()
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,obj):
    (HERE/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
signed_inputs={
    'adjudications-local-v06-part01.json':'becef8a797c0e38c8f3d842f91be19c1287a63012fade47ee8f6f68f2e8a76a0',
    'adjudications-local-v06-part08.json':'ba23aee642636a2746c4077bd0a9148f2eb18a59766d269a59833fcd7065d7fd'
}
all_inputs={}
rows=[]
for p in sorted(HERE.glob('adjudications-local-v06-part*.json')):
    all_inputs[p.name]=sha(p)
    rows.extend((p.name,x) for x in json.loads(p.read_text(encoding='utf-8-sig')))
assert len(rows)==657 and len({r['candidate_id'] for _,r in rows})==657
for f,h in signed_inputs.items(): assert all_inputs[f]==h

read_check={
    'reviewer':'/root/zongheng_vol05_full',
    'status':'actual_full_raw_reread_complete_for_two_chapters',
    'source_id':SID,'revision':REV,
    'chapters':[{'chapter_id':'ch-1098','start_line':88875,'end_line':88948,'complete_read':True},
                {'chapter_id':'ch-1209','start_line':97112,'end_line':97183,'complete_read':True}],
    'truncated_pending':[],
    'identity_rows':[
        {'chapter_id':'ch-1098','line':88905,'player_id':'吻痕','region':'中国','level':165,'profession':'刺客','guild':'谁与争锋'},
        {'chapter_id':'ch-1098','line':88906,'player_id':'吻痕','region':'美国','level':192,'profession':'战士','guild':'英雄联盟'},
        {'chapter_id':'ch-1098','line':88907,'player_id':'吻痕','region':'无籍／荷兰背景','level':199,'profession':'战士','guild':'神圣盟约'},
        {'chapter_id':'ch-1209','line':97116,'player_id':'谁与争锋','region':'巴西','level':212,'profession':'剑术宗师','guild':'锋芒','office':'盟主'}],
    'error_type':'derived-research-entity-misattribution-not-source-text-anomaly',
    'conclusion':'1098的中国165刺客ID是吻痕；谁与争锋是其所属公会。1209的谁与争锋是巴西锋芒盟主。没有据此列出中国165刺客谁与争锋或美国192战士谁与争锋的依据。',
    'origin_boundary':'primary先完整回读发现；本代理随后再次BEGIN—END完整读1098/1209，纠正本人旧裁定与旧派生材料误配，不倒改冻结分卷原字段。'
}
for line,token in [(88905,'吻痕（中国）：刺客系玩家，LV-165，隶属于公会【谁与争锋】'),
                   (88906,'吻痕（美国）：战士系玩家，LV-192'),
                   (97116,'谁与争锋'),(97118,'行会：锋芒'),(97119,'职位：盟主')]:
    assert token in lines[line-1]
write('same-name-identity-source-check.json',read_check)
check_path=(HERE/'same-name-identity-source-check.json').relative_to(WS).as_posix()
def evidence(raw,start,end):
    return dict(source_id=SID,revision=REV,chapter_id=f'ch-{raw:04d}',start_line=start,end_line=end,
                claim_kind='fact',access_level='full-raw-chapter-reread-by-this-agent',
                research_path=check_path,reader='/root/zongheng_vol05_full')
new_evidence=[evidence(1098,88904,88909),evidence(1209,97115,97121)]
rationales={
    'v06-local-issue_log-001-01':
        '本项answered仅指实体消歧的研究记录约束已落实，并纠正原记录的误读：1098查询的是吻痕三同ID——中国165刺客、美国192战士及无籍199荷兰战士；中国刺客所属【谁与争锋】是公会名。1209另一玩家ID谁与争锋为巴西212剑术宗师、锋芒盟主，不能据1098公会名造出中国165刺客或美国192战士的同ID谁。原title/observation保为历史研究误读，不作新增人物事实；后续保护伞吻痕的行动不回填另服吻痕，巴西谁的盟约独立记录。',
    'v06-local-chapter_unresolved_index-151-02':
        '本项answered仅指身份记录约束，不是剧情伏笔回收。1209明确ID谁与争锋是巴西212剑术宗师、飞龙城锋芒盟主；1098中国165刺客、美国192战士及无籍199荷兰战士三个同ID均为吻痕，其中【谁与争锋】是中国吻痕所属公会。此前终评把公会名误当玩家ID并给巴西谁凑出中美同名者，属于研究误配，现明确撤回；本场国际盟约只归巴西谁，不无证增造同ID实体或跨服成长史。'
}
proposals=[]
allowed={'rationale','later_chapters','later_evidence'}
for file,before in rows:
    cid=before['candidate_id']
    if cid not in rationales: continue
    after=deepcopy(before)
    after['rationale']=rationales[cid]
    after['later_chapters']=sorted(set(after['later_chapters'])|{1098,1209})
    after['later_evidence'].extend(deepcopy(new_evidence))
    changed=[k for k in before if before[k]!=after[k]]
    assert set(changed)==allowed
    assert after['status']==before['status']=='answered'
    assert after['audit_domain']==before['audit_domain']
    proposals.append(dict(candidate_id=cid,path=file,input_sha256=all_inputs[file],
                          changed_fields=changed,before=before,proposed_after=after,
                          status_and_domain_unchanged=True,
                          original_fields_unchanged=True,
                          reason='primary原文复读识别旧研究误配；保原历史字段，在终评明确纠错并补两章直接后证。'))
assert len(proposals)==2

terms=['巴西','165','192','谁与争锋']
def walk(value,path=''):
    if isinstance(value,str):
        return [dict(field=path,text=value)] if any(t in value for t in terms) else []
    if isinstance(value,list): return [r for i,v in enumerate(value) for r in walk(v,f'{path}[{i}]')]
    if isinstance(value,dict):
        return [r for k,v in value.items() if k not in ['candidate_id','chapter_id','research_path','original_path','evidence_basis']
                for r in walk(v,f'{path}.{k}' if path else k)]
    return []
scan=[]
for file,row in rows:
    hits=walk(row)
    if hits:
        cid=row['candidate_id']
        if cid in rationales: disposition='proposal-required'
        elif cid=='v06-local-issue_log-001-02':
            disposition='shared-original-record-preserved-only-current-atomic-title-and-rationale-about-xiaoman-no-change'
        elif cid=='v06-local-chapter_unresolved_index-040-02':
            disposition='correct-kissmark-three-player-query-no-change'
        elif cid=='v06-local-chapter_unresolved_index-151-01':
            disposition='brazil-only-channel-boundary-no-false-same-id-no-change'
        else: disposition='unrelated-number-or-identity-no-change'
        scan.append(dict(candidate_id=cid,file=file,matched_fields=hits,disposition=disposition))
assert len(scan)==19
write('same-name-identity-scan.json',dict(status='complete',candidate_count_scanned=657,
    input_sha256=all_inputs,terms=terms,candidates_with_string_matches=len(scan),
    genuine_correction_candidate_ids=list(rationales),matches=scan,
    scope_boundary='递归检索657个稳定候选所有字符串字段，不把原始证据行号/候选编号误算语义；19个候选有字串命中，实际需纠两项。'))

proposal=dict(title='无双旧卷六已签裁定两项同名身份误配修订proposal',
    status='proposal_only_not_applied_pending_primary_approval',
    reviewer='/root/zongheng_vol05_full',
    request_origin='primary全文复读1098/1209发现，要求先proposal不改已签',
    error_class='derived-research-entity-misattribution',
    not_source_text_anomaly=True,not_unresolved_plot=True,
    frozen_input_sha256=signed_inputs,proposals=proposals,
    retained_boundary='只拟改两候选rationale/later_chapters/later_evidence；status=answered及audit_domain、原record/title/evidence不变，两批其余各59条逐值不变。本文件尚未应用。',
    source_check='same-name-identity-source-check.json',scan='same-name-identity-scan.json')
write('same-name-identity-correction-proposal.json',proposal)
md=['# 已签卷六两项实体误配proposal','',
    '仅提案，未应用；原签part01、part08与其余批次均未写入。primary先全文回读发现，本代理本轮再次完整读取raw1098与1209，无待补截断。','',
    '1098 L88904—88909是吻痕的三同ID：中国165刺客（公会名【谁与争锋】）、美国192战士、无籍199荷兰战士。1209 L97115—97121另明确巴西玩家ID谁与争锋，212级剑术宗师、锋芒盟主。不能把公会名偷换成刺客ID，更不能派生一个美国192战士谁与争锋。这是研究误配，不是原文矛盾或剧情未知。','',
    '| 候选ID | 保持 | 拟改 |','|---|---|---|']
for p in proposals:
    md.append(f"| {p['candidate_id']} | answered / {p['before']['audit_domain']}；原字段全部保留 | {p['proposed_after']['rationale']} 后证补raw1098 L88904—88909与raw1209 L97115—97121 |")
md += ['', '已对全部657候选递归检索巴西/165/192/谁与争锋，19个候选含字串命中；完整命中内容已人工核对。实际只需上列两项。040-02正确记吻痕三同ID；151-01仅巴西谁消息渠道，无误；001-02只是共享原记录保历史，当前小蛮原子标题/终评未重复该实体误断，不改它。其余是野王等级、伤害数、章节数等无关命中。','',
       '两项均维持研究约束answered，不宣故事伏笔新增回收；原title/observation保留，终评明确纠错避免历史错误被继续当事实引用。','',
       '[完整before/proposed_after](same-name-identity-correction-proposal.json) · [657检索结果](same-name-identity-scan.json) · [原文阅读与身份对照](same-name-identity-source-check.json) · [仅结构与保留字段验证](same-name-identity-proposal-validation.json)']
(HERE/'same-name-identity-correction-proposal.md').write_text('\n'.join(md)+'\n',encoding='utf-8')

for f,h in all_inputs.items(): assert sha(HERE/f)==h, '禁止提前改已签文件'
validation=dict(status='passed',proposal_only=True,applied=False,
    candidate_count_scanned=657,proposals_count=2,
    only_rationale_and_later_evidence_projection_changed=True,
    research_constraint_answered_preserved=True,original_fields_preserved=True,
    all_11_signed_input_files_unchanged=True,source_tokens_and_ranges_verified=True,
    semantic_approval='pending-primary-review-of-proposal-not-fabricated',
    output_sha256={n:sha(HERE/n) for n in ['same-name-identity-correction-proposal.json','same-name-identity-correction-proposal.md','same-name-identity-scan.json','same-name-identity-source-check.json']})
write('same-name-identity-proposal-validation.json',validation)
print(json.dumps(validation,ensure_ascii=False,indent=2))
