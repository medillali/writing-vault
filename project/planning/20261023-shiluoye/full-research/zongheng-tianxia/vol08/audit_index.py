"""只查询既有分卷研究笔记，不能计为本代理原文阅读。"""
import json,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
R=Path(__file__).parent
terms=['白血病','病危','骨髓','冰茶的病','冰茶病','奥丹','明宇','林克','林丘','封印解除','封印全部','母亲','全知','净化','性关系','第一次','结婚','婚约']
out=[]
for name in ['vol06','vol07','vol07-primary-tail']:
 p=R.parent/name/'chapter-notes.jsonl'
 if not p.exists():continue
 ns=[json.loads(x) for x in p.read_text(encoding='utf-8').splitlines() if x.strip()]
 print(name,'research_snapshot',len(ns),'last',ns[-1]['chapter_id'])
 for n in ns:
  hits=[x for x in n.get('facts',[]) if any(t in str(x) for t in terms)]
  if hits:
   row=dict(research_path=str(p.relative_to(R.parent)),chapter_id=n['chapter_id'],title=n.get('title'),start_line=n.get('start_line'),end_line=n.get('end_line'),facts=hits)
   out.append(row);print(json.dumps(row,ensure_ascii=False))
(R/'audit-research-index.json').write_text(json.dumps(dict(status='draft-index-of-derived-research-not-direct-reading',query_terms=terms,entries=out),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
