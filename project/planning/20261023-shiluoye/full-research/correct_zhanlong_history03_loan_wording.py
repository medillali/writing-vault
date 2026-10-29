"""原文743实读后精确区分628取得战膝与743借抹，不改其他终评。"""
from pathlib import Path
import json,copy
P=Path(__file__).parent/'zhanlong/audit/whole-book';p=P/'adjudications-history-v03-batch001.json';rows=json.loads(p.read_text(encoding='utf-8'))
r=next(x for x in rows if x['candidate_id']=='v03-question-v03-q-physical-items');before=copy.deepcopy(r)
assert '628借执戟膝、648其他分装' in r['rationale']
r['rationale']=r['rationale'].replace('628借执戟膝、648其他分装','628取得执戟膝、743借抹、648其他分装')
backup=P/'history-v03-loan-wording-before.json';assert not backup.exists();backup.write_bytes(p.read_bytes())
p.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(P/'history-v03-loan-wording-delta.json').write_text(json.dumps({'reviewer':'primary','source_verification':'root实际全文重读743 L58114—58186，58160取下自己装备战膝借抹；628是取得时点，不是借用。','before':before,'after':r,'remaining_objects_unchanged':True},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
