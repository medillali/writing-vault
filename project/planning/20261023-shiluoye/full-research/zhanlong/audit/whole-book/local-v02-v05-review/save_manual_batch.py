"""仅保存已人工逐项写明的终评；不搜索、不推断、不生成理由。"""
import json,pathlib,hashlib,datetime,collections
P=pathlib.Path(__file__).resolve().parent; A=P.parent; B=A.parents[1]; ROOT=B.parents[3]
F=ROOT/'writing-vault/library/reports/zhanlong'
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def save(vol,offset,entries,batch):
 pool=read(A/'local-question-pool.json'); frozen=read(P/'assigned-candidate-id-freeze.json')
 rows=[c for c in pool['candidates'] if c['volume']==vol][offset:offset+len(entries)]
 assert 0<len(entries)<=20 and len(rows)==len(entries)
 assert [c['candidate_id'] for c in rows]==frozen['volumes'][str(vol)][offset:offset+len(rows)]
 notes={}; paths={}
 for v in range(1,7):
  f=F/f'vol{v:02d}-chapter-notes.jsonl'
  for line in f.read_text(encoding='utf-8').splitlines():
   if line.strip():
    n=json.loads(line); k=int(n['chapter_id'].split('-')[1]);notes[k]=n;paths[k]=f
 output=[]
 for c,(status,domain,rationale,chapters) in zip(rows,entries):
  assert status in ['answered','partial','unknown','unrecovered'] and rationale and chapters
  assert hashlib.sha256(json.dumps(c,ensure_ascii=False,sort_keys=True).encode('utf-8')).hexdigest()==frozen['candidate_record_sha256'][c['candidate_id']]
  evidence=[]
  for k in dict.fromkeys(chapters):
   n=notes[k]; f=paths[k]
   e=dict(source_id=n['source_id'],revision=n['revision'],chapter_id=n['chapter_id'],start_line=n['start_line'],end_line=n['end_line'],claim_kind='fact',evidence_access='正式逐章四栏派生笔记；原文归属不转移',material_path=str(f.relative_to(ROOT)).replace('\\','/'),material_sha256=sha(f),source_reader=n.get('reader','原卷原reader'))
   if k==314:
    corr=F/'vol02-primary-corrections.json';e.update(priority_correction_path=str(corr.relative_to(ROOT)).replace('\\','/'),priority_correction_sha256=sha(corr),correction_application='斩华与巴林佩剑两物分离；优先纠错已读，另本轮BEGIN-END定向复读314，不冒全书原文复读')
   evidence.append(e)
  output.append(dict(candidate_id=c['candidate_id'],volume=vol,title=c['title'],original_field=c['original_field'],original_index=c['original_index'],atomic_index=c['atomic_index'],original_record_sha256=frozen['candidate_record_sha256'][c['candidate_id']],status=status,audit_domain=domain,rationale=rationale,later_chapters=list(dict.fromkeys(chapters)),later_evidence=evidence,actual_reviewer='/root/zongheng_vol04_full',reading_attribution='人工终评；卷2 prefix及卷5为本人原文旧实读，卷2尾原文reader=primary，跨卷以所列正式派生为据；不称个人重读全书。'))
 file=P/f'adjudications-local-v{vol:02d}-batch{batch:03d}.json'; assert not file.exists();write(file,output)
 md=['# 《斩龙》局部候选终评草稿',f'卷{vol}，offset {offset}—{offset+len(rows)-1}；{len(rows)}项，待primary实际主审。','']
 for x in output: md += [f"- **{x['candidate_id']}** · {x['status']} / {x['audit_domain']}",f"  原题：{x['title']}",f"  终评：{x['rationale']}",f"  证据raw：{', '.join(map(str,x['later_chapters']))}；访问为正式派生，保原reader。",'']
 file.with_suffix('.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
 state=read(P/'reader-state.json'); ids=[x['candidate_id'] for x in output]
 assert not set(ids)&set(state['adjudicated_ids']);state['adjudicated_ids']+=ids
 state['submitted_batches'].append(dict(path=file.name,sha256=sha(file),count=len(ids),primary_review='pending-actual-primary-review'))
 state.update(current_volume=vol,next_offset=offset+len(rows),updated_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
 write(P/'reader-state.json',state)
 print(json.dumps(dict(path=str(file.relative_to(ROOT)).replace('\\','/'),sha256=sha(file),count=len(output),done=len(state['adjudicated_ids']),status_counts=dict(collections.Counter(x['status'] for x in output))),ensure_ascii=False))
