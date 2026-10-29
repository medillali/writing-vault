"""只落实primary指定两项文字定位；保留before，不重跑文学构建器。"""
import json,hashlib,shutil
from pathlib import Path
P=Path(__file__).parent
files=['analysis.json','report.md','handoff.md','build_research.py','validation.json','delivery-freeze.json','review-changes.json']
S=P/'before-primary-delta-20261026'
S.mkdir(exist_ok=True)
for f in files:
    assert not (S/f).exists(), '已有before，禁止重复覆盖'
    shutil.copy2(P/f,S/f)
old='如204老K换斧是归还后证';new='如205老K换斧是归还后证'
for f in ['analysis.json','report.md','build_research.py']:
    t=(P/f).read_text(encoding='utf-8');assert t.count(old)==1
    (P/f).write_text(t.replace(old,new),encoding='utf-8')
t=(P/'handoff.md').read_text(encoding='utf-8');assert t.count('实体官网由原4加薛柔为5')==1
(P/'handoff.md').write_text(t.replace('实体官网由原4加薛柔为5','实体工作室由原4加薛柔为5'),encoding='utf-8')
a=json.loads((P/'analysis.json').read_text(encoding='utf-8'))
for dimension,rows in a['dimensions'].items():
    for r in rows:
        if new in r.get('limits_and_counterevidence',''):
            print(json.dumps({'dimension':dimension,'row_id':r.get('id'),'evidence_chapters':[e['chapter_id'] for e in r.get('evidence',[])]},ensure_ascii=False))
delta={'scope':'primary指定两项，不改逐章原notes/其他文学语义','changes':[{'files':['analysis.json','report.md','build_research.py'],'before':old,'after':new,'verification':'本代理2026-10-26定向全文复读raw0205 BEGIN-END L18130—18216；L18164明确冉闵换了一把战斧；204掉落/李牧拾与205换斧分别保留。该定向复读不新增原全量覆盖或改primary reader归属。'},{'files':['handoff.md'],'before':'实体官网由原4加薛柔为5','after':'实体工作室由原4加薛柔为5','verification':'按primary指定纠正用词，不改人数和住处归属。'}],'before_directory':str(S),'semantic_other_changes':False}
(P/'primary-delta-20261026.json').write_text(json.dumps(delta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('targeted text delta saved')
