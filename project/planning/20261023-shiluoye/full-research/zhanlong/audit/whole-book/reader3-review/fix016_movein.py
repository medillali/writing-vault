from revision import revise
from common import A
import json
f=A/'adjudications-local-v01-batch016.json';rows=json.loads(f.read_text(encoding='utf-8'))
r=rows[17];revise(1,16,r['candidate_id'],'movein-318',{'rationale':r['rationale'].replace('156已在室做饭/认错主','156已在室床上睡觉并将夜归主误认色狼')},'定向原文L13791—13799证入住睡觉非做饭，只纠此动作。')
r=rows[19];revise(1,16,r['candidate_id'],'movein-320',{'rationale':r['rationale'].replace('156在实体室做饭/工作室互动证明已入住工作','156在实体室房间床上睡觉、与夜归主及三友互动证明已经入住')},'同一入住证据仅证明睡觉居住，撤做饭动作；等级/合同判断不动。')
