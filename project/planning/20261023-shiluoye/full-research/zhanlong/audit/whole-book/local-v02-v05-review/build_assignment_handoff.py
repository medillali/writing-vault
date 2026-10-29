import collections,datetime,json
from save_focus_manual import P,A,B,ROOT,read,write,sha
st=read(P/'reader-state.json');fixed=read(P/'assigned-candidate-id-freeze.json');batches=[];rows=[]
ledger=read(B/'primary-audit-review-progress.json');reviewed={x['path'].replace('\\','/').split('/')[-1]:x for x in ledger['batches']}
for b in st['submitted_batches']:
 p=P/b['path'];x=read(p);r=reviewed.get(p.name)
 assert r and r['sha256']==sha(p) and set(r['candidate_ids'])=={z['candidate_id'] for z in x}
 batches.append({'path':p.name,'sha256':sha(p),'count':len(x),'root_registered_sha_match':True});rows+=x
expected=fixed['volumes']['2']+fixed['volumes']['5'];assert [x['candidate_id'] for x in rows]==expected
assert len(rows)==len(set(x['candidate_id'] for x in rows))==749
counts=dict(collections.Counter(x['status'] for x in rows));domains=dict(collections.Counter(x['audit_domain'] for x in rows))
val={'status':'passed-assignment-coverage-and-primary-register-match','scope':'只核本分配749；不是全书最终验收','count':749,'volumes':{'2':448,'5':301},'batch_count':len(batches),'by_status':counts,'by_audit_domain':domains,'primary_progress_sha256_observed':sha(B/'primary-audit-review-progress.json'),'batches':batches,'original_candidate_id_freeze_sha256':sha(P/'assigned-candidate-id-freeze.json'),'findings_semantics':'所有终评手写；本工具只核对应primary实际主审登记与SHA，不产生终点评定','answered_limit':'含证据约束/研究纠正/规则边界，不能视为400剧情伏笔全部回收。'}
write(P/'assignment-coverage-validation.json',val)
lines=['# 《斩龙》卷2/5局部终评交接','',f'本分配749项已逐项手写：卷2 448、卷5 301；39批，每批至多20。当前root逐项主审登记的ID/SHA已机械对齐；这不是全书验收。','',f"终点状态：answered {counts['answered']}，partial {counts['partial']}，unknown {counts['unknown']}，unrecovered {counts['unrecovered']}。answered含75项evidence-boundary及其他证据/规则限制关闭，不能全算故事答案。",'', '当前批次是唯一合并入口；不合入before、proposal、unsubmitted快照、手写源或旧差分副本：','']
for b in batches:lines.append(f"- {b['path']} · {b['count']}项 · SHA `{b['sha256']}`")
lines += ['', '固定候选ID、原条目/原reader不变，两池未改。输入原指纹收据保input-receipt.json；重点组单独记录正式vol06-handoff链接适配SHA更正，未覆盖原收据。','', '原文归属：本人旧亲读卷2 raw252—404及卷5全卷；卷2 405—504是primary亲读/本人完整派生；其他卷为正式派生与单列定向原文。本轮原文复读见derived-access-checkpoint.json，不自称个人重新全文读全书。','', '优先：vol02-primary-corrections.json撤314两剑误合；全书priority-corrections-delta.json按已批overlay读取，撤狮盾“后才装备”、王域单体回血、乘风潜力上限、百里/龙忠近名误读。','', '重点研究另在父目录focused-findings-part01/02/03.json与end-state-audit-draft.json，按root各组主审状态，不在本终评账本伪填研究组签收。','']
(P/'HANDOFF.md').write_text('\n'.join(lines),encoding='utf-8');print(json.dumps({'validation_sha256':sha(P/'assignment-coverage-validation.json'),'handoff_sha256':sha(P/'HANDOFF.md'),'count':749,'by_status':counts},ensure_ascii=False))
