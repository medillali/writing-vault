from pathlib import Path
import sys,subprocess,json,zipfile,hashlib
sys.stdout.reconfigure(encoding='utf-8');R=Path(__file__).resolve().parents[2];P=Path(__file__).parent;L=R/'writing-vault';sha=json.loads((P/'content-commit.json').read_text(encoding='utf-8'))['commit']
def git(*args):return subprocess.run(['git','-c',f'safe.directory={L.as_posix()}','-C',str(L),*args],capture_output=True,check=True).stdout
with zipfile.ZipFile(R/'backups/full-two-books-20261025'/f'writing-vault-{sha[:12]}.zip') as archive:
 errors=[]
 for row in git('ls-tree','-rz',sha).decode().split('\0'):
  if not row:continue
  header,name=row.split('\t',1);expected=header.split()[2];raw=archive.read(name);actual=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
  if actual!=expected:
   original=git('show',sha+':'+name);errors.append({'name':name,'archive_bytes':len(raw),'git_bytes':len(original),'equals_after_crlf':raw.replace(b'\r\n',b'\n')==original,'attributes':git('check-attr','--all','--',name).decode().strip()})
   if len(errors)==4:break
 print(json.dumps(errors,ensure_ascii=False))
