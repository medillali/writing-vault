"""机械全收正式分卷问题，保原记录；不生成任何终点语义判断。"""
from pathlib import Path
import hashlib
import json
import re
import sys
from check_volume import ROOT, WORK, read

sys.stdout.reconfigure(encoding="utf-8")
book = "zhanlong"
formal = ROOT / "writing-vault" / "library" / "reports" / book
audit = WORK / book / "audit" / "whole-book"
audit.mkdir(parents=True, exist_ok=True)
historical, local, inputs, originals = [], [], [], []

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def refs(value):
    if isinstance(value, dict):
        if {"source_id", "revision", "chapter_id", "start_line", "end_line"}.issubset(value):
            return [value]
        return [e for child in value.values() for e in refs(child)]
    if isinstance(value, list):
        return [e for child in value for e in refs(child)]
    return []

def title(row):
    if not isinstance(row, dict):
        return str(row)
    return next((str(row[key]) for key in ["question", "description", "detail", "claim", "title", "text", "summary"] if row.get(key)), json.dumps(row, ensure_ascii=False))

def atoms(row, field):
    # 只按明确的中文分号切分，完整原记录另存；切分不是文学解释。
    if isinstance(row, dict) and field in ["chapter_unresolved_index", "chapter_source_anomaly_index"]:
        raw = row.get("unresolved", row.get("original_unresolved", row.get("source_anomalies", [])))
        assert isinstance(raw, list)
    elif isinstance(row, dict):
        raw = [title(row)] + ([row["handling"]] if row.get("handling") else [])
    else:
        raw = [str(row)]
    return [piece.strip() for text in raw for piece in re.split("[；]", text) if piece.strip()]

for volume in range(1, 7):
    ap = formal / f"vol{volume:02d}-analysis.json"
    gp = formal / f"vol{volume:02d}-graph.json"
    if not ap.exists() or not gp.exists():
        inputs.append({"volume": volume, "status": "pending-delivery", "analysis": None, "graph": None})
        continue
    analysis, graph = read(ap), read(gp)
    fields = [name for name in ["open_questions", "unresolved_volume_end"] if name in analysis]
    assert len(fields) == 1, (volume, fields)
    qfield = fields[0]
    questions = analysis[qfield]
    assert isinstance(questions, list)
    inp = {"volume": volume, "status": "formal-library", "analysis": ap.relative_to(ROOT).as_posix(), "graph": gp.relative_to(ROOT).as_posix(), "analysis_sha256": sha(ap), "graph_sha256": sha(gp), "open_questions": len(questions), "open_questions_field": qfield, "graph_threads": len(graph["threads"])}
    inputs.append(inp)
    for index, question in enumerate(questions):
        historical.append({"candidate_id": f"v{volume:02d}-question-" + question.get("id", f"{index+1:03d}"), "volume": volume, "entry_type": "analysis." + qfield, "original_field": qfield, "original_path": inp["analysis"], "original_index": index, "original_stage_status": question.get("status"), "title": title(question), "original_record": question, "original_evidence": refs(question)})
    nodes, edges = {n["id"]: n for n in graph["nodes"]}, {e["id"]: e for e in graph["edges"]}
    for index, thread in enumerate(graph["threads"]):
        evidence = refs(thread) or refs([nodes[n] for n in thread.get("node_ids", [])] + [edges[e] for e in thread.get("edge_ids", [])])
        historical.append({"candidate_id": f"v{volume:02d}-thread-" + thread["id"], "volume": volume, "entry_type": "graph.threads", "original_field": "threads", "original_path": inp["graph"], "original_index": index, "original_stage_status": thread["status"], "title": thread["title"], "original_record": thread, "original_evidence": evidence})
    for field in ["source_anomalies", "unresolved_and_anomalies", "unresolved_and_source_issues", "anomalies", "chapter_unresolved_index", "chapter_source_anomaly_index"]:
        if field not in analysis:
            continue
        rows = analysis[field]
        assert isinstance(rows, list), (volume, field)
        empty_indices = []
        originals.append({"volume": volume, "field": field, "path": inp["analysis"], "original_records": rows, "empty_record_indices": empty_indices})
        for index, row in enumerate(rows):
            texts = atoms(row, field)
            if not texts:
                assert field in ["chapter_unresolved_index", "chapter_source_anomaly_index"] and isinstance(row, dict)
                assert row.get("unresolved", row.get("original_unresolved", row.get("source_anomalies", None))) == []
                empty_indices.append(index)
                continue
            for atomic_index, text in enumerate(texts):
                local.append({"candidate_id": f"v{volume:02d}-local-{field}-{index+1:04d}-{atomic_index+1:02d}", "volume": volume, "entry_type": "local-atomic-item", "original_path": inp["analysis"], "original_field": field, "original_index": index, "atomic_index": atomic_index, "original_record": row, "title": text, "original_evidence": refs(row)})
    # 笔记所有非空unresolved必须在索引原串逐项保留，且reader不被组装者替换。
    notes = [json.loads(line) for line in (formal / f"vol{volume:02d}-chapter-notes.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    actual = {n["chapter_id"]: (n["reader"], n["unresolved"]) for n in notes if n.get("unresolved")}
    indexed = {n["chapter_id"]: (n["reader"], n.get("unresolved", n.get("original_unresolved"))) for n in analysis["chapter_unresolved_index"] if n.get("unresolved", n.get("original_unresolved"))}
    assert actual == indexed, (volume, "原未明串或读者归属丢失")

pending = [row["volume"] for row in inputs if row["status"] != "formal-library"]
for name, rows in [("historical", historical), ("local", local)]:
    path = audit / f"{name}-question-pool.json"
    old = {row["candidate_id"]: row for row in read(path)["candidates"]} if path.exists() else {}
    assert len({row["candidate_id"] for row in rows}) == len(rows)
    for row in rows:
        previous = old.get(row["candidate_id"])
        if previous:
            assert {k: v for k, v in previous.items() if k != "terminal_assessment"} == row, "已建候选输入变化，不能覆盖旧判定"
            row["terminal_assessment"] = previous["terminal_assessment"]
            if row["terminal_assessment"].get("review_progress") == "pending-manual-adjudication":
                row["terminal_assessment"]["depends_on_volumes"] = pending
        else:
            row["terminal_assessment"] = {"status": "unknown", "review_progress": "pending-manual-adjudication", "rationale": "只机械保留原问题；终点尚未逐项人工判断，unknown不表示作者未回收。", "later_evidence": [], "depends_on_volumes": pending}
    data = {"source_id": read(WORK / book / "source.json")["source_id"], "status": "draft-pending-inputs-or-semantic-adjudication", "method": "仅收正式分卷，完整保留原问题/阶段线程/局部异常/逐章unresolved及原读者；终点判断另写，不改原卷。", "inputs": inputs, "pending_inputs": pending, "candidates": rows}
    if name == "historical":
        data["local_issue_records"] = originals
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    represented = {(r["volume"], r["original_field"], r["original_index"]) for r in local}
    assert all((g["volume"], g["field"], i) in represented for g in originals for i in range(len(g["original_records"])) if i not in g["empty_record_indices"])
print(json.dumps({"formal_volumes": [r["volume"] for r in inputs if r["status"] == "formal-library"], "pending_inputs": pending, "historical_candidates": len(historical), "local_atomic_candidates": len(local), "semantic_adjudications_created": 0, "notes_unresolved_exact_preservation": True}, ensure_ascii=False))
