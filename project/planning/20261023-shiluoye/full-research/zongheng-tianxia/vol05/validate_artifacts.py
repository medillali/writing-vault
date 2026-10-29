"""本卷草稿只读自检；仅把检查结果写回本卷validation.json。"""
import collections,json,pathlib,sys
BASE=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(BASE.parent.parent))
from check_volume import load_and_check
sys.stdout.reconfigure(encoding='utf-8')
source,spec,directory,analysis,cards,graph,mapping,result=load_and_check('zongheng-tianxia',5)
read=lambda p:json.loads((BASE/p).read_text(encoding='utf-8'))
notes=[json.loads(s) for s in (BASE/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if s.strip()]
expected=[s for u in spec['units'] for s in u['segments']]
assert len(notes)==108
assert [n['chapter_id'] for n in notes]==[s['chapter_id'] for s in expected]
assert all((n['start_line'],n['end_line'])==(s['start_line'],s['end_line']) for n,s in zip(notes,expected))
assert all(notes[i]['end_line']+1==notes[i+1]['start_line'] for i in range(107))
assert all(n['facts'] and n['inferences'] and n['state_changes'] for n in notes)
assert all((BASE/f).exists() and (BASE/f).stat().st_size for f in ['read-log.json','reader-state.json','chapter-notes.jsonl','analysis.json','cards.json','graph.json','report.md','handoff.md'])
scene_fields=['summary','goal','obstacle','choice','consequence','state_change','why_it_works','applicability','failure_mode']
for card in cards:
    if card['asset_type']=='scene':assert all(card['content'].get(k) for k in scene_fields)
    if card['asset_type']=='pattern':assert card['content']['originality_transform'] and card['content']['derived_from_origin_keys']
original_graph=read('graph.json')
for key,chapter,arc in [('thunder-escort',459,'escort'),('craft-affection',439,'hold-care'),('annie-reversal',528,'reveal-next')]:
    n=next(n for n in original_graph['nodes'] if n['id']=='v05-scene-'+key)
    assert n['core_original_chapter']==chapter and n['narrative_order']==chapter-422 and n['parent_id']=='v05-arc-'+arc
assert all('source_scene_origin_key' not in n for n in original_graph['nodes'])
claim_counts=collections.Counter()
def collect(v):
    if isinstance(v,list):
        for x in v:collect(x)
    elif isinstance(v,dict):
        if {'source_id','revision','chapter_id'}.issubset(v):claim_counts[v['claim_kind']]+=1
        for x in v.values():collect(x)
for v in [analysis,cards,original_graph]:collect(v)
result.update(review_status='draft',notes_contiguous=True,notes_exact_ranges=True,required_artifacts_present=True,scene_core_order_checked=True,evidence_claim_kind_counts=dict(claim_counts),complete_book=False,remaining_truncations=[],literary_review='结构、定位与引用检查通过不等于文学解释获得用户认可')
(BASE/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
