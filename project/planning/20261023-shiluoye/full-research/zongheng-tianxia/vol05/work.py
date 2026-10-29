import json, pathlib, sys
sys.stdout.reconfigure(encoding='utf-8')
base=pathlib.Path(__file__).resolve().parent
source=json.loads((base.parent/'source.json').read_text(encoding='utf-8'))
if sys.argv[1]=='meta':
    print(json.dumps({k:v for k,v in source.items() if k not in ['chapters','volumes']},ensure_ascii=False,indent=2))
    print(json.dumps([v for v in source['volumes'] if v.get('volume')==5],ensure_ascii=False,indent=2))
elif sys.argv[1]=='sync':
    notes=[json.loads(x) for x in (base/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
    notes.sort(key=lambda x:x['chapter_id'])
    assert len({x['chapter_id'] for x in notes})==len(notes)
    (base/'chapter-notes.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in notes),encoding='utf-8')
    ids=[x['chapter_id'] for x in notes]
    units=next(v for v in source['volumes'] if v['volume']==5)['units']
    chapters=[c for u in units for c in u['segments']]
    pending=[c['chapter_id'] for c in chapters if c['chapter_id'] not in ids]
    state={'source_id':source['source_id'],'revision':source['revision'],'volume':5,'read_chapter_ids':ids,'read_count':len(ids),'next_chapter_id':pending[0] if pending else None,'pending_chapter_ids':pending,'truncated_pending':[],'status':'reading' if pending else 'read-complete-artifacts-pending','current_state':notes[-1]['state_changes'],'boundary':'未读卷三四，前史依赖交主代理跨卷核验'}
    (base/'reader-state.json').write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'read':len(ids),'next':state['next_chapter_id']},ensure_ascii=False))
