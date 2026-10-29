import json,hashlib,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');P=Path(__file__).parent
f=P/'adjudications-history-v01-v04.json'; old=f.read_bytes();rows=json.loads(old)
affected=['v01-thread-004','v02-question-007','v02-thread-007','v03-thread-006','v04-thread-011']
notes={json.loads(s)['chapter_id']:json.loads(s) for s in (P.parents[2]/'vol08/chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if s.strip()}
delta=[]
for x in rows:
 if x['candidate_id'] not in affected:continue
 before={k:x[k] for k in ['rationale','later_chapters','later_evidence']}
 x['rationale']=x['rationale'].replace('1595林明确拒欧爱陆','1596林明确拒欧爱陆').replace('1595拒欧','1596拒欧').replace('1595林明确爱陆','1596林当众明确爱陆并拒欧').replace('1595林公开选陆','1596林公开选陆')
 x['later_chapters']=[1596 if n==1595 else n for n in x['later_chapters']]
 x['later_chapters']=sorted(set(x['later_chapters']))
 for e in x['later_evidence']:
  if e['chapter_id']=='ch-1595':
   n=notes['ch-1596'];e['chapter_id']=n['chapter_id'];e['start_line']=n['start_line'];e['end_line']=n['end_line']
 after={k:x[k] for k in before};assert before!=after
 delta.append({'candidate_id':x['candidate_id'],'before':before,'after':after,'specific_anchor':'raw1596 L126536；1595母家聚/抗原事实不改。'})
f.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# Markdown仅重建这五条展示段，不全局替换原条或家聚段。
md=P/'adjudications-history-v01-v04.md';text=md.read_text(encoding='utf-8')
for d in delta:
 x=next(x for x in rows if x['candidate_id']==d['candidate_id'])
 text=text.replace(d['before']['rationale'],x['rationale'])
 oldev='后证：'+'；'.join(f"{e['chapter_id']} L{e['start_line']}—{e['end_line']}（reader={e['notes_reader']}）" for e in d['before']['later_evidence'])
 newev='后证：'+'；'.join(f"{e['chapter_id']} L{e['start_line']}—{e['end_line']}（reader={e['notes_reader']}）" for e in x['later_evidence'])
 text=text.replace(oldev,newev)
md.write_text(text,encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
save=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
save(P/'primary-anchor-delta.json',{'reason':'root原文确认拒欧公开爱语在1596非1595','old_json_sha256':hashlib.sha256(old).hexdigest(),'affected_count':5,'delta':delta,'new_json_sha256':sha(f),'new_md_sha256':sha(md)})
val=json.loads((P/'validation.json').read_text(encoding='utf-8'))
for a in val['artifacts']:
 p=P/a['path'].split('/')[-1]
 if p.exists():a['sha256']=sha(p);a['bytes']=p.stat().st_size
val['checks']['public_choice_1596_anchor_corrected']=True
save(P/'validation.json',val)
print(json.dumps({'affected':affected,'new_json':sha(f),'new_md':sha(md),'delta':sha(P/'primary-anchor-delta.json'),'validation':sha(P/'validation.json')},ensure_ascii=False,indent=2))
