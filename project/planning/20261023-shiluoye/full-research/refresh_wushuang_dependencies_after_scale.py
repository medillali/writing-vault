"""只更新已核语义不变的依赖SHA；绝不重新生成36综合或20专项的结论。"""
from pathlib import Path
import copy,hashlib,json,runpy,sys
B=Path(__file__).resolve().parent;R=B.parents[2];D=B/'tianxia-wushuang';F=R/'writing-vault/library/reports/tianxia-wushuang'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
s=read(D/'book-synthesis-draft.json');f=read(D/'cross-volume-focused-review.json')
allowed={'writing-vault/library/reports/tianxia-wushuang/'+n for n in ['vol07-analysis.json','vol07.md','audit/review-vol07.json','audit/full-reading-validation.json']}
changes=[];mapping={}
for label,docs in [('synthesis',[x for g in s['upstream_documents'] for x in g['documents'] if x['exists']]),('focused',f['input_sha256_snapshot'])]:
 for x in docs:
  now=sha(R/x['path'])
  if now!=x['sha256']:
   assert x['path'] in allowed
   changes.append(dict(package=label,path=x['path'],before=x['sha256'],after=now));mapping[x['sha256']]=now
assert len(changes)==5
def replace(x):
 if isinstance(x,str):return mapping.get(x,x)
 if isinstance(x,list):return [replace(v) for v in x]
 if isinstance(x,dict):return {k:replace(v) for k,v in x.items()}
 return x
new_s,new_f=replace(s),replace(f)
def diffs(old,new,path=''):
 if old==new:return []
 if isinstance(old,dict):return [p for k in old for p in diffs(old[k],new[k],path+'/'+str(k))]
 if isinstance(old,list):return [p for i in range(len(old)) for p in diffs(old[i],new[i],path+'/'+str(i))]
 return [path]
delta_paths=diffs(s['dimensions'],new_s['dimensions'])
sys.stdout.reconfigure(encoding='utf-8');print(json.dumps({'dimension_changed_paths':delta_paths},ensure_ascii=False))
assert all('/supporting_observations/' in p and p.endswith('/material_sha256') for p in delta_paths),'36条中只有支持观察的material_sha256允许刷新；语义/证据不允许改变'
assert new_f['findings']==f['findings'],'20专项判断不允许被此步骤改变'
archive=F/'audit/research-corrections';archive.mkdir(parents=True,exist_ok=True)
for name in ['book-synthesis.json','book-synthesis.md','cross-volume-focused-review.json','cross-volume-focused-review.md']:
 p=archive/('before-scale-'+name);assert not p.exists();p.write_bytes((F/name).read_bytes())
for name in ['book-synthesis-draft.json','cross-volume-focused-review.json']:
 p=D/(name+'.before-scale-dependency-refresh');assert not p.exists();p.write_bytes((D/name).read_bytes())
write(D/'book-synthesis-draft.json',new_s);write(D/'cross-volume-focused-review.json',new_f)
sr=read(D/'primary-synthesis-review.json');sr['input_sha256']={n:sha(D/n) for n in ['book-synthesis-draft.json','book-synthesis-draft.md']}
sr['dependency_refresh']='1305完整核源纠分盟误读后，36综合全部主张、继承观察语义和证据逐值相同；只更新两正式依赖及支持观察的material_sha256。'
write(D/'primary-synthesis-review.json',sr)
fr=read(F/'audit/cross-volume-focused-review-primary.json');fr['input_sha256']={n:sha(D/n) for n in ['cross-volume-focused-review.json','cross-volume-focused-review.md']}
fr['dependency_refresh']='20项findings逐值相同；刷新修订卷7分析/主审凭据和重验全文覆盖三份输入SHA。'
for n in fr['input_sha256']:(F/n).write_bytes((D/n).read_bytes())
write(F/'audit/cross-volume-focused-review-primary.json',fr)
receipt=dict(reviewer='primary',status='semantic-arrays-identical-dependency-hashes-refreshed',changes=changes,
 current_synthesis_draft_sha256=sha(D/'book-synthesis-draft.json'),current_focused_sha256=sha(D/'cross-volume-focused-review.json'),
 note='旧final-freeze-manifest及旧3e270...是修订前版本快照；当前有效签收以primary-synthesis-review及正式发布回执为准。')
write(D/'dependency-refresh-after-scale-correction.json',receipt)
sys.stdout.reconfigure(encoding='utf-8');print(json.dumps(receipt,ensure_ascii=False))
sys.argv=['publish_book_synthesis.py','tianxia-wushuang'];runpy.run_path(str(B/'publish_book_synthesis.py'),run_name='__main__')
