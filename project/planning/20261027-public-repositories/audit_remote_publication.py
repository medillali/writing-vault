"""只读核远程所有refs可达历史，输出范围/疑点位置，不打印凭据内容。"""
from pathlib import Path
import collections,datetime,hashlib,json,re,subprocess
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent/'remote-publication-audit.json'
PATTERNS={
 'private_key':re.compile(rb'-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----'),
 'github_token':re.compile(rb'\b(?:gh[pousr]_[A-Za-z0-9]{36,255}|github_pat_[A-Za-z0-9_]{60,255})\b'),
 'openai_token':re.compile(rb'\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{40,255}\b'),
 'aws_access_key':re.compile(rb'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b')}
def git(repo,*args):
 return subprocess.run(['git','-c',f'safe.directory={repo.as_posix()}','-c','core.quotepath=false','-C',str(repo),*args],capture_output=True,check=True).stdout
def run(name,remote,full):
 repo=ROOT/name;remote_lines=git(repo,'ls-remote',remote).decode('utf-8').splitlines()
 refs={ref:oid for oid,ref in (line.split('\t',1) for line in remote_lines)}
 tips=sorted(set(refs.values()))
 # fetch已完成；所有公开refs都必须在本地可实际核查，否则不继续公开。
 for oid in tips:git(repo,'cat-file','-e',oid)
 objects={}
 for line in git(repo,'rev-list','--objects',*tips).decode('utf-8').splitlines():
  oid,_,path=line.partition(' ');objects[oid]=path
 process=subprocess.Popen(['git','-c',f'safe.directory={repo.as_posix()}','-C',str(repo),'cat-file','--batch'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 findings=[];counts=collections.Counter();total=0;max_blob=0;raw_candidates=[]
 for oid,path in objects.items():
  process.stdin.write((oid+'\n').encode('ascii'));process.stdin.flush();header=process.stdout.readline().split()
  assert len(header)==3 and header[0].decode()==oid,(oid,header)
  typ=header[1].decode();size=int(header[2]);content=process.stdout.read(size);assert len(content)==size and process.stdout.read(1)==b'\n'
  counts[typ]+=1;total+=size
  if typ=='blob':
   max_blob=max(max_blob,size)
   lower=path.lower();parts=Path(lower).parts
   private_path=(any(x in parts for x in ['private-sources','.ssh','.aws']) and Path(lower).name not in ['readme.md','.gitkeep','.gitignore']) or Path(lower).name in ['.env','credentials.json','secrets.json','vault.local.json','sources.local.json'] or lower.endswith(('.pem','.p12','.pfx','.key'))
   if private_path:findings.append({'category':'private_or_machine_file_path','path':path,'object':oid,'bytes':size})
   if lower.endswith(('.txt','.epub','.mobi','.azw3','.zip','.7z','.rar')) and size>65536:raw_candidates.append({'path':path,'object':oid,'bytes':size})
  for category,pattern in PATTERNS.items():
   if pattern.search(content):findings.append({'category':category,'path':path or '(commit or tag)','object':oid,'bytes':size})
 process.stdin.close();assert process.wait()==0
 paths=sorted(set(git(repo,'log','--format=','--name-only',*tips).decode('utf-8').splitlines()))
 paths=[p for p in paths if p]
 return {'repository':full,'remote_refs':refs,'unique_objects':len(objects),'object_types':dict(counts),'object_bytes':total,'largest_blob_bytes':max_blob,'all_history_paths':len(paths),'credential_or_private_path_findings':findings,'large_text_or_archive_candidates':raw_candidates,'git_push_performed':False}
results=[run('distill-novels','personal','medillali/distill-novels'),run('writing-vault','origin','medillali/writing-vault')]
report={'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'freshly fetched remote refs reachable Git objects only; uncommitted local research excluded','repositories':results,'limits':'路径与高确定性凭据模式核查，不作绝对保密性担保；不自动修改或上传本地工作树。'}
OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False),flush=True)
assert all(not r['credential_or_private_path_findings'] and not r['large_text_or_archive_candidates'] for r in results),'需先逐项核实疑点，不能先公开'
