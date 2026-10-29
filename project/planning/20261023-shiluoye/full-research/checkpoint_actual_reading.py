"""将真实逐片阅读检查点汇入单独的实读run，不提前标分卷研究完成。"""
import collections
import json
import pathlib
import runpy
import sys

base = pathlib.Path(__file__).resolve().parent
root = base.parents[2]
sys.path.insert(0, str(root / "distill-novels/scripts"))
from fictionlib.vault import Vault

sys.stdout.reconfigure(encoding="utf-8")
slug = sys.argv[1]
source = json.loads((base / slug / "source.json").read_text(encoding="utf-8"))
chapters = {c["chapter_id"]: c for c in source["chapters"]}
done = set()
readers = collections.Counter()
finished_volumes = []
canonical_notes = {}
for spec in source["volumes"]:
    folder = base / slug / ("vol%02d" % spec["volume"])
    if not (folder / "reader-state.json").is_file() or not (folder / "chapter-notes.jsonl").is_file():
        continue
    state = json.loads((folder / "reader-state.json").read_text(encoding="utf-8"))
    assert state["source_id"] == source["source_id"] and state["revision"] == source["revision"]
    notes = [json.loads(line) for line in (folder / "chapter-notes.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    by_id = {n["chapter_id"]: n for n in notes}
    canonical_notes.update(by_id)
    assert len(by_id) == len(notes)
    # 保存者可能刚写完notes而尚未更新state；只采用两者共同确认的部分。
    confirmed = set(state.get("completed_chapter_ids", state.get("read_chapter_ids", [])))
    expected = {s["chapter_id"] for u in spec["units"] for s in u["segments"]}
    assert confirmed.issubset(expected) and confirmed.issubset(by_id)
    for cid in confirmed:
        row, chapter = by_id[cid], chapters[cid]
        assert row["full_text_read"] is True and (row["start_line"], row["end_line"]) == (chapter["start_line"], chapter["end_line"])
        assert cid not in done
        done.add(cid)
        readers[row.get("reader", state.get("reader", "not-recorded"))] += 1
    if confirmed == expected:
        finished_volumes.append(spec["volume"])
# 新书分工后的primary隔离尾段：尚未合卷也可记真实实读，合卷后逐值核对并去重。
for folder in sorted((base / slug).glob('primary-vol*-tail')):
    statepath, notepath = folder/'reader-state.json', folder/'chapter-notes.jsonl'
    if not statepath.exists() or not notepath.exists():
        continue
    state=json.loads(statepath.read_text(encoding='utf-8'))
    assert state['source_id']==source['source_id'] and state['revision']==source['revision']
    rows=[json.loads(line) for line in notepath.read_text(encoding='utf-8').splitlines() if line.strip()]
    by_id={r['chapter_id']:r for r in rows}
    assert len(rows)==len(by_id)
    confirmed=set(state['completed_chapter_ids']);assert confirmed.issubset(by_id)
    a,z=state['assigned_raw_range']
    for cid in confirmed:
        row,c=by_id[cid],chapters[cid]
        assert a<=int(cid[3:])<=z and row['reader']=='primary' and row['full_text_read'] is True
        assert (row['start_line'],row['end_line'])==(c['start_line'],c['end_line'])
        if cid in done:
            assert canonical_notes[cid]==row,'合卷后的primary原始笔记须保逐值，不重复计覆盖'
            continue
        done.add(cid);readers['primary']+=1
finished_volumes=[spec['volume'] for spec in source['volumes'] if {s['chapter_id'] for u in spec['units'] for s in u['segments']}.issubset(done)]
supplement = base / slug / "supplementary-read-log.json"
if supplement.is_file():
    extra = json.loads(supplement.read_text(encoding="utf-8"))
    assert extra["source_id"] == source["source_id"] and extra["revision"] == source["revision"]
    for row in extra["chapters"]:
        cid = row["chapter_id"]
        chapter = chapters[cid]
        assert cid not in done and row["full_text_read"] is True
        assert (row["start_line"], row["end_line"]) == (chapter["start_line"], chapter["end_line"])
        done.add(cid)
        readers[row.get("reader", "not-recorded")] += 1
body = [u for spec in source["volumes"] for u in spec["units"] if u["kind"] in ["body", "prologue"]]
body_done = sum(set(u["segment_ids"]).issubset(done) for u in body)
run = {
    "run_id": "run-read-" + slug + "-20261025", "source_id": source["source_id"], "source_revision": source["revision"],
    "state": "actual-reading-in-progress", "completed_chapters": sorted(done),
    "pending_chapters": [c for c in chapters if c not in done], "completed_volumes": finished_volumes,
    "assets": [], "reader_counts_by_segment": dict(readers), "body_units_read": body_done,
    "formal_research_complete": False,
    "notes": "仅汇总实际全文阅读日志与逐片笔记，不证明本卷九维/卡片/图已审查入库。正式分卷研究以run-deep及整书验收为准；不同读者归属保留，不冒认单人全文。",
}
Vault(root / "writing-vault").checkpoint(run)
runpy.run_path(str(root / "writing-vault/library/reports/collection/rebuild_catalog.py"), run_name="__main__")
print(json.dumps({"book": slug, "actual_body_read": body_done, "body_total": len(body), "segments_read": len(done), "fully_read_volumes": finished_volumes, "reader_counts": dict(readers), "research_complete": False}, ensure_ascii=False))
