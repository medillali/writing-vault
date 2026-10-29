"""仅用于root已明确批准的精确before/after；不会自己批准或生成结论。"""
from save_manual_batch import P,read,write,sha
import copy,sys
q=P/sys.argv[1];label=sys.argv[2];changes=read(q)['changes'];deltas=[]
for ch in changes:
    f=P/ch['path'];assert sha(f)==ch['input_sha256'];rows=read(f);old=copy.deepcopy(rows)
    i=next(i for i,x in enumerate(rows) if x['candidate_id']==ch['candidate_id']);assert rows[i]==ch['before']
    snap=P/'history'/f'{f.stem}-before-{label}.json';assert not snap.exists();snap.write_bytes(f.read_bytes())
    rows[i]=ch['after'];write(f,rows);assert all(a==b for j,(a,b) in enumerate(zip(old,rows)) if j!=i)
    md=f.with_suffix('.md');s=md.read_text(encoding='utf-8').replace(ch['before']['rationale'],ch['after']['rationale'])
    s=s.replace(f"**{ch['candidate_id']}** · {ch['before']['status']}",f"**{ch['candidate_id']}** · {ch['after']['status']}")
    s=s.replace('证据raw：'+', '.join(map(str,ch['before']['later_chapters']))+'；','证据raw：'+', '.join(map(str,ch['after']['later_chapters']))+'；');md.write_text(s,encoding='utf-8')
    deltas.append(dict(batch_before_sha256=ch['input_sha256'],batch_after_sha256=sha(f),before_snapshot=str(snap.relative_to(P)),change=ch,other_objects_equal=True))
    state=read(P/'reader-state.json')
    for b in state['submitted_batches']:
        if b['path']==f.name:b.update(sha256=sha(f),primary_review='pending-primary-delta-resign')
    write(P/'reader-state.json',state);print(f.name,sha(f))
out=P/f'{label}-merged-delta.json';assert not out.exists();write(out,dict(status='applied-exact-primary-approved-awaiting-resign',primary_approval='root实际完整读提案后消息明确批准；非用户品味批准',proposal_sha256=sha(q),changes=deltas));print('delta',sha(out))
