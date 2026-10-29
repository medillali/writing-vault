import json,pathlib,sys
sys.stdout.reconfigure(encoding='utf-8')
base=pathlib.Path(__file__).resolve().parent
source=json.loads((base.parent/'source.json').read_text(encoding='utf-8'))
notes=[json.loads(x) for x in (base/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
notes.sort(key=lambda n:n['chapter_id'])
if sys.argv[1]=='notes':
    a,b=map(int,sys.argv[2:4])
    for n in notes:
        if a<=int(n['chapter_id'].split('-')[1])<=b:print(json.dumps(n,ensure_ascii=False))
elif sys.argv[1]=='sync':
    for n in notes:n.setdefault('reader','primary' if int(n['chapter_id'].split('-')[1])<=575 else '/root/zongheng_vol05_full')
    ids=[n['chapter_id'] for n in notes]
    assert len(set(ids))==len(ids)
    expected=[s['chapter_id'] for u in next(v for v in source['volumes'] if v['volume']==6)['units'] for s in u['segments']]
    assert all(i in expected for i in ids)
    pending=[i for i in expected if i not in ids]
    (base/'chapter-notes.jsonl').write_text(''.join(json.dumps(n,ensure_ascii=False)+'\n' for n in notes),encoding='utf-8')
    state=dict(source_id=source['source_id'],revision=source['revision'],volume=6,reader='collaborative',reader_attribution={'primary':{'chapter_ids':[i for i in ids if int(i.split('-')[1])<=575],'method':'主代理实际全文阅读，本代理复用其逐章观察，不宣称个人重读'},'/root/zongheng_vol05_full':{'chapter_ids':[i for i in ids if int(i.split('-')[1])>=576],'method':'接续后实际逐章全文阅读'}},completed_chapter_ids=ids,read_count=len(ids),next_chapter_id=pending[0] if pending else None,pending_chapter_ids=pending,unresolved_truncations=[],complete_volume=not pending,status='reading' if pending else 'read-complete-artifacts-pending',current_state=notes[-1]['state_changes'])
    (base/'reader-state.json').write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(read=len(ids),primary=sum(n['reader']=='primary' for n in notes),own=sum(n['reader']!='primary' for n in notes),next=state['next_chapter_id']),ensure_ascii=False))
