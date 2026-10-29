"""将已审冻结包与差分副本纳入真实资料库，保证备份保留复核路径。"""
import pathlib,json,hashlib,sys
from check_volume import ROOT,WORK,read
sys.stdout.reconfigure(encoding='utf-8')
base=WORK/'zhanlong';dest=ROOT/'writing-vault/library/reports/zhanlong/audit/volume-provenance'
def sha(q):return hashlib.sha256(q.read_bytes()).hexdigest()
def store(src,out):
 out.parent.mkdir(parents=True,exist_ok=True)
 if out.exists():assert out.read_bytes()==src.read_bytes(),out
 else:out.write_bytes(src.read_bytes())
entries=[]
for n in range(1,7):
 p=base/f'vol{n:02d}';out=dest/f'vol{n:02d}';paths=set()
 for q in p.iterdir():
  if q.is_file() and q.suffix in ['.json','.jsonl','.md','.py'] and q.name!='import-result.json':paths.add(q)
 for folder in ['primary-delta','continuity-proposal','review-corrections']:
  if (p/folder).exists():paths.update(q for q in (p/folder).rglob('*') if q.is_file() and q.suffix in ['.json','.jsonl','.md','.py'])
 manifest=[]
 for q in sorted(paths):
  rel=q.relative_to(p).as_posix();stored=rel+'.source.txt' if q.suffix=='.md' else rel
  target=out/'packet'/stored;store(q,target)
  manifest.append(dict(original_path=rel,stored_path='packet/'+stored,sha256=sha(q),bytes=q.stat().st_size))
 for q in sorted(base.glob(f'*vol{n:02d}*.json')):
  target=out/'primary'/q.name;store(q,target);manifest.append(dict(original_path='../'+q.name,stored_path='primary/'+q.name,sha256=sha(q),bytes=q.stat().st_size))
 review=read(base/f'review-vol{n:02d}.json');assert review['reviewer']=='primary' and review['status']=='reviewed_for_library_import'
 data=dict(volume=n,source_id=review['source_id'],status='frozen-research-provenance-copy',files=manifest,scope='冻结研究/真实主审凭据/修订before与差分；非额外正文阅读。原Markdown以source.txt字节保存，正常阅读走正式入口。')
 target=out/'artifact-manifest.json';encoded=(json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode()
 if target.exists():assert target.read_bytes()==encoded
 else:target.write_bytes(encoded)
 (out/'README.md').write_text(f'# 卷{n}冻结研究证据副本\n\n[正式分卷阅读](../../../vol{n:02d}.md) · [逐文件SHA清单](artifact-manifest.json)\n\n此处保存冻结研究、真实主审凭据和修订前后版本。原Markdown按原字节存为source.txt，不将其暂存链接当正式导航。正文原书不在该研究副本内。\n',encoding='utf-8')
 for e in manifest:assert sha(out/e['stored_path'])==e['sha256']
 entries.append(dict(volume=n,files=len(manifest),manifest_sha256=sha(target)))
print(json.dumps({'status':'copied-and-byte-verified','volumes':entries,'files':sum(e['files'] for e in entries)},ensure_ascii=False))
