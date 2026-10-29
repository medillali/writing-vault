from pathlib import Path
import subprocess,sys
root=Path(__file__).parent
replacements={
 'b02.py':[("status='anomaly',answer='神称呼", "status='unknown',answer='神称呼")],
 'b03.py':[("333训练若干", "433训练若干"),("哥哥身份待遇", "哥哥身份待揭"),("[411,25217,25221]", "[411,25207,25210]"),("糖的14岁以下无血痛保护和神佑奖，与地精缩小器、神圣血瓶道具分别组成不同规则资源；不能将禁普通药直接等同禁回血技能。", "糖的14岁以下无血痛保护和神佑奖，与地精缩小器、神圣血瓶道具分别组成不同资源；411黑赛禁任何药剂特殊道具，443全服赛使用回血道具，赛事是否同域未解释。"),("神圣血瓶是早购道具技能而不是自费药剂，443竞技使用与先前禁药/特殊道具的具体适用存在需核差别，照实记录不自造统一法条。", "神圣血瓶是早购道具技能，411黑赛禁任何药剂特殊道具，443全服赛确用回血道具；两赛事适用规则是否不同未说明，照实保留疑点。")],
 'b04.py':[("30万级伤害、数百万元素等", "30万级伤害、数百水元素等")],
}
for name,changes in replacements.items():
 p=root/name;s=p.read_text(encoding='utf-8')
 for a,b in changes:s=s.replace(a,b)
 p.write_text(s,encoding='utf-8')
 subprocess.run([sys.executable,str(p)],check=True)
