"""显示定位纠错的语义与章界，省去重复的来源字段。"""
from pathlib import Path
import json, sys

sys.stdout.reconfigure(encoding="utf-8")
packet = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
rows=packet.get("delta", [packet])
for row in rows:
    assert row.get("candidate_id") and isinstance(row.get("before"), dict), "未识别纠错格式；不能据空字段计为已读"
    out = {"candidate_id": row.get("candidate_id"), "specific_anchor": row.get("specific_anchor", packet.get("reason"))}
    for key in ("before", "after"):
        value = row.get(key)
        if value is None:
            value = next((v for k,v in row.items() if k != "before" and isinstance(v,dict) and "rationale" in v), {})
        assert value.get("rationale") and "later_chapters" in value, "纠错缺少可审的前后语义"
        out[key] = {
            "rationale": value.get("rationale"),
            "status": value.get("status"),
            "later_chapters": value.get("later_chapters"),
            "later_evidence": [
                {k: e.get(k) for k in ("chapter_id", "start_line", "end_line")}
                for e in value.get("later_evidence", [])
            ],
        }
    print(json.dumps(out, ensure_ascii=False))
print("FULL_DELTAS_READ", len(rows))
