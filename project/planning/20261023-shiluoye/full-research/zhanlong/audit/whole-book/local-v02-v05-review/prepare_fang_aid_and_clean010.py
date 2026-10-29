import copy,json,hashlib
from save_manual_batch import P,ROOT,F,read,write,sha
b=P/'adjudications-local-v05-batch009.json';rows=read(b);before=next(x for x in rows if x['candidate_id'].endswith('0098-01'));after=copy.deepcopy(before)
after['status']='partial'
after['rationale']=before['rationale']+' 城战结果已答，但原题指定的方新二百万援凡书是否同量实际抵城仍未独证，故复合项保partial，不据此说方全未援。'
proposal={'status':'proposal-pending-primary-review-not-applied','reason':'按primary已完整主审意见，限定原题指定军援与城战复合口径。','changes':[{'path':b.name,'candidate_id':before['candidate_id'],'input_sha256':sha(b),'before':before,'after':after,'scope':'仅status与理由补一句，后证/域/其余19逐值不变'}]}
write(P/'fang-two-million-specific-aid-proposal.json',proposal)
print('proposal',sha(P/'fang-two-million-specific-aid-proposal.json'))
# 010尚未向primary交付：自核发现铠真正取得1126，保未送审中稿，改正局部章号与证据。
b=P/'adjudications-local-v05-batch010.json';rows=read(b);old=copy.deepcopy(rows)
for x in rows:
 if x['candidate_id'].endswith(('0115-01','0116-01')):
  x['rationale']=x['rationale'].replace('1124第六铠','1126第六铠').replace('铠1124','铠1126')
  x['later_chapters']=[1126 if k==1124 else k for k in x['later_chapters']]
  n=next(json.loads(s) for s in (F/'vol05-chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if json.loads(s)['chapter_id']=='ch-1126')
  for e in x['later_evidence']:
   if e['chapter_id']=='ch-1124':
    e.update(chapter_id=n['chapter_id'],start_line=n['start_line'],end_line=n['end_line'])
history=P/'unsubmitted-self-check';history.mkdir(exist_ok=True)
write(history/'v05-batch010-before-armor-chapter.json',old);write(b,rows)
md=['# 《斩龙》局部候选终评草稿','卷5，offset 180—199；20项，待primary实际主审。','']
for x in rows:md += [f"- **{x['candidate_id']}** · {x['status']} / {x['audit_domain']}",f"  原题：{x['title']}",f"  终评：{x['rationale']}",f"  证据raw：{', '.join(map(str,x['later_chapters']))}；访问为正式派生，保原reader。",'']
b.with_suffix('.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
state=read(P/'reader-state.json')
for x in state['submitted_batches']:
 if x['path']==b.name:x['sha256']=sha(b)
write(P/'reader-state.json',state)
write(history/'v05-batch010-armor-chapter-delta.json',{'status':'self-check-before-submission','changes':[{'before':a,'after':z} for a,z in zip(old,rows) if a!=z],'unchanged_other_objects':18,'sha256':sha(b)})
print('batch010',sha(b))
