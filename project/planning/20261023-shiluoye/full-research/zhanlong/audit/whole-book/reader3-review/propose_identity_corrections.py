from common import P,dump,sha,evidence
import json
sc=json.loads((P/'identity-fields-scan.json').read_text(encoding='utf-8'))
subs=[
('百里伦861系统死后又现且885再斩，没有解释的重复不能擅当复活规则。','861系统所杀是玩家百里若风；NPC百里伦879仍活、885被主斩首，本例不构成NPC复活冲突。'),
('百里伦系统杀后又称未死需源异常，','861被系统击杀者为玩家百里若风，百里伦未死并不冲突；'),
('百里伦仍活重现持续861死亡矛盾。','861被杀者为玩家百里若风，NPC百里伦此时仍活不存在前死后现矛盾。'),
('火云一级/系统次级源差与百里伦死后再杀保留。','火云一级/系统次级源差保留；861系统杀的是百里若风，百里伦本章斩首不构成死后再杀。'),
('861系统清眸杀百里伦，879报未死/880出现，885主再斩。','861系统清眸击杀玩家百里若风，NPC百里伦879/880仍活、885被主斩首，原复现冲突系研究误读。'),
('无明确复活/同名说明，保源冲突不造新王。','861被杀者为玩家百里若风、NPC百里伦885才被主斩首；撤销误读造成的复现冲突，不造NPC复活或新王。'),
('并称百里伦还未死，与861清眸击杀百里伦的系统存在源冲突。','并称百里伦还未死；861清眸系统击杀的是玩家百里若风，非此NPC，不构成复现冲突。'),
('玩家复活雷熊明确不能套NPC百里伦冲突自动解释。','玩家雷熊复活与NPC百里伦分层；861被杀者为玩家百里若风，NPC此时仍活不需复活解释。'),
('861系统清眸杀百里伦vs879称未死/880同场；','861系统清眸杀玩家百里若风，NPC百里伦879/880仍活不冲突；'),
('百里伦861系统死后重现再死','861玩家百里若风被杀与NPC百里伦885斩首分人（撤复现误读）'),
('火象国王百里伦复现异常不可她解释补完。','NPC清流军统帅百里伦与861被杀的玩家百里若风分人，不存在本例的NPC死后复现；两者均不能与她合并身份。'),
('清眸系统真杀百里114分','清眸系统真杀玩家百里若风（CBN第5）114分'),
('899授龙硎上将/炎龙统，919称正二级。','899授龙忠上将/炎龙统，919称龙忠正二级镇国将军，称衔差保留；两处不是御林将领龙硎。'),
('后炎龙统领换龙硎。','后炎龙统领换龙忠，与御林龙硎分人。'),
('899获炎龙新统职位；919等级称差单列，非一直留御林任相同官。','899获炎龙新统职位及919称衔差属于龙忠，不能记作御林龙硎异动；本卡龙硎仍为御林将领。'),
('此章现三上将主罗雷、秦龙正2与899龙忠上将授衔口径差。','此章三上将为主、罗嗣、雷斯，秦烨/龙忠被称正2镇国，与899龙忠上将授衔口径差保；秦龙为原笔记过度缩略，非新姓名或龙硎。'),
('943秦龙镇国二级与899龙忠上将差留。','919秦烨/龙忠称正二级与899龙忠上将差另保；本章提撤番号者为蛟龙军秦烨，不是御林龙硎。'),
]
rs=[]
for h in sc['hits']:
 old=h['value'];new=old
 for a,b in subs:
  if a in new:new=new.replace(a,b)
 if new==old:continue
 issue='longzhong-not-longxing' if any(t in old for t in ['龙硎','秦龙','龙忠','899获炎龙新统']) and not '百里伦' in old else 'bailiruofeng-not-baililun'
 refs=[dict(evidence([n])[0],start_line=l,end_line=r) for n,l,r in ([(899,67796,67812),(919,69037,69050),(943,70581,70594)] if issue.startswith('long') else [(861,65626,65634),(879,66609,66609),(885,66927,66930)])]
 shared=h['field']=='/line/36'
 if shared:new=new.replace('乘风10/27/后实15','乘风当前10→后实15及27仅潜力未实测（非硬上限10自冲）')
 rs.append({'issue_id':issue,'path':h['path'],'sha256':h['sha256'],'field':h['field'],'before':old,'after':new,'evidence':refs,'claim_kind':'fact','apply_mode':'仅外置纠正层建议，未就地改；原reader及池原record保历史','composition_note':'此共享handoff行after合并了已批准wind更正，不回退旧10/27措辞；原before仍为实际冻结源。' if shared else ''})
f=P/'vol04-identity-two-issues-proposal.v2.json';assert not f.exists()
dump(f,{'status':'proposal-only','actual_reviewer':'/root/zongheng_vol03_full','scope':'仅百里若风/百里伦误读与龙忠/龙硎错归、相关原笔记名缩略；龙忠899至919称衔差仍保','affected_fields':rs,'scanned_documents':sc['scanned_documents'],'graph_scan':'stage/formal graph全部文本扫描，未检出两误读直接进入节点/边/知识；保持图不动。cards明确列9龙硎stage_change、18徐翊stage_change、40美丽清眸relationships（stage/formal镜像）。','reader_boundary':'新定向原文片段日志在targeted-source-access，非新增整章覆盖；不改变原逐章实读归属。','shared_field_priority':'handoff L36与已批准wind同字段，after已含两层修正；请唯一整合人按原before+组合after收录，勿用本层退回wind。'})
ls=['# 卷四两处实体误读最小纠正提案','','未就地修改冻结材料/卡图/正式库/池。龙忠上将→正2称衔差仍保；百里伦不是861被杀的玩家。','',f'{len(rs)}个直接字段；每项原SHA、before/after、固定源引用齐。','']
for r in rs:ls += ['## '+r['path']+' '+r['field'],'',r['sha256'],'','旧：'+r['before'],'','新：'+r['after'],'',r['composition_note'],'','后证：'+'；'.join(f'{e["chapter_id"]} L{e["start_line"]}—{e["end_line"]}' for e in r['evidence']),'']
f.with_suffix('.md').write_text('\n'.join(ls),encoding='utf-8');print(f.name,sha(f),len(rs))
