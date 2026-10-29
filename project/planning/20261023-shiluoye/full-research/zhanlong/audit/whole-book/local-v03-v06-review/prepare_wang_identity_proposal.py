"""仅提交外置与已签010的逐值提案；不修改任何旧材料。"""
from pathlib import Path
import json,hashlib,copy,sys
sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;A=H.parent;R=Path('C:/Users/Administrator/Documents/ChatGPT/Novel');F=R/'writing-vault/library/reports/zhanlong'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
scan=json.loads((A/'wangjiang-wangjian-identity-scan.json').read_text(encoding='utf-8'));changes=[]
replacements={
'王翦／王将｜卷二阶段':'王翦｜卷二阶段',
'斩龙一分领袖/前排骨干，现实陪护秦雨并表白。':'斩龙第一分盟领袖/前排骨干；现实陪秦雨并表白者是独立玩家王将。',
'保同伴、取得战斗位并与若雨发展。':'保同伴、取得战斗位；王将对若雨的情感目标不归本角色。',
'多次真死复、掉级；若雨哀悼兄并未答应恋人。':'多次真死复、掉级；若雨暂拒的是独立玩家王将，不是王翦。',
'为主吸火/后王战救刺再死，接让装与SS旋；向若雨说爱且愿等。':'为主吸火/后王战救刺再死，接让装与SS旋。',
'秦雨暂称现在不能，不能写已情侣；一分权限不等兄弟间无利益安排。':'与主、李牧互救并有一分盟权限；王将和王翦分人，500秦雨暂拒王将，不归王翦。'}
excluded=[]
for hit in scan['current_material_hits']:
 p=hit['path'];old=hit['value']
 if p.endswith('character-arcs-part03.json'):continue
 if 'chapter-notes' in p or 'prefix-chapter-notes' in p or '/batch-' in p:
  excluded.append(dict(path=p,field_path=hit['field_path'],reason='原笔记已经把两人同场分别记，斜杠为三人名单/两人对照，保原值'));continue
 new=old
 for before,after in replacements.items():new=new.replace(before,after)
 if p.endswith('research_characters.py'):new=new.replace("'王翦／王将'","'王翦'")
 if p.endswith('handoff.md'):new=new.replace('王翦/王将','王翦、王将（独立两人）')
 if new!=old:changes.append(dict(path=p,input_sha256=hit['sha256'],field_path=hit['field_path'],before=old,proposed_after=new))
view=R/'writing-vault/library/views/chr-04223464f4115843afe8e06dd1c4f08d.md'
already={tuple(c['field_path']) for c in changes if c['path']==view.relative_to(R).as_posix()}
for n,line in enumerate(view.read_text(encoding='utf-8').splitlines(),1):
 if ('line',n) in already:continue
 new=line
 for before,after in replacements.items():new=new.replace(before,after)
 if line!=new:changes.append(dict(path=view.relative_to(R).as_posix(),input_sha256=sha(view),field_path=['line',n],before=line,proposed_after=new))
part=A/'character-arcs-part03.json';d=json.loads(part.read_text(encoding='utf-8'));row=d['characters'][3];proposed=copy.deepcopy(row)
proposed['key_decisions']='接受主纠错、守后队与吸火任务，作为一分领袖承担组织分工。658/659与星痕现实台球和互给ID，734她称王翦为男友，确立这条关系后证；499—500照护秦雨并表白的是独立玩家王将，不属于王翦。后多次骑兵突击、护炮撤退与情报转述，获断海等装备后仍与多人轮锋；956列斩龙殿第七，二国战被玫瑰杀后继续战线。'
proposed['costs']='冲阵、护后和被强敌集中击杀带来游戏死亡与掉级；装备资格不能被分配意图跳过。与星痕关系按734称谓及后同住消息记录，不擅补分手、争执或性交细节；秦雨暂拒王将的代价不归王翦。'
proposed['terminal_state']='仍为斩龙前线骨干和分路指挥，游戏死后持续返场；关系至少在734已确认星痕称王翦男友，卷四东城转述同住，终点没有专门否定或新婚证明。王将对秦雨的情感线不归王翦，也不以听说同住宣现场亲见性关系。'
proposed['evidence_boundaries']='玩家王翦与NPC军将分域；甲剑取得、穿戴和后续更换按时点。战场情报转述不作他亲见所有幕后。王将与王翦有499同句互指及445/1199同场分职业证；734王翦与星痕的关系独立成立，不把500王将的暂拒误排为王翦前段恋情。'
proposed['evidence']=[e for e in proposed['evidence'] if e['chapter_id'] not in ['ch-0499','ch-0500']]
sigchanges=[dict(path=['characters',3,k],before=row[k],proposed_after=proposed[k]) for k in row if proposed[k]!=row[k]]
sid=d['source_id'];rev=d['revision'];evidence=[dict(source_id=sid,revision=rev,chapter_id=f'ch-{n:04d}',start_line=lo,end_line=hi,claim_kind='fact') for n,lo,hi in [(499,40953,40992),(500,41038,41043),(445,37035,37043),(1199,87365,87384)]]
pool_mentions=[]
for file in ['local-question-pool.json','historical-question-pool.json']:
 p=A/file;data=json.loads(p.read_text(encoding='utf-8'))
 for c in data.get('candidates',data.get('questions',[])):
  t=c.get('terminal_assessment') or {};s=t.get('rationale','')
  if '王将' in s:pool_mentions.append(dict(pool=file,pool_sha256=sha(p),candidate_id=c.get('candidate_id'),title=c.get('title'),rationale=s,provisional_scan_class='ordinary_grammar_not_character' if c.get('candidate_id') in ['v04-local-chapter_unresolved_index-0034-01','v04-local-chapter_unresolved_index-0060-01'] else 'correct_separate_wangjiang_identity_no_change'))
out=dict(status='proposal_pending_primary_not_applied',issue='王将与王翦被派生研究误合；二人源文明示分体',source_id=sid,revision=rev,actual_reviewer='zongheng_vol05_full',reading_scope='本次实际完整再读raw499 L40949—41036、raw500 L41037—41107；有限定向读445/1199明确分人行及407/479/481/495/496原卡技能装备上下文，后者不冒整章复读。首次覆盖不增，原reader不变。',evidence=evidence,changes=changes,signed_character_changes=dict(path=part.relative_to(R).as_posix(),input_sha256=sha(part),old_md_sha256=sha(part.with_suffix('.md')),audit_id='character-arc-010',changes=sigchanges,other_characters_unchanged_required=True),excluded_correct_fields=excluded,pool_scan=dict(initial_cross_identity_hits=scan['pool_terminal_hits'],all_wangjiang_terminal_mentions=pool_mentions,rule='仅定位/读后判断，未改两池或任何已签候选；原题/record一律保留。'),new_entity_proposal=dict(name='王将',entity_type='player_and_real_person',proposed_audit_id='character-arc-047',owner='zongheng_vol05_full',boundary='在本代理46原分配之外追加独立人物，不重编号已签；500若雨暂拒，1199第一分盟长老212狂战，与王翦剑士/龙骑不同；待primary批准再写人物。'),reading_precedence='获批后用外置解释层优先，冻结六卷/卡/view/历史导入字节不改。原行误合不作为小说改名或恋情转移的证据。')
q=A/'priority-corrections-wang-identity-proposal.json';q.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
md=['# 王将／王翦分人及已签010最小外置提案','','原冻结/两池/已签人物未改。raw499/500本次完整再读；L40992王将亲说“我和王翦”，445两职业列第2/第9，1199同场再分狂战与龙骑。','',f'当前材料拟外置{len(changes)}字段；010另{len(sigchanges)}字段仅提案。原正确四栏同场名单不改。','']
for c in changes:md+=['- '+c['path']+' '+str(c['field_path'])+' SHA '+c['input_sha256'],'  - before：'+c['before'],'  - after：'+c['proposed_after']]
md+=['','## 已签010单独待批','']
for c in sigchanges:md+=['- '+str(c['path']),'  - before：'+json.dumps(c['before'],ensure_ascii=False),'  - after：'+json.dumps(c['proposed_after'],ensure_ascii=False)]
md+=['','两池原题/原记录不改；终评所有王将提及另在JSON完整列出供语义核对，检索不冒全文。']
q.with_suffix('.md').write_text('\n'.join(md)+'\n',encoding='utf-8');print(json.dumps(dict(json_sha256=sha(q),md_sha256=sha(q.with_suffix('.md')),external_fields=len(changes),signed_character_fields=len(sigchanges),correct_excluded=len(excluded),pool_mentions=len(pool_mentions),all_mentions=[dict(candidate_id=x['candidate_id'],rationale=x['rationale']) for x in pool_mentions]),ensure_ascii=False,indent=2))
