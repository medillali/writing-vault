from pathlib import Path
import subprocess,json,hashlib
V=Path('writing-vault').resolve();P=Path('.planning/tree-maps-20261025');result=[]
for f in ('zeidan','leveling'):
 rel=f'library/reports/two-books-full-20261025/{f}/plot/graph.json';p=V/rel;raw=p.read_bytes()
 base=subprocess.check_output(['git','-c',f'safe.directory={V.as_posix()}','-C',str(V),'show','HEAD:'+rel])
 assert raw.replace(b'\r\n',b'\n')==base,'仅允许规范与Git内容完全相同的生成副本'
 if raw!=base:
  (P/f'{f}-graph-before-lf.json').write_bytes(raw);p.write_bytes(base)
  result.append({'path':rel,'original_sha256':hashlib.sha256(raw).hexdigest(),'canonical_sha256':hashlib.sha256(base).hexdigest(),'semantic_content_unchanged':True})
(P/'local-newline-normalization.json').write_bytes((json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps({'normalized_generated_copies':len(result),'same_as_committed_graphs':True}))
