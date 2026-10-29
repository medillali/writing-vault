import json,hashlib,collections,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
P=Path(__file__).parent;A=P.parent;B=P.parents[2]
load=lambda p:json.loads(p.read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
pool=load(A/'local-question-pool.json');freeze=load(A/'candidate-id-freeze.json')
source_sha={1:'07dcdbeb47552dbc3ddef7089a8583f60774e92cf78d7de44022dc4907f17320',3:'6b7018d485c077654bf042cfd10b393ef7284a3a413f79d8365a5ca080fe538f'}
notes={}
for v in range(1,9):
 for s in (B/f'vol{v:02d}'/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines():
  if s.strip():
   n=json.loads(s);notes[int(n['chapter_id'][3:])]=n
readlog=load(P/'material-read-log.json');validation=[];all_ids=[]
for v,total,nparts,groups in [(1,350,4,90),(3,645,9,360)]:
 np=B/f'vol{v:02d}'/'chapter-notes.jsonl';assert sha(np)==source_sha[v],('original notes changed',v)
 cand={r['candidate_id']:r for r in pool['candidates'] if r['volume']==v and r.get('original_field')=='notes-unresolved'}
 rows=load(P/f'adjudications-local-note-v{v:02d}.json');assert len(rows)==len(cand)==total
 ids=[r['candidate_id'] for r in rows];assert len(set(ids))==total and set(ids)==set(cand)
 parts=[];joined=[]
 for i in range(1,nparts+1):
  p=P/f'adjudications-local-note-v{v:02d}-part{i:02d}.json';rs=load(p);joined+=rs
  parts.append({'path':p.name,'atomic_candidates':len(rs),'sha256':sha(p)})
 assert joined==rows,('frozen blocks differ from aggregate',v)
 for r in rows:
  c=cand[r['candidate_id']]
  for k in ['original_record','original_evidence','original_path','original_field','original_index','source_note_index','source_unresolved_index','source_subatomic_index','title','original_notes_sha256']:
   assert r[k]==c[k],(r['candidate_id'],k)
  assert r['status'] in ['answered','partial','unrecovered','unknown'] and r['rationale'].strip()
  assert r['later_chapters']==sorted(set(r['later_chapters'])) and r['later_chapters']
  assert len(r['later_chapters'])==len(r['later_evidence'])
  for raw,e in zip(r['later_chapters'],r['later_evidence']):
   n=notes[raw]
   assert e['chapter_id']==n['chapter_id'] and e['start_line']==n['start_line'] and e['end_line']==n['end_line']
   assert e['claim_kind']=='synthesis' and e['source_reader']==n.get('reader','unspecified')
 log=[r for r in readlog if r['volume']==v]
 assert len(log)==groups and {r['group'] for r in log}==set(range(1,groups+1))
 assert sum(r['atomic_count'] for r in log)==total and all(not r['new_full_source_reading'] for r in log)
 report={'volume':v,'total':total,'complete_four_field_notes':groups,'status_counts':dict(collections.Counter(r['status'] for r in rows)),
  'original_notes_sha256':sha(np),'blocks':parts,'aggregate_path':f'adjudications-local-note-v{v:02d}.json',
  'aggregate_sha256':sha(P/f'adjudications-local-note-v{v:02d}.json'),
  'checks':{'exact_candidate_set':True,'no_duplicate':True,'original_record_and_evidence_unchanged':True,
    'frozen_blocks_equal_aggregate':True,'all_later_chapter_bounds_and_readers_match_notes':True,'all_scope_four_field_notes_logged':True}}
 validation.append(report);all_ids+=ids
assert len(all_ids)==len(set(all_ids))==995
rows=load(P/'adjudications-local-note-v03.json')
md=['# 无双卷三新增逐章未明项终点复核（全范围待主审合并）','',
 '范围：360条相关四栏笔记、371条原未明串、645个原子，分九个冻结块。本人原先亲读卷三全部正文；本轮以完整四栏笔记及最终分卷材料做派生终审，必要5章重复全文复读另记，不增加覆盖。','',
 '状态分布：'+json.dumps(validation[1]['status_counts'],ensure_ascii=False)+'。','',
 'answered包括明确否定、拒绝、失败、后来规则说明或作者纠错；partial逐子项结算；unrecovered表示专属承诺/处置未见匹配回执，不判作者遗忘或肯定没发生；unknown保源差、精确统计、未明身份/动机。','',
 '|ID|原子|终点|理由及raw后证|','|---|---|---|---|']
for r in rows:md.append('|'+ '|'.join([r['candidate_id'],r['title'].replace('|','/'),r['status'],r['rationale'].replace('|','/')+'（raw '+','.join(map(str,r['later_chapters']))+'）'])+'|')
(P/'adjudications-local-note-v03.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
out={'status':'scope-complete-structural-checks-passed-pending-primary-semantic-review-and-assembler-merge','atomic_candidates':995,
 'scope':[1,3],'original_unresolved_strings':580,'complete_four_field_notes':450,'volumes':validation,
 'local_identity_sha256':freeze['local']['candidate_identity_sha256'],
 'method':{'answered':'原事件有明确完成/失败/拒绝/规则后释/作者纠错或边界判据，不等愿望成功。',
 'partial':'复合原子中部分有专属回收、部分仍未明；逐子项记。',
 'unrecovered':'特定承诺/账目/物件去向未找到匹配回执；不称客观必未履行/作者忘。',
 'unknown':'源差、精确数字、身份、动机或证词不足，不能由相似后期事补早期。'},
 'reader_attribution':'卷1原文primary，本代理派生完整四栏复核；卷3原先本代理实读，本轮四栏复核不虚增覆盖；其他卷后证为实际分工读者notes/最终研究。',
 'targeted_repeated_source_rereads':{'raw_chapters':[316,320,323,333,352],'new_coverage':False,'logs':['targeted-source-rereads.json','targeted-source-reread-105.json']},
 'merge_instruction':'只由agent4合并已primary主审签名冻结块；聚合与快照不是重复增量输入。未改主池/正式库/冻结分卷。',
 'next_assignment':'旧local卷5 offset178—556共379，独立local-v05-tail-review；root已完成前177/5批。',
 'documents':[{'path':'adjudications-local-note-v03.md','sha256':sha(P/'adjudications-local-note-v03.md')}]}
save(P/'notes-995-validation.json',out)
state=load(P/'review-state.json');state['status']=out['status'];state['next_action']=out['next_assignment'];state['scope_complete']=True
for x in state['by_volume'].values():x['next_group']=None
save(P/'review-state.json',state)
lines=['# 新增notes卷1/3审计交付','',
 '995/995原子已逐项裁定，450条相关原notes均完整复核四栏。结构验证通过，语义审阅与合并由primary/agent4继续；不冒称已入池或终审全签。','',
 '保原问题、四栏、原证据和原notes SHA；后证均有raw整数、完整章界及真实source_reader。unknown与unrecovered不等作者遗忘；不因省略单独交接镜头否定已有实际后状态。','',
 '卷1四块=350；卷3九块=645。请只按主审签名冻结块合并，聚合与before/unsubmitted快照不可重复输入。','',
 '新增定向正文复读为316/320/323/333/352共5章（已有覆盖的重复读取），其余本轮是派生材料复核。','',
 '本轮原note自纠：087黑水→飞马并非同日CD冲突；343-02关悦后证为风月本名，不是原note猜的口误；175-01融合定位按primary改370，342为另一斩龙融合。','']
for v in validation:
 lines+=['## 卷'+str(v['volume']), '']
 for x in v['blocks']:lines.append(f"- {x['path']}：{x['atomic_candidates']}条；SHA {x['sha256']}")
 lines+=['',f"聚合SHA：{v['aggregate_sha256']}",'']
lines+=['## 后续边界','',out['next_assignment'],
 '卷五注意root已核：837月光石返门的返会后证为1413 L111970；845七星枪赠何在866 L71607/08/22已拿、1169 L94329实用，省略递交不等未回收；986奥维亚先被斩首/魂消后已救赎复体，无头血指实际现身，不写永久魂散；987母魂真耗尽与苏自主誓言分人。','']
(P/'notes-995-handoff.md').write_text('\n'.join(lines),encoding='utf-8')
print(json.dumps({'status':out['status'],'count':995,'v1':validation[0]['status_counts'],'v3':validation[1]['status_counts'],
 'validation_sha256':sha(P/'notes-995-validation.json'),'handoff_sha256':sha(P/'notes-995-handoff.md'),
 'v03_md_sha256':sha(P/'adjudications-local-note-v03.md')},ensure_ascii=False,indent=2))
