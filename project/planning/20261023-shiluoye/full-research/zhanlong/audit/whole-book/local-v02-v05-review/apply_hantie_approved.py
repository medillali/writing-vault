from save_manual_batch import P,read,write,sha
import copy
q=P/'hantie-gift-compensation-proposal.json';ch=read(q)['changes'][0];f=P/ch['path'];assert sha(f)==ch['input_sha256']
rows=read(f);old=copy.deepcopy(rows);i=next(i for i,x in enumerate(rows) if x['candidate_id']==ch['candidate_id']);assert rows[i]==ch['before']
snap=P/'history'/'batch010-before-hantie-gift.json';assert not snap.exists();snap.write_bytes(f.read_bytes());rows[i]=ch['after'];write(f,rows)
assert all(a==b for j,(a,b) in enumerate(zip(old,rows)) if j!=i)
md=f.with_suffix('.md');s=md.read_text(encoding='utf-8').replace(ch['before']['rationale'],ch['after']['rationale']).replace(f"**{ch['candidate_id']}** · partial",f"**{ch['candidate_id']}** · answered")
s=s.replace('证据raw：'+', '.join(map(str,ch['before']['later_chapters']))+'；','证据raw：'+', '.join(map(str,ch['after']['later_chapters']))+'；');md.write_text(s,encoding='utf-8')
d=P/'hantie-gift-compensation-merged-delta.json';assert not d.exists();write(d,dict(status='applied-exact-primary-approved-awaiting-resign',primary_approval='root完整读后明确批准，仅所列一条；非用户品味批准',proposal_sha256=sha(q),before_snapshot=str(snap.relative_to(P)),batch_before_sha256=ch['input_sha256'],batch_after_sha256=sha(f),change=ch,other_objects_equal=True))
state=read(P/'reader-state.json')
for b in state['submitted_batches']:
    if b['path']==f.name:b.update(sha256=sha(f),primary_review='pending-primary-delta-resign')
write(P/'reader-state.json',state);print('batch010',sha(f),'delta',sha(d))
