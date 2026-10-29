"""仅在primary已完整读给定JSON范围后记范围回执；不自动生成语义结论。"""
import sys,json,hashlib,datetime
from check_volume import WORK,read
sys.stdout.reconfigure(encoding='utf-8')
book,vol,name,key,start,end=sys.argv[1:7];vol=int(vol);start=int(start);end=int(end)
assert '--read' in sys.argv
folder=WORK/book/f'vol{vol:02d}';source=folder/name
data=read(source)
if key!='.':
 for k in key.split('.'):data=data[k]
assert isinstance(data,list) and 0<=start<end<=len(data)
selected=data[start:end];digest=hashlib.sha256(source.read_bytes()).hexdigest()
path=WORK/book/f'vol{vol:02d}-primary-review-progress.json'
progress=read(path) if path.exists() else {'reviewer':'primary','volume':vol,'method':'完整逐项读派生研究并语义审阅；不是个人原文全文覆盖，范围回执不代替语义判断。','batches':[]}
section=name+'::'+key
prior=[b for b in progress['batches'] if b['section']==section]
if any(b['input_sha256']!=digest for b in prior):
 # 允许只修改尚未读到的部分；已签片段按原对象SHA逐项强校，旧签收不改。
 checked=[]
 for b in prior:
  left,right=b['range']
  current_slice=hashlib.sha256(json.dumps(data[left:right],ensure_ascii=False,sort_keys=True).encode('utf-8')).hexdigest()
  assert current_slice==b['selected_sha256'],'已读语义对象发生变更：需先逐项差异主审，不可静默沿用'
  checked.append({'range':b['range'],'selected_sha256':current_slice})
 proof={'section':section,'old_input_sha256':sorted(set(b['input_sha256'] for b in prior)),'new_input_sha256':digest,'previously_read_objects_exactly_unchanged':checked}
 if proof not in progress.setdefault('unchanged_read_slice_proofs',[]):progress['unchanged_read_slice_proofs'].append(proof)
assert not any(max(start,b['range'][0])<min(end,b['range'][1]) for b in prior),'已记范围不得重签'
progress['batches'].append({'section':section,'range':[start,end],'items':len(selected),'input_sha256':digest,'selected_sha256':hashlib.sha256(json.dumps(selected,ensure_ascii=False,sort_keys=True).encode('utf-8')).hexdigest(),'read_at':datetime.datetime.now(datetime.timezone.utc).isoformat()})
path.write_text(json.dumps(progress,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'recorded':section,'range':[start,end],'items':len(selected),'total_batches':len(progress['batches'])},ensure_ascii=False))
