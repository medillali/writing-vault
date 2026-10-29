from save_focus_manual import P,A,read,write,sha
import copy
p=A/'focused-findings-part03.json';old=read(p);new=copy.deepcopy(old);b=old['findings'][-1];a=new['findings'][-1]
a['title']='两条长线与末段记忆新线：目标关闭后仍有责任与期待'
a['conclusion']='研究归纳：游戏军政与现实保护是两条长期推进的线，人物关系和责任持续牵制同一主角的时间、选择与承诺；记忆重塑是末段才打开的新线，延续失落后的身份与关系期待。局部目标兑现后，新的权限、知情和生存条件继续制造期待，终点同时有关闭与开放。'
assert b['stage_chain']==a['stage_chain'] and b['evidence']==a['evidence'] and old['findings'][:-1]==new['findings'][:-1]
write(P/'focus03-before-longlines-precision.json',old);write(p,new)
write(P/'focus03-longlines-precision-delta.json',{'primary_approval':'root全读8项后明确要求仅末项title/conclusion收窄，记忆不是贯穿全书长线','before':b,'after':a,'other_seven_identical':True,'stage_and_evidence_identical':True,'after_sha256':sha(p)})
md=p.with_suffix('.md');s=md.read_text(encoding='utf-8').replace(b['title'],a['title']).replace(b['conclusion'],a['conclusion']);md.write_text(s,encoding='utf-8')
src=P/'manual_focus_part03.py';s=src.read_text(encoding='utf-8').replace(b['title'],a['title']).replace(b['conclusion'],a['conclusion']);src.write_text(s,encoding='utf-8')
print(sha(p));print(sha(P/'focus03-longlines-precision-delta.json'))
