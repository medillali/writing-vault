from save_manual_batch import P,F,read,write,sha
import json,copy
f=F/'vol02-chapter-notes.jsonl';n=next(json.loads(l) for l in f.read_text(encoding='utf-8').splitlines() if l.strip() and json.loads(l)['chapter_id']=='ch-0398')
e=dict(source_id=n['source_id'],revision=n['revision'],chapter_id=n['chapter_id'],start_line=n['start_line'],end_line=n['end_line'],claim_kind='fact',evidence_access='本轮BEGIN-END定向完整复读398；亦完整读正式原notes',material_path='writing-vault/library/reports/zhanlong/vol02-chapter-notes.jsonl',material_sha256=sha(f),source_reader=n['reader'])
changes=[]
for batch,cid,newstatus,newrationale in [
 (12,'v02-local-chapter_unresolved_index-0108-01','partial','377罗雷只报女遭断指未具名/主未亲见，后398 L33402林穹明确此前联姻嫁出者名莱兰，并与他所求的养女安吉拉分说，远嫁公主已有姓名后证。断指施害过程与莱兰战后返国/伤愈仍未实演，414城战胜不能代人身结局；不能再把公主整条身份一概未明或并为安吉拉。'),
 (9,'v02-local-chapter_unresolved_index-0073-02','partial','335汪称发展三个分盟后返凡书；398烟与汪单独对话已说在八荒另建四个私分盟/近万，汪谈问剑或更高兴，故必须保条件后规模已越三的当事人后述，不能说全书连后规模都未提。此时仍在八荒作战，实际迁回凡书及何时履约未给；不因缺UI否认已叙组织发展，也不强断书外永不返。'),
]:
 file=P/f'adjudications-local-v02-batch{batch:03d}.json';rows=read(file);before=next(x for x in rows if x['candidate_id']==cid);after=copy.deepcopy(before);after.update(status=newstatus,rationale=newrationale)
 if 398 not in after['later_chapters']:after['later_chapters'].append(398);after['later_evidence'].append(copy.deepcopy(e))
 changes.append(dict(path=file.name,candidate_id=cid,input_sha256=sha(file),before=before,after=after,scope='仅所列判断/理由和新增398后证，其他对象不变'))
q=P/'later398-princess-and-private-branches-proposal.json';assert not q.exists();write(q,dict(status='proposal-pending-primary-review-not-applied',reason='本轮继续读到398并BEGIN-END核原文，对已经交出的前阶段判断补明确后文；不静改已交批。',direct_reread=dict(raw=398,start_line=33348,end_line=33407,full_text_read=True),changes=changes));print(sha(q))
