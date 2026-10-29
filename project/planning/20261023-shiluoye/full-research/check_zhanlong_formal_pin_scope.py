"""查询已签组的正式依赖是否会错误要求恢复旧暂存目录。"""
from pathlib import Path
import json
B=Path(__file__).resolve().parent;A=B/'zhanlong/audit/whole-book'
progress=json.loads((B/'zhanlong/primary-research-group-review-progress.json').read_text(encoding='utf-8'))
bad=[]
for g in progress['groups']:
    d=json.loads((A/g['path']).read_text(encoding='utf-8'))
    for name in d.get('formal_input_sha256',{}):
        if not name.startswith('writing-vault/'):
            bad.append(dict(group=g['path'],path=name,sha256=d['formal_input_sha256'][name]))
print(json.dumps(dict(signed_groups_checked=len(progress['groups']),nonportable_formal_pins=bad,read_only=True),ensure_ascii=False))
