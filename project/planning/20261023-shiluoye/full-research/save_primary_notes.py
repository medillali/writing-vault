"""保存主代理已实际读完的章节观察；注释必须由模型提供。"""
import pathlib,json,sys
WORK=pathlib.Path(__file__).resolve().parent
book=sys.argv[1];volume=int(sys.argv[2]);batch=json.loads(pathlib.Path(sys.argv[3]).read_text(encoding='utf-8'))
source=json.loads((WORK/book/'source.json').read_text(encoding='utf-8'));chapters={c['chapter_id']:c for c in source['chapters']}
spec=next(v for v in source['volumes'] if v['volume']==volume);expected=[c['chapter_id'] for u in spec['units'] for c in u['segments']]
directory=WORK/book/f'vol{volume:02d}';directory.mkdir(parents=True,exist_ok=True);notes=directory/'chapter-notes.jsonl'
records=[json.loads(line) for line in notes.read_text(encoding='utf-8').splitlines() if line.strip()] if notes.exists() else []
done={r['chapter_id'] for r in records}
for observation in batch:
    cid=observation['chapter_id'];assert cid in expected and cid not in done and observation.pop('model_full_text_read') is True
    chapter=chapters[cid]
    records.append({**observation,'reader':'primary','title':chapter['title'],'start_line':chapter['start_line'],'end_line':chapter['end_line'],'full_text_read':True})
    done.add(cid)
notes.write_text(''.join(json.dumps(record,ensure_ascii=False)+'\n' for record in records),encoding='utf-8')
state={'source_id':source['source_id'],'revision':source['revision'],'volume':volume,'reader':'primary','completed_chapter_ids':[cid for cid in expected if cid in done],'next_chapter_id':next((cid for cid in expected if cid not in done),None),'pending_chapter_ids':[cid for cid in expected if cid not in done],'unresolved_truncations':[],'complete_volume':len(done)==len(expected),'note':'这里只是实际阅读笔记，尚未完成九维、卡片、图及正式入库。'}
(directory/'reader-state.json').write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'volume':volume,'read':len(done),'total':len(expected),'next':state['next_chapter_id']},ensure_ascii=False))
