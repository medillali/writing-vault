from common import *
old='性交易未履行';new='未见性交易履行证据'
changed=[]
for name in ['cards.json','graph.json','analysis.json','report.md','handoff.md']:
 p=P/name;t=p.read_text(encoding='utf-8');n=t.count(old)
 if n:p.write_text(t.replace(old,new),encoding='utf-8');changed.append(dict(file=name,replacements=n))
assert changed==[{'file':'cards.json','replacements':3},{'file':'graph.json','replacements':1},{'file':'report.md','replacements':1}],changed
print(json.dumps(changed,ensure_ascii=False))
