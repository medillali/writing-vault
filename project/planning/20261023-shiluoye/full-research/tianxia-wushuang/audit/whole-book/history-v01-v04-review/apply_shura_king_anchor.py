import json,hashlib,copy,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');P=Path(__file__).parent;B=P.parents[2]
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
f=P/'adjudications-history-v01-v04.json';old=load(f);rows=copy.deepcopy(old);oldsha=sha(f)
x=next(x for x in rows if x['candidate_id']=='v01-thread-001');before=copy.deepcopy(x)
assert '371修罗王' in x['rationale']
x['rationale']=x['rationale'].replace('371修罗王','579修罗王')
x['later_chapters']=[579 if c==371 else c for c in x['later_chapters']];x['later_chapters'].sort()
n=next(json.loads(s) for s in (B/'vol03/chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if s.strip() and json.loads(s)['chapter_id']=='ch-0579')
for e in x['later_evidence']:
 if e['chapter_id']=='ch-0371':e['chapter_id']='ch-0579';e['start_line']=n['start_line'];e['end_line']=n['end_line']
assert [a['candidate_id'] for a,b in zip(old,rows) if a!=b]==['v01-thread-001']
save(f,rows)
md=P/'adjudications-history-v01-v04.md';t=md.read_text(encoding='utf-8').replace(before['rationale'],x['rationale'])
def edis(row):return '后证：'+'；'.join(f"{e['chapter_id']} L{e['start_line']}—{e['end_line']}（reader={e['notes_reader']}）" for e in row['later_evidence'])
t=t.replace(edis(before),edis(x));md.write_text(t,encoding='utf-8')
delta={'authorization':'root已逐条复核提议，准仅本条371→579与证据','candidate_id':x['candidate_id'],'before_json_sha256':oldsha,'before':before,'after':x,
 'new_json_sha256':sha(f),'new_md_sha256':sha(md),'unchanged_other_rows':54}
save(P/'primary-shura-anchor-delta.json',delta)
v=load(P/'validation.json')
for a in v['artifacts']:
 p=P/a['path'].split('/')[-1]
 a['sha256']=sha(p);a['bytes']=p.stat().st_size
v['checks']['shura_king_579_anchor_corrected']=True;v['checks']['other54_unchanged_in_shura_delta']=True
save(P/'validation.json',v)
print(json.dumps({'json':sha(f),'md':sha(md),'delta':sha(P/'primary-shura-anchor-delta.json'),'validation':sha(P/'validation.json')},ensure_ascii=False))
