import json,hashlib,collections,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');P=Path(__file__).parent;A=P.parent;B=P.parents[2]
load=lambda p:json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
pool=load(A/'local-question-pool.json');scope=[c for c in pool['candidates'] if c['volume']==1 and c.get('original_field')=='notes-unresolved']
rows=load(P/'adjudications-local-note-v01.json');blocks=[];ids=[]
for n in range(1,5):
 p=P/f'adjudications-local-note-v01-part{n:02d}.json';r=load(p);ids.extend(x['candidate_id'] for x in r)
 blocks.append({'path':p.name,'count':len(r),'sha256':sha(p)})
assert len(ids)==350 and len(set(ids))==350 and set(ids)=={x['candidate_id'] for x in scope}
assert {x['candidate_id']:x for n in range(1,5) for x in load(P/f'adjudications-local-note-v01-part{n:02d}.json')}=={x['candidate_id']:x for x in rows}
for r in rows:
 c=next(c for c in scope if c['candidate_id']==r['candidate_id'])
 assert r['title']==c['title'] and r['original_record']==c['original_record'] and r['original_evidence']==c['original_evidence']
 assert r['later_chapters'] and len(r['later_evidence'])==len(r['later_chapters'])
report={'status':'v01-scope-complete-pending-remaining-primary-batch-review','original_notes':90,'original_unresolved_strings':209,'atomic_candidates':350,
 'material_read':'90相关原notes完整facts/inferences/state_changes/unresolved均已输出判读；不是本代理重读卷一正文。',
 'reading_attribution':'卷一正文primary亲读；本代理本轮仅派生四栏笔记与最终报告复核，无新增卷一全文覆盖。',
 'status_counts':dict(collections.Counter(r['status'] for r in rows)),'blocks':blocks,
 'checks':{'exact_frozen_id_set':True,'no_duplicate_ids':True,'original_records_unchanged':True,'blocks_equal_aggregate':True,'all90_material_notes_logged':len([x for x in load(P/'material-read-log.json') if x['volume']==1])==90},
 'local_identity_current':load(A/'candidate-id-freeze.json')['local']['candidate_identity_sha256'],
 'source_notes_sha256':sha(B/'vol01/chapter-notes.jsonl'),'next_scope':'v03新增645，之后旧v05稳定556，均未宣完成。'}
save(P/'v01-coverage-validation.json',report)
md=['# 无双卷一新增逐章未明项终点复核（待主审全块）','',
 '范围：90条相关笔记、209原串、350原子，四个冻结块覆盖完整且无重叠。原文阅读归primary，本代理仅完整复核四栏笔记与最终研究材料，不冒新增正文实读。','',
 '状态：'+json.dumps(report['status_counts'],ensure_ascii=False)+'。unknown含源差、对象身份、证词及精确数值边界；unrecovered只表示特定义务/道具去向未见专属回执，不等作者遗忘。','',
 '卷三645尚待继续，整个995任务未完成。','', '|ID|原子|终点|理由与raw后证|','|---|---|---|---|']
for r in rows:md.append('|'+ '|'.join([r['candidate_id'],r['title'].replace('|','/'),r['status'],r['rationale'].replace('|','/')+'（raw '+','.join(map(str,r['later_chapters']))+'）'])+'|')
(P/'adjudications-local-note-v01.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
