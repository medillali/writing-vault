"""补齐新分工交接的正式支持文件，不重复保存卡片或改读者归属。"""
import hashlib
from check_volume import ROOT, WORK, read

source = WORK / "zhanlong" / "vol01"
dest = ROOT / "writing-vault" / "library" / "reports" / "zhanlong"
prefix = source / "PREFIX-HANDOFF.md"
assert prefix.is_file()
target = dest / "vol01-PREFIX-HANDOFF.md"
target.write_bytes(prefix.read_bytes())
handoff = dest / "vol01-handoff.md"
text = handoff.read_text(encoding="utf-8")
assert "(PREFIX-HANDOFF.md)" in text
handoff.write_text(text.replace("(PREFIX-HANDOFF.md)", "(vol01-PREFIX-HANDOFF.md)"), encoding="utf-8")
delta = source / "primary-delta-20261026.json"
(dest / "vol01-primary-delta-20261026.json").write_bytes(delta.read_bytes())
assert hashlib.sha256(target.read_bytes()).digest() == hashlib.sha256(prefix.read_bytes()).digest()
print("补齐卷一前段交接和主审delta；未重新保存卡片、图或原阅读记录。")
