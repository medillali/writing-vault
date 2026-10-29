"""主审已实际读三处原文和十三字段提案，保存附加优先层。"""
from check_volume import ROOT,WORK,read
from pathlib import Path
import copy,hashlib,json,sys
sys.stdout.reconfigure(encoding='utf-8')
A=WORK/'zhanlong/audit/whole-book';p=A/'local-v03-v06-review/priority-ring-corrections-proposal.json'
def sha(q):return hashlib.sha256(q.read_bytes()).hexdigest()
assert sha(p)=='42f38a82b9103ff1b67540913da3011dfa6f9e74f2bf8cbd33c9d23e9f0eb38c'
proposal=read(p);assert len(proposal['affected_fields'])==13
for c in proposal['affected_fields']:
 q=ROOT/c['file'];assert sha(q)==c['input_sha256'],c['file']
 if 'jsonl_index' in c:
  value=[json.loads(line) for line in q.read_text(encoding='utf-8').splitlines() if line.strip()][c['jsonl_index']];keys=c['json_path_within_row']
 else:value=read(q);keys=c['json_path']
 for key in keys:value=value[key]
 assert value==c['before'],c
out=copy.deepcopy(proposal)
out['primary_approval']=dict(reviewer='primary',status='approved-for-library-reading-overlay',user_approval=False,proposal_sha256=sha(p),scope='只收窄自身指代的旧研究断言，不改冻结原稿/原reader/read_at；不倒灌后强化面板。',actual_verification=[dict(chapter_id='ch-0530',start_line=42940,end_line=42963,full_raw_reread_this_turn=False),dict(chapter_id='ch-0541',start_line=43770,end_line=43784,full_raw_reread_this_turn=False),dict(chapter_id='ch-1109',start_line=81317,end_line=81329,full_raw_reread_this_turn=False)],findings='原句的自身可分配指每个友方目标，541实际全体玩家获回血与1109同句式下队友回血印证；无依据认原句限定只佩戴者，不再列必然源冲突。')
out['approval_precedence']='原提案status是历史字段，当前按primary_approval与proposed_after阅读。'
formal=ROOT/'writing-vault/library/reports/zhanlong/audit'
f=formal/'priority-corrections-kings-domain.json';assert not f.exists();f.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
md='# 王者领域回血范围的优先纠正\n\n主代理已核对三处原文，研究仍待用户审阅。530的面板句先说所有友方目标，再说每秒获自身10%回血；“自身”可指各受益目标自身血量，不能强读成只有佩戴者回血。541实际各会玩家均获回血，1109强化后仍用同句式并明确解释为队友回血。旧笔记据此列出的必然规则冲突撤回。\n\n保留初版500码、100%、120秒、120怒和12小时；不把1109强化版1000码、150%、10分钟等倒灌初版。蛮王当阶段尚未杀/分装仍保留。[十三字段前后和核源](priority-corrections-kings-domain.json)。\n\n[狮王盾另一项纠正](priority-corrections-lion-shield.md) · [本书入口](../README.md) · [卷三报告](../vol03.md)\n'
(formal/'priority-corrections-kings-domain.md').write_text(md,encoding='utf-8')
combined=A/'priority-corrections-delta.json';old=read(combined)
assert len(old['affected_fields'])==11
history=A/'priority-corrections-before-ring.json';assert not history.exists();history.write_bytes(combined.read_bytes())
merged=dict(schema_version='explicit-priority-reading-overlays-v1',status='primary-approved-not-in-place-mutated',operation='preserve-frozen-originals-and-prioritize-corrected-reading',issues=[old,out],affected_fields=old['affected_fields']+out['affected_fields'],primary_approval=dict(reviewer='primary',status='approved-for-library-reading-overlay',user_approval=False,approved_issues=2,approved_fields=24),formal_reading_entries=['audit/priority-corrections-lion-shield.md','audit/priority-corrections-kings-domain.md'])
combined.write_text(json.dumps(merged,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(approved_fields=13,combined_fields=24,formal_sha256=sha(f),original_files_unchanged=True)))
