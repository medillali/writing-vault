"""保留重复换行版，用原MD字节只改获批材料词，避免Windows二次换行翻译。"""
from pathlib import Path
import hashlib, json
B = Path(__file__).resolve().parent
P = B / 'zhanlong/audit/whole-book/reader3-review'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
original = P / 'synthesis-worldbuilding-before-material-delta.md'
current = P / 'synthesis-worldbuilding.md'
intermediate = P / 'synthesis-worldbuilding-before-md-newline-repair.md.source.txt'
assert sha(original) == '96f05e531a629731852b9961d1e9ffff1f139e481a54dc95f5ae7cf74d965b17'
assert sha(current) == '0e96db877c788f241bafc4b2e48a3bd3c1e1cfb5924fb7f88a7624bcc1372bb2'
assert not intermediate.exists()
expected = original.read_bytes().replace('百炼铁'.encode(), '100份麒麟铁'.encode())
# 实际诊断：每个原CRLF被写成CRCRLF；排除此序列后只有已批准的词替换。
assert current.read_bytes().replace(b'\r\r\n', b'\r\n') == expected
intermediate.write_bytes(current.read_bytes())
current.write_bytes(expected)
report = dict(status='exact-approved-word-replacement-and-newline-repair',
              original_sha256=sha(original), intermediate_sha256=sha(intermediate), final_sha256=sha(current),
              literary_changes_beyond_approved_material_name=False,
              json_group_sha256=sha(P / 'synthesis-worldbuilding.json'), signed_json_group_changed=False)
(P / 'primary-worldbuilding-md-newline-repair.json').write_bytes((json.dumps(report, ensure_ascii=False, indent=2)+'\n').encode())
print(json.dumps(report, ensure_ascii=False))
