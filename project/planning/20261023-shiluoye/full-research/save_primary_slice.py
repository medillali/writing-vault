"""逐批保存独立分段的真实主代理阅读，禁止当作整卷完成。"""
import json,sys
from pathlib import Path
B=Path(__file__).parent
book,vs,leaf,ss,es,batchpath=sys.argv[1:];vol=int(vs);start,end=int(ss),int(es)
assert Path(leaf).name==leaf and '/' not in leaf and '\\' not in leaf
src=json.loads((B/book/'source.json').read_text(encoding='utf-8'))
spec=next(v for v in src['volumes'] if v['volume']==vol)
allowed={c['chapter_id'] for u in spec['units'] for c in u['segments']}
chapters={c['chapter_id']:c for c in src['chapters']}
expected=[f'ch-{i:04}' for i in range(start,end+1)];assert set(expected)<=allowed
d=B/book/leaf;d.mkdir(exist_ok=True);p=d/'chapter-notes.jsonl'
rows=[json.loads(l) for l in p.read_text(encoding='utf-8').splitlines() if l.strip()] if p.exists() else []
done={r['chapter_id'] for r in rows}
for obs in json.loads(Path(batchpath).read_text(encoding='utf-8')):
 cid=obs['chapter_id'];assert cid in expected and cid not in done and obs.pop('model_full_text_read') is True
 c=chapters[cid];rows.append({**obs,'reader':'primary','title':c['title'],'start_line':c['start_line'],'end_line':c['end_line'],'full_text_read':True});done.add(cid)
p.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows),encoding='utf-8')
state=dict(source_id=src['source_id'],revision=src['revision'],volume=vol,reader='primary',scope='assigned_slice_only',assigned_chapter_ids=expected,completed_chapter_ids=[cid for cid in expected if cid in done],pending_chapter_ids=[cid for cid in expected if cid not in done],next_chapter_id=next((cid for cid in expected if cid not in done),None),unresolved_truncations=[],complete_assigned_slice=len(done)==len(expected),complete_volume=False,note='仅独立分段全文阅读；未宣称本人读整卷/研究入库。')
(d/'reader-state.json').write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8');print(json.dumps(dict(directory=leaf,read=len(done),total=len(expected),next=state['next_chapter_id']),ensure_ascii=False))
