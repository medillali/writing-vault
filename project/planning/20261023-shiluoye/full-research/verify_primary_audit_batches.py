"""只核已签批次的完整性与候选覆盖，不代替逐项文学主审。"""
from pathlib import Path
from collections import Counter
import hashlib, json, sys

sys.stdout.reconfigure(encoding="utf-8")
book = Path(__file__).parent / sys.argv[1]
audit = book / "audit/whole-book"
progress = json.loads((book / "primary-audit-review-progress.json").read_text(encoding="utf-8"))
pools = {
    name: json.loads((audit / f"{name}-question-pool.json").read_text(encoding="utf-8"))["candidates"]
    for name in ("historical", "local")
}
seen = []
for group in progress["batches"]:
    path = audit / group["path"]
    assert hashlib.sha256(path.read_bytes()).hexdigest() == group["sha256"], str(path)
    rows = json.loads(path.read_text(encoding="utf-8"))
    ids = [row["candidate_id"] for row in rows]
    assert ids == group["candidate_ids"] and len(ids) == group["count"], str(path)
    assert all(row["status"] in ("answered", "partial", "unknown", "unrecovered") and row["rationale"] for row in rows)
    seen.extend(ids)
assert all(count == 1 for count in Counter(seen).values()), "已签批次发生重叠"
assert sorted(seen) == progress["distinct_reviewed_candidate_ids"]
assert len(seen) == progress["distinct_reviewed_candidates"]
pool_ids = {name: {row["candidate_id"] for row in rows} for name, rows in pools.items()}
assert not pool_ids["historical"] & pool_ids["local"]
assert set(seen) <= set.union(*pool_ids.values())
result = {
    "status": "partial-reviewed-batches-integrity-passed",
    "batches": len(progress["batches"]),
    "reviewed": len(seen),
    "pool_coverage": {
        name: {"reviewed": len(ids & set(seen)), "total": len(ids)}
        for name, ids in pool_ids.items()
    },
    "limit": "仅核记录SHA/ID一致；不是全书完成或语义正确性的独立证明",
}
print(json.dumps(result, ensure_ascii=False))
