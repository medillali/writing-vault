import json,pathlib,collections
H=pathlib.Path(__file__).resolve().parent
def rd(f):return json.loads((H/f).read_text(encoding='utf-8'))
S=rd('../source.json');A=rd('analysis.json');C=rd('cards.json');G=rd('graph.json');L=rd('read-log.json');ST=rd('reader-state.json');N=[json.loads(x) for x in (H/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines()]
expected=S['chapters'][101:245];by={x['chapter_id']:x for x in expected};ids=[x['chapter_id'] for x in expected]
assert len(N)==144 and len(set(ids))==144
assert [x['chapter_id'] for x in N]==ids==A['read_chapter_ids']==ST['read_chapter_ids']==[x['chapter_id'] for x in L['chapters']]==G['coverage'][0]['chapter_ids']
assert all(x['full_text_read'] for x in N+L['chapters'])
assert all(x['start_line']==by[x['chapter_id']]['start_line'] and x['end_line']==by[x['chapter_id']]['end_line'] for x in N+L['chapters'])
assert not ST['pending_truncations'] and not L['complete_book']
evcount=0;types=collections.Counter()
def walk(x):
 global evcount
 if isinstance(x,dict):
  if all(k in x for k in ('source_id','revision','chapter_id','start_line','end_line')):
   assert x['source_id']==S['source_id'] and x['revision']==S['revision'];ch=by[x['chapter_id']];assert ch['start_line']<=x['start_line']<=x['end_line']<=ch['end_line'];assert x['claim_kind'] in ('fact','inference','synthesis','plan');evcount+=1;types[x['claim_kind']]+=1
  for v in x.values():walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
for x in (A,C,G):walk(x)
assert set(A['dimensions'])==set('worldbuilding characters plot style narrative dialogue pacing themes continuity'.split()) and all(len(v)>=3 for v in A['dimensions'].values())
keys={c['origin_key'] for c in C};assert len(keys)==len(C)
assert collections.Counter(c['asset_type'] for c in C)=={'character':18,'scene':23,'pattern':8}
for c in C:
 assert c['content']['summary'] and c['review_status']=='draft' and not c['favorite'] and c['user_notes']==''
 assert all(k in keys for k in c['content'].get('derived_from_origin_keys',[]))
nodes={x['id']:x for x in G['nodes']};edges={x['id']:x for x in G['edges']};assert len(nodes)==len(G['nodes']) and len(edges)==len(G['edges']);assert sum(x['parent_id'] is None for x in nodes.values())==1
for n in nodes.values():
 seen=set();p=n['id']
 while p is not None:
  assert p not in seen;seen.add(p);p=nodes[p]['parent_id']
 assert all(x in keys for x in n.get('characters',[]));assert 'knowledge' not in G
 if n['kind']=='scene':assert n['asset_origin_key'] in keys and n['characters']
 for k in n.get('knowledge',[]):assert k['observer']=='reader' or k['observer'] in keys
for e in edges.values():assert e['from'] in nodes and e['to'] in nodes and e['kind'] in ('cause','setup','reveal','misdirection','reversal','echo','payoff') and e['evidence']
for t in G['threads']:
 assert t['status'] in ('open','partial','resolved','abandoned','unknown');assert set(t['node_ids'])<=set(nodes);assert set(t['edge_ids'])<=set(edges)
 if t['status']=='resolved':assert t['resolution_note'] and t['resolution_evidence']
res={'status':'passed_local_structure_and_provenance','source_id':S['source_id'],'revision':S['revision'],'volume':3,'read_count':len(N),'first':ids[0],'last':ids[-1],'first_line':N[0]['start_line'],'last_line':N[-1]['end_line'],'dimension_observations':sum(len(v) for v in A['dimensions'].values()),'card_counts':dict(collections.Counter(c['asset_type'] for c in C)),'node_count':len(nodes),'edge_count':len(edges),'thread_count':len(G['threads']),'evidence_object_count':evcount,'claim_kinds':dict(types),'checks':['coverage exact continuous source chapters','chapter bounds and revision','all evidence claim_kind','tree parent and cycle','edges endpoints and allowed kinds','threads status/resolution evidence','card keys and derived links','node character and knowledge refs'],'limits':'纯本目录JSON与source索引检查，不初始化Vault、不占库锁；不等文学解释获认可。','review_status':'draft'}
(H/'validation.json').write_text(json.dumps(res,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(res,ensure_ascii=False))
