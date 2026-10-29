from save_manual_batch import P,read,write,sha
f=P/'adjudications-local-v05-batch003.json';rows=read(f)
old='后1110兰等回到龙城不指明这次冲锋谷寻宝得何物；'
new='后1069子舒治兰臂/两女留守龙城，没有指明这次冲锋谷寻宝得何物；'
assert old in rows[19]['rationale'];rows[19]['rationale']=rows[19]['rationale'].replace(old,new);write(f,rows)
for x in [f.with_suffix('.md'),P/'manual_v05_003.py']:
    s=x.read_text(encoding='utf-8');assert old in s;x.write_text(s.replace(old,new),encoding='utf-8')
s=read(P/'reader-state.json')
for b in s['submitted_batches']:
    if b['path']==f.name:b['sha256']=sha(f)
write(P/'reader-state.json',s);print(sha(f))
