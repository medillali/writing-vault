"""把标准备份白名单外的阅读入口保存成可核验报告附件，隔离恢复时还原。"""
from pathlib import Path,PurePosixPath
import hashlib,json,sys
B=Path(__file__).resolve().parent;R=B.parents[2]
sys.path.insert(0,str(R/'distill-novels/scripts'))
from fictionlib.storage import safe_path
SINGLE={'START-HERE.md','CONTENT-GUIDE.md','RESEARCH-QUEUE.md'}
PREFIX={'templates','书库'}
def allowed(name):
 p=PurePosixPath(name)
 return name in SINGLE or len(p.parts)>1 and p.parts[0] in PREFIX
def sha(b):return hashlib.sha256(b).hexdigest()
def prepare(vault):
 vault=Path(vault).resolve();qa=vault/'library/reports/collection/qa'
 entries=[];names=[p for n in sorted(SINGLE) if (p:=vault/n).is_file()]
 for n in sorted(PREFIX):
  if (vault/n).exists():names.extend(p for p in (vault/n).rglob('*') if p.is_file())
 for p in sorted(names):
  name=p.relative_to(vault).as_posix();assert allowed(name)
  assert safe_path(vault,name)==p
  data=p.read_bytes();digest=sha(data)
  relative=f'library/reports/collection/qa/support-snapshots/{digest}.bin'
  target=safe_path(vault,relative);target.parent.mkdir(parents=True,exist_ok=True)
  if target.exists():assert target.read_bytes()==data
  else:target.write_bytes(data)
  entries.append(dict(path=name,snapshot=relative,sha256=digest,bytes=len(data)))
 plan=dict(schema_version=1,purpose='仅保存标准备份外的阅读导航、指南与模板；不包含原小说、Git或本机路径配置',entries=entries)
 (qa/'support-restore-plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 return dict(files=len(entries),bytes=sum(e['bytes'] for e in entries))
def regenerate(vault):
 vault=Path(vault).resolve();plan=json.loads((vault/'library/reports/collection/qa/support-restore-plan.json').read_text(encoding='utf-8'))
 assert plan['schema_version']==1
 names=[x['path'] for x in plan['entries']];assert len(names)==len(set(names))
 checked=[]
 for e in plan['entries']:
  assert allowed(e['path'])
  assert e['snapshot']==f"library/reports/collection/qa/support-snapshots/{e['sha256']}.bin"
  data=safe_path(vault,e['snapshot']).read_bytes();assert sha(data)==e['sha256'] and len(data)==e['bytes']
  target=safe_path(vault,e['path'])
  assert not target.exists() or target.is_file() and target.read_bytes()==data,'拒绝覆盖内容不同的入口文件'
  checked.append((target,data))
 for p,data in checked:
  if not p.exists():p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
 return dict(verified_files=len(checked),verified_bytes=sum(len(b) for _,b in checked))
if __name__=='__main__':
 sys.stdout.reconfigure(encoding='utf-8');print(json.dumps(globals()[sys.argv[1]](Path(sys.argv[2])),ensure_ascii=False))
