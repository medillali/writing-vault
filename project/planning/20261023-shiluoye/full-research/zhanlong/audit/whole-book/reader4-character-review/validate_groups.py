import json,hashlib,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
D=Path(__file__).resolve().parent;A=D.parent;ROOT=D.parents[6]
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
src=rd(A.parents[1]/'source.json');cs={c['chapter_id']:c for c in src['chapters']};seen=set();groups=[];count=0
for p in sorted(A.glob('reader4-character-arcs-part*.json')):
 d=rd(p);n=0
 for r in d['characters']:
  assert r['audit_id'] not in seen;r0=r['audit_id'];seen.add(r0);assert r['review_status']=='draft'
  assert all(r.get(k) for k in ['initial_comparison_stage','key_decisions','costs','terminal_state','evidence_boundaries'])
  for e in r['evidence']:
   c=cs[e['chapter_id']];assert c['start_line']<=e['start_line']<=e['end_line']<=c['end_line'],(p.name,r0,e,c)
   assert e['source_id']==src['source_id'] and e['revision']==src['revision'] and e['claim_kind']
   assert sha(ROOT/e['research_path'])==e['research_sha256'],(r0,e['research_path'])
   n+=1
 groups.append({'path':p.name,'sha256':sha(p),'count':len(d['characters']),'evidence_count':n});count+=n
result={'status':'passed-structure-provenance-only-not-primary-semantic-review','characters':len(seen),'evidence_count':count,'groups':groups,'next_assignment':max([int(x.rsplit('-',1)[1]) for x in seen],default=0)+1}
(D/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,ensure_ascii=False))
