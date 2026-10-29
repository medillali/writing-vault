"""在主代理逐项审阅及定向修订复核完成后固定签收输入。"""
import datetime
import hashlib
import json
import pathlib
import sys

assert "--reviewed" in sys.argv
base = pathlib.Path(__file__).resolve().parent
stage = base / "zongheng-tianxia"
audit = stage / "vol08"
root = base.parents[2]
def read(path):
    return json.loads(path.read_text(encoding="utf-8"))
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

freeze_path = audit / "audit-freeze-manifest.json"
freeze = read(freeze_path)
for name, digest in freeze["audit_sha256"].items():
    assert pathlib.Path(name).name == name and sha(audit / name) == digest, name
for name, digest in freeze["formal_input_sha256"].items():
    assert sha(root / name) == digest, name
validation = read(audit / "audit-validation.json")
assert validation["historical_candidates"] == 105
assert validation["local_candidates"] == 404
assert validation["character_arcs"] == 48 and validation["focused_findings"] == 27
assert not validation["pending_inputs"] and validation["unadjudicated_candidates"] == 0
assert validation["frozen_volume08_unchanged"]
history = read(audit / "historical-question-pool.json")["candidates"]
local = read(audit / "local-question-pool.json")["candidates"]
characters = read(audit / "character-arc-audit-draft.json")["characters"]
findings = read(audit / "end-state-audit-draft.json")["findings"]
assert len(history) == 105 and len(local) == 404 and len(characters) == 48 and len(findings) == 27
assert all(not r.get("terminal_assessment", {}).get("depends_on_volumes") for r in history + local)
assert all(r.get("terminal_assessment", {}).get("status") in {"answered", "partial", "unknown", "unrecovered"} for r in history + local)
review = {
    "status": "reviewed_for_library_import", "reviewer": "primary",
    "reviewed_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "source_id": freeze["source_id"], "user_approval": False,
    "freeze_manifest_sha256": sha(freeze_path),
    "reviewed_counts": {"character_arcs": 48, "focused_findings": 27, "historical_questions": 105, "local_atomic_items": 404},
    "reviewed_ids": {
        "characters": [r["audit_id"] for r in characters],
        "findings": [r["key"] for r in findings],
        "historical": [r["candidate_id"] for r in history],
        "local": [r["candidate_id"] for r in local],
    },
    "review_method": "主代理逐批读取全部审计独立判断；重复来源/异常模板仅压缩重复措辞。与既有分卷全文读者笔记及主代理实际阅读区间对照，不冒认主代理独自重读1180章。",
    "semantic_checks": [
        "丁舒升原名、丁书生误称；许琳真堂姐与冰茶临时借名分开",
        "林克与林丘分人；CGL同名邱华不据姓名合并；龙神两种死亡来源未证同体",
        "灵儿0922第三即最后封至0963醒后状态同一链，不造第四封",
        "冰兰封冻无确醒；明宇魂格毁；奥丹系统陨落与剧情最终死亡分时",
        "军力75%/80%恢复不抹战时损失，亦不自动复活有名个体",
        "性关系、同床、知情及同意逐场保存；婚礼未来与已婚分人",
        "预测、资格、掉落、交付、实穿、付款及逐人到账分开",
        "扫墓按主体区分；主母童年离家不证明亡故",
        "原子项源异常与阶段认知不作为作者未回收伏笔总数",
        "月后期天域等级误写与神殿/古秦场景误配已定向纠正",
        "终点未匹配明确证据保unknown/partial，不写仍缺整卷或研究未执行",
    ],
    "independent_review": "cross-review-late.json/md：10项建议与14项复核，原读者归属及定点复核范围保留",
    "limits": ["研究草稿尚待用户审阅", "不等穷尽正文每一潜在线索", "定位有效不自动证明解释唯一", "不写入用户审美、收藏或原创正典"],
}
out = stage / "primary-whole-book-review.json"
out.write_text(json.dumps(review, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")
print(json.dumps({k: review[k] for k in ["status", "reviewer", "freeze_manifest_sha256", "reviewed_counts", "user_approval"]}, ensure_ascii=False))
