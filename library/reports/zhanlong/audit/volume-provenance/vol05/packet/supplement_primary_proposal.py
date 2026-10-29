"""仅更新尚未应用的提案；保上一版提案/manifest和新增差异，不写六核心或报告。"""
import pathlib,json,hashlib,copy,sys
P=pathlib.Path(__file__).parent;sys.stdout.reconfigure(encoding='utf-8')
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(n):return json.loads((P/n).read_text(encoding='utf-8'))
def save(n,x):(P/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
old=read('primary-review-proposal.json');new=copy.deepcopy(old);A=read('analysis.json');S=read('../source.json')
ch={int(x['chapter_id'].split('-')[1]):x for x in S['chapters']}
before=P/'review-corrections/primary-proposal-before-supplement.json';before.write_bytes((P/'primary-review-proposal.json').read_bytes())
oldmanifest=P/'review-corrections/manifest-before-proposal-supplement.json';oldmanifest.write_bytes((P/'freeze-manifest.json').read_bytes())
titles={0:'当面认名与亲属对白使旧行动重新可辨',1:'交付延迟与实装动作维持获得感',3:'名称数值滑移削弱规则的可预判性'}
for i,t in titles.items():new['changes'][i]['after']['title']=t
new['changes'][0]['after']['textual_fact']=new['changes'][0]['after']['textual_fact'].replace('纸为景堂妹','纸上画魅=薛景，是薛柔堂妹')
assert new['changes'][0]['after']['textual_fact']!=old['changes'][0]['after']['textual_fact']
for i,n in [(1,1090),(2,1094),(3,1178)]:
 for field,kind in [('evidence','fact'),('interpretation_evidence','inference')]:
  a=new['changes'][i]['after'][field];assert not any(e['chapter_id']==f'ch-{n:04d}' for e in a)
  a.append(dict(source_id=A['source_id'],revision=A['revision'],chapter_id=f'ch-{n:04d}',start_line=ch[n]['start_line'],end_line=ch[n]['end_line'],claim_kind=kind))
report=(P/'report.md').read_text(encoding='utf-8');paragraph=next(x for x in report.splitlines() if x.startswith('**连续性**'))
replacement='**连续性**通过本人揭名和亲属对白，让失联时的行动重新归到可辨认的人；寄存、代送、亲手接收与立即实装分段延迟或收束获得感。游戏玩家可复、普通军部分恢复、具名尸证与现实断肋的差异维持风险层次；没有说明的数值/名称滑移则使读者难以稳定预判规则。局部任务发奖后再给缺一步的条件，把完成感接到新期待：百岛SSS已成不等子舒已封龙神，星辰戒叫到千万也仍未落槌。'
new['text_changes']=[dict(file='report.md',before=paragraph,after=replacement,reason='只同步主审新连续性文学解释这一段，其余report/handoff不改。')]
new['unchanged']='原四栏notes/read-log/reader-state不动；新增仅cont01事实精确成纸=薛景/薛柔堂妹、cont02/03/04各追加直接后证及三title和report单段同步；其余已读提案内容逐值不动。'
for i in range(4,10):assert old['changes'][i]==new['changes'][i]
for i in range(5):
 for k in ['observation','mechanism','limits_and_counterevidence']:assert old['changes'][i]['after'][k]==new['changes'][i]['after'][k]
delta=[]
for i in range(5):
 for k,v in new['changes'][i]['after'].items():
  if v!=old['changes'][i]['after'][k]:delta.append(dict(proposal_path=['changes',i,'after',k],before=old['changes'][i]['after'][k],after=v))
save('primary-review-proposal.json',new)
save('primary-review-supplement-delta.json',dict(status='additional-proposal-only-not-applied',previous_proposal_sha256=h(before),new_proposal_sha256=h(P/'primary-review-proposal.json'),changes=delta,text_changes=new['text_changes'],confirmed_unchanged='10个核心路径不增加；此前已读的5项observation/mechanism/limits与5个其他修改对象逐值不变。',core_sha256={n:h(P/n) for n in old['before_core_sha256']}))
manifest=read('freeze-manifest.json')
for n in ['primary-review-proposal.json','primary-review-supplement-delta.json','review-corrections/primary-proposal-before-supplement.json','review-corrections/manifest-before-proposal-supplement.json']:manifest['support_sha256'][n]=h(P/n)
save('freeze-manifest.json',manifest)
assert old['before_core_sha256']=={n:h(P/n) for n in old['before_core_sha256']}
print(json.dumps(dict(proposal_sha256=h(P/'primary-review-proposal.json'),supplement_delta_sha256=h(P/'primary-review-supplement-delta.json'),manifest_sha256=h(P/'freeze-manifest.json'),extra_fields=len(delta),core_unchanged=True),ensure_ascii=False))
