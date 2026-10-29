"""暂存卷六的结构、归属、相对链接与哈希回执；不写正式库，不伪填主审。"""
from pathlib import Path
import json,hashlib,datetime,sys,re,collections
sys.stdout.reconfigure(encoding='utf-8')
D=Path(__file__).resolve().parent;WORK=D.parents[1]
sys.path.insert(0,str(WORK))
from check_volume import load_and_check
def read(n):return json.loads((D/n).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(n,x):(D/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
A=read('analysis.json');A['artifact_status']='draft_artifacts_ready';dump('analysis.json',A)
state=read('reader-state.json')
state.update(status='draft_artifacts_ready',research_status='pending_primary_final_acceptance',updated_at=stamp)
dump('reader-state.json',state)
result=load_and_check('tianxia-wushuang',6)[-1]
notes=[json.loads(s) for s in (D/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if s.strip()]
assert [x['chapter_id'] for x in notes]==[f'ch-{n:04}' for n in range(1059,1294)]
assert collections.Counter(x['reader'] for x in notes)=={'zongheng_vol05_full':175,'primary':60}
attr=read('reading-attribution.json')
for rel,expected in attr['original_tail_files'].items():assert sha(D.parent/rel)==expected
assert (D/'primary-tail-notes.jsonl').read_bytes()==(D.parent/'vol06-tail-primary/chapter-notes.jsonl').read_bytes()
assert (D/'primary-tail-reader-state.json').read_bytes()==(D.parent/'vol06-tail-primary/reader-state.json').read_bytes()
for reader,file,first,last in [('zongheng_vol05_full','prefix-chapter-notes.jsonl',1059,1233),('primary','primary-tail-notes.jsonl',1234,1293)]:
 rows=[json.loads(s) for s in (D/file).read_text(encoding='utf-8').splitlines() if s.strip()]
 assert [r['chapter_id'] for r in rows]==[f'ch-{n:04}' for n in range(first,last+1)]
 assert all(r['reader']==reader and r['full_text_read'] for r in rows)
links=[]
for name in ['report.md','handoff.md']:
 for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)',(D/name).read_text(encoding='utf-8')):
  assert not re.match(r'^[A-Za-z]:|^/|https?://',target),('非本卷相对链接',name,target)
  resolved=(D/target).resolve();assert resolved.is_relative_to(D)
  assert target=='validation.json' or resolved.is_file(),(name,target)
  links.append(dict(source=name,target=target))
C=read('cards.json');G=read('graph.json')
assert all(c['review_status']=='draft' and c['user_notes']=='' and c['favorite'] is False for c in C)
assert all(x['complete'] is False for x in G['coverage'])
by_origin={c['origin_key']:c for c in C}
for c in C:
 for v in c['content'].get('character_origin_keys',[]):assert by_origin[v]['asset_type']=='character'
 for v in c['content'].get('derived_from_origin_keys',[]):assert by_origin[v]['asset_type']=='scene'
for n in G['nodes']:
 if n.get('asset_origin_key'):assert by_origin[n['asset_origin_key']]['asset_type']=='scene'
assert next(c for c in C if c['origin_key'].endswith('/scene/wild-city'))['content']['consequence'].startswith('系统飞炎领地归泪所在野性王座')
assert next(n for n in G['nodes'] if n['id']=='three-souls')['knowledge'][0]['state']=='misbelieves'
files=['analysis.json','cards.json','graph.json','read-log.json','chapter-notes.jsonl','reader-state.json','report.md','handoff.md',
 'reading-attribution.json','primary-corrections.json','merge-receipt.json']
validation=dict(result,readers={'zongheng_vol05_full':dict(raw_segments=175,body_units=174,headers=1),
 'primary':dict(raw_segments=60,body_units=60,headers=0)},
 integration_attribution='zongheng_vol05_full完整读primary60条notes后派生整合，不冒称尾正文独读',
 truncation_pending=[],notes_contiguous=True,original_primary_tail_unchanged=True,user_drafts_preserved=True,
 relative_links=links,source_index_sha256=sha(D.parent/'source.json'),output_sha256={n:sha(D/n) for n in files},
 validated_at=stamp,freeze_state='generated_draft_ready_for_primary_final_acceptance',literary_review='primary_owns_review_receipt_not_filled_here',
 formal_import=False,limitations='核验只证明实际阅读记录覆盖/读者归属、证据范围、图结构与卡片链接；不替文学解释和用户审美认可。',
 corrections_applied=['primary六项九维delta','三生弓交易错归删除','卡兰断臂明宇/断腿米分开','飞炎归野性王座非烛','保护伞整编/命名归因分开','艾蕾拉误信真悔过','降级续穿非盾规则冲突'])
dump('validation.json',validation)
assert all((D/x['target']).is_file() for x in links)
print(json.dumps(dict(preflight='passed',raw_segments=235,body_units=234,evidence_refs=result['evidence_references_checked'],
 cards=result['cards'],nodes=result['nodes'],edges=result['edges'],threads=result['threads'],frozen_outputs=len(files)),ensure_ascii=False))
