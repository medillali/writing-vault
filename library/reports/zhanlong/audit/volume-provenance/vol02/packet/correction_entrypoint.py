import pathlib,json
P=pathlib.Path(__file__).parent
p=P/'handoff.md';s=p.read_text(encoding='utf-8');a='不用卷五另一身份改本卷行为';b='不用后卷信息改本卷行为';assert s.count(a)==1;p.write_text(s.replace(a,b),encoding='utf-8')
# 正式导入器既有优先入口使用同一overlay完整内容，原件均保留。
(P/'primary-corrections.json').write_bytes((P/'priority-corrections-delta.json').read_bytes())
