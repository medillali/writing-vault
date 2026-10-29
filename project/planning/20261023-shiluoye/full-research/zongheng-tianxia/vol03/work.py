import json, pathlib, sys
sys.stdout.reconfigure(encoding='utf-8')
HERE = pathlib.Path(__file__).resolve().parent
SOURCE = json.loads((HERE.parent/'source.json').read_text(encoding='utf-8'))
if sys.argv[1] == 'meta':
    print(json.dumps({k:v for k,v in SOURCE.items() if k not in ('chapters','volumes')},ensure_ascii=False))
    print(json.dumps([v for v in SOURCE['volumes'] if v.get('volume')==3],ensure_ascii=False))
    print(json.dumps(SOURCE['chapters'][100:105],ensure_ascii=False))
elif sys.argv[1] == 'commit':
    batch=json.loads((HERE/(sys.argv[2] if len(sys.argv)>2 else 'batch.json')).read_text(encoding='utf-8'))
    old=[]
    if (HERE/'chapter-notes.jsonl').exists():
        old=[json.loads(x) for x in (HERE/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if x]
    existing={x['chapter_id'] for x in old}
    for item in batch:
        chapter=SOURCE['chapters'][item.pop('index')-1]
        assert chapter['chapter_id'] not in existing
        old.append({**chapter,'full_text_read':True,**item})
    (HERE/'chapter-notes.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in old),encoding='utf-8')
    ids=[x['chapter_id'] for x in old]
    state={'source_id':SOURCE['source_id'],'revision':SOURCE['revision'],'volume':3,'status':'reading','read_chapter_ids':ids,'completed_count':len(ids),'next_chapter_id':f'ch-{int(ids[-1][3:])+1:04d}','pending_truncations':[],'current_volume_state':batch[-1].get('state_changes',[]),'boundary':'只据卷三已读原文；全部为待审阅草稿；全书未完'}
    (HERE/'reader-state.json').write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('已持久化',len(ids),'章；下一索引',int(ids[-1][3:])+1)
