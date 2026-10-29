"""只追加卷1/3/8缺少显式analysis索引的原notes未决；不重排旧候选。"""
import pathlib,json,hashlib,copy,re,sys,collections
sys.stdout.reconfigure(encoding='utf-8');H=pathlib.Path(__file__).resolve().parent;B=H.parents[1];R=H.parents[5]
read=lambda p:json.loads(p.read_text(encoding='utf-8'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
write=lambda p,v:p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
local=read(H/'local-question-pool.json');history=read(H/'historical-question-pool.json');old=copy.deepcopy(local['candidates']);oldids=[x['candidate_id'] for x in old]
assert len(old)==2625 and not any(x['original_field']=='notes-unresolved' for x in old)
source=read(B/'source.json');S={c['chapter_id']:c for c in source['chapters']}
archive=H/'reviewed-batches/candidate-ids-before-notes-supplement.json';assert not archive.exists();archive.write_bytes((H/'candidate-id-freeze.json').read_bytes())
groups=[]
for v in [1,3,8]:
 p=B/f'vol{v:02d}/chapter-notes.jsonl';path=p.relative_to(R).as_posix();notes=[json.loads(l) for l in p.read_text(encoding='utf-8').splitlines() if l.strip()]
 records=[];new=[];string_count=0
 for source_index,n in enumerate(notes):
  ss=n.get('unresolved',[])
  if not ss:continue
  if isinstance(ss,str):ss=[ss]
  assert isinstance(ss,list) and all(isinstance(s,str) for s in ss)
  record={k:copy.deepcopy(n[k]) for k in ['chapter_id','title','reader','start_line','end_line'] if k in n};record['unresolved']=copy.deepcopy(ss);record['source_note_index']=source_index
  original_index=len(records);records.append(record);string_count+=len(ss);atomic_index=0
  c=S[n['chapter_id']]
  es=[dict(source_id=source['source_id'],revision=source['revision'],chapter_id=c['chapter_id'],start_line=c['start_line'],end_line=c['end_line'],claim_kind='fact',access_level='derived-reader-notes-not-this-agent-full-reading',research_path=path,source_reader=n.get('reader','见分卷reading_attribution'))]
  for si,s in enumerate(ss):
   for ai,atom in enumerate([s.strip(' \n；;') for s in re.split('[；;]',s) if s.strip(' \n；;')]):
    new.append(dict(candidate_id=f'v{v:02d}-local-notes-unresolved-{original_index+1:03d}-{atomic_index+1:02d}',volume=v,original_path=path,original_field='notes-unresolved',original_index=original_index,source_note_index=source_index,source_unresolved_index=si,source_subatomic_index=ai,atomic_index=atomic_index,original_record=copy.deepcopy(record),title=atom,original_evidence=copy.deepcopy(es),original_notes_sha256=sha(p),terminal_assessment=dict(status='unknown',review_progress='pending-manual-adjudication',rationale='补充保全原notes未决，未判读，不能视为已完成终点匹配。',later_evidence=[])));atomic_index+=1
 local['candidates'].extend(new)
 history['local_issue_records'].append(dict(volume=v,field='notes-unresolved',original_path=path,original_notes_sha256=sha(p),scope='原notes内有unresolved的记录依原序筛选；source_note_index保真实JSONL非空行索引，original_index为本筛选字段中的序号。',original_records=records))
 groups.append(dict(volume=v,original_path=path,original_notes_sha256=sha(p),notes_records=len(records),original_unresolved_strings=string_count,atomic_candidates=len(new),candidate_ids=[x['candidate_id'] for x in new]))
assert local['candidates'][:len(old)]==old
assert len({x['candidate_id'] for x in local['candidates']})==len(local['candidates'])
local['scope']='八卷analysis本地字段及其显式逐章未明索引，另追加卷1/3/8缺少analysis索引的原notes未明；旧2625完整不动，增量独立field。'
write(H/'local-question-pool.json',local);write(H/'historical-question-pool.json',history)
write(H/'notes-unresolved-additions.json',dict(status='all_missing_notes_mechanically_preserved_pending_adjudication',previous_local_candidates=2625,old_candidates_unchanged=True,old_candidate_ids_sha256=hashlib.sha256('\n'.join(oldids).encode('utf-8')).hexdigest(),new_candidates=sum(x['atomic_candidates'] for x in groups),local_candidates_total=len(local['candidates']),groups=groups,not_personal_full_book_rereading=True))
inv=read(H/'input-inventory.json');inv['counts']['local']=len(local['candidates']);inv['counts']['by_volume']={str(v):dict(historical=sum(x['volume']==v for x in history['candidates']),local=sum(x['volume']==v for x in local['candidates'])) for v in range(1,9)};inv['notes_input_sha256']={x['original_path']:x['original_notes_sha256'] for x in groups};inv['status']='all_formal_studies_plus_missing_note_fields_preserved_pending_reading_and_adjudication';write(H/'input-inventory.json',inv)
print(json.dumps(dict(old_unchanged=True,total=len(local['candidates']),groups=[{k:v for k,v in x.items() if k!='candidate_ids'} for x in groups]),ensure_ascii=False))
