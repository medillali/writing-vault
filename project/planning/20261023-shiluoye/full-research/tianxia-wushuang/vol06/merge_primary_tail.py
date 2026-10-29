"""合并实际阅读记录，保留原分段副本和读者，绝不改写primary尾段原件。"""
from pathlib import Path
import json,hashlib,datetime
D=Path(__file__).resolve().parent;T=D.parent/'vol06-tail-primary'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def rows(p):return [json.loads(x) for x in p.read_text(encoding='utf-8').splitlines() if x.strip()]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
S=read(D.parent/'source.json');spec=next(x for x in S['volumes'] if x['volume']==6)
ids=[c['chapter_id'] for u in spec['units'] for c in u['segments']]
ts=read(T/'reader-state.json');tr=rows(T/'chapter-notes.jsonl')
assert ts['complete_assigned_slice'] and not ts['complete_volume'] and not ts['unresolved_truncations']
assert [x['chapter_id'] for x in tr]==[f'ch-{n:04}' for n in range(1234,1294)]
assert all(x['reader']=='primary' and x['full_text_read'] is True for x in tr)
for name in ['chapter-notes.jsonl','reader-state.json','read-log.json']:
    target=D/('prefix-'+name)
    if not target.exists():target.write_bytes((D/name).read_bytes())
pr=rows(D/'prefix-chapter-notes.jsonl');ps=read(D/'prefix-reader-state.json')
assert [x['chapter_id'] for x in pr]==[f'ch-{n:04}' for n in range(1059,1234)]
assert all(x['reader']=='zongheng_vol05_full' and x['full_text_read'] for x in pr)
assert not ps['complete_volume'] and not ps['truncated_pending']
both=pr+tr;assert [x['chapter_id'] for x in both]==ids
meta={x['chapter_id']:x for x in S['chapters']}
for x in both:
    c=meta[x['chapter_id']];assert (x['start_line'],x['end_line'])==(c['start_line'],c['end_line'])
for src,dst in [('chapter-notes.jsonl','primary-tail-notes.jsonl'),('reader-state.json','primary-tail-reader-state.json')]:
    (D/dst).write_bytes((T/src).read_bytes())
(D/'chapter-notes.jsonl').write_text('\n'.join(json.dumps(x,ensure_ascii=False) for x in both)+'\n',encoding='utf-8')
stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
attr=dict(source_id=S['source_id'],revision=S['revision'],volume=6,kind='actual_reading_split',
 original_tail_files={str((T/n).relative_to(D.parent)).replace('\\','/'):sha(T/n) for n in ['chapter-notes.jsonl','reader-state.json']},
 segments=[dict(reader='zongheng_vol05_full',first='ch-1059',last='ch-1233',raw_segments=175,body_units=174,headers=1,
  actual_full_text=True,notes_copy='prefix-chapter-notes.jsonl'),
 dict(reader='primary',first='ch-1234',last='ch-1293',raw_segments=60,body_units=60,headers=0,
  actual_full_text=True,notes_copy='primary-tail-notes.jsonl')],
 integration=dict(reader='zongheng_vol05_full',method='完整逐条读取primary尾60条实际阅读笔记，连同本人前175片全文记录派生全卷研究；未声称本人重读尾60片正文。',tail_notes_rows_reviewed=60,reviewed_at=stamp),
 complete_volume=True,complete_book=False,formal_import=False)
dump(D/'reading-attribution.json',attr)
state=dict(ps);state.update(reader='multiple_readers',readers=['zongheng_vol05_full','primary'],
 read_chapter_ids=ids,completed_chapter_ids=ids,raw_segments_completed=235,body_units_completed=234,volume_headers_completed=1,
 next_chapter_id=None,complete_volume=True,complete_book=False,status='full_reading_complete_artifacts_in_progress',
 pending_chapter_ids=[],truncated_pending=[],reading_attribution_file='reading-attribution.json',updated_at=stamp,
 current_stage='两读者实际阅读全文覆盖235片234正文，归属见reading-attribution。卷末陆221、心然双小腿断仍活，斯特血脉回血6000万后未死，SS委托未交；寻剑SSS已交后剑遭拾荒者夺，任务不撤。研究产物待完成与主审。')
dump(D/'reader-state.json',state)
log=dict(source_id=S['source_id'],revision=S['revision'],volume=6,reader='multiple_readers',
 chapters=[{k:x[k] for k in ['chapter_id','title','start_line','end_line','reader','full_text_read']} for x in both],
 complete_volume=True,complete_book=False,method='前175片由zongheng_vol05_full、尾60片由primary各自实际逐片全文阅读并2—4片持久化；整合者完整读取尾段60条笔记，保留原读者不冒称本人全卷独读。',
 reading_attribution_file='reading-attribution.json',anomalies=[])
dump(D/'read-log.json',log)
dump(D/'merge-receipt.json',dict(status='reading_records_merged_not_literary_review',at=stamp,
 raw_segments=235,body_units=234,headers=1,notes=[dict(reader='zongheng_vol05_full',raw=175),dict(reader='primary',raw=60)],
 original_primary_unchanged={n:sha(T/n) for n in ['chapter-notes.jsonl','reader-state.json']},
 outputs={n:sha(D/n) for n in ['chapter-notes.jsonl','read-log.json','reader-state.json','reading-attribution.json']}))
print(json.dumps(dict(raw=235,body=234,readers={'zongheng_vol05_full':175,'primary':60},tail_originals_unchanged=True),ensure_ascii=False))
