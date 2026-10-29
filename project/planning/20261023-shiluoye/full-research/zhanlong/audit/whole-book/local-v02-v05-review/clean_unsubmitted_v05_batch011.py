import copy
from save_manual_batch import P,read,write,sha
f=P/'adjudications-local-v05-batch011.json';rows=read(f);old=copy.deepcopy(rows);r=rows[6]
a='天策主仍拒入，1359后方主动改令燕掌大节/主辞后新军权安排存在，但没有按1103百人投票重选所有节的完整制度回执。'
z='天策主仍拒入，1348后来仅提出辞大执戈/荐燕是NPC军职安排，不能当成1103百人投票重选天策诸节已执行；该投票改制未独立回执。'
assert a in r['rationale'];r['rationale']=r['rationale'].replace(a,z)
r['later_chapters']=[1348 if k==1359 else k for k in r['later_chapters']]
from save_manual_batch import F
import json
n=next(json.loads(s) for s in (F/'vol06-chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if json.loads(s)['chapter_id']=='ch-1348')
for e in r['later_evidence']:
 if e['chapter_id']=='ch-1359':e.update(chapter_id=n['chapter_id'],start_line=n['start_line'],end_line=n['end_line'])
h=P/'unsubmitted-self-check';h.mkdir(exist_ok=True);write(h/'v05-batch011-before-office-scope.json',old);write(f,rows)
src=P/'manual_v05_011.py';s=src.read_text(encoding='utf-8').replace(a,z).replace('1103,1107,1109,1359]','1103,1107,1109,1348]');src.write_text(s,encoding='utf-8')
md=f.with_suffix('.md');s=md.read_text(encoding='utf-8').replace(a,z).replace('1103, 1107, 1109, 1359；','1103, 1107, 1109, 1348；');md.write_text(s,encoding='utf-8')
st=read(P/'reader-state.json')
for b in st['submitted_batches']:
 if b['path']==f.name:b['sha256']=sha(f)
write(P/'reader-state.json',st);write(h/'v05-batch011-office-scope-delta.json',{'status':'self-check-before-submission','changes':[{'before':x,'after':y} for x,y in zip(old,rows) if x!=y],'unchanged_other_objects':19,'sha256':sha(f)});print(sha(f))
