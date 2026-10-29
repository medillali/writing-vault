"""只应用逐项明列的人工差异，并保before；不进行语义匹配裁定。"""
from common import P,A,dump,sha,evidence
import json,shutil,collections
def revise(volume,number,cid,tag,changes,reason):
 f=A/f'adjudications-local-v{volume:02d}-batch{number:03d}.json';before=json.loads(f.read_text(encoding='utf-8'))
 ix=next(i for i,r in enumerate(before) if r['candidate_id']==cid)
 snap=P/f'batch{number:03d}-before-{tag}.json';assert not snap.exists();shutil.copy2(f,snap)
 after=json.loads(json.dumps(before));r=after[ix];r.update(changes)
 if 'later_chapters' in changes:r['later_evidence']=evidence(r['later_chapters'])
 assert all(a==b for j,(a,b) in enumerate(zip(before,after)) if j!=ix)
 dump(f,after)
 rp=P/f'v{volume:02d}-batch{number:03d}-receipt.json';rc=json.loads(rp.read_text(encoding='utf-8'));rc['sha256']=sha(f);rc['counts']=dict(collections.Counter(x['status'] for x in after));dump(rp,rc)
 md=f.with_suffix('.md');head=md.read_text(encoding='utf-8').split('\n## ')[0]
 ls=[head]
 for j,x in enumerate(after,rc['start_onebased_offset']):
  ls += [f'## {j} {x["candidate_id"]}','','原题：'+x['original_question'],'',x['status']+' / '+x['audit_domain']+'：'+x['rationale'],'','后证：'+'；'.join(f'{e["chapter_id"]} L{e["start_line"]}—{e["end_line"]}' for e in x['later_evidence']),'']
 md.write_text('\n'.join(ls),encoding='utf-8')
 state=P/'reader-state.json';st=json.loads(state.read_text(encoding='utf-8'))
 for j,x in enumerate(st['batches']):
  if x['file']==f.name:st['batches'][j]=rc
 dump(state,st)
 dump(P/f'batch{number:03d}-{tag}-delta.json',{'candidate_id':cid,'reason':reason,'before_sha256':sha(snap),'after_sha256':sha(f),'before':before[ix],'after':r,'other_rows_equal':True})
 print(json.dumps(rc,ensure_ascii=False))
