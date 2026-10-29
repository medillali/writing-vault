"""核对主审八项后的1380单一后证追加，不产生语义审阅声明。"""
from pathlib import Path
import copy, hashlib, json
B = Path(__file__).parent
A = B / 'zhanlong/audit/whole-book'
P = A / 'local-v02-v05-review'
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
old, cur = P / 'focus01-before-1380-evidence.json', A / 'focused-findings-part01.json'
assert sha(old) == '6ca0b5621e3841473fab98054b6ebc1947c16d8f214c708389a18f27b9fe2d3e'
assert sha(cur) == 'a9981b95aa9da0923d918cd474f899f61f3a432fa8d706c53ef7ad9a99e03e1f'
before, after = read(old), read(cur)
expected = copy.deepcopy(before)
evidence = after['findings'][0]['evidence'][-1]
assert evidence['chapter_id'] == 'ch-1380' and evidence['start_line'] == 99222 and evidence['end_line'] == 99289
assert evidence['access_level'] == 'derived-primary-independent-ending-reread'
expected['findings'][0]['evidence'].append(evidence)
assert expected == after and len(after['findings']) == 8
result = dict(status='exact-approved-single-evidence-addition-verified', other_seven_and_all_literary_fields_unchanged=True,
              after_sha256=sha(cur), semantic_reading_created=False)
(P / 'primary-focus01-delta-verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps(result, ensure_ascii=False))
