import json,hashlib,collections
from pathlib import Path
P=Path(__file__).parent;A=P.parent;B=P.parents[2]
load=lambda p:json.loads(p.read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):
 text=json.dumps(x,ensure_ascii=False,indent=2)+'\n'
 if not p.exists() or p.read_text(encoding='utf-8')!=text:p.write_text(text,encoding='utf-8')
scope=[r for r in load(A/'local-question-pool.json')['candidates'] if r['volume']==5]
assert len(scope)==556
rows=load(P/'adjudications-local-v05-tail.json');manifest=load(P/'input-manifest.json');log=load(P/'material-read-log.json')
assert len(rows)==379 and [r['scope_onebased_offset'] for r in rows]==list(range(178,557))
assert len(set(r['candidate_id'] for r in rows))==379
fields=['candidate_id','volume','original_path','original_field','original_index','atomic_index','title','original_record','original_evidence']
ident=[{k:c[k] for k in fields} for c in scope[177:]]
identity_sha=hashlib.sha256(json.dumps(ident,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
assert identity_sha==manifest['assigned_identity_sha256']
prefix_ids={r['candidate_id'] for r in scope[:177]}
assert not prefix_ids & {r['candidate_id'] for r in rows}
interfaces=[n for e in log['candidate_interfaces_read'] for n in range(e['onebased_start'],e['onebased_end']+1)]
assert interfaces==list(range(178,557))
read=set(log['complete_four_field_notes_read'])|set(log['complete_four_field_notes_reused_from_prior_scope'])
notes={};note_paths={}
for v in range(1,9):
 p=B/f'vol{v:02d}'/'chapter-notes.jsonl'
 for s in p.read_text(encoding='utf-8').splitlines():
  if s.strip():
   n=json.loads(s);raw=int(n['chapter_id'][3:]);notes[raw]=n;note_paths[raw]=str(p.relative_to(B)).replace('\\','/')
missing=sorted({n for r in rows for n in r['later_chapters']}-read)
assert not missing,('later chapter notes not logged',missing)
for r,c in zip(rows,scope[177:]):
 assert all(r[k]==c[k] for k in fields),(r['candidate_id'],'original changed')
 assert r['status'] in {'answered','partial','unrecovered','unknown'} and r['rationale'].strip() and r['audit_domain'].strip()
 assert r['later_chapters']==sorted(set(r['later_chapters'])) and r['later_chapters']
 assert len(r['later_evidence'])==len(r['later_chapters'])
 for raw,e in zip(r['later_chapters'],r['later_evidence']):
  n=notes[raw]
  assert e['chapter_id']==n['chapter_id'] and e['start_line']==n['start_line'] and e['end_line']==n['end_line']
  assert e['source_reader']==n.get('reader','unspecified') and e['research_path']==note_paths[raw]
  assert e['source_id']=='src-d8926e2a35f04bcf8139cff0ea516bbd' and e['revision']=='d819f7d0ecf5a2004a0a434e987569bbe25015422d45e16676af913292346857' and e['claim_kind']=='synthesis'
  if 'source_id' in n:assert e['source_id']==n['source_id']
  if 'revision' in n:assert e['revision']==n['revision']
parts=[];joined=[]
for i in range(1,8):
 p=P/f'adjudications-local-v05-tail-part{i:02d}.json';rs=load(p);v=load(P/f'part{i:02d}-validation.json')
 assert len(rs)==(60 if i<7 else 19) and sha(p)==v['sha256']
 joined+=rs;parts.append({'path':str(p.relative_to(A)).replace('\\','/'),'count':len(rs),'onebased_offsets':[rs[0]['scope_onebased_offset'],rs[-1]['scope_onebased_offset']],'sha256':sha(p)})
assert joined==rows
source_changes=[{'volume':r['volume'],'at_start':r['sha256'],'now':sha(B/r['path'])} for r in manifest['notes'] if sha(B/r['path'])!=r['sha256']]
assert not source_changes,('source notes SHA drift',source_changes)
log['targeted_source_points']=[{'chapter_id':'ch-1117','start_line':90389,'end_line':90416,'reader':'/root/zongheng_vol03_full','mode':'targeted-source-lines-only','full_chapter_read':False,'finding':'L90403每日照顾母亲为林逸欣自述，非陆；L90404—407陆附和/差清华250分。已报root，未改原notes/正式库。'}]
save(P/'material-read-log.json',log)
counts=dict(collections.Counter(r['status'] for r in rows))
md=['# 无双旧 local 卷五尾段 379 项终点裁定（待主审/唯一整合）','',
 '范围：原池 volume=5 的 1 基 offset178—556，排除 primary 已负责的前177。七块60×6+19恰为379；块文件是整合输入，聚合/快照不得重复导入。','',
 '阅读归属：本代理以完整原候选、相关四栏 notes 及对应后来四栏材料派生终审。卷五原文 reader 为 agent4；后证各保真实 reader。本轮新增一处 raw1117 L90389—90416 定点原文复核，不增加全文覆盖，不冒称独读无双全书。','',
 '判据：answered 包括完成、明确拒绝/失败、同物后态足证、规则解释与作者纠错；partial 明列复合项已答/仍未证；unrecovered 限具体承诺/账目未找到匹配回执，不宣作者忘或肯定未做；unknown 保身份、数字、动机、机制和源差。省略交接镜头不否定后来明确同物实用，后来相似事件也不能替原事件。','',
 f'状态分布：{json.dumps(counts,ensure_ascii=False)}。结构覆盖通过不等语义已签；正式导入由 agent4 按 root 白名单与固定 SHA 唯一组装。','']
for r in rows:
 md += [f'## {r["scope_onebased_offset"]}. {r["candidate_id"]}', '',f'原项：{r["title"]}', '',f'终点：**{r["status"]}**；域：{r["audit_domain"]}', '',r['rationale'],'',
 '后证：'+'；'.join(f'{e["chapter_id"]} L{e["start_line"]}—{e["end_line"]}（原 reader {e["source_reader"]}）' for e in r['later_evidence']),'']
(P/'adjudications-local-v05-tail.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
handoff=['# 卷五尾 379 项交接','',
 '本目录独占原池 volume5 的 offset178—556；primary 前177完全排除。379项原记录/原证据未改，17个接口范围连续覆盖，七个冻结块拼接与聚合逐值相等。','',
 '只整合七个 adjudications-local-v05-tail-partNN.json，勿再导聚合、before、unsubmitted-snapshots。当前均为待 root 语义主审的裁定产物，已签与待签状态由 root 的白名单管理。','',
 f'材料为分工原文 reader 的完整四栏笔记及最终研究派生，{len(log["complete_four_field_notes_read"])}条本轮完整四栏阅读/{len(log["complete_four_field_notes_reused_from_prior_scope"])}条前域复用；另 raw1117 28行定点原文确认照顾母亲为林。不是本代理卷五全文或全书新增全文覆盖。','',
 '重点边界：935国内MVP升10与974国际MVP分开；941俱乐存杯实际完成但另奖200万独账；986奥维亚净魂复体、987苏母耗尽真散；989千骨龙实付运达受控、1596守暗月实际出动；1196北冥CGL22实际入榜；994陆自述10%持股；1185晴空本人喜欢陆，非仍只十三解释。','',
 '林纳未被写死。两场山洪/临时榜与后战MVP/集团人数与单人末击不互替。千骑换千法、镇魂盒万魂释放仍需同事件回执，不用自家扩军或奥魂代答。陆母已亡与乱姥分开，不套纵横。','',
 'raw1117旧笔记主体误归已只读报root；本目录保原notes不改。主审指定 delta 的 before/after 另存，未把快照列整合输入。','']
for p in parts:handoff.append(f'- {p["path"]}：{p["count"]}项；SHA256 {p["sha256"]}')
(P/'handoff.md').write_text('\n'.join(handoff)+'\n',encoding='utf-8')
validation={'status':'scope-complete-structural-checks-passed-pending-primary-semantic-review-and-assembler-merge','scope_onebased':[178,556],'count':379,'status_counts':counts,
 'checks':{'exact_ids_offsets':True,'no_overlap_primary_prefix_177':True,'original_records_and_evidence_unchanged':True,'assigned_identity_hash_matches':True,'interfaces_exactly_cover_379_once':True,'seven_parts_equal_aggregate':True,'later_evidence_bounds_revision_reader_verified':True,'all_later_notes_logged_complete_or_reused':True,'eight_notes_sha_unchanged':True},
 'parts':parts,'inputs_manifest_sha256':sha(P/'input-manifest.json'),'material_read_log_sha256':sha(P/'material-read-log.json'),
 'outputs':[{'path':p.name,'sha256':sha(p)} for p in [P/'adjudications-local-v05-tail.json',P/'adjudications-local-v05-tail.md',P/'handoff.md']],
 'targeted_point_only':{'chapter_id':'ch-1117','lines':[90389,90416],'new_full_text_coverage':False},
 'later_notes_inheriting_source_metadata_from_book_manifest':[notes[n]['chapter_id'] for n in sorted({raw for r in rows for raw in r['later_chapters']}) if 'source_id' not in notes[n] or 'revision' not in notes[n]],
 'not_written':['formal library','source notes','main audit pools','primary prefix directory','other agents files']}
save(P/'validation.json',validation)
state=load(P/'review-state.json');state.update(status=validation['status'],completed=379,next_onebased_offset=None,validation='validation.json');save(P/'review-state.json',state)
print(json.dumps({'status':validation['status'],'count':379,'counts':counts,'aggregate_sha':sha(P/'adjudications-local-v05-tail.json'),'md_sha':sha(P/'adjudications-local-v05-tail.md'),'handoff_sha':sha(P/'handoff.md'),'validation_sha':sha(P/'validation.json'),'parts':parts},ensure_ascii=False,indent=2))
