from synthesis_common import *
changes=[
('characters',0,'fact_summary','准用尸桥/降俘失保/矿工未改善的行动者层次',
'李逍遥早期凭承伤、救援和个人武力保护同伴；紫魔林追击造成四千人损失后须面对指挥错误。成为军将后，他能救囚女、安置军属，也准尸填沟、对降俘未获保全最终退让、支持不救盛临；见危险矿工只内想善待而无改善令。后期更参与强迁及镇压平民。末战选择让玩家断后、救NPC，但50万NPC返不足18万。',[821,941,965]),
('themes',0,'fact_summary','区分不作为/退让与主动施暴，不扩大矿工事件',
'李多次救同伴、囚女和军属，逐渐以保护者自居；同一人物仍准尸桥、未能兑现降俘不杀承诺，对危险矿工只想善待未下改善令，后期又参与强迁与镇压平民。后期结盟与讨伐仍伴平民真实死亡，花枪等质问其刽子手式行为，李以战争机器自况而未形成彻底无暴力的解决。',[821,965]),
('plot',2,'fact_summary','秦蒙是现实失踪者，不能误写游戏秦王',
'早期匕首攀援、站位与草丛利用把弱属性变成战术题；现实秦蒙救援受挫后改用卧底和协作，比赛败给问剑后又有技术学习及实战验证。国家战截粮、烧仓在不同敌军上并非都有效：亡灵可食尸、火云条件亦限制围粮。后段地雷、盖亚与传送各有用处，却不能穿越鬼城位面障碍。',[356])]
out=[]
for d,i,field,reason,after,nums in changes:
 p=P/f'synthesis-{d}.json';a=json.loads(p.read_text(encoding='utf-8'));r=a['rows'][i]
 out.append({'file':str(p.relative_to(ROOT)).replace('\\','/'),'input_sha256':sha(p),'json_pointer':f'/rows/{i}/{field}','row_id':r['id'],'before':r[field],'after':after,'reason':reason,'source_evidence':[ref(n) for n in nums],'other_fields':'全部不动，仅顶层事实句精确收窄/更正，引用原本已有相应章，不改上游'} )
dump(P/'synthesis-three-facts-selfcheck-proposal.json',{'status':'proposal-only-awaiting-primary','new_actual_original_rereads':[{'chapter_id':CH[n]['chapter_id'],'start_line':CH[n]['start_line'],'end_line':CH[n]['end_line'],'full_text_read':True,'actual_reader':'/root/zongheng_vol03_full','unique_coverage_increment':0} for n in [965,821,356,941]],'changes':out})
print(sha(P/'synthesis-three-facts-selfcheck-proposal.json'))
