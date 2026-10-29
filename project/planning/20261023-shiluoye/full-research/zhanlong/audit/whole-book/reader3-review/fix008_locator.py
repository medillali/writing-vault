from common import P,A,dump,sha,evidence
import json,shutil
f=A/'adjudications-local-v01-batch008.json';before=json.loads(f.read_text(encoding='utf-8'))
assert before[11]['candidate_id']=='v01-local-chapter_unresolved_index-0050-02'
snap=P/'batch008-before-locator.json';assert not snap.exists();shutil.copy2(f,snap)
after=json.loads(json.dumps(before));r=after[11];assert r['later_chapters']==[54,216,421]
r['later_chapters']=[54,216,420];r['later_evidence']=evidence(r['later_chapters']);dump(f,after)
md=f.with_suffix('.md');s=md.read_text(encoding='utf-8');old=evidence([421])[0];new=evidence([420])[0]
s=s.replace(f'ch-0421 L{old["start_line"]}—{old["end_line"]}',f'ch-0420 L{new["start_line"]}—{new["end_line"]}');md.write_text(s,encoding='utf-8')
receipt=P/'v01-batch008-receipt.json';x=json.loads(receipt.read_text(encoding='utf-8'));x['sha256']=sha(f);dump(receipt,x)
state=P/'reader-state.json';st=json.loads(state.read_text(encoding='utf-8'));st['batches'][-1]=x;dump(state,st)
dump(P/'batch008-locator-delta.json',{'candidate_id':r['candidate_id'],'reason':'定向原文L35059归raw420，非421；只修后证章行，不改语义/其余19。','before_sha256':sha(snap),'after_sha256':sha(f),'before':before[11]['later_evidence'],'after':r['later_evidence']})
print(sha(f))
