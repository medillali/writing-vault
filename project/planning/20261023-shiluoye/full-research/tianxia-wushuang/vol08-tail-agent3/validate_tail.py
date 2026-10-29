import json,hashlib,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
P=Path(__file__).parent;S=json.loads((P.parent/'source.json').read_text(encoding='utf-8'));C={c['chapter_id']:c for c in S['chapters']}
N=[json.loads(x) for x in (P/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()];ST=json.loads((P/'reader-state.json').read_text(encoding='utf-8'));L=json.loads((P/'read-log.json').read_text(encoding='utf-8'))
expected=[f'ch-{i:04d}' for i in range(1573,1610)]
assert [n['chapter_id'] for n in N]==expected==ST['read_chapter_ids']==[n['chapter_id'] for n in L['chapters']]
assert ST['complete_assigned_tail'] and ST['next_chapter_id'] is None and not ST['complete_volume'] and not ST['complete_book'] and not ST['pending_chapter_ids'] and not ST['pending_truncations']
for n in N:
 c=C[n['chapter_id']];assert n['reader']=='/root/zongheng_vol03_full' and n['full_text_read']
 assert n['source_id']==S['source_id'] and n['revision']==S['revision']
 assert (n['start_line'],n['end_line'])==(c['start_line'],c['end_line'])
 assert all(n[k] for k in ['facts','inferences','state_changes','unresolved'])
v=dict(status='assigned_tail_coverage_passed',source_id=S['source_id'],revision=S['revision'],reader='/root/zongheng_vol03_full',segments=37,pending_truncations=0,complete_assigned_tail=True,complete_volume=False,complete_book=False,sha256={n:hashlib.sha256((P/n).read_bytes()).hexdigest() for n in ['chapter-notes.jsonl','reader-state.json','read-log.json','handoff.md']})
(P/'validation.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v[k] for k in ['status','segments','pending_truncations']},ensure_ascii=False))
