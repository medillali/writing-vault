"""将已实际执行的串行验证结果记入本卷草稿，不操作Vault。"""
import json,hashlib
from pathlib import Path
P=Path(__file__).parent
v=json.loads((P/'validation.json').read_text(encoding='utf-8'))
v.update(preflight='passed',vault_validation='passed_check_volume_serial',literary_review='primary_full_reviewed_delta_submitted_user_unapproved',review_changes='review-changes.md')
v['checks']+=['find_thread_outside无越成员输出','check_volume完整Vault证据与图校验通过；2956引用']
v['limitations']=['文学解释与风格取舍仍draft，未由用户批准','正式导入与最终SHA冻结由主代理执行；子代理不写正式库']
v['sha256']={n:hashlib.sha256((P/n).read_bytes()).hexdigest() for n in ['analysis.json','cards.json','graph.json','report.md','handoff.md','read-log.json','chapter-notes.jsonl','reader-state.json']}
(P/'validation.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'preflight':v['preflight'],'sha256':{n:v['sha256'][n] for n in ['analysis.json','cards.json','graph.json','report.md','handoff.md','read-log.json']}},ensure_ascii=False))
