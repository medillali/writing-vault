"""王者领域指代的逐值优先纠正提案；只读正式/冻结，不执行更正。"""
from pathlib import Path
import hashlib,json,sys
sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;BOOK=H.parent.parents[1];ROOT=BOOK.parents[3];F=ROOT/'writing-vault/library/reports/zhanlong'
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def at(x,path):
    for k in path:x=x[k]
    return x
source=load(BOOK/'source.json');fields=[]
new_inference='530 L42945的“自身10%”承接所有友方目标，可指每个受益目标自身血量，不能强读成仅佩戴者回血；541实际群体回血与此不直接冲突。1109 L81321同句式及L81328队友解释可作终审回指，非新补丁；此章范围收益明确跨敌会。'
new_unresolved='蛮王BOSS/装备分法尚未落实；王戒实际群体收益已见，不据“自身”指代另造回复范围冲突。'
def add_notes(p):
    rows=[json.loads(s) for s in p.read_text(encoding='utf-8').splitlines()]
    for n,path,after in [(530,['facts',1],None),(541,['inferences',0],new_inference),(541,['unresolved',0],new_unresolved)]:
        i=next(i for i,r in enumerate(rows) if r['chapter_id']==f'ch-{n:04d}');r=rows[i];before=at(r,path)
        if after is None:
            assert '每秒自己10%回血' in before;after=before.replace('每秒自己10%回血','各友方目标每秒获自身10%回血')
        assert before!=after
        fields.append(dict(file=p.relative_to(ROOT).as_posix(),input_sha256=sha(p),jsonl_index=i,chapter_id=r['chapter_id'],json_path_within_row=path,before=before,proposed_after=after,original_research_reader=r['reader'],original_read_at=r['read_at']))
for p in [F/'vol03-chapter-notes.jsonl',F/'vol03-prefix-chapter-notes.jsonl',BOOK/'vol03/chapter-notes.jsonl',BOOK/'vol03/prefix-chapter-notes.jsonl']:add_notes(p)
p=F/'vol03-analysis.json';path=['chapter_unresolved_index',34,'unresolved',0]
fields.append(dict(file=p.relative_to(ROOT).as_posix(),input_sha256=sha(p),json_path=path,before=at(load(p),path),proposed_after=new_unresolved,original_research_reader='zongheng_vol05_full（原逐章行）；primary合卷'))
refs=[dict(source_id=source['source_id'],revision=source['revision'],chapter_id=f'ch-{n:04d}',start_line=a,end_line=b,claim_kind='fact') for n,a,b in [(530,42939,42950),(541,43775,43782),(1109,81317,81329)]]
proposal=dict(status='proposal_only_not_applied',issue_id='kings-domain-pronoun-scope',book='zhanlong',actual_reviewer='zongheng_vol05_full',finding='原面板“所有友方目标…并且每秒获自身10%”可分配指各目标自身血量，没有明说仅装备者；实际群体回血不构成必然矛盾。旧研究误把指代收为佩戴者，不当小说异常。',source_evidence=refs,affected_fields=fields,dependent_local_candidates=['v03-local-chapter_unresolved_index-0035-02'],reading_attribution='530/541原初全文与本轮定向段落由本裁定者实际读；1109原初全文属卷5原reader，本轮只实际读L81317—81329定向段，不冒整章。',preserved_boundaries=['只收窄原研究“自身=仅佩戴者”和必然冲突断言，不删原阶段蛮王未杀/尚待分配。','1109是后来的成长强化版；1000码/150%/10分钟/4小时不能倒灌530的500码/100%/120秒/12小时。','初读notes、reader/read_at、原批次、冻结研究、正式库和原池均未修改。','stage原批次batch0529-0530与batch0539-0542仅保历史；若从这些归档引用同原句，亦须遵优先纠正层，提案不改原件。'],scan_scope='正式卷3 analysis/cards/graph/report/handoff与canonical/prefix notes已扫描并逐命中读；除列明13字段之外，诸如吸血/披风秒回/团体实用属于不同语义，不改。')
target=H/'priority-ring-corrections-proposal.json';assert not target.exists();target.write_text(json.dumps(proposal,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
md=['# 王者领域回血指代优先纠正提案','','仅提案；原正式库与冻结记录未改。','',proposal['finding'],'','原文：530 L42945；541 L43777—82；1109 L81321/81328。','']
for i,r in enumerate(fields,1):
    path=r.get('json_path',r.get('json_path_within_row'));where=('JSONL '+str(r['jsonl_index'])+' / ') if 'jsonl_index' in r else ''
    md += [f'## {i}. '+r['file'],'',where+'.'.join(map(str,path)),'','原：'+r['before'],'','拟优先：'+r['proposed_after'],'','原归属：'+r['original_research_reader'],'']
md+=['## 边界','',*proposal['preserved_boundaries'],'',proposal['reading_attribution'],'']
(H/'priority-ring-corrections-proposal.md').write_text('\n'.join(md),encoding='utf-8')
assert len(fields)==13
assert all(sha(ROOT/r['file'])==r['input_sha256'] for r in fields)
print(json.dumps(dict(fields=len(fields),proposal_sha256=sha(target),no_frozen_changes=True),ensure_ascii=False))
