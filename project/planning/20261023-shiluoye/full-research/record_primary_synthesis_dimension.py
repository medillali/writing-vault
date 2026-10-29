"""实际读完稳定维度组后记录签收；与人物/重点签表分开。"""
from pathlib import Path
import datetime, hashlib, json, sys
B = Path(__file__).resolve().parent
R = B.parents[2]
book, relative, confirmation = sys.argv[1:]
assert book == 'zhanlong' and confirmation == '--reviewed'
S = B / book
A = S / 'audit/whole-book'
path = (A / relative).resolve()
assert path.is_relative_to(A.resolve()) and path.suffix == '.json'
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
data = read(path)
dim = data['dimension']
dimensions = set(read(R / 'writing-vault/library/reports/zhanlong/vol01-analysis.json')['dimensions'])
assert len(dimensions) == 9 and dim in dimensions
rows = data['rows']
assert len(rows) == 4 and len({r['id'] for r in rows}) == 4
for row in rows:
    assert row['claim_kind'] == 'synthesis' and row['review_status'] == 'draft'
    assert all(row[k] for k in ['claim','fact_summary','mechanism','conditions','limits_and_counterevidence','originality_transform','late_stage_result'])
    for obs in row['supporting_observations']:
        material = (R / obs['material_path']).resolve()
        assert material.is_relative_to(R) and sha(material) == obs['material_sha256']
        original = read(material)
        for part in obs['json_pointer'].strip('/').split('/'):
            original = original[int(part)] if isinstance(original,list) else original[part]
    for correction in row.get('priority_corrections', []):
        assert sha(R / correction['path']) == correction['sha256']
dest = S / 'primary-synthesis-dimension-reviews.json'
progress = read(dest) if dest.exists() else dict(reviewer='primary', user_approval=False,
    scope='各稳定维度组的全部顶层文学字段与继承事实解释已实际阅读；完整原文归各卷实际读者，哈希校验不产生阅读。', groups=[])
assert not any(g['dimension'] == dim for g in progress['groups']), '已签维度不静默重签，需先保存旧签表与批准delta'
progress['groups'].append(dict(dimension=dim, path=relative, sha256=sha(path),
    reviewed_ids=[r['id'] for r in rows], count=4, reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat()))
dest.write_text(json.dumps(progress, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps(dict(reviewed_dimensions=len(progress['groups']), reviewed_observations=sum(g['count'] for g in progress['groups']),
                     whole_book_reviewed=False, signed_group_sha256=sha(path)), ensure_ascii=False))
