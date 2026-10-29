"""只读校验与当前交付哈希；不写Vault，不伪造primary审阅。"""
import json,sys,hashlib,collections,re,runpy
from pathlib import Path
from datetime import datetime,timezone
P=Path(__file__).parent;W=P.parent.parent
sys.path.insert(0,str(W))
from check_volume import load_and_check
def save(name,x):(P/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
_,spec,_,A,C,G,_,result=load_and_check('zhanlong',1)
notes=[json.loads(s) for s in (P/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if s.strip()]
prefix=(P/'prefix-chapter-notes.jsonl').read_bytes();tail=(P.parent/'primary-vol01-tail/chapter-notes.jsonl').read_bytes()
assert (P/'chapter-notes.jsonl').read_bytes()==prefix+(b'' if prefix.endswith(b'\n') else b'\n')+tail
assert dict(collections.Counter(n['reader'] for n in notes))=={'/root/zongheng_vol03_full':150,'primary':100}
assert len(A['dimensions'])==9 and all(len(r)==4 for r in A['dimensions'].values())
assert all(r['mechanism'] and r['limits_and_counterevidence'] and r['textual_fact'] for rows in A['dimensions'].values() for r in rows)
assert len(A['chapter_unresolved_index'])==sum(bool(n['unresolved']) for n in notes)
assert sum(len(x['unresolved']) for x in A['chapter_unresolved_index'])==sum(len(n['unresolved']) for n in notes)
link_errors=[]
for name in ('report.md','handoff.md','PREFIX-HANDOFF.md'):
 for target in re.findall(r'\]\(([^)]+)\)',(P/name).read_text(encoding='utf-8')):
  if '://' not in target and not target.startswith('#') and not (P/target).exists() and target!='validation.json':link_errors.append((name,target))
assert not link_errors,link_errors
now=datetime.now(timezone.utc).isoformat()
files=['analysis.json','cards.json','graph.json','read-log.json','chapter-notes.jsonl','reader-state.json','report.md','handoff.md','reading-attribution.json','merge-receipt.json']
hashes={f:sha(P/f) for f in files}
validation={'source_id':A['source_id'],'revision':A['revision'],'volume':1,'status':'passed-local-preflight-draft-awaiting-primary-literary-review','verified_at':now,
 'preflight':result,'observations':36,'dimensions':9,'reading_attribution':dict(collections.Counter(n['reader'] for n in notes)),
 'primary_rows_byte_identical':True,'coverage_complete_volume':True,'complete_book':False,'unresolved_truncations':[],
 'notes_unresolved_preservation':{'chapters':len(A['chapter_unresolved_index']),'original_strings':sum(len(n['unresolved']) for n in notes),'all_preserved':True},
 'source_anomalies':len(A['source_anomalies']),'volume_end_questions':len(A['unresolved_volume_end']),
 'knowledge_records':sum(len(n.get('knowledge',[])) for n in G['nodes']),'markdown_links':'passed',
 'semantic_boundary':'本代理自审，不伪造primary审阅或用户审美批准；证据章界通过不等每条解释都正确。','input_sha256':hashes}
save('validation.json',validation)
freeze={'status':'frozen-for-primary-review','source_id':A['source_id'],'revision':A['revision'],'volume':1,'created_at':now,'input_sha256':hashes,'validation_sha256':sha(P/'validation.json'),'core_six_sha256':{f:hashes[f] for f in files[:6]},'not_library_imported_by_this_agent':True,'review_status':'draft'}
save('delivery-freeze.json',freeze)
save('review-changes.json',{'status':'self-review-before-primary','changes':[{'field':'scene/bear','before':'draft曾称魂绑且引用16—20','after':'纠为12死亡后ROLL仍结、14实穿；证据11—14；保主故意缓疗的灰色行为。'},{'field':'selection','after':'补徐月/问剑独立人物，补假救援/比克尾杀两场；43人物47场景12机制。'},{'field':'graph','after':'补问剑相关场景人物引用，去一条仅泛比救援的echo，现54节点33边16线程。'},{'field':'reading','after':'首批尾笔记编码乱码后已utf8重读152—161全部，才计完整派生阅读；primary原行不改。'}],
 'fixed_inputs':hashes,'next_work':'通知primary实际统计后立即继续卷四raw754—968，不等批准；若primary定向反馈只局部改并留delta。'})
save('research-checkpoint.json',{'status':'vol01-delivered-local-preflight-passed-awaiting-primary-review','coverage':{'raw_fragments':250,'body_units':248,'agent3_raw':150,'primary_raw':100},'counts':result,'frozen_files':'delivery-freeze.json','next_work':'卷四raw0754—0968逐章全文/2—4章笔记；卷一不再重跑builder除定向审阅修订。'})
print(json.dumps({'preflight':result,'input_sha256':hashes,'validation_sha256':freeze['validation_sha256']},ensure_ascii=False,indent=2))
