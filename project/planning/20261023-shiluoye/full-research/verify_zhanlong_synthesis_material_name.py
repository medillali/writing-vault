"""核实世界观稳定组仅修改已实际核源的材料名称。"""
from pathlib import Path
import hashlib, json
B = Path(__file__).resolve().parent
P = B / 'zhanlong/audit/whole-book/reader3-review'
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
old = P / 'synthesis-worldbuilding-before-material-delta.json'
new = P / 'synthesis-worldbuilding.json'
delta = read(P / 'synthesis-worldbuilding-material-delta.json')
assert sha(old) == delta['before_json_sha256'] == '4b3d0b4f78d09a1a5c72be59f4ff69a4a9f10879603880045fca2606c3482646'
assert sha(new) == delta['after_json_sha256'] == 'a5ca756dc0eb69f74411757cbb46a41c7b5f0cba3906697ad2dc36e4d522d7f8'
expected = read(old)
before = expected['rows'][1]['fact_summary']
assert before.count('百炼铁') == 1
expected['rows'][1]['fact_summary'] = before.replace('百炼铁', '100份麒麟铁')
assert expected == read(new) and len(delta['changes']) == 1
oldmd = P / 'synthesis-worldbuilding-before-material-delta.md'
newmd = P / 'synthesis-worldbuilding.md'
assert sha(oldmd) == delta['before_md_sha256']
intermediate = P / 'synthesis-worldbuilding-before-md-newline-repair.md.source.txt'
if intermediate.exists():
    assert sha(intermediate) == delta['after_md_sha256']
    assert newmd.read_bytes() == oldmd.read_bytes().replace('百炼铁'.encode(), '100份麒麟铁'.encode())
else:
    assert sha(newmd) == delta['after_md_sha256']
assert oldmd.read_text(encoding='utf-8').replace('百炼铁', '100份麒麟铁') == newmd.read_text(encoding='utf-8')
print(json.dumps(dict(status='exact-one-approved-fact-summary-delta', other_three_rows_unchanged=True, source_limited_rereads=['257 L22394—22418','258 L22424—22449'], semantic_reading_created=False), ensure_ascii=False))
