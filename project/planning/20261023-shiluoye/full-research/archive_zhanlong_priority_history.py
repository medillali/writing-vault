"""保留已签专题引用的旧优先层，签名对象及其原指纹不变。"""
from pathlib import Path
import hashlib, json
B = Path(__file__).resolve().parent
R = B.parents[2]
A = B / 'zhanlong/audit/whole-book'
F = R / 'writing-vault/library/reports/zhanlong/audit/material-history'
digest = 'a60be7a55b50f2ed5eebdedab3902163a816e50d7a14ae057db68204fdaf8109'
source = A / 'priority-corrections-before-yan-recommendation.json'
assert hashlib.sha256(source.read_bytes()).hexdigest() == digest
data = json.loads(source.read_text(encoding='utf-8'))
assert len(data['affected_fields']) == 97 and len(data['issues']) == 5
F.mkdir(parents=True, exist_ok=True)
dest = F / (digest + '.json')
if dest.exists():
    assert dest.read_bytes() == source.read_bytes()
else:
    dest.write_bytes(source.read_bytes())
manifest = dict(schema_version=1, purpose='按原资料路径和原SHA解析已签研究的历史材料；不改写原签名或用新层倒填旧审阅。',
                materials=[dict(original_path=(A / 'priority-corrections-delta.json').relative_to(R).as_posix(),
                                original_sha256=digest, archive_path=dest.relative_to(R).as_posix(),
                                archived_sha256=digest, cause='燕荐对象新增第六问题后，24专题仍引用已审阅的97字段版本。')])
mp = F / 'manifest.json'
if mp.exists():
    assert json.loads(mp.read_text(encoding='utf-8')) == manifest
else:
    mp.write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
assert hashlib.sha256(dest.read_bytes()).hexdigest() == digest
print(json.dumps(dict(status='historical-material-byte-exact', material_sha256=digest,
                      archive_path=dest.relative_to(R).as_posix(), signed_findings_changed=False), ensure_ascii=False))
