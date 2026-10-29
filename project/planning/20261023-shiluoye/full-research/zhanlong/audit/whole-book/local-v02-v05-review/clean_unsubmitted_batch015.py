from save_manual_batch import P,read,write,sha
f=P/'adjudications-local-v02-batch015.json';rows=read(f)
old='后续复生/重建和多轮异魔战持续，最终1360以后终战另有结局。'
new='后续复生/重建和多轮异魔战持续。'
assert old in rows[7]['rationale'];rows[7]['rationale']=rows[7]['rationale'].replace(old,new);write(f,rows)
for x in [f.with_suffix('.md'),P/'manual_v02_015.py']:
    s=x.read_text(encoding='utf-8');assert old in s;x.write_text(s.replace(old,new),encoding='utf-8')
s=read(P/'reader-state.json')
for b in s['submitted_batches']:
    if b['path']==f.name:b['sha256']=sha(f)
write(P/'reader-state.json',s);print(sha(f))
