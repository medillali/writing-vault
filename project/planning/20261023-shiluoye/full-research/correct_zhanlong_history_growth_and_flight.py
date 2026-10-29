"""主审后证补齐与角色时点校正，保旧完整组及逐对象差分。"""
from pathlib import Path
import json,hashlib,copy,sys
sys.stdout.reconfigure(encoding='utf-8')
B=Path(__file__).parent/'zhanlong';A=B/'audit/whole-book'
S=json.loads((B/'source.json').read_text(encoding='utf-8'));C={int(c['chapter_id'][3:]):c for c in S['chapters']}
changes=[
 ('adjudications-history-v03-batch001.json','v03-question-v03-q-city','铁刃后844达1.8万主骑，915池军一万余实战/原龙城失，926原池军安置新凡书；972主实调19000余炎鹰、973到场空袭，规模和生产已有明确后证，不能再将五千目标一概说未产。原玩家龙城和新凡书是不同领地，九级目标后态与年利五千万指定入账未全有同口径凭据；军事实力超标不等原城所有经营目标都结清。',[972,973]),
 ('adjudications-history-v03-batch002.json','v03-thread-v03-t-city','城级/资源/招募按时点，915原池军参战/916仍听主、926安置凡书，972调19000余炎鹰、973到场轰援军和传送阵，足证真实扩军，不停在领地菜单。旧龙城已失而新凡书另建，后军量超过五千可确认，不由此追填旧城年利五千万已到账；保持领地对象与财务口径。',[972,973]),
 ('adjudications-history-v04-batch001.json','v04-question-v04-q-realcase','1045酒吧开业/1046赴约、1093仍营业，裴1276真实被打晕取盒/1277被捕；汪1278殖装现身、1279逃脱而实验室三十余科学家活捕获新证，1355汪才现实被主杀死。沈真实死亡、魏854保释/959在押缺桥与最终裁判、国外完整产业网仍未全给，不把清剿等同汪该次被捕或全球司法结案。',[1355]),
 ('adjudications-history-v04-batch002.json','v04-thread-t-reality','1045—1047PaPa开业与赴场收回装修计划；1276裴接近/取盒、1277裴捕沈死、1278汪殖装/1279实验室科学家活捕而汪逃，1355汪真死，证据与复仇都有阶段结果。魏854保释/959在押缺桥与终判、全球组织仍缺完整清册；末白墨颜数字醒不能改沈原身死亡，也不写汪1279已落网。',[1355]),
 ('adjudications-history-v05-batch002.json','v05-question-v05-q-eightturn','1178加三级后等级继续，1264第一次神帝挑战失败、1266林中位而主仍未飞升；1272主才借卡/丹/霸王重生真杀云浅炼上位格，末300级与多神技有成长结果。但未单演原八转门槛/转职手续，不把飞升机制或等级变高等同已看见八转任务，旧210不能倒说已满足。',[1264,1266,1272]),
]
out=A/'primary-growth-flight-corrections';out.mkdir(exist_ok=True)
delta=[]
for name in dict.fromkeys(c[0] for c in changes):
 p=A/name;backup=out/name
 if not backup.exists():backup.write_bytes(p.read_bytes())
 old=json.loads(backup.read_text(encoding='utf-8'));new=copy.deepcopy(old)
 for _,cid,reason,nums in [x for x in changes if x[0]==name]:
  matches=[x for x in new if x['candidate_id']==cid];assert len(matches)==1,(name,cid)
  row=matches[0];before=copy.deepcopy(row);row['rationale']=reason
  for n in nums:
   if n not in row['later_chapters']:
    row['later_chapters'].append(n);row['later_evidence'].append({k:S[k] for k in ['source_id','revision']}|{k:C[n][k] for k in ['chapter_id','start_line','end_line']}|{'claim_kind':'inference'})
  delta.append(dict(path=name,candidate_id=cid,before=before,after=copy.deepcopy(row)))
 current=json.loads(p.read_text(encoding='utf-8'));assert current in [old,new],name
 p.write_text(json.dumps(new,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(out/'delta.json').write_text(json.dumps(delta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('SAVED',len(delta),'PRIMARY CORRECTIONS')
