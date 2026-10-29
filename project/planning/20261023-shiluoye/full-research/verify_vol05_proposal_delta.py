import copy,hashlib,json,sys
from check_volume import WORK,read
sys.stdout.reconfigure(encoding='utf-8')
p=WORK/'zhanlong/vol05';o=read(p/'review-corrections/primary-proposal-before-supplement.json');n=read(p/'primary-review-proposal.json');s=read(p/'primary-review-supplement-delta.json')
assert hashlib.sha256((p/'primary-review-proposal.json').read_bytes()).hexdigest()=='aad046aaea881c6801ed6c290d6a7b464eb90bdd7ad6abcb499ade105e6570fb'
assert hashlib.sha256((p/'review-corrections/primary-proposal-before-supplement.json').read_bytes()).hexdigest()==s['previous_proposal_sha256']
e=copy.deepcopy(o)
for r in s['changes']:
 t=e
 for k in r['proposal_path'][:-1]:t=t[k]
 assert t[r['proposal_path'][-1]]==r['before'];t[r['proposal_path'][-1]]=copy.deepcopy(r['after'])
assert n['text_changes']==s['text_changes']
assert n['unchanged']=='原四栏notes/read-log/reader-state不动；新增仅cont01事实精确成纸=薛景/薛柔堂妹、cont02/03/04各追加直接后证及三title和report单段同步；其余已读提案内容逐值不动。'
e['text_changes']=s['text_changes'];e['unchanged']=n['unchanged']
if e!=n:
 def diff(a,b,path=()):
  if type(a)!=type(b):return [{'path':path,'before':a,'after':b}]
  if isinstance(a,dict):return [r for k in set(a)|set(b) for r in diff(a.get(k),b.get(k),path+(k,))]
  if isinstance(a,list) and len(a)==len(b):return [r for i,(x,y) in enumerate(zip(a,b)) for r in diff(x,y,path+(i,))]
  return [] if a==b else [{'path':path,'before':a,'after':b}]
 print(json.dumps({'unlisted_differences':diff(e,n)},ensure_ascii=False))
 raise AssertionError('提案出现未列变化')
print(json.dumps({'supplement_fields':len(s['changes']),'all_other_proposal_values_exactly_equal':True,'text_changes_read':len(s['text_changes'])},ensure_ascii=False))
