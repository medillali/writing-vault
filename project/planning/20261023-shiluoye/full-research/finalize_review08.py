"""保存已完成的卷八主代理文学审阅回执，并固定所审输入版本。"""
import pathlib,json,hashlib
base=pathlib.Path(__file__).resolve().parent
folder=base/'zongheng-tianxia/vol08'
record={
 'volume':8,'reviewer':'primary','status':'reviewed_for_library_import','user_approval':False,
 'scope':'121个正文单元由primary前20、分卷读者后101全文阅读。primary另完整重读终点raw1180—1181核实；审阅36项九维、22人物、29场景、8机制、37节点26边10线及全部集中疑点。不得据此称primary一人亲读整卷。',
 'corrections_verified':[
  '秦韵怀孕话题保为本人解释与恐孕，改掉无检验依据的非孕断言',
  '灵儿第三封印前卷已解与母史未明拆分，前卷证据在全书审计绑定，不计本卷亲读',
  'e06改呼应：失亲搬居与关系协商的并置不宣直接因果；e19改呼应：冰茶离开已发生但结尾婚条件未触发',
  '明宇明确神格及黑心毁；冰兰生命封冰半年静止，恍惚浅笑不确认苏醒，也不作永灭断言',
  '系统终极任务成功与人物损失及地理灾变分账；黄金灾毁不写主角夺城',
  '工作室解散不等公会消失；随风雪见已婚、龙魂林霜后天婚安排、主雪未写举行分开',
  '月哀已绑、北冥已毁；单刷S6/S7仅书预测，装备数值或榜单不替代实际战果',
  '原文活祭降级算术、17神殿名/14与15名单、迁居地名和股份分母差异保留'
 ],
 'preflight':{'indexed_segments':121,'character_cards':22,'scene_cards':29,'pattern_cards':8,'evidence_references':856,'nodes':37,'edges':26,'threads':10,'result':'passed'},
 'remaining':['须依卷序在卷六七导入后才正式导入本卷','整书人物弧与全历史问题池终点审计另验','研究仍待用户审阅，未自动批准或收藏'],
 'input_sha256':{name:hashlib.sha256((folder/name).read_bytes()).hexdigest() for name in ['analysis.json','cards.json','graph.json','read-log.json','chapter-notes.jsonl','reader-state.json']}
}
path=base/'zongheng-tianxia/review-vol08.json'
path.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('review-vol08.json: reviewed_for_library_import; 6 input hashes pinned; import waits for volumes 6 and 7')
