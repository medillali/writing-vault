import json,hashlib,sys,collections
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');P=Path(__file__).parent;A=P.parent
load=lambda p:json.loads(p.read_text(encoding='utf-8'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
part,lo,hi=map(int,sys.argv[1:]);rows=load(P/'adjudications-local-v05-tail.json')
subset=[r for r in rows if lo<=r['scope_onebased_offset']<=hi]
assert len(subset)==hi-lo+1 and [r['scope_onebased_offset'] for r in subset]==list(range(lo,hi+1))
scope=[r for r in load(A/'local-question-pool.json')['candidates'] if r['volume']==5]
for r in subset:
 c=scope[r['scope_onebased_offset']-1]
 assert r['candidate_id']==c['candidate_id'] and r['original_record']==c['original_record'] and r['original_evidence']==c['original_evidence']
 assert r['later_chapters'] and len(r['later_chapters'])==len(r['later_evidence'])
p=P/f'adjudications-local-v05-tail-part{part:02d}.json';assert not p.exists(),'frozen file exists'
p.write_text(json.dumps(subset,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
v={'status':'structural-checks-passed-pending-primary-semantic-review','assigned_scope':[178,556],
 'onebased_offsets':[lo,hi],'candidate_count':len(subset),'first_id':subset[0]['candidate_id'],'last_id':subset[-1]['candidate_id'],
 'sha256':sha(p),'status_counts':dict(collections.Counter(r['status'] for r in subset)),
 'checks':{'exact_offset_range':True,'original_records_unchanged':True,'original_evidence_unchanged':True,'all_rows_have_specific_later_evidence':True},
 'reading_attribution':'卷五原文agent4，本代理派生相关完整四栏notes/最终研究；后证各保原reader，不新增正文覆盖。'}
(P/f'part{part:02d}-validation.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(v,ensure_ascii=False,indent=2))
