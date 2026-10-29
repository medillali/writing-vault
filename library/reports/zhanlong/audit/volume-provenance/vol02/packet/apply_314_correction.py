"""只应用primary已指出的四个定向语义更正；原笔记保留。"""
import pathlib,json,hashlib,sys
sys.stdout.reconfigure(encoding='utf-8');P=pathlib.Path(__file__).parent
def replace(n,a,b):
 p=P/n;s=p.read_text(encoding='utf-8');assert s.count(a)==1,(n,a);p.write_text(s.replace(a,b),encoding='utf-8')
replace('research_dimensions.py','不可用卷五身份倒称本卷失误都装。','不可用后卷信息倒称本卷失误都装。')
p=P/'research_dimensions.py';s=p.read_text(encoding='utf-8');marker="obs('continuity','分卷共同全文不冒个人整卷或全书',";assert s.count(marker)==1
s=s.split(marker)[0]+"""obs('continuity','同场两剑的指代与流转分离',
 '314主先收巴林佩剑入包；26902—06看的却是流霜自己的斩华，她说请九黎大师重铸刻名。26912—23回龙城另持巴林权力剑献罗/建议毁，罗同意并带走；406霜再持斩华不矛盾。','连续场面中相近名词不保证同物，镜头对象和交接动作优先于研究者的顺读联想。','给两物独立持有链：霜自己的斩华与暂由主收、后霜持交罗的巴林权力剑；每次代词回指核最近明示对象，跨场再用时只接证过的物。','权力剑实交有证，毁剑只有建议与罗同意，未现场毁；不以噬灵后来参战替代人格解放/毁剑回执，也不虚构斩华失而复得。',[314,406])
""";p.write_text(s,encoding='utf-8')
p=P/'research_graph.py';ls=p.read_text(encoding='utf-8').splitlines();assert sum(x.startswith("question('zhanhua'") for x in ls)==1;p.write_text('\n'.join(x for x in ls if not x.startswith("question('zhanhua'"))+'\n',encoding='utf-8')
replace('research_scenes.py','无水晶通道/姐妹目的不同','无水晶通道/双方目的不同')
replace('report.md','- 斩华314作为巴林权剑交罗林拟毁，406流霜使用同名剑，中间物链未明；不能自造毁后重铸。巴林四儿后态、囚女释放与毁剑诺也保留。','- 314同场有两剑：斩华是流霜自己的剑，巴林权力之剑才交罗林并被建议销毁；406霜持斩华不构成物链缺口。此前研究误合已撤回，原笔记保留，[优先更正](priority-corrections-delta.json)附原文定位。权力剑毁剑只有建议/同意，未见现场毁；巴林四儿后态、囚女释放也分别保留。')
replace('handoff.md','巴林311—315线：四儿背景/囚女放免、罗答毁权剑还人格未见专门回执；314剑名斩华/交罗拟毁，406霜又用同名，中间如何流转或是否同物未证，不自造重铸。','巴林311—315线：四儿背景/囚女放免、罗答毁权剑还人格未见专门回执。两剑必须分开：314L26902—06斩华是流霜自己的剑；L26912—23献罗/建议毁的是巴林权力之剑，406霜用斩华没有流转异常。旧研究误合已撤回，原314笔记措辞保留，[优先更正overlay](priority-corrections-delta.json)提供完整before/更正与证据，不声称原笔记已就地改写。')
replace('handoff.md','45观察/16末问','45观察/15末问')
replace('handoff.md','本代理将继续卷五raw1019','本代理已续卷五至1036、next1037')
S=json.loads((P.parent/'source.json').read_text(encoding='utf-8'));n=next(json.loads(x) for x in (P/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if json.loads(x)['chapter_id']=='ch-0314')
def e(a,b):return {'source_id':S['source_id'],'revision':S['revision'],'chapter_id':'ch-0314','start_line':a,'end_line':b,'claim_kind':'fact'}
overlay={'status':'applied-as-priority-reading-overlay-original-notes-unchanged','reviewer':'primary','user_approval':False,'source_id':S['source_id'],'revision':S['revision'],'correction_id':'v02-research-correction-raw0314-two-swords','original_record':n,'original_record_sha256':hashlib.sha256(json.dumps(n,ensure_ascii=False,sort_keys=True).encode('utf-8')).hexdigest(),'original_notes_file_sha256':hashlib.sha256((P/'chapter-notes.jsonl').read_bytes()).hexdigest(),'original_field':'ch-0314/facts/2','before':n['facts'][2],'corrected_reading':'敷药后流霜止血能走；她提起的是自己长剑斩华，说明来历不明、曾请九黎大师重铸刻名，希望最后杀死自己。回龙城时她另外握巴林佩剑/权力之剑，献罗林并建议当噬灵面毁掉诅咒剑还人格；罗林同意、持巴林佩剑出发，但没有现场毁剑。两剑不是一件。','withdrawn_research_claim':'撤回v02-q-zhanhua：314巴林权剑名斩华/交罗拟毁→406霜再持的假物链；这是研究者误合，不是源文连续性异常。','retained_open_boundary':'巴林权力之剑毁剑仅建议与罗同意，未见现场毁；不以噬灵后参战代毁剑证。斩华来历不明是霜自说，不另造流转故事。','evidence':[e(26901,26906),e(26912,26923)],'reread_receipt':{'reader':'/root/zongheng_vol04_full','method':'read_chapters.py zhanlong 314实际完整BEGIN—END回读','start_line':26847,'end_line':26930,'full_text_read':True,'reason':'primary主审指出两剑误合后必要回读，不增加原覆盖计数。'},'primary_request':'主代理已完整回读314指出误合，要求原笔记不静改另加overlay；本更正不冒用户审批。','priority':'读本卷原314笔记及研究旧快照时先看此纠正；当前analysis/report/handoff已撤假问，原笔记/旧before保历史。'}
(P/'priority-corrections-delta.json').write_text(json.dumps(overlay,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(P/'priority-corrections.md').write_text('# 优先阅读更正：raw314同场两剑\n\n斩华是流霜自己的剑（L26902—06）。献罗林/被建议毁掉的是另一把巴林权力之剑（L26912—23）。旧整合把二者误合形成假疑点，现已撤回；权力剑只有同意毁、未现场毁的边界仍保。原逐章笔记不改，[完整before与证据overlay](priority-corrections-delta.json)优先解释旧模糊记录。\n',encoding='utf-8')
print('四项定向更正与原笔记优先overlay已写；待重建/逐值delta核。')
