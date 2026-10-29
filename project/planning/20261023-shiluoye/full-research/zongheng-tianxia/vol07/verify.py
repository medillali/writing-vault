import json,pathlib,collections,sys,hashlib,copy,uuid
sys.stdout.reconfigure(encoding='utf-8')
P=pathlib.Path(__file__).resolve().parent;ROOT=P.parents[4]
load=lambda name:json.loads((P/name).read_text(encoding='utf-8'))
S=json.loads((P.parent/'source.json').read_text(encoding='utf-8'))
SPEC=next(v for v in S['volumes'] if v['volume']==7)
expected=[c['chapter_id'] for u in SPEC['units'] for c in u['segments']]
source={c['chapter_id']:c for c in S['chapters']}
N=[json.loads(x) for x in (P/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines()]
A=load('analysis.json');C=load('cards.json');G=load('graph.json');L=load('read-log.json');ST=load('reader-state.json')
assert expected==[f'ch-{i:04d}' for i in range(776,1061)]
assert [r['chapter_id'] for r in N]==expected==[r['chapter_id'] for r in L['chapters']]==A['read_chapter_ids']==ST['read_chapter_ids']
assert collections.Counter(r['reader'] for r in N)=={'zongheng_vol03_full':175,'primary':110}
assert all(r['reader']=='zongheng_vol03_full' for r in N[:175]) and all(r['reader']=='primary' for r in N[175:])
for r in N+L['chapters']:
 orig=source[r['chapter_id']]
 assert r['full_text_read'] is True
 assert (r['start_line'],r['end_line'])==(orig['start_line'],orig['end_line'])
assert L['complete_book'] is False and L['complete_volume'] is True
assert ST['next_chapter_id'] is None and not ST['pending_truncations']
assert {x for cov in G['coverage'] for x in cov['chapter_ids']}==set(expected)
assert all(cov['complete'] is False for cov in G['coverage'])
assert len(A['dimensions'])==9 and all(len(v)>=3 for v in A['dimensions'].values())
count=collections.Counter(c['asset_type'] for c in C);assert count=={'character':29,'scene':37,'pattern':10}
origins={c['origin_key']:c for c in C};assert len(origins)==len(C)
claims=collections.Counter();evidence_count=0
def check(value):
 global evidence_count
 if isinstance(value,list):
  for x in value:check(x)
 elif isinstance(value,dict):
  if {'source_id','revision','chapter_id'}<=value.keys():
   assert value['source_id']==S['source_id'] and value['revision']==S['revision']
   assert value['chapter_id'] in expected
   s=source[value['chapter_id']]
   assert s['start_line']<=value['start_line']<=value['end_line']<=s['end_line']
   assert value.get('claim_kind') in {'fact','inference','synthesis','plan'}
   claims[value['claim_kind']]+=1;evidence_count+=1
  for v in value.values():check(v)
for x in [A,C,G]:check(x)
for c in C:
 assert c['review_status']=='draft' and not c['favorite'] and not c['user_notes']
 assert c['origin_key'].startswith(S['source_id']+'/full-20261025/vol07/')
 assert c['content']['summary'] and c['evidence']
 for k in c['content'].get('derived_from_origin_keys',[]):assert k in origins and origins[k]['asset_type']=='scene'
 for k in c['content'].get('characters',[]):assert k in origins and origins[k]['asset_type']=='character'
for node in G['nodes']:
 if node['kind']=='scene':assert node['asset_origin_key'] in origins
 for k in node.get('characters',[]):assert k in origins and origins[k]['asset_type']=='character'
 for k in node.get('knowledge',[]):
  assert k['state'] in {'knows','unknown','misbelieves','suspects'}
  if k['state']=='misbelieves':assert k['belief']
  assert k['observer']=='reader' or k['observer'] in origins
for t in G['threads']:
 if t['status']=='resolved':assert t['resolution_note'] and t['resolution_evidence']
# 使用库的纯结构验证器，不创建Vault、不取正式库锁、不写正式库。
sys.path.insert(0,str(ROOT/'distill-novels'/'scripts'))
from fictionlib.graph import validate_graph
mapping={k:'chr-'+uuid.uuid5(uuid.NAMESPACE_URL,k).hex for k,c in origins.items() if c['asset_type']=='character'}
def remap(x):
 if isinstance(x,dict):return {k:remap(v) for k,v in x.items()}
 if isinstance(x,list):return [remap(v) for v in x]
 return mapping.get(x,x) if isinstance(x,str) else x
validate_graph(remap(copy.deepcopy(G)))
bykey={c['origin_key'].rsplit('/',1)[1]:c for c in C}
assert {e['chapter_id'] for e in bykey['sagelong']['evidence']}=={'ch-0810','ch-0815','ch-0816','ch-0817'}
assert '双牧' not in bykey['s4']['title']
assert '保卫战中' in bykey['shusheng']['content']['summary']
assert '刑天' in bykey['longhun']['content']['summary'] and '推断' in bykey['longhun']['content']['summary']
audan_character=next(c for c in C if c['asset_type']=='character' and c['origin_key'].endswith('/audan'))
assert '雨露峡谷' in audan_character['content']['stage_change'] and '黑堡要塞' not in audan_character['content']['stage_change']
assert '第三道即最后封' in bykey['aryan']['content']['failure_mode']
assert not any(e['id']=='v07-e-toolreturn' for e in G['edges'])
assert any(k['state']=='misbelieves' and k['belief'] for n in G['nodes'] for k in n.get('knowledge',[]))
assert any(k['state']=='suspects' for n in G['nodes'] for k in n.get('knowledge',[]))
assert all(c['review_status']=='draft' for c in C)
ST.update(status='complete',complete_volume=True,deliverables_complete=True,review_status='draft',completed_chapter_ids=ST['read_chapter_ids'])
(P/'reader-state.json').write_text(json.dumps(ST,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
personal=load('personal-reader-state.json');personal.update(reader='zongheng_vol03_full',assigned_range=[776,950],complete_assigned_segment=True,next_chapter_id=None,status='complete_assigned_segment')
(P/'personal-reader-state.json').write_text(json.dumps(personal,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
result=dict(status='passed',validation_kind='local_structure_and_evidence_bounds_no_Vault',source_id=S['source_id'],revision=S['revision'],volume=7,body_units=SPEC['body_units'],indexed_segments=285,readers=dict(collections.Counter(r['reader'] for r in N)),dimensions={k:len(v) for k,v in A['dimensions'].items()},cards=dict(count),nodes=len(G['nodes']),edges=len(G['edges']),threads=len(G['threads']),knowledge_entries=sum(len(n.get('knowledge',[])) for n in G['nodes']),evidence_references_checked=evidence_count,claim_kinds=dict(claims),pure_library_validate_graph=True,review_guards='passed',pending_truncations=[],official_Vault_preflight='not_run_by_subagent; primary_to_run_serially',literary_approval='draft; revisions require primary final review')
(P/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
names=['chapter-notes.jsonl','reader-state.json','personal-reader-state.json','read-log.json','analysis.json','cards.json','graph.json','report.md','handoff.md','review-changes.md','validation.json']
manifest={'freeze':'vol07-review-candidate-final','source_revision':S['revision'],'note':'验证后冻结；向主代理交付后不再运行builder。正式入库/后续修正另由主代理维护。','sha256':{name:hashlib.sha256((P/name).read_bytes()).hexdigest() for name in names}}
(P/'freeze-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False));print('freeze-manifest.json saved')
