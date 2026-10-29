from save_focus_manual import A,P,E,read,write,sha
import copy
f=A/'focused-findings-part02.json';data=read(f);b=next(x for x in data['findings'] if x['key']=='canglan-body-soul-report-and-next-threat');a=copy.deepcopy(b)
a['stage_chain'][2]='1350石林卡败军自述沧欲吞希遭玄月镜反炼、希得力/琴败被俘，为后来明确魂结局报告；1369主叙两次称希吞沧魂吸部分力，主对希当面也沿用其能反噬沧的结果。1370琴又为希寻天域兵，世界威胁另续。'
a['conclusion']='不能把1331标题胜利记成魂已亡，也不能把全书终点仍写没有任何魂后证。终点先有石林卡报告，1369主叙及当面对话再沿用希吞沧魂/部分吸力的结果，说明后文持续承接；吞魂过程仍未由主现场亲见。'
a['limits_and_counterevidence']='1369是主叙/主对希讲话，不冒希亲口自认，也不冒现场目击吞魂；报告和后续承接足以收窄未知，全部力量去向仍非全知实测。希后来被击败、琴新任务与沧原体死亡是不同事件，不套一个终王全清结果。'
a['evidence'].append(E(1369))
p=P/'focus02-canglan-later-narration-proposal.json';write(p,{'status':'proposal-pending-primary-review-not-applied','reason':'按primary本轮原文完整复读1369新增后承接；本代理已完整读正式1369四栏，不冒原文亲读。','changes':[{'path':f.name,'input_sha256':sha(f),'key':b['key'],'before':b,'after':a,'scope':'仅stage_chain第3段/conclusion/limits及追加1369，partial/其余7项逐值不变'}]});print(sha(p))
# 03尚未发primary：修单个笔误“实验首批”到“实际首批”，不改判断。
f=A/'focused-findings-part03.json';d=read(f);before=copy.deepcopy(d);r=d['findings'][6];r['stage_chain'][1]=r['stage_chain'][1].replace('1141实验首批','1141实际首批');write(P/'unsubmitted-self-check/focus03-before-typo.json',before);write(f,d)
md=f.with_suffix('.md');md.write_text(md.read_text(encoding='utf-8').replace('1141实验首批','1141实际首批'),encoding='utf-8')
src=P/'manual_focus_part03.py';src.write_text(src.read_text(encoding='utf-8').replace('1141实验首批','1141实际首批'),encoding='utf-8');print('part03',sha(f))
