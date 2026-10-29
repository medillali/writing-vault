from save_manual_batch import P,F,read,write,sha
import json
f=P/'adjudications-local-v05-batch007.json';rows=read(f);row=rows[18]
old='1138定现实回国航期、后1140实际回杭由主等接见需按原章核；至少游戏去向及现实行程已非主永不知，'
new='1138定现实回国航期、1141实际回国与同学建工作室/住别墅，游戏与现实归来均有具体后证；'
assert old in row['rationale'];row['rationale']=row['rationale'].replace(old,new)
row['later_chapters']=[1141 if k==1140 else k for k in row['later_chapters']]
n=next(json.loads(l) for l in (F/'vol05-chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if l.strip() and json.loads(l)['chapter_id']=='ch-1141')
for e in row['later_evidence']:
    if e['chapter_id']=='ch-1140':e.update(chapter_id='ch-1141',start_line=n['start_line'],end_line=n['end_line'])
write(f,rows)
md=f.with_suffix('.md');s=md.read_text(encoding='utf-8').replace(old,new).replace('1138, 1140；','1138, 1141；');md.write_text(s,encoding='utf-8')
src=P/'manual_v05_007.py';s=src.read_text(encoding='utf-8').replace(old,new).replace('1109,1138,1140]','1109,1138,1141]');src.write_text(s,encoding='utf-8')
state=read(P/'reader-state.json')
for b in state['submitted_batches']:
    if b['path']==f.name:b['sha256']=sha(f)
write(P/'reader-state.json',state);print(sha(f))
