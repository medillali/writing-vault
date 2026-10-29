"""本卷研究草稿持久化工具；只记录已由阅读者确认读完的批次。"""
import json,sys
from pathlib import Path
root=Path(__file__).parent
source=json.loads((root.parent/'source.json').read_text(encoding='utf-8'))
units=next(v for v in source['volumes'] if v['volume']==4)['units']
segments=[s for u in units for s in u['segments']]
by_id={s['chapter_id']:s for s in segments}
path=root/'chapter-notes.jsonl'
notes=[json.loads(x) for x in path.read_text(encoding='utf-8').splitlines()] if path.exists() else []
batch=json.loads((root/sys.argv[1]).read_text(encoding='utf-8'))
existing={x['chapter_id'] for x in notes}
for item in batch:
    idx=item.pop('index')
    chapter=source['chapters'][idx-1]
    assert chapter['chapter_id'] in by_id
    assert chapter['chapter_id'] not in existing
    item={**{k:chapter[k] for k in ('chapter_id','title','start_line','end_line')},'full_text_read':True,**item}
    notes.append(item)
ids=[n['chapter_id'] for n in notes]
assert ids==[s['chapter_id'] for s in segments[:len(ids)]]
path.write_text(''.join(json.dumps(n,ensure_ascii=False)+'\n' for n in notes),encoding='utf-8')
next_id=segments[len(ids)]['chapter_id'] if len(ids)<len(segments) else None
state={'source_id':source['source_id'],'revision':source['revision'],'volume':4,'read_chapter_ids':ids,'completed_count':len(ids),'total_segments':len(segments),'current_chapter_id':None,'next_chapter_id':next_id,'truncated_pending':[],'status':'reading' if next_id else 'read-complete-analysis-pending','complete_book':False,'current_volume_state':batch[-1].get('state_changes',[]),'boundary_note':'卷三前史未由本阅读者阅读全文，跨卷依赖待主代理核验。'}
(root/'reader-state.json').write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding='utf-8')
log={'source_id':source['source_id'],'revision':source['revision'],'volume':4,'chapters':[{k:n[k] for k in ('chapter_id','start_line','end_line','full_text_read')} for n in notes],'complete_book':False,'complete_volume':next_id is None,'method':'逐次调用read_chapters.py输出1至2章实际全文，核对BEGIN/END后人工阅读；每2至4章持久化基于全文的简洁笔记。','anomalies':[]}
(root/'read-log.json').write_text(json.dumps(log,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'persisted {len(ids)}/{len(segments)}; next={next_id}')
