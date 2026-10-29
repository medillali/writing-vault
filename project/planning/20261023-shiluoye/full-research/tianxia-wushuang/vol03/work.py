"""仅保存本代理实际全文读完的卷三观察；不生成事实或读取原文。"""
import json
import pathlib
import sys
from datetime import datetime, timezone

sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parent
SOURCE = json.loads((ROOT.parent / "source.json").read_text(encoding="utf-8"))
VOLUME = next(v for v in SOURCE["volumes"] if v["volume"] == 3)
EXPECTED = [s["chapter_id"] for u in VOLUME["units"] for s in u["segments"]]
CHAPTERS = {c["chapter_id"]: c for c in SOURCE["chapters"]}
UNITS = {s["chapter_id"]: u for u in VOLUME["units"] for s in u["segments"]}
READER = "/root/zongheng_vol03_full"

def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def commit(batch_path):
    records = [json.loads(line) for line in (ROOT / "chapter-notes.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    done = [r["chapter_id"] for r in records]
    assert done == EXPECTED[:len(done)], "笔记必须保持实际来源顺序"
    batch = json.loads(pathlib.Path(batch_path).read_text(encoding="utf-8"))
    for observation in batch:
        observation = dict(observation)
        cid = observation["chapter_id"]
        assert cid == EXPECTED[len(records)], f"越界、重复或跳读: {cid}"
        assert observation.pop("model_full_text_read") is True
        for key in ("facts", "inferences", "state_changes", "unresolved"):
            assert isinstance(observation[key], list), key
        chapter = CHAPTERS[cid]
        unit = UNITS[cid]
        records.append({**observation, "source_id": SOURCE["source_id"], "revision": SOURCE["revision"], "reader": READER, "title": chapter["title"], "start_line": chapter["start_line"], "end_line": chapter["end_line"], "unit_id": unit.get("unit_id", unit.get("chapter_id")), "full_text_read": True})
    done = [r["chapter_id"] for r in records]
    done_set = set(done)
    completed_units = [u for u in VOLUME["units"] if all(s["chapter_id"] in done_set for s in u["segments"])]
    # 独立卷标题不计正文；误识别续片并入原正文单元。
    body = [u for u in completed_units if not CHAPTERS[u["segments"][0]["chapter_id"]]["title"].startswith("卷三")]
    complete = len(done) == len(EXPECTED)
    state = json.loads((ROOT / "reader-state.json").read_text(encoding="utf-8"))
    assert state["source_id"] == SOURCE["source_id"] and state["revision"] == SOURCE["revision"]
    state.update(reader=READER, status="read_complete" if complete else "reading", metadata_only=False, reading_authorized=True, read_chapter_ids=done, completed_chapter_ids=done, completed_count=len(done), completed_body_units=len(body), completed_units_including_header=len(completed_units), next_chapter_id=next((c for c in EXPECTED if c not in done_set), None), pending_chapter_ids=[c for c in EXPECTED if c not in done_set], pending_truncations=[], unresolved_truncations=[], complete_volume=complete, complete_book=False, updated_at=datetime.now(timezone.utc).isoformat(), note="已获主代理明确启动授权；仅记录本代理逐片实际全文阅读。研究产物仍为待审草稿。")
    log = json.loads((ROOT / "read-log.json").read_text(encoding="utf-8"))
    log.update(status=state["status"], metadata_only=False, complete=complete, complete_volume=complete, complete_book=False, reader=READER, body_unit_count=376, total_units_including_header=377, completed_body_units=len(body), assigned_segment_count=378, chapters=[{k: r[k] for k in ("chapter_id", "title", "start_line", "end_line", "reader", "full_text_read", "unit_id")} for r in records], method="本代理按raw顺序逐片全文阅读，逐批核BEGIN/END；0398/0399为同一正文的两个证据片段，卷标题另计。")
    (ROOT / "chapter-notes.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records), encoding="utf-8")
    write(ROOT / "reader-state.json", state)
    write(ROOT / "read-log.json", log)
    assignment = json.loads((ROOT / "assignment.json").read_text(encoding="utf-8"))
    assignment.update(status=state["status"], reading_authorized=True, start_gate="2026-10-25 主代理确认纵横正式验收、catalog已切无双后明确授权。")
    write(ROOT / "assignment.json", assignment)
    print(json.dumps({"segments":len(done),"body_units":len(body),"total_body":376,"next":state["next_chapter_id"],"complete":complete}, ensure_ascii=False))

if __name__ == "__main__":
    assert len(sys.argv) == 3 and sys.argv[1] == "commit"
    commit(sys.argv[2])
