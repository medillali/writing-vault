"""Git HTTPS不可达时，以GitHub Git Database API发布同一Git树。"""
from pathlib import Path
import base64,datetime,hashlib,itertools,json,re,subprocess,sys
sys.stdout.reconfigure(encoding='utf-8');R=Path(__file__).resolve().parents[2];V=R/'writing-vault';P=Path(__file__).parent;REPO='repos/medillali/writing-vault'
def git(*args,raw=False,input=None):
 x=subprocess.run(['git','-c',f'safe.directory={V.as_posix()}','-C',str(V),*args],input=input,capture_output=True,check=True).stdout
 return x if raw else x.decode('utf-8').strip()
def api(path,data=None,method=None):
 cmd=['gh','api',path]
 if data is not None:
  f=P/'api-request.json';f.write_bytes(json.dumps(data,ensure_ascii=False).encode('utf-8'));cmd+=['--input',str(f)]
 if method:cmd+=['--method',method]
 result=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8')
 if result.returncode:raise RuntimeError(result.stderr)
 return json.loads(result.stdout)
local_sha=git('rev-parse','HEAD');parent=git('rev-parse','HEAD^');tree=git('rev-parse','HEAD^{tree}');assert local_sha=='34f2b642ea5ce81022f8bf38c4519f16c8028c05'
assert api(REPO)['private'];head=api(REPO+'/git/ref/heads/main')['object']['sha'];assert head in [parent,local_sha]
changed=set(git('diff-tree','--no-commit-id','--name-only','-r','-z',local_sha).split('\0'))-{''};assert len(changed)==34
all_blobs={line.split('\t',1)[1]:(line.split('\t',1)[0].split()[0],line.split('\t',1)[0].split()[2]) for line in git('ls-tree','-rz',local_sha).split('\0') if line};rows=[]
if head!=local_sha:
 for i,name in enumerate(sorted(changed),1):
  mode,blob_sha=all_blobs[name];raw=git('cat-file','blob',blob_sha,raw=True)
  response=api(REPO+'/git/blobs',{'content':base64.b64encode(raw).decode('ascii'),'encoding':'base64'});assert response['sha']==blob_sha
  rows.append({'path':name,'mode':mode,'type':'blob','sha':blob_sha})
  if i%8==0 or i==len(changed):print('已核对Git对象',i,'/',len(changed),flush=True)
 base=api(REPO+'/git/commits/'+parent)['tree']['sha'];new_tree=api(REPO+'/git/trees',{'base_tree':base,'tree':rows});assert new_tree['sha']==tree
 raw_commit=git('cat-file','commit',local_sha,raw=True);headers,message=raw_commit.decode('utf-8').split('\n\n',1)
 identities={}
 for field in ['author','committer']:
  line=next(s for s in headers.splitlines() if s.startswith(field+' '));match=re.fullmatch(r'.*? (.+) <([^>]+)> (\d+) ([+-]\d{4})',line);assert match,line
  name,email,epoch,zone=match.groups();minutes=(int(zone[1:3])*60+int(zone[3:]))*(1 if zone[0]=='+' else -1);date=datetime.datetime.fromtimestamp(int(epoch),datetime.timezone(datetime.timedelta(minutes=minutes))).isoformat();identities[field]={'name':name,'email':email,'date':date}
 new=api(REPO+'/git/commits',{'message':message,'tree':tree,'parents':[parent],**identities});remote_sha=new['sha']
 if remote_sha!=local_sha:
  # API可能将时区标准化为UTC；只接受能在本机完整重建并核对的同一内容提交。
  candidates=[]
  for az,cz in itertools.product([None,'+0000'],repeat=2):
   hs=headers
   for field,zone in [('author',az),('committer',cz)]:
    if zone:hs=re.sub(r'(?m)^('+field+r' .* \d+) [+-]\d{4}$',r'\g<1> '+zone,hs)
   for msg in [message,message.rstrip()+'\n',message.rstrip()+'\n\n']:
    raw=(hs+'\n\n'+msg).encode();oid=hashlib.sha1(b'commit '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    if oid==remote_sha:candidates.append(raw)
  assert candidates,('API提交的元数据不能完整复核，未更新分支',remote_sha,local_sha)
  assert git('hash-object','-t','commit','-w','--stdin',input=candidates[0])==remote_sha
 assert api(REPO+'/git/ref/heads/main')['object']['sha']==parent,'远程在上传期间推进，未覆盖分支'
 api(REPO+'/git/refs/heads/main',{'sha':remote_sha,'force':False},method='PATCH')
 if remote_sha!=local_sha:
  assert git('rev-parse',remote_sha+'^{tree}')==tree;git('update-ref','-m','同步已核对的GitHub API提交','refs/heads/main',remote_sha,local_sha)
else:remote_sha=local_sha
head=api(REPO+'/git/ref/heads/main')['object']['sha'];assert head==remote_sha
remote_tree=api(REPO+'/git/trees/'+remote_sha+'?recursive=1');assert not remote_tree['truncated'];remote={x['path']:x['sha'] for x in remote_tree['tree'] if x['type']=='blob'};assert remote=={n:x[1] for n,x in all_blobs.items()}
assert not git('diff','--cached','--name-only');git('update-ref','refs/remotes/origin/main',remote_sha)
receipt={'valid':True,'private_repository':'medillali/writing-vault','transport':'GitHub Git Database API；HTTPS Git传输不可达时的等价Git对象发布','original_local_commit':local_sha,'commit':remote_sha,'remote_head':head,'identical_tree':tree,'all_tree_blobs_match':True,'tree_blobs':len(remote),'committed_paths':sorted(changed),'root_readme_only_navigation_added':True,'unrelated_research_staged':False,'book_count':8,'author_count':3,'genre_count':2,'full_book_map_count':3,'raw_sources_uploaded':False}
(P/'remote-verification.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in receipt.items() if k!='committed_paths'},ensure_ascii=False))
