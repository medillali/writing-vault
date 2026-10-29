import json,hashlib,sys,copy
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');P=Path(__file__).parent;A=P.parent;B=P.parents[2]
load=lambda p:json.loads(p.read_text(encoding='utf-8'))
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
f=P/'adjudications-local-note-v01-part01.json';old=load(f);oldsha=sha(f)
new=[r for r in load(P/'adjudications-local-note-v01.json') if r['original_index']<24]
deltas=[]
for before,after in zip(old,new):
 assert before['candidate_id']==after['candidate_id']
 if before!=after:deltas.append({'candidate_id':before['candidate_id'],'before':before,'after':after})
assert [x['candidate_id'] for x in deltas]==['v01-local-notes-unresolved-009-04','v01-local-notes-unresolved-013-01','v01-local-notes-unresolved-016-01']
save(f,new)
save(P/'primary-delta-part01.json',{'reason':'root定向三原子纠修罗王章号与专家身份后证','old_part_sha256':oldsha,'new_part_sha256':sha(f),'delta':deltas})
hf=A/'history-v01-v04-review/adjudications-history-v01-v04.json';r=next(x for x in load(hf) if x['candidate_id']=='v01-thread-001');proposed=copy.deepcopy(r)
proposed['rationale']=proposed['rationale'].replace('371修罗王','579 L50259系统进化修罗王（575仍差5%）')
proposed['later_chapters']=sorted(set(579 if n==371 else n for n in proposed['later_chapters']))
note=next(json.loads(s) for s in (B/'vol03/chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if s.strip() and json.loads(s)['chapter_id']=='ch-0579')
for e in proposed['later_evidence']:
 if e['chapter_id']=='ch-0371':e['chapter_id']='ch-0579';e['start_line']=note['start_line'];e['end_line']=note['end_line']
save(P/'historical-v01-thread001-shura-king-delta.json',{'status':'proposed-primary-review-not-applied-to-frozen55','base_json_sha256':sha(hf),'candidate_id':r['candidate_id'],'before':r,'proposed_after':proposed,
 'reason':'371为白狐店铺，575仍预期，579 L50259才系统进化修罗王；旧55已签不静默改。'})
print(json.dumps({'new_part01_sha256':sha(f),'delta_sha256':sha(P/'primary-delta-part01.json'),'historical_proposal_sha256':sha(P/'historical-v01-thread001-shura-king-delta.json')},ensure_ascii=False))
