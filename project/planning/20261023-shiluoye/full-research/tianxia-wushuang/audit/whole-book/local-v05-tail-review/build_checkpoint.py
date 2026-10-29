import json,hashlib,collections,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');P=Path(__file__).parent;A=P.parent;B=P.parents[2]
load=lambda p:json.loads(p.read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):
 body=json.dumps(x,ensure_ascii=False,indent=2)+'\n'
 if not p.exists() or p.read_text(encoding='utf-8')!=body:p.write_text(body,encoding='utf-8')
pool=load(A/'local-question-pool.json');scope=[r for r in pool['candidates'] if r['volume']==5]
assert len(scope)==556 and scope[176]['candidate_id']=='v05-local-local_historical_questions-057-01'
assert scope[177]['candidate_id']=='v05-local-local_historical_questions-057-02'
assert all(r['original_field']!='notes-unresolved' for r in scope)
notes={};paths={}
for v in range(1,9):
 p=B/f'vol{v:02d}'/'chapter-notes.jsonl'
 for line in p.read_text(encoding='utf-8').splitlines():
  if line.strip():
   n=json.loads(line);raw=int(n['chapter_id'][3:]);notes[raw]=n;paths[raw]=p
decisions={}
for p in sorted(P.glob('decisions-b*.json')):
 for k,d in load(p).items():
  i=int(k);assert 178<=i<=556 and i not in decisions;decisions[i]=d
rows=[]
for i,d in sorted(decisions.items()):
 c=scope[i-1];s,chs,reason=d[:3];assert s in ['answered','partial','unrecovered','unknown']
 r={k:c[k] for k in ['candidate_id','volume','original_path','original_field','original_index','atomic_index','title','original_record','original_evidence']}
 r.update(scope_onebased_offset=i,status=s,later_chapters=sorted(set(chs)),rationale=reason,
  audit_domain=d[3] if len(d)>3 else 'specific-event-terminal-match',
  access_level='derived-complete-four-field-notes-and-final-research;no-new-full-source-reading')
 ev=[]
 for raw in r['later_chapters']:
  n=notes[raw];ev.append({'source_id':'src-d8926e2a35f04bcf8139cff0ea516bbd','revision':'d819f7d0ecf5a2004a0a434e987569bbe25015422d45e16676af913292346857',
   'chapter_id':n['chapter_id'],'start_line':n['start_line'],'end_line':n['end_line'],'claim_kind':'synthesis',
   'source_reader':n.get('reader','unspecified'),'research_path':str(paths[raw].relative_to(B)).replace('\\','/'),
   'evidence_role':'同一原事件/后状态/反例的具体关系见rationale，章界有效不等单章独证整项。'})
 r['later_evidence']=ev;rows.append(r)
save(P/'adjudications-local-v05-tail.json',rows)
save(P/'review-state.json',{'status':'in-progress-not-final','assigned_onebased':[178,556],'assigned_count':379,
 'completed':len(rows),'next_onebased_offset':min(set(range(178,557))-set(decisions),default=None),
 'status_counts':dict(collections.Counter(r['status'] for r in rows)),
 'scope_first_id':scope[177]['candidate_id'],'scope_last_id':scope[-1]['candidate_id'],
 'original_records_unchanged':True,'reader_attribution':'卷五原文由agent4亲读；本代理仅派生完整四栏笔记及最终研究终审，定向后证另保真实reader，不冒全书独读。',
 'not_to_touch':'root local-v05-primary-review前177/5批；主池/正式库/既有分卷和已签块。',
 'local_identity_sha256':load(A/'candidate-id-freeze.json')['local']['candidate_identity_sha256']})
print(json.dumps({'completed':len(rows),'remaining':379-len(rows),'next':min(set(range(178,557))-set(decisions),default=None)},ensure_ascii=False))
