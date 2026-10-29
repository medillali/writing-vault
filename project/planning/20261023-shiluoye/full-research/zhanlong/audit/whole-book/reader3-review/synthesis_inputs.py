from common import ROOT,P,B,dump,sha
import json,datetime
F=ROOT/'writing-vault/library/reports/zhanlong'
groups=[]
for n in range(1,7):
 docs=[]
 for kind,suffix in [('analysis','analysis.json'),('cards','cards.json'),('graph','graph.json'),('read-log','read-log.json'),('handoff','handoff.md'),('report','.md')]:
  f=F/(f'vol{n:02d}'+(suffix if suffix=='.md' else '-'+suffix))
  assert f.exists();docs.append({'kind':kind,'path':str(f.relative_to(ROOT)).replace('\\','/'),'exists':True,'sha256':sha(f),'version_location':'formal'})
 groups.append({'volume':n,'documents':docs})
more=[]
paths=[F/'vol02-primary-corrections.json',F/'audit/full-reading-validation.json']+sorted((F/'audit').glob('priority-corrections-*.json'))+sorted((F/'audit/primary-rereads').glob('*.json'))
for f in paths:
 more.append({'kind':'priority-correction-or-reread','path':str(f.relative_to(ROOT)).replace('\\','/'),'exists':True,'sha256':sha(f),'version_location':'formal'})
groups.append({'volume':'cross-volume-corrections','documents':more})
out=P/'synthesis-current-input-receipt.json'
assert not out.exists();dump(out,{'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'upstream_documents':groups,'boundary':'只指纹当前formal依赖；读取范围另记，不将文件存在冒充全文实读。'})
print('DOCS',sum(len(x['documents']) for x in groups))
for f in paths:
 d=json.loads(f.read_text(encoding='utf-8'))
 print(f.name,list(d) if isinstance(d,dict) else ['list',len(d)])
