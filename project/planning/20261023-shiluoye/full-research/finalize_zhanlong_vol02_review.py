"""记录已经逐项完成的卷二语义主审，并复核限定纠错和输入冻结。"""
import collections
import copy
import hashlib
import json
import sys
from datetime import datetime, timezone
from check_volume import WORK, load_and_check, read

sys.stdout.reconfigure(encoding="utf-8")
source, spec, folder, analysis, cards, graph, mapping, preflight = load_and_check("zhanlong", 2)
freeze = read(folder / "freeze-manifest.json")
for section in ["core_sha256", "support_sha256", "external_input_sha256"]:
    for name, digest in freeze[section].items():
        assert hashlib.sha256((folder / name).read_bytes()).hexdigest() == digest, name
before_dir = folder / "review-corrections" / "raw0314-two-swords-before"
old_analysis = read(before_dir / "analysis.json")
old_cards = read(before_dir / "cards.json")
expected = copy.deepcopy(old_analysis)
expected["dimensions"]["characters"][2]["limits_and_counterevidence"] = analysis["dimensions"]["characters"][2]["limits_and_counterevidence"]
expected["dimensions"]["continuity"][4] = analysis["dimensions"]["continuity"][4]
expected["open_questions"] = [q for q in expected["open_questions"] if q["id"] != "v02-q-zhanhua"]
for row in expected["major_character_states"]:
    current = next(c for c in analysis["major_character_states"] if c["origin_key"] == row["origin_key"])
    if row["origin_key"].endswith("/leizi"):
        row["stage_change"] = current["stage_change"]
    if row["origin_key"].endswith("/yelai"):
        row["relationships"] = current["relationships"]
assert expected == analysis, "其他analysis语义发生变化，需重新主审"
expected_cards = copy.deepcopy(old_cards)
for row in expected_cards:
    current = next(c for c in cards if c["origin_key"] == row["origin_key"])
    for suffix, field in [("/unseal", "obstacle"), ("/leizi", "stage_change"), ("/yelai", "relationship_direction")]:
        if row["origin_key"].endswith(suffix):
            row["content"][field] = current["content"][field]
assert expected_cards == cards, "其他卡片发生变化，需重新主审"
assert hashlib.sha256((before_dir / "graph.json").read_bytes()).digest() == hashlib.sha256((folder / "graph.json").read_bytes()).digest()
assert analysis["plot_and_hidden_threads"] == read(folder / "graph.json")["threads"]
notes_raw = (folder / "chapter-notes.jsonl").read_bytes().splitlines()
tail_raw = (WORK / "zhanlong" / "primary-vol02-tail" / "chapter-notes.jsonl").read_bytes().splitlines()
assert notes_raw[-100:] == tail_raw
notes = [json.loads(row) for row in notes_raw if row.strip()]
assert collections.Counter(row["reader"] for row in notes) == {"/root/zongheng_vol04_full": 153, "primary": 100}
assert len(analysis["chapter_unresolved_index"]) == 228 and len(analysis["open_questions"]) == 15
overlay = read(folder / "primary-corrections.json")
assert overlay == read(folder / "priority-corrections-delta.json")
assert overlay["original_record"] == next(row for row in notes if row["chapter_id"] == "ch-0314")
review = {
    "source_id": source["source_id"], "revision": source["revision"], "volume": 2,
    "reviewer": "primary", "status": "reviewed_for_library_import", "user_approval": False,
    "reviewed_at": datetime.now(timezone.utc).isoformat(),
    "scope": "primary全文实读raw405—504，另因两剑问题完整复读314/498；raw252—404原阅读归agent4。逐项主审45九维、101卡、52图节点33边15线、45人物阶段、18异常、15生死核查、16逐章源异常、卷尾问题及完整报告/交接；不冒称primary独读全卷。",
    "review_groups": {"dimensions": 45, "cards": 101, "nodes": 52, "edges": 33, "threads": 15, "major_character_states": 45, "source_anomalies": 18, "named_life_states": 15, "chapter_source_anomalies": 16, "volume_end_questions_after_correction": 15},
    "semantic_findings": [
        "314斩华是流霜自有剑，献罗林并建议毁的是巴林佩剑/权力之剑；两物独立，撤回假物链疑点。毁权剑仍仅建议/同意，军出战不代人格解放。",
        "原314笔记原行不改，优先纠错overlay保完整原行/更正/撤回范围和行证；九维连续性改为真正文本指代研究，元流程不充文学观察。",
        "秦王重铸可用、309补丁50%与443进龙池100层分版本；左右双持、旧膝治愈/旧戒赤龙失去与新装门槛分别记。",
        "个人竞技排名、城战守御令/阵营胜/MVP、紫魔林四千核心降十级均分别结算，不因最终得驻地抹指挥失误。",
        "林独立近卫救场、468—470迁会/殿、473神隐与此前同行分层；亲吻唱歌不代双方正式确恋，秦雨暂拒不代情侣。",
        "现实秦蒙已尸证死亡，但犯罪加害/保护链未完全侦破；欧阳阳炎压制后活离，主断肋昏迷不误记击败或拘捕。",
        "落海与洛克林是独立人物；紫星/林煌已死、苏克装死/达林装伤、林穹断臂逃，普通军80%恢复不套命名BOSS。",
        "池兄妹空血/掉落仍活，父遗念不是本体复生，498活捕SSS已结而501另开守护；504仅公主放行，未满24h或入渊。",
        "李百断后救回一人、其余99明确死，主误判伏弓真实付数百死，不能以局部救援遮群体损失。",
        "刀锤两次物链与一次成交分款分开；A4钥已交，工资政策/照护20万缺独立到账不能泛闭；作者七符明纠与其余源数差分别保。",
        "图逐项核知识渠道、因果/兑现/呼应，不以同主题代剧情硬因果；后卷具体提示已改为通用阶段边界，未将其他实体职务套叶来。"
    ],
    "preflight": preflight,
    "remaining": ["228条历史疑点章节索引和全部原串留待全书终点逐项审计，不因撤回一个研究误读删除原笔记。", "卷三至六及整书综合/终点审计继续，用户品味未自动认可。"],
    "input_sha256": {**freeze["core_sha256"], **{n: h for n, h in freeze["support_sha256"].items() if "/" not in n}}
}
review["input_sha256"]["freeze-manifest.json"] = hashlib.sha256((folder / "freeze-manifest.json").read_bytes()).hexdigest()
path = WORK / "zhanlong" / "review-vol02.json"
path.write_text(json.dumps(review, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"status": review["status"], "preflight": preflight, "review": str(path)}, ensure_ascii=False))
