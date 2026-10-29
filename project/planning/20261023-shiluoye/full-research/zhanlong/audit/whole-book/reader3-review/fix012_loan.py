from common import P,A,dump,sha,evidence
import json,shutil
f=A/'adjudications-local-v01-batch012.json';before=json.loads(f.read_text(encoding='utf-8'))
ix=17;assert before[ix]['candidate_id']=='v01-local-chapter_unresolved_index-0095-01'
snap=P/'batch012-before-loan.json';assert not snap.exists();shutil.copy2(f,snap)
after=json.loads(json.dumps(before));r=after[ix]
r['status']='answered';r['rationale']='99片真实借3000金，125片李认债拟以3万R还；128片银行实际转4万R，并明确额外行动佣金为1万，故原3万R借款已经实还。130片主又将其中3万转工作室是自己的再分配，不是李仍欠。前稿只核125—127而过早判未知，现以相邻128明确实款纠正，不要求再造另一个单独3万回执。';r['later_chapters']=[99,125,128,130];r['later_evidence']=evidence(r['later_chapters'])
r['source_attribution']['later_source']+='；续完整读128—130四栏，发现128直接银行实款，定向纠此条。';dump(f,after)
md=f.with_suffix('.md');s=md.read_text(encoding='utf-8');old=before[ix]
s=s.replace(old['status']+' / '+old['audit_domain']+'：'+old['rationale'],r['status']+' / '+r['audit_domain']+'：'+r['rationale'])
fmt=lambda es:'；'.join(f'{e["chapter_id"]} L{e["start_line"]}—{e["end_line"]}' for e in es)
s=s.replace('后证：'+fmt(old['later_evidence']),'后证：'+fmt(r['later_evidence']));md.write_text(s,encoding='utf-8')
receipt=P/'v01-batch012-receipt.json';x=json.loads(receipt.read_text(encoding='utf-8'));x['sha256']=sha(f);x['counts']={'answered':15,'partial':4,'unknown':1};dump(receipt,x)
state=P/'reader-state.json';st=json.loads(state.read_text(encoding='utf-8'));st['batches'][-1]=x;dump(state,st)
dump(P/'batch012-loan-delta.json',{'candidate_id':r['candidate_id'],'reason':'新续读128直接后证纠早判，其他19逐值不动','before_sha256':sha(snap),'after_sha256':sha(f),'before':old,'after':r,'other_rows_equal':all(a==b for j,(a,b) in enumerate(zip(before,after)) if j!=ix)})
print(sha(f))
