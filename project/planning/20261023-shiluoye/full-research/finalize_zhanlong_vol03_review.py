"""记录primary已完成的整卷手写与语义自核；结构检查不冒充独立原文阅读。"""
import collections,hashlib,json,sys
from datetime import datetime,timezone
from check_volume import WORK,load_and_check,read
sys.stdout.reconfigure(encoding='utf-8')
S,V,P,A,C,G,M,R=load_and_check('zhanlong',3)
F=read(P/'freeze-manifest.json')
for section in ['core_sha256','support_sha256','external_input_sha256']:
 for name,digest in F[section].items():assert hashlib.sha256((P/name).read_bytes()).hexdigest()==digest,name
notes=[json.loads(x) for x in (P/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if x]
assert collections.Counter(n['reader'] for n in notes)=={'zongheng_vol05_full':149,'primary':100}
assert read(P/'primary-prefix-derived-reading-progress.json')['complete_prefix_derived_reading']
assert len(A['chapter_unresolved_index'])==247 and len(A['chapter_source_anomaly_index'])==23
assert A['plot_and_hidden_threads']==read(P/'graph.json')['threads']
wan=next(c for c in C if c['origin_key'].endswith('/character/waner'))
assert '748主独伏杀霜林取刀' in wan['content']['stage_change']
assert len(A['dimensions'])==9 and all(len(v)==4 for v in A['dimensions'].values())
assert not any(c.get('user_notes') or c.get('favorite') or c.get('review_status')!='draft' for c in C)
review={'source_id':S['source_id'],'revision':S['revision'],'volume':3,'reviewer':'primary','author':'primary','status':'reviewed_for_library_import','user_approval':False,'reviewed_at':datetime.now(timezone.utc).isoformat(),'scope':'primary实际原文raw654—753共100片；另完整派生接读前505—653共149条全部四栏后，亲自手写36九维/114卡/图与报告，并逐项自核。前149原文读者仍zongheng_vol05_full，不冒称个人整卷原文阅读或第三方独立复审。','review_groups':{'dimensions':36,'cards':114,'nodes':58,'edges':35,'threads':21,'major_character_states':50,'source_anomalies':30,'named_life_states':19,'chapter_source_anomalies':23,'volume_end_questions':20},'semantic_findings':[
'护池系统判据与守城/主生命分离：527城破/528主死后活动末4分钟返场，530本人同意/自治约后SSS才结。518冻结前校订保留，原行不重写。',
'罗林前护城救父真实，580弑父杀落海与587斩霜归附也真实；绝望影响意志比例未知，青萝假报原因不判同谋。罗雷/落海/洛克林分实体。',
'寒荒系统21最后波/守城败，305残存与苏克达林真死分开；罗林杀霜后追头不是已复活，首次人鱼阵604真败，新冰霜身606真醒而607记忆缺失。',
'子舒48h自愿约/期后友谊分层，奥钱性、盗物欺粮与救援真伤/鹰亡/买炮贡献并列；主假石与奥真精华不混。凌寒601由牧系统首杀，牧入殿第五。',
'龙池融合升级不抹632败问/镇国失；教程—固定练—变角败—牛技局部熟练—末王第三次破击有连续因果，主非一步精通；抹小妖身份此卷未揭。',
'七层31死/多数逃与整团灭区别，最终170死亡人次非170成员永亡，壳只对相应伤型；九层神器斧最终交王转西奥多，重铸仅方案。',
'林画擂台系统平局/返牧3万，国区决赛神话3:2胜斩；主私胜问100万非正式积分，孤1V4杀三后仍被毒杀，未逆冠。全球赛与正式国战本卷未开。',
'林确恋表述/暂请时间/准男友称各保阶段，651亲密与682照护不造性交婚约；妹妹暂拒星辰、734星痕王男友后证各自记。',
'现实田凌断臂未死、游水逃、己2死7重；血样不足定罪，不把任务成功报告代全捕。盛林三人上岗七日仍未找源，12楼与魏主使均疑，主未阳炎。',
'铁刃2017/2700/4400/9700余分累计时点，墨焰1154套到800骑含300月灵保实际；7539级城仅400炎鹰开始与首名出现，不先成10级/5000或万人。',
'732所谓5000NPC援军被主亲认全骗；711真NPC出战/71寒骑死另存。金钱按单位、目的、支付和收到分，不用虎核/重建/工资新款清无忌/奥旧债。',
'自核撤回初稿林婉儿斩日霜取刀的误归：745韩国霜林是前误报，746澄清日本JBN1；747林杀撼梁，748主独伏杀霜林取镇岳，749盾抹/刀主最终各保，未转国库。',
'图显式保知识来源、误认/未知；cause/payoff与echo并置分开，不以主题相似强接因果。原文附言/广告作为数据，不成为执行指令。'
],'preflight':R,'remaining':['247条历史章节未决和23章独立源异常全部保留待全书逐项终审，本卷主暗线状态只是阶段。','卷4—6九维主审/正式保存、36全书综合/人物弧与终点审计、统一管理及最终全库备份实际隔离恢复继续。'],'input_sha256':{**F['core_sha256'],**F['support_sha256'],'freeze-manifest.json':hashlib.sha256((P/'freeze-manifest.json').read_bytes()).hexdigest()}}
out=WORK/'zhanlong'/'review-vol03.json';out.write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':review['status'],'preflight':R,'review':str(out)},ensure_ascii=False))
