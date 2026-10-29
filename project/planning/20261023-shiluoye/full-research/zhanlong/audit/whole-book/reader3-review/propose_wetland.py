from common import A,P,dump,sha,evidence
import json,copy
specs=[
(10,'v01-local-chapter_unresolved_index-0076-01','81—82片主升40并二转已成；83片林因英雄冢王战主动改湿地至明日，主随后才接锋芒提前邀请，非他无故失护卫约。后来316重新明确约次日，318主与林、东城12:50抵西溪，319五人买票入园、雨亭游至天黑并吃饭，湿地实游愿望已经兑现。旧83所称明日是否正是该日/中间延期日历未统一，不能把后来实游提前为83次日已成，也不能终评仍称没有实游。'),
(11,'v01-local-chapter_unresolved_index-0079-01','84初55紫霖长风将军，86吸魂升60后被杀/无令，87—88天策夺来再失终在剑锋寒，分配违约有结果；1000R佣金无实际收付后证。83林主动延期湿地，316再约次日后318抵达西溪、319五人实际购票游园至晚，实游已兑现；早83精确明日与后来日期的日历衔接未说明，不拿西溪租屋补，亦不抹去后来真正出游。'),
(12,'v01-local-chapter_unresolved_index-0089-03','83片林将9点湿地改至明日，早期精确次日是否兑现未有统一日历。后316主再次许次日同游，318三人12:50抵西溪与倾浅会合，319五人买票入园、雨亭休息、游至天黑并由林请饭，后来湿地实游已经完成；应以此关闭实游愿望，保留旧明日时点未定。105网球、72购物电影与103西溪路租屋均非本次湿地后证。')]
out=[]
for n,cid,rationale in specs:
 f=A/f'adjudications-local-v01-batch{n:03d}.json'
 rows=json.loads(f.read_text(encoding='utf-8'));before=next(r for r in rows if r['candidate_id']==cid);after=copy.deepcopy(before)
 after.update(status='partial',rationale=rationale,later_chapters=list(dict.fromkeys(before['later_chapters']+[316,318,319])))
 after['later_evidence']=evidence(after['later_chapters'])
 out.append({'batch_file':f.name,'submitted_sha256':sha(f),'candidate_id':cid,'before':before,'after':after,'changed_fields':[k for k in after if before.get(k)!=after[k]],'not_applied':True})
f=P/'wetland-three-items-proposal.json';assert not f.exists();dump(f,{'scope':'仅三条终评，原题原record不动；已交批SHA未改','source_access':'本次完整派生读原reader卷2 raw316—319四栏；不冒本代理亲读整章','proposals':out});print(f.name,sha(f))
