from common import P,A,scope,CH,S,sha
import json,collections
st=json.loads((P/'reader-state.json').read_text(encoding='utf-8'));ids=[];states=collections.Counter()
for rec in st['batches']:
 f=A/rec['file'];rows=json.loads(f.read_text(encoding='utf-8'));assert sha(f)==rec['sha256'];assert f.with_suffix('.md').exists();assert len(rows)==rec['count']<=20
 for r in rows:
  c=next(c for c in scope if c['candidate_id']==r['candidate_id']);assert r['original_record']==c['original_record'] and r['original_question']==c['title'];assert r['actual_reviewer']=='/root/zongheng_vol03_full';assert r['rationale'] and r['later_evidence'];assert r['status'] in ['answered','partial','unknown','unrecovered']
  assert r['later_chapters']==[int(e['chapter_id'].split('-')[1]) for e in r['later_evidence']]
  for e in r['later_evidence']:
   n=int(e['chapter_id'].split('-')[1]);assert e['source_id']==S['source_id'] and e['revision']==S['revision'];assert e['start_line']==CH[n]['start_line'] and e['end_line']==CH[n]['end_line'];assert e['claim_kind'] in ['fact','inference','synthesis','plan']
  ids.append(r['candidate_id']);states[r['status']]+=1
assert len(ids)==len(set(ids));assert ids==st['completed_candidate_ids']
for v in [1,4]:
 got=[x for x in ids if x.startswith(f'v{v:02d}-')];expected=[c['candidate_id'] for c in scope if c['volume']==v][:len(got)];assert got==expected
print(json.dumps({'structural_check':'passed-not-literary-approval','batches':len(st['batches']),'completed':len(ids),'scope':len(scope),'next_v01':st['v01_next_onebased_offset'],'next_v04':st['v04_next_onebased_offset'],'counts':dict(states)},ensure_ascii=False))
