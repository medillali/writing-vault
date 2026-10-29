"""只读估算标准备份体积与文件数，不创建备份或读取小说。"""
import collections
import json
import pathlib
import sys

root = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(root / "distill-novels/scripts"))
from fictionlib.exchange import backup_allowed

vault = root / "writing-vault"
files = [p for p in vault.rglob("*") if p.is_file() and backup_allowed(p.relative_to(vault).as_posix())]
sizes = collections.Counter()
for p in files:
    rel = p.relative_to(vault)
    group = "/".join(rel.parts[:4] if rel.parts[:2] == ("library", "reports") else rel.parts[:2])
    sizes[group] += p.stat().st_size
print(json.dumps({
    "status": "estimate-only-not-backup",
    "files": len(files), "uncompressed_bytes": sum(p.stat().st_size for p in files),
    "groups": dict(collections.Counter(p.relative_to(vault).parts[0] for p in files)),
    "largest_groups": sizes.most_common(12),
}, ensure_ascii=False))
