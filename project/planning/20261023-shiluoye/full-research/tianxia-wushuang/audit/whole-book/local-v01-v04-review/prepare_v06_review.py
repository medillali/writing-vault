"""仅为已授权旧v6稳定657建立独立审阅目录。"""
import json
from pathlib import Path

here=Path(__file__).resolve().parent
destination=here.parent/'local-v06-review'
destination.mkdir(exist_ok=True)
pool=json.loads((here.parent/'local-question-pool.json').read_text(encoding='utf-8-sig'))
if isinstance(pool,dict):
    pool=next(pool[k] for k in ('candidates','items','questions') if k in pool)
selected=[r for r in pool if int(r['volume'])==6]
freeze=json.loads((here.parent/'candidate-id-freeze.json').read_text(encoding='utf-8-sig'))
frozen=[cid for cid in freeze['local']['ids'] if cid.startswith('v06-local-')]
assert len(selected)==len(frozen)==657
assert [r['candidate_id'] for r in selected]==frozen
helper=(here/'review_io.py').read_text(encoding='utf-8')
helper=helper.replace("int(r['volume']) <= 4", "int(r['volume']) == 6").replace("int(r['volume'])<=4", "int(r['volume'])==6")
helper=helper.replace('923','657').replace('range(1,4)', '(6,)').replace("FORMAL.glob('vol0[123]*')", "FORMAL.glob('vol06*')")
helper=helper.replace("'primary' if v<3 else '/root/zongheng_vol03_full'", "'mixed: /root/zongheng_vol05_full raw1059—1233; primary raw1234—1293'")
helper=helper.replace("[{'volume':1,'offset':1,'count':27,'format':'exact complete original prose/observation/detail, evidence metadata deduplicated, all atomic titles preserved','truncated_attempt_repaired':True}]", "[]")
helper=helper.replace("本审阅者原亲读卷四和卷六前175片；本次卷一至三接口为派生材料阅读，不声称原文重读。", "本审阅者实际原读卷六raw1059—1233共175片；primary原读1234—1293共60片，本人已完整逐条读其尾段notes并在原卷六构建时保归属。本次再读正式卷六接口与必要后证，不冒一人全卷/全书原文重读。")
target=destination/'review_io.py'
assert not target.exists(),target
target.write_text(helper,encoding='utf-8')
(destination/'task_plan.md').write_text('# 无双旧卷六657项本地候选终点评定\n\n1. 核657稳定ID；完整读正式卷六报告/交接，保存独立原记录快照与输入SHA。\n2. 每批约60项完整读原observation/detail及全部原子，核必要后证后逐项裁定，交root语义审阅。\n3. 全657后覆盖/出处/原字段校验，agent4唯一合并。\n\n只写本目录，不碰主池、历史v6、分卷、正式库、Git。不读斩龙。保本人原175片与primary尾60实际阅读归属。\n',encoding='utf-8')
(destination/'progress.md').write_text('# 进度\n\n- v1—4原923全部完成后续接；agent4确认旧v6无附加notes，当前volume6与冻结657 ID顺序完全相同。\n- 仅完成ID边界准备，尚未逐项读取本地候选，未伪标原文重读。\n',encoding='utf-8')
print(json.dumps({'destination':str(destination),'stable_v06_candidates':len(selected),'frozen_id_order_matches':True},ensure_ascii=False))
