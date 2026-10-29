from pathlib import Path
import json
P=Path(__file__).parent
bs=[]
for d in ['l-a','l-b']:
 for f in sorted((P/d).glob('batch-*.json')):bs.append(json.loads(f.read_text(encoding='utf-8')))
units={u['ordinal']:u for b in bs for u in b['units']};assert set(units)==set(range(1,388))
es=[e for n in [379,380,383,384,385,386,387] for e in units[n]['evidence']]
data={'summary':'萧翎取得个人、与花舞双人及团队等赛事冠军，天狂团队成为第一强团。最终大战分工完成：萧翎等击毁沃顿躯体，萧御毁本命神格，系统确认任务结束；众神的力量转移为任务阶段增幅，事后诸神以凡人形态重现。主角在新星与紫焰、牧琳、霏雨、花舞相继重逢，伙伴也获得现实后日谈。最后与萧御再战的胜负刻意未揭示。','interpretation':'结尾把最初的等级与实力竞争、机械专长和团队建设推到公共领导权，再把游戏关系带回现实。战斗的最高强度没有成为永久日常：神力消退，诸神继续作为凡人存在，终局资源从属性胜负转成共同经历及关系。奥斯林兰与塔布雷特在神之境相拥，为早段悲剧补上后置收束；这不能改写他们此前死亡与净化的实际经过。\n\n终局同时明显加速：大规模战争、二转、全员神格、主神战力和最终神王在少数单元密集结算，与前期细拆制作和练级形成尺度反差。最终事件有系统确认和现实重逢，仍不意味着所有早先物件、细节承诺或数值冲突都获得解释。竞技冠军也包含同盟让分、情报和资源投入，不能仅写成一个人的纯技术自然胜出。\n\n感情线终点可确认现实共同相聚及家庭接纳；前段各场互动中的拒绝、压力和性关系暗示仍需分别记录。结局重逢不能追认每一次过程都已得到自由同意。研究学习可取其长期资源铺垫、群体协作与虚实呼应机制，价值取舍仍交由用户审阅。','evidence':es}
(P/'l-ending-synthesis.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
