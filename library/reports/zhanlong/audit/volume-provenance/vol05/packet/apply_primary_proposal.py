"""只在主代理明确批准后调用：应用已冻结提案的精确路径，不重跑研究builder。"""
import pathlib,json,copy,hashlib,sys,datetime
P=pathlib.Path(__file__).resolve().parent;sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,str(P.parents[1]))
from check_volume import load_and_check
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(n):return json.loads((P/n).read_text(encoding='utf-8'))
def save(n,x):(P/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert sys.argv[1:] == ['--primary-approved'], '只能在primary明确批准现提案之后调用。'
proposal=read('primary-review-proposal.json');manifest=read('freeze-manifest.json')
assert manifest['status']=='draft-frozen-before-primary-proposals'
assert all(h(P/n)==digest for n,digest in proposal['before_core_sha256'].items())
data={n:read(n) for n in ['analysis.json','cards.json','graph.json']};original=copy.deepcopy(data)
for c in proposal['changes']:
 obj=data[c['file']]
 for key in c['path'][:-1]:obj=obj[key]
 assert obj[c['path'][-1]]==c['before'], c['path']
 obj[c['path'][-1]]=copy.deepcopy(c['after'])
for i,(a,b) in enumerate(zip(original['analysis.json']['dimensions']['continuity'],data['analysis.json']['dimensions']['continuity'])):
 for key in ['id','review_status','claim_kind']:assert a[key]==b[key]
 for key in ['evidence','interpretation_evidence']:assert b[key][:len(a[key])]==a[key]
assert original['analysis.json']['major_character_states']==data['analysis.json']['major_character_states']
# 逆向回放必须逐值还原现件，证明没有提案外更改。
reverse=copy.deepcopy(data)
for c in reversed(proposal['changes']):
 obj=reverse[c['file']]
 for key in c['path'][:-1]:obj=obj[key]
 assert obj[c['path'][-1]]==c['after'];obj[c['path'][-1]]=copy.deepcopy(c['before'])
assert reverse==original
for n,obj in data.items():save(n,obj)
unchanged={n:d for n,d in proposal['before_core_sha256'].items() if n not in data}
assert all(h(P/n)==d for n,d in unchanged.items())
result=load_and_check('zhanlong',5)[-1]
oldval=read('validation.json');oldval.update(result,primary_proposal_exact_path_check=True,unlisted_values_unchanged=True,reading_core_sha256_unchanged=unchanged)
save('validation.json',oldval)
delta=dict(status='approved-proposal-applied-awaiting-primary-recheck',proposal='primary-review-proposal.json',proposal_sha256=h(P/'primary-review-proposal.json'),primary_approval=dict(reviewer='primary',user_approval=False,scope='仅本提案10路径，非用户审美批准'),before_core_sha256=proposal['before_core_sha256'],after_core_sha256={n:h(P/n) for n in proposal['before_core_sha256']},changes=proposal['changes'],unlisted_values_unchanged=True,reverse_replay_equal=True,notes='原四栏/日志/reader-state逐字节不变；没有重新生成研究。')
delta['text_changes']=proposal.get('text_changes',[])
save('primary-review-merged-delta.json',delta)
before_manifest=P/'review-corrections/primary-before/freeze-manifest.json';before_manifest.write_bytes((P/'freeze-manifest.json').read_bytes())
for change in proposal.get('text_changes',[]):
 n=change['file'];t=(P/n).read_text(encoding='utf-8');assert t.count(change['before'])==1
 updated=t.replace(change['before'],change['after']);assert updated.replace(change['after'],change['before'])==t
 (P/n).write_text(updated,encoding='utf-8')
manifest['status']='draft-frozen-after-approved-primary-proposals';manifest['core_sha256']=delta['after_core_sha256']
for n in manifest['support_sha256']:manifest['support_sha256'][n]=h(P/n)
for n in ['primary-review-merged-delta.json','review-corrections/primary-before/freeze-manifest.json']:manifest['support_sha256'][n]=h(P/n)
manifest['notes']='10路径获primary明确批准后精准合入；原note/log/state不变；待primary复读delta与正式保存，不等用户审美认可。'
save('freeze-manifest.json',manifest)
print(json.dumps(dict(validation=result,core_sha256=delta['after_core_sha256'],merged_delta_sha256=h(P/'primary-review-merged-delta.json'),manifest_sha256=h(P/'freeze-manifest.json')),ensure_ascii=False))
