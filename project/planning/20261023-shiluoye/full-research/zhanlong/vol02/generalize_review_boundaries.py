import pathlib
P=pathlib.Path(__file__).parent
p=P/'research_characters.py';s=p.read_text(encoding='utf-8')
for a,b in [('不使用卷五现实回顾反填本卷具体死因','不以后卷信息反填本卷现实生死'),('不借卷五NPC夏禹职倒灌','不将其他实体的职务套给叶来')]:
 assert s.count(a)==1;s=s.replace(a,b)
p.write_text(s,encoding='utf-8')
