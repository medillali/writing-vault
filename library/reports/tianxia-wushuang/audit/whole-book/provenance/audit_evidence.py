"""审计派生证据装配，不读取或代读正文。"""
import json,pathlib
H=pathlib.Path(__file__).resolve().parent;B=H.parents[1];R=H.parents[5]
source=json.loads((B/'source.json').read_text(encoding='utf-8'));chapters={int(x['chapter_id'][3:]):x for x in source['chapters']}
volume_by_id={s['chapter_id']:v['volume'] for v in source['volumes'] for u in v['units'] for s in u['segments']}
def evidence(ids):
 out=[]
 for i in sorted(set(ids)):
  c=chapters[i];v=c.get('volume') or volume_by_id[c['chapter_id']]
  out.append(dict(source_id=source['source_id'],revision=source['revision'],chapter_id=c['chapter_id'],start_line=c['start_line'],end_line=c['end_line'],claim_kind='fact',access_level='direct-reading-by-this-agent-prior-assigned-volume' if v in [5,7] else 'derived-formal-volume-research',research_path=f'writing-vault/library/reports/tianxia-wushuang/vol{v:02d}-analysis.json'))
 return out
def dump_group(filename,rows,kind,title):
 key='characters' if kind=='characters' else 'findings'
 inventory=json.loads((H/'input-inventory.json').read_text(encoding='utf-8'))
 obj=dict(title=title,status='draft_pending_primary_semantic_review',scope='无双八卷正式研究的派生终点复核；本代理亲读卷五/七，未个人重新阅读全文。',method='按各卷人物状态、历史问题/线程与必要四栏笔记逐段比较，事实/推断/未知分层；不借纵横或斩龙倒灌。',formal_input_sha256=inventory['formal_input_sha256'],**{key:rows})
 p=H/filename;p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 import hashlib
 return hashlib.sha256(p.read_bytes()).hexdigest()
def render_characters(filename,rows,title):
 lines=['# '+title,'','本组为待主审派生研究，亲读归属仅卷五/七；其余按已交付正式研究定位。','']
 for x in rows:
  lines += [f"## {x['audit_id']} {x['name']}",'',f"起点：{x['initial_comparison_stage']}",'',f"决定：{x['key_decisions']}",'',f"代价：{x['costs']}",'',f"终态：{x['terminal_state']}",'',f"边界：{x['evidence_boundaries']}",'','证据raw：'+', '.join(e['chapter_id'][3:] for e in x['evidence']),'']
 (H/filename).write_text('\n'.join(lines),encoding='utf-8')
