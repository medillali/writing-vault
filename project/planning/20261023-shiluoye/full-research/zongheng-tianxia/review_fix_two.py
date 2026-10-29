import pathlib,json,hashlib,sys,functools
sys.stdout.reconfigure(encoding='utf-8')
b=pathlib.Path(__file__).resolve().parent
root=b.parents[3]
changes=[
 ('秦韵幕外劳动/反弹','秦韵幕后劳动/反弹'),
 ('不是所有相似意象都属于直接伏笔回收；艾兰、达芙妮等本卷未复生要保时域，不能自动外推绝对规则。','艾兰复明就业与林克、米拉、达芙妮死亡分别记录；后者终态以独立审计为准，不能凭相似意象自动算回收。')
]
paths=[b/n for n in ['build_book_synthesis.py','book-synthesis-draft.json','book-synthesis-draft.md']]
before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
for p in paths:
 text=p.read_text(encoding='utf-8')
 for old,new in changes:
  assert text.count(old)==1,(p.name,old,text.count(old))
  text=text.replace(old,new)
 p.write_text(text,encoding='utf-8')
j=json.loads((b/'book-synthesis-draft.json').read_text(encoding='utf-8'))
sys.path.insert(0,str(root/'distill-novels/scripts'))
from fictionlib.vault import Vault
v=Vault(root/'writing-vault');v._source=functools.lru_cache(maxsize=None)(v._source)
evidence=[]
for ds in j['dimensions'].values():
 for x in ds:evidence+=x['evidence']
for x in j['semantic_interface_checks']:evidence+=x['evidence']
evidence+=j['identity_guard']['evidence']
v.validate_evidence(evidence)
assert len(evidence)==986
for group in j['upstream_documents']:
 for d in group['documents']:
  if d['exists']:assert hashlib.sha256((root/d['path']).read_bytes()).hexdigest()==d['sha256'],d['path']
fixes=[dict(id='book-style-objects-change-function',field='limits_and_counterevidence',result=changes[1][1]),dict(id='book-characters-distributed-competence',field='claim',result='幕外劳动改为幕后劳动')]
j['validation']['literary_review_corrections']=fixes
j['validation']['review_fix_evidence_rechecked']=len(evidence)
j['validation']['review_fix_upstream_sha256_unchanged']=True
(b/'book-synthesis-draft.json').write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
out={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
receipt=dict(review_status='draft',scope='仅两处主审修改及生成器/MD同步；未重跑全书生成器，正式上游未改。',corrections=fixes,before_sha256=before,after_sha256=out,evidence_references_checked=len(evidence),upstream_sha256_unchanged=True)
(b/'book-synthesis-review-fix.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(receipt,ensure_ascii=False))
