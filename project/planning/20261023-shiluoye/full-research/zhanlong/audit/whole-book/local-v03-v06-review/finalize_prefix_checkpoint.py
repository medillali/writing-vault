"""保存本代理200项分工检查点，不改变已交批和原输入。"""
from pathlib import Path
import json,hashlib,datetime
H=Path(__file__).resolve().parent
p=H/'review-state.json';s=json.loads(p.read_text(encoding='utf-8'))
s['volumes']['6'].update(assigned=200,original_assignment_count=399,next_candidate_index=None,status='owned_prefix_complete_pending_primary_remainder_review',remaining_tail_owner='zongheng_vol04_full',tail_scope='0-based[200:399]')
s['next_task']='按primary授权转人物全弧/终态稳定分组，正式输入SHA另存'
s['updated_at']=datetime.datetime.now(datetime.timezone.utc).isoformat();p.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
r=json.loads((H/'volume06-aggregate-validation.json').read_text(encoding='utf-8'))
md=['# 卷六本地候选前200项交接','','仅本代理所分0-based[0:200]，10批200项；reader4独占余199，未宣本人终评全399。','','人工结论统计：125 answered / 50 partial / 24 unknown / 1 unrecovered。answered含证据范围/研究约束关闭，不等125个剧情承诺全成功。','','主池SHA与原记录逐值、固定SID/rev/章行界、准确ID次序均通过。机械验证不代primary逐项语义主审；当前已签状态以root主审收据为准。','','原卷三149片/卷六207片首次全文归本代理；卷三尾100归primary。当前终评引用其他卷以派生接读/定向原文另标，不冒全书个人原文重读。','','## 当前批SHA','']
md += [f'- {k}: {v}' for k,v in r['batch_sha256'].items()]
md += ['','## 显式纠正','','- b007旧武魂关键词漏配1240/41炼魂，已按primary批准4项最小改，root再将2个domain名校齐并签88be5c；旧字节/before/after均保。','- 燕荐对象误写三字段由root正式外置priority，不改冻结notes；终评006已用荐燕→1234代理→1244正式。','- 正式优先层和原阶段不互相抹写。','','随后转人物全弧，分组交即冻结，总稿最后与分组逐值相同。']
(H/'VOL06-PREFIX-HANDOFF.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
for n in ['volume06-aggregate-validation.json','VOL06-PREFIX-HANDOFF.md']:
 print(n,hashlib.sha256((H/n).read_bytes()).hexdigest())
