"""只打包人工写明的重点结论与已读证据，保材料访问归属。"""
import json,copy,datetime
from save_manual_batch import P,A,B,F,ROOT,read,write,sha
notes={};paths={}
for v in range(1,7):
 f=F/f'vol{v:02d}-chapter-notes.jsonl'
 for s in f.read_text(encoding='utf-8').splitlines():
  n=json.loads(s);k=int(n['chapter_id'].split('-')[1]);notes[k]=n;paths[k]=f
def E(k):
 n=notes[k];p=paths[k]
 if 1375<=k<=1386:
  name='batch1375-1376.json' if k<=1376 else 'batch1377-1380.json' if k<=1380 else 'batch1381-1384.json' if k<=1384 else 'batch1385-1386.json'
  p=B/'primary-ending-reread'/name
  return dict(source_id=n['source_id'],revision=n['revision'],chapter_id=n['chapter_id'],start_line=n['start_line'],end_line=n['end_line'],claim_kind='fact',access_level='derived-primary-independent-ending-reread',research_path=str(p.relative_to(ROOT)).replace('\\','/'),material_sha256=sha(p),source_reader='primary独立复核；首次分卷reader不改')
 return dict(source_id=n['source_id'],revision=n['revision'],chapter_id=n['chapter_id'],start_line=n['start_line'],end_line=n['end_line'],claim_kind='fact',access_level='derived-formal-chapter-notes',research_path=str(p.relative_to(ROOT)).replace('\\','/'),material_sha256=sha(p),source_reader=n.get('reader'))
def O(k,start,end,issue):
 p=A/'priority-corrections-delta.json'
 return dict(source_id=notes[k]['source_id'],revision=notes[k]['revision'],chapter_id=notes[k]['chapter_id'],start_line=start,end_line=end,claim_kind='fact',access_level='primary-approved-reading-overlay',research_path=str(p.relative_to(ROOT)).replace('\\','/'),material_sha256=sha(p),source_reader='primary及原复核者，未转移原文阅读归属',issue_id=issue)
def C(key,title,status,chain,conclusion,limits,chapters,extra=None):
 return dict(key=key,title=title,terminal_status=status,stage_chain=chain,conclusion=conclusion,limits_and_counterevidence=limits,evidence=[E(k) for k in chapters]+(extra or []),review_status='draft')
def savepart(num,items):
 assert items and len({x['key'] for x in items})==len(items)
 p=A/f'focused-findings-part{num:02d}.json';assert not p.exists()
 base=read(P/'input-receipt.json')
 write(p,dict(source_id=base['source_id'],revision=next(iter(notes.values()))['revision'],status='draft-pending-actual-primary-review',formal_input_sha256=base['formal_input_sha256'],findings=items))
 out=['# 《斩龙》全书重点终态核查草稿',f'第{num}组，{len(items)}项；逐项主审前保持draft。','本代理亲读卷2 prefix及卷5；卷2尾和跨卷据正式四栏/主审复核派生，未自称个人重新全文读全书。','']
 for x in items:
  out += [f"## {x['title']}（{x['key']}）",f"终点状态：{x['terminal_status']}",'']+[f'- {s}' for s in x['stage_chain']]+['',x['conclusion'],'',f"限制与反证：{x['limits_and_counterevidence']}",f"证据raw：{', '.join(e['chapter_id'] for e in x['evidence'])}",'']
 p.with_suffix('.md').write_text('\n'.join(out)+'\n',encoding='utf-8');print(p.name,sha(p))
