import pathlib,json,hashlib,sys,datetime
sys.stdout.reconfigure(encoding='utf-8')
Q=pathlib.Path(__file__).resolve().parent;A=Q.parent;B=A.parents[1];ROOT=B.parents[3];F=ROOT/'writing-vault/library/reports/zhanlong'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
pool=read(A/'local-question-pool.json');vol=[c for c in pool['candidates'] if c['volume']==6];rows=vol[200:399];assert len(rows)==199 and not (Q/'assigned-candidate-id-freeze.json').exists()
write(Q/'assigned-candidate-id-freeze.json',dict(volume=6,volume_pool_count=len(vol),original_volume_offsets=[200,399],candidate_ids=[x['candidate_id'] for x in rows],candidate_record_sha256={x['candidate_id']:hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True).encode()).hexdigest() for x in rows}))
pins={str(p.relative_to(ROOT)).replace('\\','/'):sha(p) for p in F.glob('vol*-chapter-notes.jsonl')}
write(Q/'input-receipt.json',dict(status='fixed-before-manual-tail-adjudication',source_id='src-20f2d16e3d1b472fa4b230ab0e1770c9',revision='61ab0b114c76446fda554abfafdac8c432cd88afaba7c2541f4473a3902134e3',actual_reviewer='/root/zongheng_vol04_full',assignment='仅volume6原序0-based[200:399]；reader5只[0:200]，不重叠',local_pool_sha256_observed=sha(A/'local-question-pool.json'),candidate_id_freeze_sha256=sha(Q/'assigned-candidate-id-freeze.json'),formal_notes_sha256=pins,reading_attribution='本代理没有亲读卷六全卷；采用正式逐章四栏/primary独立复核和明确单列的定向原文，原reader不转移。'))
write(Q/'reader-state.json',dict(status='manual-terminal-adjudication-in-progress',assigned=199,done=0,next_assigned_offset=0,original_volume_offset_next=200,adjudicated_ids=[],batches=[],complete=False))
print('fixed',len(rows),rows[0]['candidate_id'],rows[-1]['candidate_id'],sha(Q/'input-receipt.json'))
