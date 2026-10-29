from synthesis_common import *
import copy
p=P/'synthesis-continuity.json';a=json.loads(p.read_text(encoding='utf-8'));before=copy.deepcopy(a['rows'][0]);after=copy.deepcopy(before)
assert after['fact_summary'].count('后期镇国刀用于求援')==1
after['fact_summary']=after['fact_summary'].replace('后期镇国刀用于求援','末期命人取镇国刀求援')
ss=after['supporting_observations'];i=next(i for i,s in enumerate(ss) if s['volume']==3)
boundary={'claim_kind':'fact','text':'740公告十小时内为争夺期；743尚余9小时17分即交抹茶，抹茶已实装并开盾技，不是等满十小时才转手。最终保满与无追杀状态另依749判断；原reported_fact保冻结字面。','evidence':[ref(740,57970,57980),ref(743,58114,58186),ref(749)]}
assert 'reported_fact_boundary' not in ss[i];ss[i]['reported_fact_boundary']=boundary
after['priority_corrections'].append({'path':'writing-vault/library/reports/zhanlong/audit/priority-corrections-lion-shield.json','sha256':sha(F/'audit/priority-corrections-lion-shield.json'),'application':'狮盾期间交付/实用与最后保满分开；原内字不可误改后。'})
out={'status':'proposal-only-awaiting-primary','input_sha256':sha(p),'file':str(p.relative_to(ROOT)).replace('\\','/'),'row_id':before['id'],'before':before,'after':after,'changed_fields':['/rows/0/fact_summary',f'/rows/0/supporting_observations/{i}/reported_fact_boundary','/rows/0/priority_corrections/-'],'evidence':[ref(1384,99517,99520),ref(1385,99614,99620)]+boundary['evidence'],'other_rows_unchanged':[1,2,3],'other_fields_unchanged':True}
dump(P/'synthesis-continuity-two-boundaries-proposal.json',out);print(sha(P/'synthesis-continuity-two-boundaries-proposal.json'))
