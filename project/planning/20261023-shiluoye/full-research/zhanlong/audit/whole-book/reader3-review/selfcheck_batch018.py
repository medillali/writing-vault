from common import A,P,dump,sha
from revision import revise
import json,shutil
f=A/'adjudications-local-v04-batch018.json'
revise(4,18,'v04-local-chapter_unresolved_index-0197-02','selfcheck-reforging-chapter',{'rationale':'957“满级不换”是主对新五星蝴蝶的预估；1289实际将图谱/万年玄铁/蝴蝶/传国玉玺交灵重铸，1290半小时后成功由五星神器进化天下国器并实穿，证明同物仍成长，不能把957当已验证永不升级。现实1355实体剑断与游戏同名剑分开，期末仍用游戏蝴蝶不等早面板永不变。','later_chapters':[957,1289,1290,1355]},'交付前自核：定向定位93277并完整读1289/1290四栏，去1310近似章号。')
revise(4,18,'v04-local-chapter_unresolved_index-0198-02','selfcheck-papa-exact',{'rationale':'959—960主沈真接裴取联系，1045PaPa正式开业邀约、1046四人实际赴吧喝至午夜；1275—1277取盒任务真行/裴实捕但盒爆沈死，不能把主护她承诺记成功无损。案件后续不等958那时已完成，也不把游戏中的新任务替现实调查。','later_chapters':[958,959,960,1045,1046,1275,1276,1277]},'交付前完整读1046四栏，77093归章1046而非1047。')
# 仅将本批访问说明的待核句改为本次已完成的真实访问，不改变任何原题。
before=json.loads(f.read_text(encoding='utf-8'));snap=P/'batch018-before-access-completion.json';assert not snap.exists();shutil.copy2(f,snap)
old='“满级不换”项另须核后重铸确章，不把大约章号当最终证据。'
new='后追加完整派生读1289—1290与1046四栏，已核后重铸和赴吧确章，未用约数作最终证据。'
for row in before:
 assert old in row['source_attribution']['later_source']
 row['source_attribution']['later_source']=row['source_attribution']['later_source'].replace(old,new)
dump(f,before)
rp=P/'v04-batch018-receipt.json';rc=json.loads(rp.read_text(encoding='utf-8'));rc['sha256']=sha(f);dump(rp,rc)
st=json.loads((P/'reader-state.json').read_text(encoding='utf-8'))
for i,x in enumerate(st['batches']):
 if x['file']==f.name:st['batches'][i]=rc
dump(P/'reader-state.json',st)
md=f.with_suffix('.md');md.write_text(md.read_text(encoding='utf-8').replace(old,new),encoding='utf-8')
dump(P/'batch018-access-completion-delta.json',{'before_sha256':sha(snap),'after_sha256':sha(f),'changed_field':'source_attribution.later_source','old':old,'new':new,'rows':20,'semantic_revisions':'另2条独立selfcheck delta'})
print('FINAL',sha(f))
