from save_manual_batch import P,read,write,sha
f=P/'adjudications-local-v02-batch011.json';x=read(f);old=x[14]['rationale'];new='358初见独立创建、366沈副盟与核心转入明确，但“初见将作第一盟”是主猜，未给这个组织后来现系统第几分盟的独立编号回执。508沈仍在对方情报位置不能替初见补分盟序号；副盟职位与分盟编号须分别判断。'
x[14]['rationale']=new;x[14]['later_chapters']=[358,366,508]
# 全为已经完整实际读取的正式笔记，复用本批相同来源引用。
refs={int(e['chapter_id'].split('-')[1]):e for a in x for e in a['later_evidence']};x[14]['later_evidence']=[refs[k] for k in [358,366,508]];write(f,x)
md=f.with_suffix('.md');s=md.read_text(encoding='utf-8').replace(old,new).replace('证据raw：358, 366, 623；','证据raw：358, 366, 508；');md.write_text(s,encoding='utf-8')
src=P/'manual_v02_011.py';s=src.read_text(encoding='utf-8').replace(old,new).replace("[358,366,623]),","[358,366,508]),");src.write_text(s,encoding='utf-8')
state=read(P/'reader-state.json');state['submitted_batches'][-1]['sha256']=sha(f);write(P/'reader-state.json',state);print(sha(f))
