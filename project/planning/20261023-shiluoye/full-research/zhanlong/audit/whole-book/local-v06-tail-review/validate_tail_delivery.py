from save_tail_manual import Q,A,ROOT,F,read,write,sha
import collections,json,datetime
freeze=read(Q/'assigned-candidate-id-freeze.json');pool=read(A/'local-question-pool.json');assigned=[c for c in pool['candidates'] if c['volume']==6][200:399]
source=read(A.parents[1]/'source.json');bounds={c['chapter_id']:(c['start_line'],c['end_line']) for c in source['chapters']}
ids=[];rows=[];batches=[];refs=0
for i in range(1,11):
 p=Q/f'adjudications-local-v06-tail-batch{i:03d}.json';part=read(p);assert len(part)==(20 if i<10 else 19);rows.extend(part);batches.append(dict(path=p.name,sha256=sha(p),count=len(part)))
for c,r in zip(assigned,rows):
 assert r['candidate_id']==c['candidate_id'];assert r['title']==c['title'];assert r['original_record_sha256']==freeze['candidate_record_sha256'][c['candidate_id']]
 assert r['status'] in ('answered','partial','unknown','unrecovered');assert r['rationale'] and r['audit_domain'];ids.append(r['candidate_id'])
 assert r['later_chapters']==[int(e['chapter_id'].split('-')[1]) for e in r['later_evidence']]
 for e in r['later_evidence']:
  assert e['source_id']==source['source_id'] and e['revision']==source['revision'];lo,hi=bounds[e['chapter_id']];assert lo<=e['start_line']<=e['end_line']<=hi
  assert sha(ROOT/e['material_path'])==e['material_sha256'];assert e['source_reader'];refs+=1
assert ids==freeze['candidate_ids'] and len(ids)==len(set(ids))==199
st=read(Q/'reader-state.json');assert st['adjudicated_ids']==ids and st['done']==199
st.update(complete=True,completion_scope='199项人工终评草稿全部完成；primary逐项主审尚按实际签收进行，不代签、不合池',next_assigned_offset=199,original_volume_offset_next=399)
for p,s in zip(batches,st['batches']):assert p['sha256']==s['sha256']
write(Q/'reader-state.json',st)
progress=read(A.parents[1]/'primary-audit-review-progress.json');signed={}
for b in progress.get('batches',[]):
 if isinstance(b,dict):
  for key in ('path','batch_path'):
   if key in b:signed[b[key]]=b
validation=dict(status='passed-structural-and-provenance-not-semantic-primary-review',assigned_count=199,exactly_once=True,original_order_preserved=True,original_candidate_hashes_preserved=True,untouched_pool=True,status_counts=dict(collections.Counter(r['status'] for r in rows)),audit_domain_counts=dict(collections.Counter(r['audit_domain'] for r in rows)),later_evidence_count=refs,batches=batches,actual_reviewer='/root/zongheng_vol04_full',original_volume_reader='zongheng_vol05_full',reading_scope='正式派生后证人工逐项终评；本代理并未亲读卷六全卷原文。原文定向读另列。',priority_materials=[])
for p in [ROOT/'writing-vault/library/reports/zhanlong/vol02-primary-corrections.json',A/'priority-corrections-delta.json',ROOT/'writing-vault/library/reports/zhanlong/audit/priority-corrections-yan-recommendation.json']:
 if p.exists():validation['priority_materials'].append(dict(path=str(p.relative_to(ROOT)).replace('\\','/'),sha256=sha(p),original_files_unchanged=True))
write(Q/'coverage-validation.json',validation)
write(Q/'access-receipt.json',dict(reader='/root/zongheng_vol04_full',scope='本专项实际完整读取正式四栏及独立原文核验；既有上下文读完后证续接，搜索命中不是全文阅读',formal_notes_full_derived_raw=list(range(1251,1387)),additional_derived_raw=[409,1064,1187,1248],source_reader_preserved='zongheng_vol05_full；409为primary；1064为本代理旧实际卷五阅读',new_actual_original_full_raw=[1251,1260],original_full_boundaries=[dict(chapter_id=f'ch-{k:04d}',start_line=bounds[f'ch-{k:04d}'][0],end_line=bounds[f'ch-{k:04d}'][1]) for k in (1251,1260)],original_full_notes='定向整章BEGIN—END，非新增全书唯一覆盖；旧本人1358等全文核读在重点稿访问回执，不冒作本专项重新读',formal_notes_sha256={f.name:sha(f) for f in F.glob('vol??-chapter-notes.jsonl')},priority_derived_materials=validation['priority_materials']))
md=['# 卷六尾199项终评交接','',f"原卷六候选399项中0-based[200:399]共199；与reader5前200不重叠。10批（20×9+19），199 ID恰一次，后证{refs}条。只结构/来源验证通过，语义签收以root逐项账本为准。",'', '原文归属保留：本人采用正式四栏及已列定向原文；未声称亲读卷六全卷。所有原题/原候选指纹、两池与冻结分卷未改。','', 'answered含规则/源口径/证据约束完成，不能合称所有剧情伏笔已回收。', '', '## 当前唯一可组装批次','']
for b in batches:md.append(f"- `{b['path']}` · {b['count']}项 · SHA256 `{b['sha256']}`")
md += ['', 'before/proposal/delta、自核历史只供追溯，不能作为额外候选重复合入。batch001原before的c0f文件SHA与6f9 LF序列化SHA差仅换行，证明另存；003只应用root批准的1295兰后证。', '', '24重点及旧749全部保既有签收版本，本专项不改。']
(Q/'HANDOFF.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
print(json.dumps(dict(count=199,refs=refs,status_counts=validation['status_counts'],validation_sha256=sha(Q/'coverage-validation.json'),handoff_sha256=sha(Q/'HANDOFF.md')),ensure_ascii=False))
