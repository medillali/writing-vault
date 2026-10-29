import pathlib
H=pathlib.Path(__file__).resolve().parent;p=H/'write_history05_remaining.py';s=p.read_text(encoding='utf-8')
for old in range(28,20,-1):
 s=s.replace(f"('v05-question-{old:03d}',",f"('v05-question-{old+1:03d}',")
s=s.replace("('v05-question-022','answered','reward-denial'", "('v05-question-021','answered','city-defense-tested','1177陆实际调暗月千骨龙毁重甲器械/逼野王撤，1596李再报千龙出守退清；城防已有实际检验，不等每次无损或全世界不可破。',[989,1007,1177,1596]),\n+('v05-question-022','answered','reward-denial'".replace('\n+','\n'))
s=s.replace('苏后与卡琳互保、参与对林战及仍控紫葡萄均有后证','苏后与卡琳互保、仍控紫葡萄有后证').replace('[987,988,1202,1459,1503,1596]','[987,988,1202,1503,1596]')
p.write_text(s,encoding='utf-8')
