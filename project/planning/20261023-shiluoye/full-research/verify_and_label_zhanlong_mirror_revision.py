"""重放四项获批后证修订，并使两个分类标签与已审理由一致。"""
from pathlib import Path
import copy, hashlib, json
B = Path(__file__).resolve().parent
A = B / 'zhanlong/audit/whole-book'
P = A / 'local-v03-v06-review'
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
old = P / 'corrections/batch007-approved-mirror-and-source/adjudications-local-v06-batch007.json'
current = A / 'adjudications-local-v06-batch007.json'
delta = read(P / 'batch007-approved-delta.json')
assert sha(old) == delta['before_sha256'] == '5b1141b9e02e28e76521c71fe3588f7a7d52e853d96bc99b7e85cea8c8bffb9b'
assert sha(current) == delta['after_sha256'] == '51e9a14a7fea7f688fe5d10aee3c9583c835c6c0b02f2822c134065a01c95d5c'
expected = read(old)
assert len(delta['changes']) == 4
for change in delta['changes']:
    row = next(r for r in expected if r['candidate_id'] == change['candidate_id'])
    assert set(change['fields']) == set(change['before']) == set(change['after'])
    for key in change['fields']:
        assert row[key] == change['before'][key]
        row[key] = copy.deepcopy(change['after'][key])
assert expected == read(current) and len(expected) == 20
revisions = [
    ('v06-local-chapter_unresolved_index-0028-01', 'rescued-survivors-and-unrealized-mirror-army', 'rescued-survivors-and-unitemized-return-roster'),
    ('v06-local-chapter_unresolved_index-0031-01', 'person-recovered-but-mirror-threat-unseen', 'person-recovered-and-mirror-battle-realized'),
]
snapshot = P / 'batch007-before-primary-domain-alignment.json'
assert not snapshot.exists()
snapshot.write_bytes(current.read_bytes())
changes = []
for cid, before, after in revisions:
    row = next(r for r in expected if r['candidate_id'] == cid)
    assert row['audit_domain'] == before
    row['audit_domain'] = after
    changes.append(dict(candidate_id=cid, field='audit_domain', before=before, after=after))
current.write_text(json.dumps(expected, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
report = dict(status='exact-four-approved-deltas-verified-and-two-domain-labels-aligned',
              primary_full_batch_reread=20, four_changed_objects_exact=True, other_16_unchanged=True,
              previous_sha256=sha(snapshot), current_sha256=sha(current), changes=changes,
              boundary='仅将仍称未成军的分类标签与已核实的炼魂实战理由对齐，不改status/理由/来源/其他字段。')
(P / 'primary-batch007-final-revision.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
