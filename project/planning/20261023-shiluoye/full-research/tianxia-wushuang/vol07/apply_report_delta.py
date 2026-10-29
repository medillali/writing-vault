"""一次定向更新报告编排措辞；保211条原始笔记不动。"""
import pathlib,json,hashlib,sys
sys.stdout.reconfigure(encoding='utf-8');H=pathlib.Path(__file__).resolve().parent
p=H/'finalize_delivery.py';s=p.read_text(encoding='utf-8')
changes=[
 ('62份独立人物卡','65份独立人物卡'),
 ('神农六分/六秒','轩辕诀六分/六秒'),
 ('1454心爱语主未听/读者已听','1455心爱语主未听/读者已听'),
 ('百骑与幼龙蛋滴血结界已启动','百骑与幼龙蛋滴血认主已启动；结界仍筹材料'),
 ('龙域新生启动3—5年未来','龙域幼龙认主启动、木石料与火魔石结界仍计划，3—5年成年未来'),
 ('龙域百骑/蛋结界已起','龙域百骑/幼龙认主已起，结界仍筹木石火魔石'),
 ('百骑与幼龙蛋滴血结界','百骑与幼龙蛋滴血认主'),
 ('百骑幼蛋滴血结界','百骑幼蛋滴血认主'),
 ('冰亲承短控后恢复/圣林吞灭；龙域百骑幼蛋启动','冰亲承短控后恢复/圣林吞灭；龙域百骑幼蛋认主启动'),
 ('解盟与解禁名','主盟解散、禁止原名重建'),
 ('敌全灭解盟，不假补60min细节','敌全灭/主盟解散、禁止原名重建，不假补60min细节'),
 ('主旧逐日靴给她','主旧逐日者斗篷给她'),
 ('本卷另真实死亡Boss/敌','本卷另真实死亡Boss/敌'),
 ('主已破盅释放/队长实放','主已破盅释放/队长实放'),
]
applied=[]
for old,new in changes:
 if old!=new and old in s:s=s.replace(old,new);applied.append([old,new])
s=s.replace("证据：{refs(x['evidence'])}","可操作机制：{'；'.join(x['mechanism'])} 限制/反例：{'；'.join(x['limits_and_counterevidence'])} 证据：{refs(x['evidence'])}")
s=s.replace('神格成、九转学技实测','1462神格成激活原三技，1464九转另学狂撞并实测')
s=s.replace('主与古剑救援对象，也是现实表达愿离者','主与古剑救援对象，也是现实表达愿离者')
s=s.replace('六人医诊无重，听风前科','陆/李/鬼/杜/斗/幽六男医诊无重；虎供房信息/1315仅派接/1324确认到，不写随六男同行，听风前科')
s=s.replace('原始全文笔记','原始全文笔记')
p.write_text(s,encoding='utf-8')
freeze=json.loads((H/'delivery-freeze.json').read_text(encoding='utf-8'))
delta=dict(status='draft_primary_corrections_applied_pending_review',original_notes_sha256=hashlib.sha256((H/'chapter-notes.jsonl').read_bytes()).hexdigest(),original_notes_preserved=True,before_core_sha256={k:v for k,v in freeze['files'].items() if k in ['analysis.json','cards.json','graph.json']},corrections=[
 '1462格成即激活原三灰技；1464九转另学狂撞，不混前置',
 '心爱语落raw1455，图卡九维交接相应引用同步',
 '1416六分/六秒对象轩辕诀，非神农；保源差',
 '月光石为法师/法攻禁疗杖，月露为牧师独立新增',
 '六男现实救援为陆李鬼杜斗幽；虎供房信息、1315派接、1324才确认到',
 '吕布衣与吕超分人，新列吕布衣与未名同乘女骑；否媳妇归女骑，不归吕超',
 '乱月得逐日者斗篷非鞋；周小萌姓周；李论坛报维杀奥佩罗得绝风，不是李得杀',
 '雷鸣称死亡剑刃，普通控制多MISS但玩家可伤；寒冰盾才使1429陆紫啸全MISS',
 '飞银本体飞银龙非骑士；心龙神战中受伤不叫自伤；1466林交药油不归何',
 '公证费主从双方各收五万实收十万，非主付',
 '铜眼控制陆尘→受控陆杀北林→明镜解主控，不是控北林',
 '首挑战主盟解散/禁止原名重建，不是解禁名',
 '龙域幼龙孵化/百骑认主已成，木石火魔石结界仍未来材料筹集',
 '十九为少女年龄非释放魂数，后释放更多魂无精数；周合作多团多会非六城',
 '45九维逐项新增mechanism与limits_and_counterevidence，各有独立触发步骤及限制/反例；其余fact/inference保留',
 '删除duel→father及mission→scales两条仅研究方法/节奏共同点边，现图55边；whip→gold收窄交易责任具体互照'
],independently_full_chapter_reread_this_delta=['ch-1370','ch-1446','ch-1416','ch-1455','ch-1467'],primary_exact_source_checks=['ch-1421 L112581/112597','ch-1495 L118501—118505','ch-1462 L115817','ch-1341','ch-1354','ch-1469','ch-1504 L119299'],report_replacements=applied,note='读后原记录作为历史不篡改，终点产物/纠正链修正；主审尚未完成，不是正式接受。')
(H/'primary-review-delta.json').write_text(json.dumps(delta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(report_changes=len(applied),notes_preserved=delta['original_notes_sha256']),ensure_ascii=False))
