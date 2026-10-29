import json,hashlib,collections,datetime
from pathlib import Path
P=Path(__file__).parent; A=P.parent; B=P.parents[2]; W=B.parents[3]
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return p.relative_to(W).as_posix()
pool=load(A/'historical-question-pool.json'); freeze=load(A/'candidate-id-freeze.json')
orig={x['candidate_id']:x for x in pool['candidates'] if x['volume']<=4}
existing={}
for f in ['adjudications-history-closed-early.json','adjudications-history-closed-middle.json']:
 for i,x in enumerate(load(A/f)):
  if x['candidate_id'] in orig:existing[x['candidate_id']]={'path':rel(A/f),'index':i,'row':x}
assert set(existing)==set(freeze['already_adjudicated_history_1_to_4'])
seeds=[]
for v in range(1,5):seeds+=load(P/f'seed_v{v:02d}.json')
for row in seeds:
 if row['candidate_id']=='v01-thread-002':
  row['rationale']='99北冥/亚现实到位，159系统血佣建会、168核心回古剑；237金鳞弓拍定净金币入账且14万金币已兑换，238炼狱权杖成交净金币入账、其银行兑换仍预计，显示独立收入渠道实际成形。本条关闭从四人实体工作室到系统组织与收入渠道成形的目标，不把全部未来债务、每期工资或基金缴足并作已结。236仅候拍，不能写成已分账。'
  row['later_chapters']=[99,159,168,237,238]
 if row['candidate_id']=='v04-thread-003':
  row['rationale']='625新第八刺盟实际成立，734伏击与757传送陷阱死亡/未停阵是不同结果；1573陆尘又实际命漂亮小蛮第八分盟到碎石林设伏，证明其后阶段组织角色。不由玩家可复通则编造757精确复活位置/时刻，也不把后活反证当场从未阵亡。本条目标是新刺盟成军/能力检验，包含真实失败而关闭；不把1573聚歼战策扩大为敌无人生还。'
  row['later_chapters']=[625,734,757,1573]
assert len(seeds)==55 and len({x['candidate_id'] for x in seeds})==55
assert set(x['candidate_id'] for x in seeds).isdisjoint(existing)
assert set(x['candidate_id'] for x in seeds)|set(existing)==set(orig)
notes={};note_paths={}
for v in range(1,9):
 p=B/f'vol{v:02d}'/'chapter-notes.jsonl'
 for line in p.read_text(encoding='utf-8').splitlines():
  if line.strip():
   n=json.loads(line);raw=int(n['chapter_id'][3:]);notes[raw]=n;note_paths[raw]=p
source=load(B/'source.json')
sourcekeys=list(source) if isinstance(source,dict) else []
allowed={'answered','partial','unrecovered','unknown'}
method={
 'purpose':'卷1—4历史80候选终点复核；本次可合并输入仅新增55。既判25保原判，不重复写入合并数组。',
 'terminal_enums':{
  'answered':'原问题有明确完成、失败、拒绝、规则解释或作者纠错回执；不等愿望成功，也不抹除后续新风险。',
  'partial':'复合项中部分已有后证，剩余独立环节仍无明确答案；理由逐层写明。',
  'unrecovered':'针对原独立承诺、账目或责任，到终点材料未找到专属回收；不等客观一定未履，不宣作者遗忘。',
  'unknown':'事实、动机、司法或源文矛盾证据仍不足；数值/文本源差归source-anomaly而非剧情遗忘。'},
 'access':'依据最终正式分卷analysis/graph/cards/report及冻结handoff、逐章notes派生复核；这55项本轮没有新增原文全文阅读。原章节行范围由逐章notes/source元数据定位，不把元数据检验当语义批准。',
 'reader_attribution':'本代理原亲读卷3 raw0229—0606和卷8尾1573—1609；卷8前1505—1572是primary实读，本代理完整复核其68条notes。其余卷引用按实际reader字段归属；不自称独自全文实读全书。',
 'matching':'原始义务、对象、事件实例、时点须匹配；不得用末期类似取样/同名人物/另一次解控/泛化玩家复活规则替代早期事件专属后证。',
 'scope':'范围80条含原resolved与open；不因已resolved而免核。既判25完整阅读理由与依据，同意且无override。'}
rows=[]
for x in seeds:
 c=orig[x['candidate_id']]
 assert x['status'] in allowed and x['rationale'] and x['audit_domain']
 x['volume']=c['volume'];x['title']=c['title'];x['entry_type']=c['entry_type']
 x['original_path']=c['original_path'];x['original_index']=c['original_index']
 x['original_stage_status']=c['original_stage_status'];x['original_record']=c['original_record']
 x['original_evidence']=c['original_evidence']
 x['later_chapters']=sorted(set(x['later_chapters']))
 ev=[]
 for raw in x['later_chapters']:
  assert raw in notes,(x['candidate_id'],raw)
  n=notes[raw]
  ev.append({'chapter_id':n['chapter_id'],'start_line':n['start_line'],'end_line':n['end_line'],
   'source_id':n.get('source_id'),'revision':n.get('revision'),'claim_kind':'synthesis',
   'access_level':'derived-chapter-notes-and-final-volume-research','notes_path':rel(note_paths[raw]),
   'notes_reader':n.get('reader','not-recorded-in-note'),'prior_direct_read_by_this_agent':229<=raw<=606 or 1573<=raw<=1609,
   'evidence_role':'原义务/回收/对照实例见rationale；列入不表示该章独立证明所有子结论。'})
 x['later_evidence']=ev
 x['access_level']='derived-audit; no-new-full-text-reading'
 x['boundary']='终点判定只对原条所述对象与义务成立；未见专属证据不推出客观未发生。原文事实与本条综合判定分层。'
 rows.append(x)
rows.sort(key=lambda x:x['candidate_id'])
save(P/'adjudications-history-v01-v04.json',rows)
save(P/'method.json',method)
coverage=[]
for cid,c in sorted(orig.items()):
 if cid in existing:
  e=existing[cid]
  coverage.append({'candidate_id':cid,'volume':c['volume'],'title':c['title'],'review_type':'existing-25-reviewed-agree',
   'status':e['row']['status'],'adjudication_path':e['path'],'adjudication_index':e['index'],
   'original_record':c['original_record'],'review_result':'完整复核原问题、既判理由及后文章号，同意；不重复交同ID合并，不提交override。'})
 else:
  r=next(x for x in rows if x['candidate_id']==cid)
  coverage.append({'candidate_id':cid,'volume':c['volume'],'title':c['title'],'review_type':'new-55',
   'status':r['status'],'adjudication_path':rel(P/'adjudications-history-v01-v04.json'),'original_record':c['original_record']})
save(P/'coverage-80.json',coverage)
save(P/'existing-25-review.json',[x for x in coverage if x['review_type'].startswith('existing')])
inputs=[]
paths=[A/'candidate-id-freeze.json',A/'historical-question-pool.json',A/'adjudications-history-closed-early.json',A/'adjudications-history-closed-middle.json',B/'source.json']
for v in range(1,9):
 formal=W/'writing-vault/library/reports/tianxia-wushuang'
 for suffix in ['analysis.json','cards.json','graph.json','report.md']:
  p=formal/f'vol{v:02d}-{suffix}'
  if p.exists():paths.append(p)
 for name in ['handoff.md','chapter-notes.jsonl']:
  p=B/f'vol{v:02d}'/name
  if p.exists():paths.append(p)
for p in paths:inputs.append({'path':rel(p),'sha256':sha(p),'bytes':p.stat().st_size})
expected_v7='5aed431e426a75bd77361dbc110e0bad9173fc71825be36f259bfb05a556d48f'
v7p=W/'writing-vault/library/reports/tianxia-wushuang/vol07-analysis.json'
assert sha(v7p)==expected_v7,'wait correct formal v7'
manifest={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'historical_identity_sha256':freeze['historical']['candidate_identity_sha256'],
 'scope_counts':{'v1':18,'v2':26,'v3':14,'v4':22,'all':80,'new':55,'existing_reviewed_no_override':25},
 'inputs':inputs,'formal_v7_dependency_refresh':'root定向纠分盟/时长误读后的正式analysis；不改36综合或任何冻结包。',
 'access':method['access'],'reader_attribution':method['reader_attribution']}
save(P/'input-manifest.json',manifest)
count=dict(collections.Counter(x['status'] for x in rows))
save(P/'review-state.json',{'scope':'history-v01-v04','new_completed':55,'existing_reviewed':25,'total_scope':80,
 'missing':[],'overrides':[],'new_status_counts':count,'status':'ready-for-primary-semantic-review-not-merged',
 'next_task':'独占卷1/3新增notes-unresolved，等agent4稳定ID接口；不改本次历史候选ID。'})
md=['# 无双卷一至四历史候选终点复核（待主审）','',
 '完整范围80条：新增裁定55条，既判25条复核同意、无override。可合并输入仅本目录`adjudications-history-v01-v04.json`，不要把coverage或既判25当新增再次合并。','',
 '本轮来源为最终正式分卷研究、冻结交接与逐章笔记；没有新增加全书正文实读。本代理亲读范围和各证据真实reader见`method.json`及JSON逐条记录。','',
 'answered可表示明确失败/拒绝/规则解释；partial逐项保留未答子项；unrecovered仅表示原独立义务未见专属回收；unknown保事实/动机/源文冲突。任何未见回收均不自动等于作者遗忘。','',
 '所有章号为raw。695早期500cc供者确证不能被1595抗原取样替代；124牧师旧SSS以系统失败关闭；667预言不能用1354另一控实例补结；达达融狼不等原犬肉身复活；796守胜与935升十级分时。','',
 f'新增状态统计：{json.dumps(count,ensure_ascii=False)}。','',
 '## 新增55条','']
for x in rows:
 md += [f"### {x['candidate_id']} · {x['title']} · {x['status']}",'',
        '原条：'+json.dumps(x['original_record'],ensure_ascii=False,separators=(',',':')),'',x['rationale'],'',
        '后证：'+ '；'.join(f"{e['chapter_id']} L{e['start_line']}—{e['end_line']}（reader={e['notes_reader']}）" for e in x['later_evidence']),'']
md+=['## 全范围80核对','', '|ID|卷|终点|处理|','|---|---:|---|---|']
md += [f"|{x['candidate_id']}|{x['volume']}|{x['status']}|{x['review_type']}|" for x in coverage]
(P/'adjudications-history-v01-v04.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
result={'scope':80,'new':55,'existing':25,'missing':[],'overlap_new_existing':[],
 'new_status_counts':count,'checks':{'unique_ids':True,'scope_union_equals_frozen_80':True,'later_chapters_resolve_to_notes':True,
 'required_fields_present':True,'valid_status_enum':True,'formal_v7_refresh_sha_matches':True,'semantic_primary_approval':False,'pool_mutated':False},
 'artifacts':[{'path':rel(p),'sha256':sha(p),'bytes':p.stat().st_size} for p in [P/'adjudications-history-v01-v04.json',P/'adjudications-history-v01-v04.md',P/'coverage-80.json',P/'existing-25-review.json',P/'method.json',P/'input-manifest.json',P/'review-state.json']]}
save(P/'validation.json',result)
print(json.dumps(result,ensure_ascii=False,indent=2))
