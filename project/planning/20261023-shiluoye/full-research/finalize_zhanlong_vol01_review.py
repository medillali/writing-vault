"""将已实际完成的卷一逐项语义主审绑定到本次冻结输入。"""
import collections
import copy
import hashlib
import json
from datetime import datetime, timezone

from check_volume import WORK, load_and_check, read

source, spec, folder, analysis, cards, graph, mapping, preflight = load_and_check("zhanlong", 1)
freeze = read(folder / "delivery-freeze.json")
for name, digest in freeze["input_sha256"].items():
    assert hashlib.sha256((folder / name).read_bytes()).hexdigest() == digest, name
before = read(folder / "before-primary-delta-20261026" / "analysis.json")
expected = copy.deepcopy(before)
entry = expected["dimensions"]["continuity"][2]
entry["limits_and_counterevidence"] = entry["limits_and_counterevidence"].replace("如204老K换斧", "如205老K换斧")
added = next(e for e in analysis["dimensions"]["continuity"][2]["evidence"] if e["chapter_id"] == "ch-0205")
entry["evidence"].append(added)
entry["evidence"].sort(key=lambda e: (e["chapter_id"], e["start_line"], e["end_line"]))
assert expected == analysis, "须重新审查超出指定两项的小修"
notes = [json.loads(row) for row in (folder / "chapter-notes.jsonl").read_text(encoding="utf-8").splitlines() if row.strip()]
assert collections.Counter(row.get("reader") for row in notes) == {"/root/zongheng_vol03_full": 150, "primary": 100}
tail = (WORK / "zhanlong" / "primary-vol01-tail" / "chapter-notes.jsonl").read_bytes().splitlines()
merged = (folder / "chapter-notes.jsonl").read_bytes().splitlines()
assert merged[-100:] == tail, "primary 原行必须原样保留"
assert len(analysis["stage_characters"]) == 43 and len(analysis["chapter_unresolved_index"]) == 242
assert len(analysis["source_anomalies"]) == 26 and len(analysis["unresolved_volume_end"]) == 15
review = {
    "source_id": source["source_id"], "revision": source["revision"], "volume": 1,
    "reviewer": "primary", "status": "reviewed_for_library_import", "user_approval": False,
    "reviewed_at": datetime.now(timezone.utc).isoformat(),
    "scope": "primary全文实读raw152—251；raw2—151原文归agent3。primary另逐项完整主审36九维、102卡、54节点33边16线、43阶段人物、26来源异常、15卷末问题及报告/交接。派生主审不冒充primary独读全卷。",
    "review_groups": {
        "dimensions": 36, "cards": 102, "nodes": 54, "edges": 33, "threads": 16,
        "stage_characters": 43, "source_anomalies": 26, "volume_end_questions": 15,
        "truncation_recovery": "九维中段单读style/narrative/dialogue；卡片重复59—74补全截断；report初读中段被截，已另读135—450行补齐。"
    },
    "semantic_findings": [
        "荆棘剑是死亡后ROLL仍结算，不是已证魂绑；天策违约与囡先助剑后看原录像转向保阶段。",
        "扬威个人17杀MVP与忠烈5:0败解散分别结算；围猎28人杀26与朋友夸27分层，不造追死卷尾简简单单。",
        "斩龙200系统成立、201二级300满、245三级972报告；实体工作室、临时队、会籍及双女外部归属分开。",
        "神庙九人不补第十；真云辰传卷后消散、冉闵NPC条件复生、老K玩家同名分别记录。",
        "流霜中途221收徒三转与234总任务终奖分离；七星/墨家书/符/等级门槛、秦王100%仍半品各有有效时点。",
        "幻境性经历不是现实性交，主能自清记忆为内述且未真正清除，亲近不代正式恋人或同意。",
        "抹茶理论贡献与真实拙操均保本卷证据，不以后卷回填伪装；圣魂盾已交但未明实穿。",
        "罗林忠诚誓言、卡特死亡两种说法、血认虎及DNA报告均保说话者和证据层，不推完整幕后。",
        "205换斧后证与204掉斧李牧拾分开，已定向修正analysis/report并补章内18164行证据；handoff工作室笔误已改。",
        "图边逐项检查因果/设置/兑现/呼应类型；主题相似不单独充当硬因果，人物、技能、物主跨书不合并。"
    ],
    "preflight": preflight,
    "remaining": [
        "242条历史疑点章节索引完整保留，终局审计须逐项判定，不能只读15个卷尾问题。",
        "本卷正式保存不等全书九维综合与终点审计完成，后五卷继续；全部研究仍draft且用户审美未自动批准。"
    ],
    "input_sha256": dict(freeze["input_sha256"])
}
for name in ["validation.json", "delivery-freeze.json", "primary-delta-20261026.json"]:
    review["input_sha256"][name] = hashlib.sha256((folder / name).read_bytes()).hexdigest()
path = WORK / "zhanlong" / "review-vol01.json"
path.write_text(json.dumps(review, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"status": review["status"], "preflight": preflight, "review": str(path)}, ensure_ascii=False))
