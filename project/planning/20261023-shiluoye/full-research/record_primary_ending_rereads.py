"""只校验并登记已手写的结局核读记录，不生成阅读事实或终点评语。"""
import hashlib
import json
import sys
from datetime import datetime, timezone
from check_volume import WORK, read

sys.stdout.reconfigure(encoding="utf-8")
stage = WORK / "zhanlong"
folder = stage / "primary-ending-reread"
source = read(stage / "source.json")
chapters = {c["chapter_id"]: c for c in source["chapters"]}
notes, inputs = [], {}
for path in sorted(folder.glob("batch*.json")):
    data = read(path)
    assert data["source_id"] == source["source_id"] and data["revision"] == source["revision"]
    assert data["reader"] == "primary" and data["complete_book"] is False
    inputs[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    for row in data["notes"]:
        original = chapters[row["chapter_id"]]
        assert row["full_text_read"] is True
        assert (row["start_line"], row["end_line"]) == (original["start_line"], original["end_line"])
        assert len(row["facts"]) >= 2 and row["inferences"] and row["state_changes"] and row["unresolved"]
        notes.append(row)
expected = [f"ch-{n:04d}" for n in range(1375, 1387)]
assert [n["chapter_id"] for n in notes] == expected
receipt = {
    "source_id": source["source_id"], "revision": source["revision"], "reader": "primary",
    "method": "结局12片实际全文独立核读后的手写研究记录；本命令仅校验章界/字段/文件哈希，不替代阅读或判断。",
    "recorded_at": datetime.now(timezone.utc).isoformat(), "chapter_ids": expected,
    "raw_range": [1375, 1386], "chapters": len(notes), "complete_assigned_reread": True,
    "complete_book": False, "count_as_additional_unique_coverage": False,
    "original_first_reader_unchanged": True, "input_sha256": inputs,
    "terminal_boundaries": [
        "鬼城惨败后50万NPC返不足18万、玩家随幕返不足千，不是全军获胜。",
        "傲天战皇仍活；镇天关已建，新版本战争未在本来源结束。",
        "主已交盟主/订婚并进南京队序，西南任务、返回和婚礼仍未演示。",
        "雷沈记忆系统是计划；结尾仅白墨颜数字角色确已在线，非现实复生。"
    ]
}
(folder / "read-log.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"chapters": len(notes), "reread_complete": True, "complete_book": False, "input_files": len(inputs), "receipt": str(folder / "read-log.json")}, ensure_ascii=False))
