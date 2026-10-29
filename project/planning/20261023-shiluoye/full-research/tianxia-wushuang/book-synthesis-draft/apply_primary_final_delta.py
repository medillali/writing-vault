import json
from pathlib import Path
P=Path(__file__).parent;p=P/'final-seed.json';a=json.loads(p.read_text(encoding='utf-8'));changes=[]
def fix(d,i,field,old,new):
 assert old in a[d][i][field],(d,i,field)
 a[d][i][field]=a[d][i][field].replace(old,new);changes.append(dict(dimension=d,index_zero_based=i,field=field,before=old,after=new))
fix('themes',2,'fact','返回国籍由制度动作而非战绩自动兑现','恢复游戏中国区玩家资格由制度动作而非战绩自动兑现')
fix('continuity',1,'fact','二队冠军杯','李承风持WEL冠军杯')
fix('continuity',3,'limits','也不提前把前五卷综合称全书结论','范围须依当前正式八卷证据，覆盖不等语义正确')
p.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
d=json.loads((P/'primary-synthesis-delta-applied.json').read_text(encoding='utf-8'));d['changes']+=changes;d['status']='all_primary_requested_semantic_changes_applied_final_sha_pending';d['upstream_inputs_unchanged']=True
(P/'primary-synthesis-delta-applied.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(final_requested_fields=len(changes),all_requested_delta_entries=len(d['changes']),upstream_inputs_unchanged=True),ensure_ascii=False))
