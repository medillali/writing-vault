"""核验本卷草稿并固定输入输出SHA；不执行正式导入，不伪造主审。"""
from pathlib import Path
import json,sys,hashlib,datetime,collections,re
sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;WORK=H.parents[1]
sys.path.insert(0,str(WORK))
from check_volume import load_and_check
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
source,spec,directory,analysis,cards,graph,mapping,result=load_and_check('zhanlong',6)
notes=[json.loads(x) for x in (H/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines()]
state=read(H/'reader-state.json');log=read(H/'read-log.json')
assert state['next_chapter_id'] is None and state['full_assigned_volume_text_read'] is True
assert state['status']=='artifacts_ready_for_primary_review' and state['complete_book'] is False
assert len(notes)==207 and len({r['unit_id'] for r in notes if r['unit_kind']=='body'})==206
assert all(r['reader']=='zongheng_vol05_full' for r in notes)
index=analysis['chapter_unresolved_index'];separate=read(H/'chapter-unresolved-index.json')['chapters']
expected=[dict(chapter_id=r['chapter_id'],title=r['title'],reader=r['reader'],read_at=r['read_at'],start_line=r['start_line'],end_line=r['end_line'],original_unresolved=r['unresolved']) for r in notes]
assert index==separate==expected
assert 'open_questions' in analysis and 'unresolved_volume_end' not in analysis
assert 'source_anomalies' in analysis and 'unresolved_and_anomalies' not in analysis
seen=[]
for batch in log['batches']:
    assert sha(H/batch['batch'])==batch['batch_sha256']
    data=read(H/batch['batch']);assert batch['chapter_ids']==[r['chapter_id'] for r in data['chapters']]
    assert 2<=len(data['chapters'])<=4
    assert all(r['begin_end_verified'] and r['full_text_read'] for r in data['chapters'])
    assert batch['begin_end_verified'] and not batch['truncated_pending']
    seen+=batch['chapter_ids']
assert seen==analysis['read_chapter_ids'] and len(log['batches'])==52
outputs=['analysis.json','cards.json','graph.json','report.md','handoff.md','chapter-unresolved-index.json','chapter-notes.jsonl','reader-state.json','read-log.json']
inputs=['build_artifacts.py','research_cards.py','research_interfaces.py','save_batch.py','finalize_validation.py']
checks=dict(original_unresolved_strings=sum(len(r['unresolved']) for r in notes),chapter_unresolved_index_rows=len(index),original_reader_and_read_at_preserved=True,batches=52,all_batch_hashes_match=True,complete_book=False,review_status='draft',primary_review_status='pending',scope='只核本卷原文覆盖/证据定位/图卡引用与索引无损，不代替文学主审。')
validation=dict(**result,additional_checks=checks,input_sha256={'source.json':sha(H.parent/'source.json'),**{n:sha(H/n) for n in inputs}},output_sha256={n:sha(H/n) for n in outputs},self_review=dict(method='完整回看本人1180—1339已存四栏/当前1340—1386全文与四栏；只读重核1298全文澄清薛柔游戏归区标识，不重复计覆盖。',correction_records=['prefreeze-reference-corrections.json','prefreeze-reference-corrections-2.json'],precise_correction='薛柔/为爱追寻是中国公告与葡榜漂移主体，雪狐为俄敌；伊薇/奈克拆两人物卡；原逐章记录未改。'),checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
(H/'validation.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
manifest=dict(book='zhanlong',volume=6,status='frozen_draft_for_primary_review',source_id=source['source_id'],revision=source['revision'],reader='zongheng_vol05_full',primary_review_status='pending',files={n:sha(H/n) for n in outputs+['validation.json']},reproduction_inputs={n:sha(H/n) for n in inputs},warning='主审如需定向修改需更新本清单；不可用本回执宣已正式保存或文学审查通过。')
(H/'freeze-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for name in ['report.md','handoff.md']:
    for target in re.findall(r'\]\(([^)]+)\)',(H/name).read_text(encoding='utf-8')):
        assert not target.startswith(('C:','file:','http:','https:')),target
        assert (H/target).is_file(),(name,target)
assert all(sha(H/n)==digest for n,digest in manifest['files'].items())
print(json.dumps(dict(result=result,checks=checks,freeze_sha256=sha(H/'freeze-manifest.json'),key_sha256={n:sha(H/n) for n in ['analysis.json','cards.json','graph.json','report.md','handoff.md','validation.json']}),ensure_ascii=False))
