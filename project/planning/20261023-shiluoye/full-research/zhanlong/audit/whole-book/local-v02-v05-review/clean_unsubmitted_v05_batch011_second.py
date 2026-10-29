from save_manual_batch import P,F,read,write,sha
import copy,json
f=P/'adjudications-local-v05-batch011.json';rows=read(f);old=copy.deepcopy(rows);r=rows[18]
r['rationale']=r['rationale'].replace('1137套升','1138套升');r['later_chapters']=[1138 if k==1137 else k for k in r['later_chapters']]
n=next(json.loads(s) for s in (F/'vol05-chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if json.loads(s)['chapter_id']=='ch-1138')
for e in r['later_evidence']:
 if e['chapter_id']=='ch-1137':e.update(chapter_id=n['chapter_id'],start_line=n['start_line'],end_line=n['end_line'])
write(P/'unsubmitted-self-check/v05-batch011-before-armor-upgrade-chapter.json',old);write(f,rows)
for name in ['manual_v05_011.py','adjudications-local-v05-batch011.md']:
 p=P/name;s=p.read_text(encoding='utf-8').replace('1137套升','1138套升').replace('1090,1113,1137]','1090,1113,1138]').replace('1090, 1113, 1137；','1090, 1113, 1138；');p.write_text(s,encoding='utf-8')
st=read(P/'reader-state.json')
for b in st['submitted_batches']:
 if b['path']==f.name:b['sha256']=sha(f)
write(P/'reader-state.json',st);print(sha(f))
