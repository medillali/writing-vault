"""仅在主代理完成实际逐项语义阅读后签收稳定研究组，不生成阅读或判断。"""
import datetime
import hashlib
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
book, relative, section, id_field, confirmation = sys.argv[1:]
assert confirmation == '--reviewed'
base = Path(__file__).resolve().parent
root = base.parents[2]
stage = base/book
audit = stage/'audit/whole-book'
path = (audit/relative).resolve()
assert path.is_relative_to(audit.resolve()) and path.suffix == '.json'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
data = read(path)
for name, expected in data.get('formal_input_sha256', {}).items():
    target = (root/name).resolve()
    assert target.is_relative_to(root.resolve()) and sha(target) == expected, name
rows = data[section]
ids = [r[id_field] for r in rows]
assert rows and len(set(ids)) == len(ids)
target = stage/'primary-research-group-review-progress.json'
progress = read(target) if target.exists() else {
    'reviewer': '/root', 'status': 'partial-primary-semantic-review',
    'user_approval': False,
    'limits': '逐项派生研究语义审阅；不冒称主代理独自重读全部原文，不等整书验收或用户审美批准。',
    'groups': []}
groups = [g for g in progress['groups'] if g['path'] != relative]
other = {i for g in groups for i in g['reviewed_ids']}
assert not other.intersection(ids), '跨组ID重复'
groups.append({'path': relative, 'section': section, 'id_field': id_field,
               'sha256': sha(path), 'count': len(ids), 'reviewed_ids': ids,
               'reviewed_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'formal_input_pins_verified': len(data.get('formal_input_sha256', {}))})
progress['groups'] = groups
target.write_text(json.dumps(progress, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps({'groups': len(groups), 'reviewed_research_items': sum(g['count'] for g in groups),
                  'signed_sha256': sha(path)}, ensure_ascii=False))
