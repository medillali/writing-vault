"""只在root已完整读完给定四栏派生笔记后记回执，不生成任何阅读内容。"""
import hashlib
import json
import sys
from datetime import datetime, timezone
from check_volume import WORK, read

sys.stdout.reconfigure(encoding="utf-8")
start, end = int(sys.argv[1]), int(sys.argv[2])
assert "--read" in sys.argv and 505 <= start <= end <= 653
folder = WORK / "zhanlong" / "vol03"
for name in ["chapter-notes.jsonl", "read-log.json", "reader-state.json"]:
    snapshot = folder / ("prefix-" + name)
    if not snapshot.exists():
        snapshot.write_bytes((folder / name).read_bytes())
path = folder / "prefix-chapter-notes.jsonl"
assert hashlib.sha256(path.read_bytes()).hexdigest() == "3e7818ff524689dc23e4f1bb9551685922463b663535b329e617f37312f64ad1"
rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
selected = [row for row in rows if start <= int(row["chapter_id"][3:]) <= end]
assert len(selected) == end - start + 1
progress_path = folder / "primary-prefix-derived-reading-progress.json"
progress = read(progress_path) if progress_path.exists() else {
    "reader": "primary", "method": "逐批完整阅读前段四栏研究笔记及独立源异常；仅派生阅读，不冒个人原文覆盖。",
    "source_notes_sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "batches": [], "complete_prefix_derived_reading": False
}
batch = {"raw_range": [start, end], "chapter_ids": [r["chapter_id"] for r in selected], "rows": len(selected), "read_at": datetime.now(timezone.utc).isoformat(), "all_four_fields_read": True, "notes_sha256": hashlib.sha256(json.dumps(selected, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()}
assert not any(set(batch["chapter_ids"]) & set(old["chapter_ids"]) for old in progress["batches"]), "已记范围不可重复签收"
progress["batches"].append(batch)
ids = sorted(cid for b in progress["batches"] for cid in b["chapter_ids"])
progress["read_chapter_ids"] = ids
progress["complete_prefix_derived_reading"] = ids == [f"ch-{n:04d}" for n in range(505, 654)]
progress_path.write_text(json.dumps(progress, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
extras = [{"chapter_id": row["chapter_id"], "source_anomalies": row["source_anomalies"]} for row in selected if row.get("source_anomalies")]
print(json.dumps({"new_rows": len(selected), "total_derived_rows": len(ids), "complete_prefix_derived_reading": progress["complete_prefix_derived_reading"], "extra_source_anomalies": extras}, ensure_ascii=False))
