from pathlib import Path
import hashlib, json, subprocess, sys
ROOT=Path(__file__).resolve().parents[2]
VAULT=ROOT/'.verify/two-books'
META=ROOT/'.planning/two-books-20261023'
def run(args):
    p=subprocess.run(args,cwd=ROOT,text=True,encoding='utf-8',capture_output=True)
    print(p.stdout)
    if p.returncode: print(p.stderr); raise SystemExit(p.returncode)
    return p.stdout
print(run(['gh','api','repos/medillali/writing-vault']))
paths=[next(Path('E:/chromedownload').glob(f'*{title}*.txt')) for title in ['贼胆','网游之练级专家']]
out=VAULT/'private-sources/normalized'
run([sys.executable,'-X','utf8',str(ROOT/'distill-novels/scripts/prepare_sources.py'),*[str(p) for p in paths],'--output',str(out)])
run([sys.executable,'-X','utf8',str(ROOT/'distill-novels/scripts/library.py'),'--vault',str(VAULT),'sources-import','--file',str(out/'manifest.json')])
manifest=json.loads((out/'manifest.json').read_text(encoding='utf-8'))
(META/'manifest-summary.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
for s in manifest['sources']:
    print('SOURCE',json.dumps({k:v for k,v in s.items() if k!='chapters'},ensure_ascii=False))
    print('CHAPTERS',len(s['chapters']))
    print(json.dumps(s['chapters'][:18],ensure_ascii=False))
old=ROOT.parent/'Chinese Novel/books/zeidan/distillation'
for name in ['README.md','coverage.json','validation.json']:
    p=old/name
    print('OLD',name,p.read_text(encoding='utf-8')[:9000])
print('OLD_PARENT', [p.name for p in old.parent.iterdir()])
