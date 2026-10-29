"""压缩重复审计措辞，逐项展示全部独立判断；不替代源文阅读。"""
import json
import pathlib
import sys

sys.stdout.reconfigure(encoding="utf-8")
data = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
for row in data["candidates"][int(sys.argv[2]):int(sys.argv[3])]:
    audit = row["terminal_assessment"]
    result = {
        "id": row["candidate_id"], "item": row["title"],
        "status": audit["status"], "domain": audit.get("audit_domain"),
    }
    rationale = audit.get("rationale", "")
    if not rationale.startswith(("数值、名号、称谓、方位或时钟源文两端不合", "终点仍保此项原认知层级或文本细节")):
        result["decision"] = rationale
    for key, value in audit.items():
        if key not in {"status", "audit_domain", "rationale", "review_progress", "later_evidence", "review_scope_note", "disposition", "terminal_action"}:
            result[key] = value
    if audit.get("later_evidence"):
        result["evidence"] = [e["chapter_id"] for e in audit["later_evidence"]]
    print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))
