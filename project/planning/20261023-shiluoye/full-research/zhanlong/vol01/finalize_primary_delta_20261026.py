"""为同一定位纠错补205行证；对照before断言不改变其他研究语义。"""
import json,copy,runpy,hashlib
from pathlib import Path
P=Path(__file__).parent;S=P/'before-primary-delta-20261026'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
a=read(P/'analysis.json');old=read(S/'analysis.json')
r=next(r for r in a['dimensions']['continuity'] if r['id']=='v01-continuity-03')
assert not any(e['chapter_id']=='ch-0205' for e in r['evidence'])
e=copy.deepcopy(r['evidence'][5]);e.update(chapter_id='ch-0205',start_line=18164,end_line=18164)
r['evidence'].insert(6,e)
test=copy.deepcopy(a);tr=next(r for r in test['dimensions']['continuity'] if r['id']=='v01-continuity-03')
tr['limits_and_counterevidence']=tr['limits_and_counterevidence'].replace('如205老K','如204老K');tr['evidence'].pop(6)
assert test==old
(P/'analysis.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
b=(P/'build_research.py').read_text(encoding='utf-8');x="[143,144,146,157,180,204,232,233,234,239,241]";y="[143,144,146,157,180,204,205,232,233,234,239,241]"
assert b.count(x)==1;(P/'build_research.py').write_text(b.replace(x,y),encoding='utf-8')
runpy.run_path(str(P/'write_report.py'))
before=(S/'report.md').read_text(encoding='utf-8');after=(P/'report.md').read_text(encoding='utf-8')
expected=before.replace('如204老K','如205老K').replace('ch-0204 L18037—18129；ch-0232','ch-0204 L18037—18129；ch-0205 L18164—18164；ch-0232')
assert after==expected,'报告出现超出两项指定改动'
delta=read(P/'primary-delta-20261026.json');delta['changes'][0]['evidence_added']={'chapter_id':'ch-0205','start_line':18164,'end_line':18164,'claim_kind':'fact'}
delta['core_semantic_equality_except_target']=True
(P/'primary-delta-20261026.json').write_text(json.dumps(delta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
runpy.run_path(str(P/'freeze_preflight.py'))
changes=read(P/'review-changes.json');changes['primary_directed_delta']=delta
(P/'review-changes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('targeted delta validated/frozen; all unrelated core semantics unchanged')
