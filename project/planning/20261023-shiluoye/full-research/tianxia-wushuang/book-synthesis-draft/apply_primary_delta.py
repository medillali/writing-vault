import json
from pathlib import Path
P=Path(__file__).parent;p=P/'final-seed.json';a=json.loads(p.read_text(encoding='utf-8'));delta=[]
def replace(d,i,field,old,new):
 r=a[d][i];assert old in r[field],(d,i,field,old)
 r[field]=r[field].replace(old,new);delta.append(dict(dimension=d,index_zero_based=i,field=field,before=old,after=new))
replace('worldbuilding',3,'fact','英雄君主死却未能保持城权','杀英雄君主未带来英雄城征服；终战征服四城为青土、七星、泰坦、灼热，英雄城未征服')
age='董欣然17岁/下月18与产权理解不足不被游戏NPC强度抹掉；'
replace('characters',2,'limits',age,'')
a['characters'][3]['limits']+=' '+age.rstrip('；')+'。'
delta.append(dict(dimension='characters',index_zero_based=3,field='limits',after='移入董欣然17岁/下月18与产权理解不足之限制；原群像引用已包含卷八characters02支持。'))
assert a['characters'][2]['fact'].endswith('；');a['characters'][2]['fact']=a['characters'][2]['fact'][:-1]+'。'
delta.append(dict(dimension='characters',index_zero_based=2,field='fact',after='末尾分号改句号。'))
tail=' 再以实际执行和状态变化检验，保不能被同一动作解决的残余。'
assert sum(tail in r['mechanism'] for rows in a.values() for r in rows)==36
for rows in a.values():
 for r in rows:r['mechanism']=r['mechanism'].replace(tail,'')
delta.append(dict(field='all36.mechanism',after='删除相同模板尾句，各保原有独立实质方法。'))
replace('plot',2,'fact','月救援促猛虎改属','月救援促虎豹骑改属')
replace('narrative',0,'fact','1455心对远处听不到的主说爱与1459当面说分受众','1455心然向冰兰谈及爱陆尘的原因，陆尘远处未听、读者已知；1459才向陆尘当面说爱')
replace('pacing',1,'fact','初神三技灰到真学能用','初神三技灰，1462龙晶凝格即激活，1464九转另学狂撞')
replace('dialogue',2,'fact','何陆床亲密被明说无圆房','何艺与陆尘床上亲密被慕容明月打断、未发生性交')
p.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(P/'primary-synthesis-delta-applied.json').write_text(json.dumps(dict(status='primary_feedback_applied_pending_final_sha_review',upstream_inputs_unchanged=True,changes=delta),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(changed_fields=len(delta),mechanism_template_removed=36,upstream_inputs_unchanged=True),ensure_ascii=False))
