"""主代理独立保存卷七末段已实读观察，避免与分卷读者并发写同文件。"""
import json,pathlib,sys
BASE=pathlib.Path(__file__).resolve().parent
source=json.loads((BASE/'zongheng-tianxia/source.json').read_text(encoding='utf-8'))
chapters={c['chapter_id']:c for c in source['chapters']}
expected=[f'ch-{i:04d}' for i in range(951,1061)]
dest=BASE/'zongheng-tianxia/vol07-primary-tail';dest.mkdir(exist_ok=True)
path=dest/'chapter-notes.jsonl'
records=[json.loads(s) for s in path.read_text(encoding='utf-8').splitlines() if s.strip()] if path.exists() else []
done={r['chapter_id'] for r in records}
for note in json.loads(pathlib.Path(sys.argv[1]).read_text(encoding='utf-8')):
    cid=note['chapter_id'];assert cid in expected and cid not in done and note.pop('model_full_text_read') is True
    c=chapters[cid]
    records.append({**note,'reader':'primary','title':c['title'],'start_line':c['start_line'],'end_line':c['end_line'],'full_text_read':True})
    done.add(cid)
path.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in records),encoding='utf-8')
state={'source_id':source['source_id'],'revision':source['revision'],'volume':7,'reader':'primary','assigned_chapter_ids':expected,'completed_chapter_ids':[x for x in expected if x in done],'next_chapter_id':next((x for x in expected if x not in done),None),'unresolved_truncations':[],'complete_assigned_segment':len(done)==len(expected),'note':'仅主代理末段实读；合并卷七时须标明各读者范围，不能宣称同一人亲读全卷。'}
(dest/'reader-state.json').write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'read':len(done),'total':len(expected),'next':state['next_chapter_id']},ensure_ascii=False))
