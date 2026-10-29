"""卷七主代理复审后固定实际导入输入。"""
import pathlib,json,hashlib
base=pathlib.Path(__file__).resolve().parent;folder=base/'zongheng-tianxia/vol07'
record={
 'volume':7,'reviewer':'primary','status':'reviewed_for_library_import','user_approval':False,
 'scope':'285正文由分卷读者前175、primary后110合作全文阅读。primary审全部36九维、29人物/37场景/10机制、46节点24关系12线、16认知和集中疑点；修订后另审全部相关文字、边及认知差分。primary另完整重读raw0779/0866/0944核时点、嘱托和据点。不得称primary一人读完全卷。',
 'corrections_verified':[
  '清风保卫战中飞升归零，不把后续战败提前为既成；玩家圣域资格与宠物封印飞升分链',
  '刑天母亲重病时嘱托不归龙魂，不称已亡母遗嘱；龙魂自陈旧回忆与书推暗恋分开',
  '第三即最后封raw0922宣布解除，raw0963醒后展示归零裸装，不造第四封',
  '奥丹雨露峡谷月内建塞命令与防黑暗城堡分清，未造黑堡要塞已建成',
  'raw1021与印刷1013明确；200万元对应黄金级据点曙光要塞，付款和次日拟让点分开',
  '萨格隆改为0810/0815—0817，S4首通秦一牧；重新核了修版卡与图边',
  '九天玄塔本就是S3，e-tank细化前段新盾验证与最终玄武失败后改策，不拆成两个副本',
  '删除送花→白银匕回收错误起点，匕来自通缉奖励；抵美上线不推专线已安装',
  '知识16条有state和时点，猜测/不知/误信/后来实知分开；正文编号及预算误算分别处理',
  '任务/战果/物权/生命/主权分账；未将王红血案角色转述当警方结案，未将醉吻当清醒恋约'
 ],
 'preflight':{'indexed_segments_read':285,'body_units_read':285,'cards':{'character':29,'scene':37,'pattern':10},'nodes':46,'edges':24,'threads':12,'evidence_references_checked':2578,'preflight':'passed'},
 'remaining':['全书问题、人物弧和综合另行审查','研究仍待用户审阅，不自动批准或收藏'],
 'freeze_note':'子代理freeze-manifest保留交接版本；主代理随后仅精确刑天母嘱措辞，正式输入以下列SHA为准。',
 'input_sha256':{name:hashlib.sha256((folder/name).read_bytes()).hexdigest() for name in ['analysis.json','cards.json','graph.json','read-log.json','chapter-notes.jsonl','reader-state.json']}
}
(base/'zongheng-tianxia/review-vol07.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('review-vol07.json: reviewed_for_library_import; 6 reviewed input hashes pinned')
