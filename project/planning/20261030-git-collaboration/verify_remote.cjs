// 核对已推送仓库的完整文件列表、Git树及实际工作树字节。
const fs=require('node:fs/promises'),crypto=require('node:crypto'),cp=require('node:child_process'),util=require('node:util');
const run=util.promisify(cp.execFile); const [localRoot,cloneRoot,output]=process.argv.slice(2);
async function git(cwd,args){return (await run('git',['-c','safe.directory='+cwd,'-c','core.quotepath=false',...args],{cwd,maxBuffer:16*1024*1024,encoding:'utf8'})).stdout}
async function check(name){const local=localRoot+'/'+name,remote=cloneRoot+'/'+name;
 const a=(await git(local,['ls-files','-z'])).split('\0').filter(Boolean).sort(),b=(await git(remote,['ls-files','-z'])).split('\0').filter(Boolean).sort();
 const result={repo:name,local_commit:(await git(local,['rev-parse','HEAD'])).trim(),remote_clone_commit:(await git(remote,['rev-parse','HEAD'])).trim(),local_tree:(await git(local,['rev-parse','HEAD^{tree}'])).trim(),remote_clone_tree:(await git(remote,['rev-parse','HEAD^{tree}'])).trim(),tracked_files:a.length,missing_paths:a.filter(x=>!b.includes(x)),extra_paths:b.filter(x=>!a.includes(x)),mismatches:[],bytes:0};
 const hashes=new Array(a.length); let next=0;
 await Promise.all(Array.from({length:8},async()=>{while(next<a.length){const i=next++,p=a[i];const [left,right]=await Promise.all([fs.readFile(local+'/'+p),fs.readFile(remote+'/'+p)]);result.bytes+=left.length;const h=crypto.createHash('sha256').update(left).digest('hex');hashes[i]=p+'\0'+h+'\n';if(!left.equals(right))result.mismatches.push(p)}}));
 result.path_and_sha256_digest=crypto.createHash('sha256').update(hashes.join('')).digest('hex');result.verified=result.local_commit===result.remote_clone_commit&&result.local_tree===result.remote_clone_tree&&!result.missing_paths.length&&!result.extra_paths.length&&!result.mismatches.length;
 result.remote_clean=(await git(remote,['status','--porcelain'])).trim()==='';result.private_source_files=a.filter(x=>x.startsWith('private-sources/'));return result}
(async()=>{const result=await Promise.all(['distill-novels','writing-vault'].map(check));await fs.writeFile(output,JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result));if(result.some(x=>!x.verified||!x.remote_clean||x.private_source_files.length))process.exitCode=1})().catch(e=>{console.error(e);process.exitCode=1});
