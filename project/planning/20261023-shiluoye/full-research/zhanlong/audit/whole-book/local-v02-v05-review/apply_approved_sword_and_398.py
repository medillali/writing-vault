from save_manual_batch import P,read,write,sha
import copy

def apply(ch,label,proposal):
    f=P/ch['path'];assert sha(f)==ch['input_sha256'];rows=read(f)
    snap=P/'history'/f'{f.stem}-before-{label}.json';assert not snap.exists();snap.write_bytes(f.read_bytes())
    idx=next(i for i,x in enumerate(rows) if x['candidate_id']==ch['candidate_id'])
    before=copy.deepcopy(rows);assert rows[idx]==ch['before'];rows[idx]=ch['after'];write(f,rows)
    assert all(a==b for i,(a,b) in enumerate(zip(before,rows)) if i!=idx)
    md=f.with_suffix('.md');s=md.read_text(encoding='utf-8')
    s=s.replace(ch['before']['rationale'],ch['after']['rationale'])
    s=s.replace(f"**{ch['candidate_id']}** · {ch['before']['status']}",f"**{ch['candidate_id']}** · {ch['after']['status']}")
    s=s.replace('证据raw：'+', '.join(map(str,ch['before']['later_chapters']))+'；','证据raw：'+', '.join(map(str,ch['after']['later_chapters']))+'；')
    md.write_text(s,encoding='utf-8')
    delta=dict(status='applied-exact-primary-approved-awaiting-resign',primary_approval='root消息明确批准限定版；不是用户品味批准',proposal_sha256=sha(proposal),batch_before_sha256=ch['input_sha256'],batch_after_sha256=sha(f),before_snapshot=str(snap.relative_to(P)).replace('\\','/'),change=ch,other_objects_equal=True)
    out=P/f'{label}-merged-delta.json';assert not out.exists();write(out,delta)
    state=read(P/'reader-state.json')
    for b in state['submitted_batches']:
        if b['path']==f.name:b.update(sha256=sha(f),primary_review='pending-primary-delta-resign')
    write(P/'reader-state.json',state)
    print(f.name,sha(f),'delta',sha(out))

proposal=P/'sword-growth-quota-limited-proposal.json'
apply(read(proposal)['change'],'sword-growth-quota-limited',proposal)
proposal=P/'later398-princess-and-private-branches-proposal.json'
for ch,label in zip(read(proposal)['changes'],['princess398','private-branches398']):apply(ch,label,proposal)
