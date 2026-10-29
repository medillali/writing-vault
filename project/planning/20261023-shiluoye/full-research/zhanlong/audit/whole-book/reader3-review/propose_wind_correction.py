from common import P,dump,sha,evidence
import json
scan=json.loads((P/'wind-fields-scan.json').read_text(encoding='utf-8'));rows=[]
old_desc='845乘风最高10层达到27层语句自冲，现场10剑，942现场15。'
new_desc='845乘风面板称可突破10层达到27层、目前10层，现场实试10剑；942实际15层，属后续成长，27仅潜力未实测。'
for h in scan['hits']:
 old=h['value'];new=old
 if old_desc in old:new=new.replace(old_desc,new_desc)
 if '文本‘最高突破10层达到27层’自相语序保，不改成已27剑。' in old:new=new.replace('文本‘最高突破10层达到27层’自相语序保，不改成已27剑。','原文‘最高可突破10层，达到27层，目前10层’区分可突破上达27与当前10；当场实试10剑，27仅潜力未实测。')
 if '乘风‘10层/27层’源语差与' in old:new=new.replace('乘风‘10层/27层’源语差与','乘风27层潜力尚未实测；')
 if '乘风10/27/后实15' in old:new=new.replace('乘风10/27/后实15','乘风当前10→后实15及27仅潜力未实测（非硬上限10自冲）')
 assert new!=old,h
 rows.append({'path':h['path'],'sha256':h['sha256'],'field':h['field'],'before':old,'after':new,'apply_mode':'仅建议外置纠正层；原始冻结文件和reader/原record不得由本代理改写','evidence':[
  dict(evidence([845])[0],start_line=64598,end_line=64607,claim_kind='fact'),
  dict(evidence([942])[0],start_line=70485,end_line=70510,claim_kind='fact')
 ],'claim_kind':'inference','reason':'可突破10/达到27/目前10分潜力与现态，后15击支持成长，撤硬自冲判读；不认当场27实用。'})
f=P/'vol04-wind-layers-correction-proposal.json';assert not f.exists()
dump(f,{'status':'proposal-only-awaiting-primary-application','actual_reviewer':'/root/zongheng_vol03_full','root_confirmation':'root已定向读845与942同意撤硬自冲，要求本最小字段proposal','source_reading':'本代理本轮定向原文L64588—64608；root另完整片段核L64590—64616/70485—70510；原全卷reader不变','scan_receipt_sha256':sha(P/'wind-fields-scan.json'),'affected_fields':rows,'cards_graph_check':'冻结及正式cards/graph均扫描，cards只称乘风/阳炎能力，无硬上限或自冲语义，graph无相关误判，不提卡图修改；所有旧before快照/生成器/原池原record保历史不动。','independent_boundary':'不扩修本条夹带部落数量、圣域词歧义或其他已审对象；仅撤乘风的旧过强解读。','scanned_documents':scan['scanned_documents']})
ls=['# 卷四乘风斩最小纠正层提案','','未应用；所有冻结原稿、notes reader与池原record不动。当前十层实试十剑，942十五层实用；二十七只潜力未实测。','',f'共{len(rows)}字段；卡图未检出同类误解，不提修改。','']
for r in rows:ls += ['## '+r['path']+' '+r['field'],'',r['sha256'],'','旧：'+r['before'],'','新：'+r['after'],'','证据：ch-0845 L64598—64607；ch-0942 L70485—70510。','']
f.with_suffix('.md').write_text('\n'.join(ls),encoding='utf-8');print(f.name,sha(f),len(rows))
