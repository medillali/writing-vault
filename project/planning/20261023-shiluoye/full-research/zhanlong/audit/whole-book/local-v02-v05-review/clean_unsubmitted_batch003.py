from save_manual_batch import P,read,write,sha
f=P/'adjudications-local-v02-batch003.json'; x=read(f)
old=x[16]['rationale']; new='266汪在篮球场与主实际交锋，球飞来是否故意仍双方不同说法；360游戏实战又直接与汪敌对，1278汪已实变殖装/断臂逃。262的警惕确有后续对立，但当次不能把主怀疑升级为汪承认暗算。'
assert old.startswith('266汪');x[16]['rationale']=new;write(f,x)
md=f.with_suffix('.md');md.write_text(md.read_text(encoding='utf-8').replace(old,new),encoding='utf-8')
src=P/'manual_v02_003.py';src.write_text(src.read_text(encoding='utf-8').replace(old,new),encoding='utf-8')
s=read(P/'reader-state.json');s['submitted_batches'][-1]['sha256']=sha(f);write(P/'reader-state.json',s);print(sha(f))
