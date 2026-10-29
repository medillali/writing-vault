from save_tail_manual import Q,read,write,sha
p=Q/'adjudications-local-v06-tail-batch003.json';proposal=read(Q/'lan-upper-godhead-later1295-proposal.json');before=read(p);assert before[1]==proposal['before'];before_sha=sha(p)
assert before_sha==proposal['batch_sha256'];snap=Q/'batch003-before-lan1295-primary-approved.json';assert not snap.exists();snap.write_bytes(p.read_bytes())
after=list(before);after[1]=proposal['after'];assert all(b==a for i,(b,a) in enumerate(zip(before,after)) if i!=1);write(p,after)
write(Q/'lan-upper-godhead-later1295-applied-delta.json',dict(status='applied-exact-primary-approved-proposal',user_approval=False,primary_approval='root完整读proposal与1295原章后明确批准此一项；非用户审美',proposal_sha256=sha(Q/'lan-upper-godhead-later1295-proposal.json'),actual_before_file=snap.name,actual_before_sha256=before_sha,actual_after_sha256=sha(p),before=proposal['before'],after=proposal['after'],other_19_equal=True))
md=['# 《斩龙》卷六尾199候选终评草稿','本批offset40—59；仅0101-01应用root已核1295后证；待当前整批主审签。','']
for x in after:md += [f"- **{x['candidate_id']}** · {x['status']} / {x['audit_domain']}",f"  原题：{x['title']}",f"  终评：{x['rationale']}",f"  后证raw：{', '.join(map(str,x['later_chapters']))}；派生保原reader。",'']
p.with_suffix('.md').write_text('\n'.join(md)+'\n',encoding='utf-8');s=read(Q/'reader-state.json');s['batches'][2]['sha256']=sha(p);write(Q/'reader-state.json',s);print(sha(p));print(sha(Q/'lan-upper-godhead-later1295-applied-delta.json'))
