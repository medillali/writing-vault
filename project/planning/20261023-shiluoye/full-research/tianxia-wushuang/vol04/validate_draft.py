"""本卷只读结构/出处/相对链接验收，写回本卷验证回执；不伪造文学主审。"""
import sys,json,pathlib,hashlib,re,datetime
D=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(D.parent.parent))
from check_volume import load_and_check
result=load_and_check('tianxia-wushuang',4)[-1]
notes=[json.loads(x) for x in (D/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines()]
assert len(notes)==186 and len({x['chapter_id'] for x in notes})==186
assert all(x['reader']=='zongheng_vol05_full' for x in notes)
assert all(b['start_line']==a['end_line']+1 for a,b in zip(notes,notes[1:]))
assert notes[0]['start_line']==52261 and notes[-1]['end_line']==65980
cards=json.loads((D/'cards.json').read_text(encoding='utf-8'))
origins={c['origin_key'] for c in cards}
assert all(not c['user_notes'] and not c['favorite'] and c['review_status']=='draft' for c in cards)
for c in cards:
    if c['asset_type']=='character':
        assert all(c['content'].get(k) for k in ['goals','constraints','relationship_directions','decisions','changes','current_state','knowledge_boundary'])
    elif c['asset_type']=='scene':
        assert all(c['content'].get(k) for k in ['goal','obstacle','choice','consequence','state_change','why_it_works','applicability','failure_mode'])
    else:
        assert all(c['content'].get(k) for k in ['causal_steps','applicability','failure_conditions','originality_transform','derived_from_origin_keys'])
        assert all(x in origins for x in c['content']['derived_from_origin_keys'])
links=[]
for name in ['report.md','handoff.md']:
    content=(D/name).read_text(encoding='utf-8')
    assert 'C:/' not in content and '.planning/' not in content
    for ref in re.findall(r'\]\(([^)]+)\)',content):
        assert '/' not in ref and '\\' not in ref and ref in ['analysis.json','cards.json','graph.json','read-log.json','chapter-notes.jsonl','reader-state.json','handoff.md','validation.json'],ref
        if ref!='validation.json':assert (D/ref).is_file(),ref
        links.append({'from':name,'target':ref})
state=json.loads((D/'reader-state.json').read_text(encoding='utf-8'))
state.update(status='draft_frozen_pending_primary_review',research_status='structural_validation_passed_literary_review_pending',
             updated_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
(D/'reader-state.json').write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
names=['analysis.json','cards.json','graph.json','read-log.json','chapter-notes.jsonl','reader-state.json','report.md','handoff.md']
receipt=dict(**result,reader='zongheng_vol05_full',reader_full_text_segments=186,body_units=185,headers=1,
    truncation_pending=[],notes_contiguous=True,user_drafts_preserved=True,relative_links=links,
    source_index_sha256=hashlib.sha256((D.parent/'source.json').read_bytes()).hexdigest(),
    output_sha256={n:hashlib.sha256((D/n).read_bytes()).hexdigest() for n in names},
    validated_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    literary_review='pending_primary_and_user_review',formal_import=False,
    limitations='本回执只证明实际阅读记录覆盖、证据有效范围、图结构和卡片/链接字段；不代替文学判断。')
(D/'validation.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in receipt.items() if k not in ['relative_links','output_sha256']},ensure_ascii=False))
