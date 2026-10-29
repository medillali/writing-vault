"""更新本代理进度与交接；保留旧进度快照，不触碰root签审账。"""
from pathlib import Path
import json,hashlib,datetime,sys
sys.stdout.reconfigure(encoding='utf-8')
R=Path('C:/Users/Administrator/Documents/ChatGPT/Novel');A=Path(__file__).resolve().parent.parent
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
vr=load(A/'character-arcs-self-validation.json')
ledger_path=A.parents[1]/'primary-research-group-review-progress.json';ledger=load(ledger_path)
signed={x['path']:x for x in ledger['groups']}
snapshot=A/'local-v03-v06-review/corrections/self-character-closeout-progress'
assert not snapshot.exists();snapshot.mkdir(parents=True)
for name in ['character-arc-reading-progress.json','character-arc-assignment.json']:
 (snapshot/name).write_bytes((A/name).read_bytes())
progress=load(A/'character-arc-reading-progress.json')
progress['status']='self_assigned_character_research_delivered_pending_primary_final_review_and_assembly'
progress['observations_are_chronological_history']='旧观察保留真实发现顺序；已被后续核源撤回的假设不再作为最终事实，现行判断见current_corrections与稳定分组。'
progress['read_scope'] += [
 dict(path='writing-vault/library/reports/zhanlong/vol02-chapter-notes.jsonl',scope='补核完整接读265/355/442/443四栏原行，265/355原reader为root/zongheng_vol04_full，442/443为primary；未新增本人原文整章覆盖。'),
 dict(path='writing-vault/library/reports/zhanlong/vol04-chapter-notes.jsonl',scope='补核完整接读853/854/959/960四栏原行，原reader=root/zongheng_vol03_full。'),
 dict(path='writing-vault/library/reports/zhanlong/vol05-chapter-notes.jsonl',scope='补核完整接读1006/1044四栏原行，原reader=root/zongheng_vol04_full。'),
 dict(path='writing-vault/library/reports/zhanlong/vol06-chapter-notes.jsonl',scope='本次再读1275/1276/1277/1280/1351/1352/1356/1357/1358/1359完整四栏，初读归本人。'),
 dict(path='normalized fixed SID/rev',scope='本次实际完整再读1352全部L97275—97343；定向再读楚社交1159 L84605—84660、裴959 L71620—71657/960 L71690—71724、443 L36933—36940、投诉1266/1267 L91644—91700、末尾1386 L99656—99695/99754—99818和1359 L97756—97783。source-matches欧阳输出曾截，漏段已用91644—91700补读；不冒本次整章1159或整卷新覆盖。'),
 dict(path='current merged historical/local question pools',scope='裴相关11条当前终评的完整具体理由、状态和全部章行已读，非全池重读。')]
progress['current_corrections']=[
 '王将与王翦为两人；秦雨500暂拒归王将。卷二旧误合38字段由formal优先层解释，010五字段已按primary批准受控应用，当前part03为e530080…，待root独立重放重签，不覆盖冻结来源。',
 '狐狸规范刘庸/琉璃狐，慕天仅旧派生误名，不再列小说姓名漂移；雷月为同一收养家庭义兄妹，不称血缘亲妹。',
 '005已精确1357祭墓/1359沈母签授权；part06 stage依赖迁additional_support后root已重签。',
 '裴社交称呼原文安迪，L71706/10/13为沈/主所叫，未演本人报Andy英文；新044已按实际句法写，旧notes原件保。',
 '047独立王将获root批准且part07已签；043技术原型三人接口、046组织接口不强称个人弧。']
progress['groups_delivered']=[]
for g in vr['groups']:
 s=signed.get(g['path']);ok=bool(s and s['sha256']==g['json_sha256'])
 progress['groups_delivered'].append(dict(**g,status='primary_signed_current_bytes' if ok else 'stable_delivered_pending_primary_current_bytes'))
progress['pending']='自辖47研究条/8组全部交付；待primary完成当前字节复核和整书组装。自辖128唯一阶段卡→47研究条映射另列；不改另两读者人物范围，不重编号，不以本代理材料冒称全书总人物稿。'
progress['pending_proposals']=[]
progress['controlled_applied_corrections']=['character-arcs-part03-approved-wang-identity-delta.json','character-arcs-part06-approved-support-delta.json']
dump(A/'character-arc-reading-progress.json',progress)
assignment=load(A/'character-arc-assignment.json')
assignment['self_scope']='原39阶段人物归并+7补核+经primary批准独立王将047=47研究条（45人物研究+2接口）；不称47个独立人物'
assignment['delivered_ids']=sorted(x for g in vr['groups'] for x in g['audit_ids'])
assignment['proposed_addition']['status']='primary_approved_and_character_arc_047_delivered_in_signed_part07'
assignment['mapping']='character-arcs-self-stage-card-mapping.json'
dump(A/'character-arc-assignment.json',assignment)
handoff=dict(status='self_scope_complete_pending_primary_final_review_and_root_assembly',actual_reviewer='zongheng_vol05_full',
 scope='八个稳定分组47研究条；本代理不覆盖reader3/reader4范围，不生成冒充全书覆盖的总稿。',
 groups=progress['groups_delivered'],counts=vr['counts'],
 validation_path='character-arcs-self-validation.json',validation_sha256=sha(A/'character-arcs-self-validation.json'),
 mapping_path='character-arcs-self-stage-card-mapping.json',mapping_sha256=sha(A/'character-arcs-self-stage-card-mapping.json'),
 reading_progress_sha256=sha(A/'character-arc-reading-progress.json'),
 root_ledger_observed_sha256=sha(ledger_path),
 assembly_rules=['按audit_id合并已审稳定row，逐值保持；不把wrapper待审状态写进row，row仍draft。',
  'formal_input仅writing-vault；additional_support保存stage池依赖，不丢依赖也不让portable恢复要求旧.planning。',
  '010新证据材料走正式王身份纠正回执f1而非private TXT，原23refs保序+4=27；旧cff只历史。',
  '128唯一阶段卡只计128；一张旧合卡有010/047两个目标，不能以链接129声称新增来源卡。',
  '人物终态按渠道和域：现实死亡、玩家返场、NPC特殊复苏、数字记忆工程分开；白墨颜实醒/雷计划，订婚/婚礼，南京入队/西南完战分开。'],
 limits='结构验证通过不是primary文学签收或用户审美认可。原分卷/正式库/root账均未改；初读归属与定向再读见进度，不能说一人全文读全书。')
dump(A/'character-arcs-self-handoff.json',handoff)
md=['# 《斩龙》本代理人物研究交接','','八组47研究条已交，待primary最终当前字节复核、与另两读者材料合卷。含45人物研究条、2技术/组织接口；数量不是47个独立真人。','',
 '自辖原39归并实体来自128张唯一阶段卡；王将独立后对应40条人物研究，另7补核。旧王合卡只计一asset/origin，允许连010/047两个目标；全局271阶段卡计数不变。','',
 '来源与结构核验：699条证据全部SID/rev/章行范围、研究材料SHA有效；所有人物row仍draft；formal_input无stage依赖且研究材料无private TXT。此项不代文学主审。','',
 '|组|数量|JSON SHA256|当前主审字节状态|','|---|---|---|---|']
for g in handoff['groups']:md.append(f"|[{g['path']}]({g['path']})|{g['count']}|{g['json_sha256']}|{g['status']}|")
md+=['','[自辖阶段卡精确映射](character-arcs-self-stage-card-mapping.md) · [结构与来源验证](character-arcs-self-validation.json) · [真实接读进度](character-arc-reading-progress.json) · [010受控修订完整差分](character-arcs-part03-approved-wang-identity-delta.json)','',
 '010本次仅四文学字段和证据数组变化；其余六人、wrapper及010其他值全同，旧JSON/MD/validation/签账字节保在本代理corrections。043将TOM、刘蔚、洛鸣明确分人，只归技术原型接口；046是组织与行动接口。裴条按原文安迪称呼者为沈/主收窄，未改旧笔记。','',
 '本人原始全章覆盖仅卷三505—653、卷六1180—1386；六卷人物卡/交接实际完整派生接读与本次定向核源另有逐项记录。余原reader不改，所有冻结分卷/正式库/root签账保持。']
(A/'character-arcs-self-handoff.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
print(json.dumps(dict(handoff_sha256=sha(A/'character-arcs-self-handoff.json'),md_sha256=sha(A/'character-arcs-self-handoff.md'),reading_progress_sha256=sha(A/'character-arc-reading-progress.json'),statuses=[(x['path'],x['status']) for x in handoff['groups']]),ensure_ascii=False,indent=2))
