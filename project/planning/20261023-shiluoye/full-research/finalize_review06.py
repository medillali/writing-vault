"""固定卷六已审版本；这是研究审阅记录，不是代替用户批准。"""
import pathlib,json,hashlib
base=pathlib.Path(__file__).resolve().parent;folder=base/'zongheng-tianxia/vol06'
validation=json.loads((folder/'validation.json').read_text(encoding='utf-8'))
record={
 'volume':6,'reviewer':'primary','status':'reviewed_for_library_import','user_approval':False,
 'scope':'244正文单元由primary前44、接续读者后200合作全文阅读；primary审46条九维、25人物、43场景、15机制、58节点42边19线、集中29项疑点，另完整重读raw0669和raw0774—0777核接口。不得称primary一人阅读全文。',
 'corrections_verified':[
  '火龙初获60分钟/24h与后期时长分阶段，未当永久固定上限',
  '秦韵对书表达爱、愿陪伴；拒留宿的是书，不反写主宾',
  'raw0669战时NPC全灭与胜后75%物资军力特殊恢复分开，书估可复七八万不是逐兵实际清册；魂殇永久毁另记',
  '圣灵惩戒预期十死后果与当章冰兰清除分开，未记实际掉十级',
  '斩剑飞扬不误为折剑；到255可入圣资格不误为当时255；赤霄已绑未用',
  '冰茶病名/40%有本人及许琳出处，手术开始但本卷未揭结果；清风破门与王宫/民心尚守分开',
  '社会与亲密关系保本人选择及证词层级；七星沈证词未据后来自述强裁调查真相',
  '任务成功、战时损失、奖励恢复与具名人物死亡各有证据，跨卷终点另验',
  '内部文件链接改为本卷相对路径，正式保存不依赖暂存目录'
 ],
 'preflight':validation['result'],
 'remaining':['研究待用户审阅，未自动收藏或批准','全书人物弧和全历史问题终点核验另验'],
 'input_sha256':{name:hashlib.sha256((folder/name).read_bytes()).hexdigest() for name in ['analysis.json','cards.json','graph.json','read-log.json','chapter-notes.jsonl','reader-state.json']}
}
(base/'zongheng-tianxia/review-vol06.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('review-vol06.json: reviewed_for_library_import; 6 reviewed input hashes pinned')
