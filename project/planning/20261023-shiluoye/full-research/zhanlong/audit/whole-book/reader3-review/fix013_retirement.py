from common import P,A,dump,sha,evidence
import json,shutil
f=A/'adjudications-local-v01-batch013.json';before=json.loads(f.read_text(encoding='utf-8'));ix=14
assert before[ix]['candidate_id']=='v01-local-chapter_unresolved_index-0103-02'
snap=P/'batch013-before-retirement-locator.json';assert not snap.exists();shutil.copy2(f,snap)
after=json.loads(json.dumps(before));r=after[ix];r['rationale']=r['rationale'].replace('早32片','早raw35（印刷第32章）');assert r['later_chapters'][0]==32;r['later_chapters'][0]=35;r['later_evidence']=evidence(r['later_chapters']);dump(f,after)
md=f.with_suffix('.md');s=md.read_text(encoding='utf-8');old=before[ix]
s=s.replace(old['rationale'],r['rationale']);fmt=lambda es:'；'.join(f'{e["chapter_id"]} L{e["start_line"]}—{e["end_line"]}' for e in es);s=s.replace('后证：'+fmt(old['later_evidence']),'后证：'+fmt(r['later_evidence']));md.write_text(s,encoding='utf-8')
receipt=P/'v01-batch013-receipt.json';x=json.loads(receipt.read_text(encoding='utf-8'));x['sha256']=sha(f);dump(receipt,x)
state=P/'reader-state.json';st=json.loads(state.read_text(encoding='utf-8'));st['batches'][-1]=x;dump(state,st)
dump(P/'batch013-retirement-locator-delta.json',{'candidate_id':r['candidate_id'],'reason':'原文L2817归raw35/印32；只修单条章号/证据，不改源差判断。','before_sha256':sha(snap),'after_sha256':sha(f),'before':old,'after':r,'other_rows_equal':all(a==b for j,(a,b) in enumerate(zip(before,after)) if j!=ix)})
print(sha(f))
