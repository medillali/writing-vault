"""主审实际核1358后补纸上画魅任职后证，保长期/薪酬缺口。"""
from pathlib import Path
import copy,hashlib,json
B=Path(__file__).parent/'zhanlong';A=B/'audit/whole-book'
p=A/'adjudications-history-v05-batch001.json'
def read(q):return json.loads(q.read_text(encoding='utf-8'))
def sha(q):return hashlib.sha256(q.read_bytes()).hexdigest()
source=read(B/'source.json');rows=read(p)
idx=next(i for i,r in enumerate(rows) if r['candidate_id']=='v05-question-v05-q-paperjob')
before=copy.deepcopy(rows[idx]);assert before['status']=='unknown'
assert before['rationale']=='1111方对纸的长期副盟/劝吕让位与加薪是同意未来安排；1181纸吕都仍核心、1206吕和轩辕被合称副盟/长老、1320两人共同领战，无法据此确认哪一职已正式换给谁。后奖励/参战不抵职位与薪酬，指定承诺执行未明，不误写吕冻宾为正确实名吕纯阳。'
after=copy.deepcopy(before);after['status']='partial'
after['rationale']='1111方提出纸上画魅任长期副盟、劝吕让位及加薪；1358 L97703薛景本人已自称副盟主，方与薛柔随即接话，是较晚实际任职后证，不能将全部职位安排继续列未知。该章未说明长期任职细则、吕如何让位或具体加薪到账，1206合称副盟/长老与1320共同领战也不能补这些程序/薪款。实际任职已答与其余缺口分开，正确实名仍为吕纯阳。'
assert 1358 in after['later_chapters']
assert any(e['chapter_id']=='ch-1358' and e['start_line']==97679 and e['end_line']==97755 for e in after['later_evidence'])
after['later_evidence'].append(dict(source_id=source['source_id'],revision=source['revision'],
    chapter_id='ch-1358',start_line=97701,end_line=97709,claim_kind='fact',
    evidence_access='primary-targeted-raw-lines',full_text_read=False))
folder=A/'primary-paper-job-correction';assert not folder.exists();folder.mkdir()
(folder/p.name).write_bytes(p.read_bytes())
rows[idx]=after
delta=dict(candidate_id=after['candidate_id'],before=before,after=after,
    method='root本轮实际限定读1358 L97698—97710，未冒整章或全书个人重读',
    original_record_unchanged=True,other_objects_unchanged=True,before_batch_sha256=sha(p))
content=(json.dumps(rows,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
replayed=read(folder/p.name);replayed[idx]=after;assert replayed==rows
p.write_bytes(content);delta['after_batch_sha256']=sha(p)
(folder/'delta.json').write_text(json.dumps(delta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(candidate_id=after['candidate_id'],status=after['status'],
    after_batch_sha256=sha(p),only_one_object_changed=True),ensure_ascii=False))
