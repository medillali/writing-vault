"""核对正式分卷、来源与检查点覆盖；不把结构核验当文学判断。"""
import pathlib,json,sys,hashlib,collections,datetime
sys.stdout.reconfigure(encoding='utf-8')
work=pathlib.Path(__file__).resolve().parent;root=work.parents[2]
slug=sys.argv[1];meta=json.loads((work/slug/'source.json').read_text(encoding='utf-8'))
vault=root/'writing-vault';folder=vault/'library/reports'/slug
def read(p):return json.loads(p.read_text(encoding='utf-8'))
index={c['chapter_id']:c for c in meta['chapters']};all_ids=set(index)
covered=set();all_cards=[];volumes=[];hashes={}
dimensions={'worldbuilding','characters','plot','style','narrative','dialogue','pacing','themes','continuity'}
for spec in meta['volumes']:
    n=spec['volume'];prefix=f'vol{n:02d}'
    expected={s['chapter_id'] for u in spec['units'] for s in u['segments']}
    analysis=read(folder/f'{prefix}-analysis.json');log=read(folder/f'{prefix}-read-log.json');graph=read(folder/f'{prefix}-graph.json')
    assert analysis['source_id']==log['source_id']==meta['source_id']
    assert analysis['revision']==log['revision']==meta['revision']
    assert set(analysis['read_chapter_ids'])==expected
    assert dimensions.issubset(analysis['dimensions'])
    rows=log['chapters'];assert len(rows)==len(expected) and {r['chapter_id'] for r in rows}==expected
    for row in rows:
        assert row['full_text_read'] is True
        original=index[row['chapter_id']]
        assert (row['start_line'],row['end_line'])==(original['start_line'],original['end_line'])
    assert {cid for cov in graph['coverage'] for cid in cov['chapter_ids']}==expected
    assert not covered&expected;covered.update(expected)
    note=folder/f'{prefix}-chapter-notes.jsonl'
    if note.exists():
        notes=[json.loads(line) for line in note.read_text(encoding='utf-8').splitlines() if line.strip()]
        assert len(notes)==len(expected) and {r['chapter_id'] for r in notes}==expected
        assert all(r['full_text_read'] for r in notes)
        readers=dict(collections.Counter(r.get('reader','not-recorded') for r in notes))
    else:
        note=folder/f'{prefix}-reading-notes.md';assert note.exists() and note.stat().st_size>500
        readers={'format':'既有逐章Markdown笔记，未追认统一JSON署名'}
    cards=read(folder/f'{prefix}-cards.json');cards=cards.get('cards',[]) if isinstance(cards,dict) else cards
    assert cards and len({r['asset_id'] for r in cards})==len(cards)
    all_cards.extend(cards)
    volumes.append({'volume':n,'body_units':spec['body_units'],'indexed_segments':len(expected),'dimensions':9,'cards':dict(collections.Counter(c['asset_type'] for c in cards)),'notes':note.name,'readers':readers})
    for name in [f'{prefix}-analysis.json',f'{prefix}-read-log.json',f'{prefix}-graph.json',f'{prefix}-cards.json',note.name]:
        hashes[name]=hashlib.sha256((folder/name).read_bytes()).hexdigest()
supplement=read(folder/'supplementary-read-log.json')
assert supplement['source_id']==meta['source_id'] and supplement['revision']==meta['revision']
for row in supplement['chapters']:
    assert row['full_text_read'] and row['chapter_id'] in all_ids
    original=index[row['chapter_id']]
    assert (row['start_line'],row['end_line'])==(original['start_line'],original['end_line'])
    covered.add(row['chapter_id'])
run=read(vault/'exchanges/runs'/('run-deep-zongheng-tianxia-20261023.json' if slug=='zongheng-tianxia' else f'run-deep-{slug}-20261025.json'))
assert covered==all_ids==set(run['completed_chapters']) and not run['pending_chapters']
assert run['completed_volumes']==[s['volume'] for s in meta['volumes']]
assert len({c['asset_id'] for c in all_cards})==len(all_cards)
source_cards=[]
for kind in ['characters','scenes','patterns']:
    for path in (vault/'library'/kind).glob('*.json'):
        card=read(path)
        if any(e.get('source_id')==meta['source_id'] for e in card.get('evidence',[])):source_cards.append(card)
formal_ids={c['asset_id'] for c in all_cards};assert formal_ids.issubset({c['asset_id'] for c in source_cards})
retained=[{'asset_id':c['asset_id'],'asset_type':c['asset_type'],'origin_key':c.get('origin_key'),'title':c['title']} for c in source_cards if c['asset_id'] not in formal_ids]
result={'status':'passed','checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_id':meta['source_id'],'source_revision':meta['revision'],'body_units':sum(s['body_units'] for s in meta['volumes']),'indexed_segments':len(covered),'volumes':volumes,'cards':dict(collections.Counter(c['asset_type'] for c in all_cards)),'source_total_cards':dict(collections.Counter(c['asset_type'] for c in source_cards)),'retained_cards_outside_volume_packages':retained,'formal_input_sha256':hashes,'limits':['全文实际阅读由逐章笔记及读者记录证明，结构检查只核对它们的一致性','分卷包卡数与本书全部卡数分列；旧开篇卡独立保留，不重复计为本次新卡','本回执只确认正式分卷资料与覆盖，不等全书综合终点审计或用户审阅完成']}
out=folder/'audit/full-reading-validation.json';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in ['volumes','formal_input_sha256','limits']},ensure_ascii=False))
