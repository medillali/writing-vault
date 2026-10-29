"""独立确认人物首组三个待审状态字段修正不改变文学内容。"""
from pathlib import Path
import hashlib, json
B = Path(__file__).resolve().parent
A = B / 'zhanlong/audit/whole-book'
old = A / 'local-v03-v06-review/corrections/character01-schema-status/character-arcs-part01.json'
current = A / 'character-arcs-part01.json'
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(old) == '464201e36fee72f025fb77e01085a2dff4f595db6755ea51e4a8a6cc6b0f9358'
assert sha(current) == '45104f6ccbba93f6703d4bbc0de8b4228b644053ff6fbb621d92fa0d655a26ea'
expected = read(old)
assert len(expected['characters']) == 3
for row in expected['characters']:
    assert row['review_status'] == 'draft_pending_primary'
    row['review_status'] = 'draft'
assert expected == read(current)
assert sha(A / 'character-arcs-part01.md') == '7415e351f17c87b3af03d804b91fa560d99f905053f2b07beaee8c8d82fd21c2'
print(json.dumps(dict(status='exact-three-status-fields-only', literary_objects_actual_read=3, all_other_values_unchanged=True, semantic_reading_created=False)))
