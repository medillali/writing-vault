from revision import revise
from common import A
import json
f=A/'adjudications-local-v01-batch020.json';rs=json.loads(f.read_text(encoding='utf-8'))
for cid in ['v01-local-chapter_unresolved_index-0190-02','v01-local-chapter_unresolved_index-0191-02']:
 r=next(x for x in rs if x['candidate_id']==cid)
 ch={'later_chapters':[n for n in r['later_chapters'] if n!=252]}
 if cid.endswith('0190-02'):ch['rationale']=r['rationale'].replace('，后来双方仍有竞争；','；')
 revise(1,20,cid,'remove-volume-title-'+cid[-7:],ch,'交付前复核252仅卷题无后证，移除无关引用；207合作转述保留。其他候选逐值不动。')
