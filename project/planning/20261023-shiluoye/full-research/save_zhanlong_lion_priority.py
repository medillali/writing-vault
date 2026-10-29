"""原文核实后保存显式优先纠正层，冻结原稿和人工评价不就地改。"""
from check_volume import ROOT,WORK,read
from pathlib import Path
import copy,hashlib,json,sys
sys.stdout.reconfigure(encoding='utf-8')
B=WORK/'zhanlong';A=B/'audit/whole-book';p=A/'local-v03-v06-review/priority-corrections-proposal.json'
def sha(q):return hashlib.sha256(q.read_bytes()).hexdigest()
assert sha(p)=='bf08d3d7bb14b11e4606151c7a38e0335c9b34ba27c5d4641280540d4ba708d7'
proposal=read(p);assert len(proposal['affected_fields'])==11
for c in proposal['affected_fields']:
 q=ROOT/c['file'];assert sha(q)==c['input_sha256'],c['file']
 if 'jsonl_index' in c:
  value=[json.loads(line) for line in q.read_text(encoding='utf-8').splitlines() if line.strip()][c['jsonl_index']]
  assert value['chapter_id']==c['chapter_id']
  keys=c['json_path_within_row']
 else:value=read(q);keys=c['json_path']
 for key in keys:value=value[key]
 assert value==c['before'],c
out=copy.deepcopy(proposal)
out['primary_approval']={'reviewer':'primary','status':'approved-for-library-reading-overlay','user_approval':False,'proposal_sha256':sha(p),'scope':'批准11个已列字段的优先解读，原notes/卷末/卡片及原reader/read_at/SHA完全保留；本层不是原文件就地替换。','actual_verification':[{'chapter_id':'ch-0740','start_line':57970,'end_line':57980,'full_raw_reread_this_turn':False},{'chapter_id':'ch-0743','start_line':58114,'end_line':58186,'full_raw_reread_this_turn':True},{'chapter_id':'ch-0744','start_line':58210,'end_line':58224,'full_raw_reread_this_turn':False}],'findings':'root实际读两份系统公告均为内；743先承诺保满后分给，随后危机提前交抹、借装备补怒并真正施技。字面不能支持旧摘要的后才装备，更不支持给所有国器新增即刻无追杀规则。'}
out['approval_precedence']='原status保留提案历史；当前解释以primary_approval.status和affected_fields.proposed_after为优先。旧摘要中内读成后的规则冲突已撤回，原字节保留审计。'
card=read(ROOT/'writing-vault/library/reports/zhanlong/vol03-cards.json')[97]
out['affected_asset_ids']=[card['asset_id']]
out['affected_origin_keys']=[card['origin_key']]
payload=(json.dumps(out,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
target=A/'priority-corrections-delta.json';assert not target.exists();target.write_bytes(payload)
formal=ROOT/'writing-vault/library/reports/zhanlong/audit';formal.mkdir(exist_ok=True)
f=formal/'priority-corrections-lion-shield.json';assert not f.exists();f.write_bytes(payload)
md='# 狮王盾规则的优先纠正\n\n本层已由主代理核对原文通过，研究仍待用户审阅。查阅卷三旧笔记、规则异常和“国器争夺把保护后卫的代价可视化”场景卡时，应先读本纠正。\n\n740及744系统公告原文均为“十小时内”，旧摘要误写成“十小时后才可装备”。743仍有9小时17分争夺时间：主先承诺保住后分给，随后遭追击，实际提前交抹、借战膝补足120怒、施放群狮之盾。不能据旧摘要制造“公告禁止、角色违规装备”的源冲突。\n\n这不取消进城、下线、死亡掉落及坐标暴露等争夺限制，也不把期间装备当最终保有或推广所有国器即刻无条件装备。旧notes、卡片版本和读者署名原样保留；[十一字段前后与核源凭据](priority-corrections-lion-shield.json)。\n\n[本书阅读入口](../README.md) · [卷三报告](../vol03.md)\n'
(formal/'priority-corrections-lion-shield.md').write_text(md,encoding='utf-8')
print(json.dumps({'status':out['primary_approval']['status'],'affected_fields':11,'affected_asset_id':card['asset_id'],'sha256':sha(f),'original_files_unchanged':True},ensure_ascii=False))
