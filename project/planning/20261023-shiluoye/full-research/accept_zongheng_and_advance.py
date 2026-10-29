"""在整书正式研究与终点审计均验收后，推进下一书的活动来源。"""
import datetime
import hashlib
import json
import pathlib
import runpy
import sys

base = pathlib.Path(__file__).resolve().parent
root = base.parents[2]
sys.path.insert(0, str(root / "distill-novels/scripts"))
from fictionlib.vault import Vault
from validate_book_audit import validate

sys.stdout.reconfigure(encoding="utf-8")
vault = root / "writing-vault"
report = vault / "library/reports/zongheng-tianxia"
collection = vault / "library/reports/collection"
def read(path):
    return json.loads(path.read_text(encoding="utf-8"))
def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

published = validate(root, "zongheng-tianxia")
coverage = read(report / "audit/full-reading-validation.json")
assert coverage["status"] == "passed" and coverage["body_units"] == 1180 and coverage["indexed_segments"] == 1181
for name, digest in coverage["formal_input_sha256"].items():
    assert sha(report / name) == digest, name
synthesis = read(report / "book-synthesis.json")
synthesis_review = read(report / "audit/book-synthesis-review.json")
assert len(synthesis["dimensions"]) == 9 and sum(map(len, synthesis["dimensions"].values())) == 36
assert sha(report / "book-synthesis.json") == synthesis_review["published_json_sha256"]
assert sha(report / "book-synthesis.md") == synthesis_review["published_markdown_sha256"]
run_id = "run-deep-zongheng-tianxia-20261023"
run = read(vault / "exchanges/runs" / (run_id + ".json"))
assert not run["pending_chapters"] and len(run["completed_chapters"]) == 1181
assert run["completed_volumes"] == list(range(1, 9))
receipt = {
    "status": "full-source-nine-dimensions-and-terminal-audit-complete",
    "accepted_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "source_id": run["source_id"], "source_revision": run["source_revision"],
    "body_units": 1180, "indexed_segments": 1181, "volumes": 8,
    "volume_package_cards": coverage["cards"], "source_total_cards": coverage["source_total_cards"],
    "whole_book_synthesis_observations": 36, "whole_book_audit": published,
    "review_status": "draft", "user_approval": False,
    "remaining_project_work": ["天下无双全量蒸馏", "斩龙全量蒸馏", "三书及蜗牛材料统一比较管理", "三书最终备份与实际恢复", "用户审阅"],
    "remote_save": "本轮未提交或推送；本地完成不等远程已保存",
}
write(report / "ACCEPTANCE.json", receipt)
(report / "ACCEPTANCE.md").write_text("""# 《网游之纵横天下》整书研究验收

1180个正文阅读单元及书首共1181片段全文阅读与8卷九维研究已正式保存。36条全书综合、48人物弧、27聚焦终态、105历史问题/线程及404分卷原子项完成主代理审阅与正式发布；解释仍待用户审阅。

分卷包426卡（150人物、205场景、71机制），另保留旧开篇6卡，全源432卡。两个卡数口径不能重复累计。

[全书入口](README.md) · [九维综合](book-synthesis.md) · [人物全弧](character-arcs.md) · [问题分类账本](question-ledger.md) · [独立发布验收](audit/whole-book/publication-validation.json) · [实际阅读覆盖](audit/full-reading-validation.json) · [结构化验收](ACCEPTANCE.json)

图线程保留原卷末状态，终点判断独立叠加。unknown包含源文异常、阶段认知、具体后证未明和结局留白，不等于404条作者未收伏笔。

下一书为《网游之天下无双》，之后《斩龙》。本验收不代表三书项目完成，三书统一比较、最终备份与实际恢复另做。本轮未提交或推送Git，未写入Space或ChatGPT记忆；个人收藏、审美和原创设定没有自动填写。
""", encoding="utf-8")
run.update(state="full-source-read-and-distilled", all_dimensions_complete=True,
           terminal_audit_complete=True, user_review_pending=True,
           book_acceptance="library/reports/zongheng-tianxia/ACCEPTANCE.json",
           notes="1180正文及书首1181片段、8卷九维和全书综合/人物弧/问题终点审计均已正式保存并经主代理审阅；用户评价仍待审阅。三书任务继续无双→斩龙；本轮未推送Git。")
Vault(vault).checkpoint(run)
config = read(collection / "catalog-config.json")
book = config["books"][run["source_id"]]
book.update(task_state="completed_full_nine", note="1180正文及书首已全文阅读，8卷九维、全书综合和终态审计已正式保存；研究仍待用户审阅。本轮未推送Git。保留旧来源、卡片历史和人工评价。")
extra = {r["path"]: r for r in book.get("additional_reports", [])}
extra["../zongheng-tianxia/ACCEPTANCE.md"] = {"title": "本地整书研究验收", "path": "../zongheng-tianxia/ACCEPTANCE.md"}
book["additional_reports"] = list(extra.values())
sid = "src-d8926e2a35f04bcf8139cff0ea516bbd"
config["active_source_id"] = sid
config["books"][sid].update(task_state="active", note="纵横全书研究与终态审计已完成正式验收，现开始按8卷全量阅读；未读区间不标完成。")
write(collection / "catalog-config.json", config)
runpy.run_path(str(collection / "rebuild_catalog.py"), run_name="__main__")
print(json.dumps({"zongheng_status": receipt["status"], "active_source_id": sid, "wushuang_body_read": 0, "project_complete": False}, ensure_ascii=False))
