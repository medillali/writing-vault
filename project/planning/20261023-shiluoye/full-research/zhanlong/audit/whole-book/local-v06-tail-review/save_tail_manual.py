"""只保存人工逐题明确写出的判断；禁止搜索/模型/模板填判。"""
import pathlib,json,hashlib,datetime,sys
sys.stdout.reconfigure(encoding='utf-8');Q=pathlib.Path(__file__).resolve().parent;A=Q.parent;B=A.parents[1];ROOT=B.parents[3];F=ROOT/'writing-vault/library/reports/zhanlong'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def save(off,entries,batch):
 freeze=read(Q/'assigned-candidate-id-freeze.json');pool=read(A/'local-question-pool.json');allrows=[x for x in pool['candidates'] if x['volume']==6][200:399];rows=allrows[off:off+len(entries)];assert 0<len(entries)<=20 and [x['candidate_id'] for x in rows]==freeze['candidate_ids'][off:off+len(entries)]
 notes={};paths={}
 for v in range(1,7):
  f=F/f'vol{v:02d}-chapter-notes.jsonl'
  for s in f.read_text(encoding='utf-8').splitlines():
   n=json.loads(s);k=int(n['chapter_id'].split('-')[1]);notes[k]=n;paths[k]=f
 out=[]
 for c,(status,domain,rationale,chapters) in zip(rows,entries):
  assert status in ['answered','partial','unknown','unrecovered'] and rationale and chapters
  assert hashlib.sha256(json.dumps(c,ensure_ascii=False,sort_keys=True).encode()).hexdigest()==freeze['candidate_record_sha256'][c['candidate_id']]
  ev=[]
  for k in dict.fromkeys(chapters):
   n=notes[k];p=paths[k];ev.append(dict(source_id=n['source_id'],revision=n['revision'],chapter_id=n['chapter_id'],start_line=n['start_line'],end_line=n['end_line'],claim_kind='fact',evidence_access='完整正式四栏派生；不转移原文实读归属',material_path=str(p.relative_to(ROOT)).replace('\\','/'),material_sha256=sha(p),source_reader=n.get('reader')))
  out.append(dict(candidate_id=c['candidate_id'],volume=6,title=c['title'],original_field=c['original_field'],original_index=c['original_index'],atomic_index=c['atomic_index'],original_record_sha256=freeze['candidate_record_sha256'][c['candidate_id']],status=status,audit_domain=domain,rationale=rationale,later_chapters=list(dict.fromkeys(chapters)),later_evidence=ev,actual_reviewer='/root/zongheng_vol04_full',reading_attribution='本代理仅读正式派生及另列定向材料；未冒亲读卷6全卷，原文reader=zongheng_vol05_full及primary原覆盖仍各自保留。'))
 p=Q/f'adjudications-local-v06-tail-batch{batch:03d}.json';assert not p.exists();write(p,out)
 md=['# 《斩龙》卷六尾199候选终评草稿',f'独占原序[200:399]，本批assigned offset {off}—{off+len(out)-1}；待primary逐项主审。','']
 for x in out:md += [f"- **{x['candidate_id']}** · {x['status']} / {x['audit_domain']}",f"  原题：{x['title']}",f"  终评：{x['rationale']}",f"  后证raw：{', '.join(map(str,x['later_chapters']))}；派生保原reader。",'']
 p.with_suffix('.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
 st=read(Q/'reader-state.json');ids=[x['candidate_id'] for x in out];assert not set(ids)&set(st['adjudicated_ids']);st['adjudicated_ids']+=ids;st['done']=len(st['adjudicated_ids']);st.update(next_assigned_offset=off+len(out),original_volume_offset_next=200+off+len(out));st['batches'].append(dict(path=p.name,sha256=sha(p),count=len(out),primary_review='pending-actual-primary-review'));write(Q/'reader-state.json',st)
 print(json.dumps(dict(path=p.name,sha256=sha(p),count=len(out),done=st['done']),ensure_ascii=False))
