"""只读分卷交付状态，供全书综合草稿追踪来源归属。"""
import json,hashlib
from pathlib import Path
P=Path(__file__).parent;B=P.parent;S=json.loads((B/'source.json').read_text(encoding='utf-8'))
out=[]
for spec in S['volumes']:
 v=spec['volume'];d=B/f'vol{v:02d}';row=dict(volume=v,expected_body_units=spec['body_units'],files={})
 for name in ['analysis.json','cards.json','graph.json','report.md','handoff.md','reader-state.json','validation.json']:
  p=d/name
  if p.exists():row['files'][name]=dict(path=p.resolve().as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
 if (d/'reader-state.json').exists():
  st=json.loads((d/'reader-state.json').read_text(encoding='utf-8'));row.update(reader=st.get('reader'),complete_volume=st.get('complete_volume',False),next_chapter_id=st.get('next_chapter_id'),read_segments=len(st.get('read_chapter_ids',st.get('completed_chapter_ids',[]))))
 if (d/'analysis.json').exists():
  a=json.loads((d/'analysis.json').read_text(encoding='utf-8'));row['dimensions']={k:len(x.get('observations',[])) if isinstance(x,dict) else len(x) for k,x in a.get('dimensions',{}).items()}
 out.append(row)
result=dict(source_id=S['source_id'],revision=S['revision'],status='draft_in_progress',source_attribution='综合者仅亲读卷三；其他卷以其分卷研究包为派生材料，不冒称原文亲读。',volumes=out)
(P/'material-inventory.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for r in out: print(json.dumps({k:r[k] for k in r if k!='files'},ensure_ascii=False))
