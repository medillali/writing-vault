"""续接主代理前20章；只追加本阅读者已核END全文读完的笔记。"""
import json,sys
from pathlib import Path
r=Path(__file__).parent
s=json.loads((r.parent/'source.json').read_text(encoding='utf-8'))
v=next(v for v in s['volumes'] if v['volume']==8)
segments=[c for u in v['units'] for c in u['segments']]
expected=[x['chapter_id'] for x in segments]
cs={x['chapter_id']:x for x in s['chapters']}
p=r/'chapter-notes.jsonl';ns=[json.loads(x) for x in p.read_text(encoding='utf-8').splitlines()]
assert [x['chapter_id'] for x in ns]==expected[:len(ns)]
for n in json.loads((r/sys.argv[1]).read_text(encoding='utf-8')):
    i=n.pop('index');cid=f'ch-{i:04}'
    assert cid==expected[len(ns)]
    c=cs[cid]
    ns.append(dict(chapter_id=cid,title=c['title'],start_line=c['start_line'],end_line=c['end_line'],full_text_read=True,reader='zongheng_vol04_full',**n))
p.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in ns),encoding='utf-8')
ids=[x['chapter_id'] for x in ns]
state=dict(source_id=s['source_id'],revision=s['revision'],volume=8,reader='primary+zongheng_vol04_full',reader_ranges=[dict(reader='primary',chapter_ids=expected[:20],basis='主代理逐章全文读取并原样保留其批次与笔记'),dict(reader='zongheng_vol04_full',chapter_ids=ids[20:],basis='逐次read_chapters.py核BEGIN/END后阅读全文，每2—4章持久化')],completed_chapter_ids=ids,read_chapter_ids=ids,completed_count=len(ids),total_segments=len(expected),next_chapter_id=expected[len(ids)] if len(ids)<len(expected) else None,pending_chapter_ids=expected[len(ids):],unresolved_truncations=[],truncated_pending=[],complete_volume=len(ids)==len(expected),complete_book=False,status='reading' if len(ids)<len(expected) else 'read-complete-analysis-pending',current_volume_state=ns[-1]['state_changes'],boundary_note='卷五至七前史未由本续读者逐章全文读，阶段信息以卷八实际文本为准，跨卷待主代理核验。')
(r/'reader-state.json').write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
log=dict(source_id=s['source_id'],revision=s['revision'],volume=8,chapters=[{**{k:n[k] for k in ['chapter_id','start_line','end_line','full_text_read']},'reader':'primary' if j<20 else n['reader']} for j,n in enumerate(ns)],complete_volume=len(ids)==len(expected),complete_book=False,method=state['reader_ranges'],anomalies=[],truncated_pending=[])
(r/'read-log.json').write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'persisted {len(ids)}/{len(expected)}; next={state["next_chapter_id"]}')
