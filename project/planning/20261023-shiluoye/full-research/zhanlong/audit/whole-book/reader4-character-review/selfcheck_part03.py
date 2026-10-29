import json,hashlib
from pathlib import Path
D=Path(__file__).resolve().parent;A=D.parent;ROOT=D.parents[6]
def rd(p):return json.loads(p.read_text(encoding='utf-8'))
def wr(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
p=A/'reader4-character-arcs-part03.json';ac=D/'part03-access-receipt.json';m=p.with_suffix('.md');b=D/'unsubmitted-part03-before-last-source-selfcheck';b.mkdir(exist_ok=False)
for f in [p,ac,m]:(b/f.name).write_bytes(f.read_bytes())
d=rd(p);changes=[]
for aid,key,before,after in [
 ('character-arc-r4-019','initial_comparison_stage','到960堂亲与1110实名/身份进一步明','到960堂亲关系进一步明'),
 ('character-arc-r4-018','key_decisions','后来替问剑挡攻击、1322受命拖达伦','1206试引饮火三秒被杀；1322受命拖达伦'),
 ('character-arc-r4-018','costs','挡剑游戏真死不代表现实身亡','1206魔殿试引王游戏真死不代表现实身亡')]:
 r=next(x for x in d['characters'] if x['audit_id']==aid);old=r[key];assert before in old;r[key]=old.replace(before,after);changes.append({'audit_id':aid,'field':key,'before':old,'after':r[key]})
r=next(x for x in d['characters'] if x['audit_id']=='character-arc-r4-018');r['evidence'].append(dict(source_id=d['source_id'],revision=d['revision'],chapter_id='ch-1206',start_line=87788,end_line=87807,claim_kind='fact',access_level='targeted-limited-source-excerpt-not-full-chapter',research_path=ac.relative_to(ROOT).as_posix(),original_reader='zongheng_vol05_full'))
a=rd(ac);a['limited_source_ranges'].append(dict(chapter_id='ch-1206',start_line=87788,end_line=87807,actual_reader='/root/zongheng_vol04_full',access_scope='targeted-limited-source-excerpt-not-full-chapter',additional_unique_chapters=0));wr(ac,a)
for r in d['characters']:
 for e in r['evidence']:
  if e.get('research_path')==ac.relative_to(ROOT).as_posix():e['research_sha256']=sha(ac)
d['additional_support_sha256'][ac.relative_to(ROOT).as_posix()]=sha(ac);wr(p,d)
text=m.read_text(encoding='utf-8')
for c in changes:text=text.replace(c['before'],c['after'])
m.write_text(text+'\n自核补定位：唐古ch-1206 L87788—87807；未以其他人物卡短句未经核便作挡剑事实。\n',encoding='utf-8')
wr(D/'part03-last-source-selfcheck-delta.json',{'submitted_to_primary_before_this_delta':False,'changes':changes,'after_sha256':sha(p),'other_rows_unchanged':True});print(sha(p))
