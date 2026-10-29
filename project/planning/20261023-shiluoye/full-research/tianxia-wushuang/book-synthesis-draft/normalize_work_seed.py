import json
from pathlib import Path
P=Path(__file__).parent
R=lambda n:json.loads((P/n).read_text(encoding='utf-8'))
a=R('extended-seed-work.json');base=R('synthesis-seed.json')
for d,rows in a['dimensions'].items():
 for i,row in enumerate(rows):
  old=base[d][i]['fact'].replace('前五卷','前中段')
  remainder=row['fact'][len(old):].strip();eight,six=remainder.split(' 卷六：',1)
  row['phase_updates']={'6':six,'8':eight}
  row['fact']=old+' 卷六：'+six+' 卷八：'+eight
(P/'extended-seed-work.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
state=dict(status='working_final_synthesis_waiting_volume7_complete_package',partial_original_preserved=True,partial_original_included_volumes=[1,2,3,4,5],completed_stage_material_read=[1,2,3,4,5,6,8],pending_stage_material_read=[7],final_bookroot_files_created=False,observations_in_working_seed=36,formal_analysis_dimensions_equal_to_read_stage=[1,2,3,4,5,6],personal_complete_book_read=False,remaining=['卷七整包冻结后完整阅读其九维/交接','依七更新36条后段检验与适用边界','选择正式1—8或明确已审冻结暂存依赖并校验SHA','生成book根兼容JSON/MD，本地验证，交primary实际语义审签'])
(P/'completion-state.json').write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(state,ensure_ascii=False))
