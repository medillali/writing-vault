"""只读定位重点稿输入指纹差异，不改稿或主审凭据。"""
from pathlib import Path
import hashlib, json, sys
B = Path(__file__).parent
R = B.parents[2]
data = json.loads((B / 'zhanlong/audit/whole-book' / sys.argv[1]).read_text(encoding='utf-8'))
coverage = json.loads((R / 'writing-vault/library/reports/zhanlong/audit/full-reading-validation.json').read_text(encoding='utf-8'))
for name, old in data.get('formal_input_sha256', {}).items():
    p = R / name
    current = hashlib.sha256(p.read_bytes()).hexdigest()
    if current != old:
        key = p.relative_to(R / 'writing-vault/library/reports/zhanlong').as_posix()
        print(json.dumps(dict(path=name, expected=old, actual=current,
                              current_full_reading_pin=coverage['formal_input_sha256'].get(key)), ensure_ascii=False))
