import json,hashlib,collections,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');P=Path(__file__).parent;A=P.parent;B=P.parents[2];W=B.parents[3]
load=lambda p:json.loads(p.read_text(encoding='utf-8'))
def save(p,x):
 body=json.dumps(x,ensure_ascii=False,indent=2)+'\n'
 if not p.exists() or p.read_text(encoding='utf-8')!=body:p.write_text(body,encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
pool=load(A/'local-question-pool.json');freeze=load(A/'candidate-id-freeze.json');add=load(A/'notes-unresolved-additions.json')
scope={v:[c for c in pool['candidates'] if c['volume']==v and c.get('original_field')=='notes-unresolved'] for v in [1,3]}
notes={};paths={}
for v in range(1,9):
 p=B/f'vol{v:02d}'/'chapter-notes.jsonl'
 for line in p.read_text(encoding='utf-8').splitlines():
  if line.strip():n=json.loads(line);r=int(n['chapter_id'][3:]);notes[r]=n;paths[r]=p
summary={};read_log=[]
for v in [1,3]:
 decisions={}
 for p in sorted(P.glob(f'decisions-v{v:02d}-b*.json')):
  for g,values in load(p).items():
   assert g not in decisions,(v,g,'duplicate group')
   decisions[g]=values
 rows=[]
 for g,values in sorted(decisions.items()):
  cand=sorted([c for c in scope[v] if c['original_index']==int(g)-1],key=lambda c:c['atomic_index'])
  assert len(cand)==len(values),(v,g,len(cand),len(values))
  for c,d in zip(cand,values):
   status,chapters,reason=d[:3];domain=d[3] if len(d)>3 else 'specific-event-and-terminal-match'
   assert status in ['answered','partial','unrecovered','unknown']
   row={k:c[k] for k in ['candidate_id','volume','original_path','original_field','original_index','source_note_index','source_unresolved_index','source_subatomic_index','atomic_index','title','original_record','original_evidence','original_notes_sha256']}
   row.update(status=status,audit_domain=domain,rationale=reason,later_chapters=sorted(set(chapters)),
    access_level='derived-full-four-field-notes-and-final-research;no-new-source-full-text-reading')
   ev=[]
   for r in row['later_chapters']:
    assert r in notes,(row['candidate_id'],r)
    n=notes[r]
    ev.append({'source_id':'src-d8926e2a35f04bcf8139cff0ea516bbd','revision':'d819f7d0ecf5a2004a0a434e987569bbe25015422d45e16676af913292346857',
     'chapter_id':n['chapter_id'],'start_line':n['start_line'],'end_line':n['end_line'],'claim_kind':'synthesis','access_level':'derived-reader-notes-and-final-volume-research',
     'research_path':paths[r].relative_to(W).as_posix(),'source_reader':n.get('reader','unspecified'),
     'evidence_role':'判据/原事件/后续/反例具体关系见rationale，范围核验不表示该章独立证明整项。'})
   row['later_evidence']=ev
   if row['candidate_id']=='v03-local-notes-unresolved-087-01':
    reread=load(P/'targeted-source-rereads.json')
    row['access_level']='direct-targeted-repeated-source-reread-plus-derived-research'
    row['direct_reread_evidence']=reread['chapters']
    row['direct_reread_log']='targeted-source-rereads.json'
   if row['candidate_id']=='v03-local-notes-unresolved-105-01':
    reread=load(P/'targeted-source-reread-105.json')
    row['access_level']='direct-targeted-repeated-source-reread-plus-derived-research'
    row['direct_reread_evidence']=reread['chapters']
    row['direct_reread_log']='targeted-source-reread-105.json'
   rows.append(row)
  n=notes[int(cand[0]['original_record']['chapter_id'][3:])]
  read_log.append({'volume':v,'group':int(g),'chapter_id':n['chapter_id'],'material':'complete-facts-inferences-state_changes-unresolved-note',
   'original_reader':n.get('reader'),'audit_reader':'/root/zongheng_vol03_full','new_full_source_reading':False,'atomic_count':len(cand)})
 save(P/f'adjudications-local-note-v{v:02d}.json',rows)
 pending=[c['candidate_id'] for c in scope[v] if c['candidate_id'] not in {r['candidate_id'] for r in rows}]
 summary[str(v)]={'total':len(scope[v]),'completed':len(rows),'groups_reviewed':len(decisions),'next_group':max(map(int,decisions),default=0)+1,
  'status_counts':dict(collections.Counter(r['status'] for r in rows)),'pending_count':len(pending),'pending_ids':pending}
save(P/'material-read-log.json',read_log)
save(P/'review-state.json',{'status':'in-progress-not-final-not-ready-to-merge','scope_total':995,'by_volume':summary,
 'next_action':'按下一组完整四栏+原子标题继续逐条判读；全部995完成后才终交。',
 'method':'unknown保文本矛盾/证词界限；answered可为否定/失败/已界定来源；unrecovered只特定承诺未见回执；partial逐子项分账，不推作者忘记。',
 'reader_attribution':'卷1原文primary亲读，本代理派生四栏笔记复核；卷3原文为本代理先前实读，本轮复核笔记不虚增实读覆盖；其他后证来自分工终稿和notes。',
 'local_identity_at_checkpoint':freeze['local']['candidate_identity_sha256'],
 'source_notes':[{'volume':g['volume'],'path':g['original_path'],'sha256':g['original_notes_sha256']} for g in add['groups'] if g['volume'] in [1,3]]})
print(json.dumps({v:{k:vv for k,vv in x.items() if k!='pending_ids'} for v,x in summary.items()},ensure_ascii=False,indent=2))
