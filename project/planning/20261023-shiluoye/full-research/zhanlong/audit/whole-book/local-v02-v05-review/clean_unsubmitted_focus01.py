from save_focus_manual import A,P,E,read,write,sha
import copy
f=A/'focused-findings-part01.json';rows=read(f);old=copy.deepcopy(rows)
a='1289游戏蝴蝶升级与1371梦见希神兵断蝴蝶/纯钧分开，梦醒不撤销现实1355真断，也不算游戏两国器已毁。'
z='1289游戏蝴蝶只在重铸中，1290才系统国器实成；1371梦见希神兵断蝴蝶/纯钧又另层，梦醒不撤销现实1355真断，也不算游戏两国器已毁。'
assert rows[3]['stage_chain'][2]==a;rows[3]['stage_chain'][2]=z;rows[3]['evidence'].append(E(1290))
write(P/'unsubmitted-self-check/focus01-before-game-recast-completion.json',old);write(f,rows)
md=f.with_suffix('.md');s=md.read_text(encoding='utf-8').replace(a,z).replace('ch-1355, ch-1371\n','ch-1355, ch-1371, ch-1290\n');md.write_text(s,encoding='utf-8')
src=P/'manual_focus_part01.py';s=src.read_text(encoding='utf-8').replace(a,z).replace('1289,1355,1371]','1289,1355,1371,1290]');src.write_text(s,encoding='utf-8')
print(sha(f))
