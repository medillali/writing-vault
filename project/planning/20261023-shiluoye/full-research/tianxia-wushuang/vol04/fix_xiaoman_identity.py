"""625回读纠正本卷误加别名；仅改精确人物标题，保留其他字段。"""
from pathlib import Path
import json
D=Path(__file__).resolve().parent
counts={}
for name in ['build_artifacts.py','analysis.json','cards.json','report.md','handoff.md']:
    path=D/name
    text=path.read_text(encoding='utf-8')
    counts[name]=text.count('水云谣／小蛮')
    assert counts[name]==1,(name,counts[name])
    path.write_text(text.replace('水云谣／小蛮','漂亮小蛮／小蛮'),encoding='utf-8')
(D/'identity-correction.json').write_text(json.dumps(dict(status='corrected_draft_identity',
    character_origin_key='src-d8926e2a35f04bcf8139cff0ea516bbd/full-20261025/vol04/character/xiaoman',
    before='水云谣／小蛮',after='漂亮小蛮／小蛮',reason='原625明确刺客漂亮小蛮，误加另一姓名应删除，保留人物与origin_key。',
    evidence=[dict(source_id='src-d8926e2a35f04bcf8139cff0ea516bbd',revision='d819f7d0ecf5a2004a0a434e987569bbe25015422d45e16676af913292346857',
        chapter_id='ch-0625',start_line=53463,end_line=53512,claim_kind='fact')],changed_occurrences=counts,
    formal_upstream_changed=False),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(counts)
