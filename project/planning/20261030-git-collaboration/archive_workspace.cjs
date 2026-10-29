// 原工作区资料的可审计归档；不复制源小说、运行副本或二进制备份。
const fs=require('node:fs/promises'),path=require('node:path'),crypto=require('node:crypto');
const root=path.resolve(__dirname,'../..'),dest=path.join(root,'writing-vault/project');
const ignored=new Set(['.git','node_modules','__pycache__','.cache','catalog-stage']);
const rows=[],excluded=[];
async function copyOne(source,relative){
 const stat=await fs.lstat(source);
 if(stat.isSymbolicLink()){excluded.push({path:path.relative(root,source).replaceAll('\\','/'),reason:'symbolic-link'});return}
 if(stat.isDirectory()){
  const name=path.basename(source);
  if(ignored.has(name)||name.startsWith('.assembly-tmp-')||(name==='package'&&source.replaceAll('\\','/').endsWith('/full_distill/graph-layout/package'))){excluded.push({path:path.relative(root,source).replaceAll('\\','/'),reason:'runtime-or-assembly-temp'});return}
  for(const name of await fs.readdir(source))await copyOne(path.join(source,name),path.join(relative,name));
 }else if(stat.isFile()){
  if(/\.(pyc|pyo|tgz|zip)$/i.test(source)||path.basename(source)==='.DS_Store'){excluded.push({path:path.relative(root,source).replaceAll('\\','/'),reason:'runtime-or-backup'});return}
  const target=path.join(dest,relative);await fs.mkdir(path.dirname(target),{recursive:true});
  await fs.copyFile(source,target);const body=await fs.readFile(source);
  rows.push({workspace_path:path.relative(root,source).replaceAll('\\','/'),repository_path:path.relative(path.join(root,'writing-vault'),target).replaceAll('\\','/'),bytes:body.length,sha256:crypto.createHash('sha256').update(body).digest('hex')});
 }
}
(async()=>{
 for(const name of ['AGENTS.md','novel.cmd','小说工作台.md','task_plan.md','findings.md','progress.md'])await copyOne(path.join(root,name),path.join('workspace',name));
 await copyOne(path.join(root,'docs'),'workspace/docs');
 await copyOne(path.join(root,'.planning'),'planning');
 await copyOne(path.join(root,'exports'),'exports');
 for(const name of ['full_distill','review'])await copyOne(path.join(root,'distill-novels/work',name),path.join('tool-work',name));
 // 下载的图布局依赖不是项目研究内容，避免再次归档第三方包。
 const vendors=rows.filter(r=>r.repository_path.includes('/graph-layout/package/'));
 if(vendors.length)throw Error('第三方依赖包未被排除，应先调整目录筛选');
 await fs.mkdir(path.join(dest,'sync'),{recursive:true});
 const report={requested_on:'2026-10-30',scope:'workspace framework, plans, workbench, handoff exports and authored research work',copied_files:rows.length,total_bytes:rows.reduce((s,x)=>s+x.bytes,0),files:rows,excluded,other_excluded:['private-sources','backups/*.zip','.verify','.codex-remote-attachments','distill-novels/work/demo*','distill-novels/work/devdeps','distill-novels/work/real_novel_test']};
 await fs.writeFile(path.join(dest,'sync/local-inputs-manifest.json'),JSON.stringify(report,null,2)+'\n');
 console.log(JSON.stringify({copied_files:report.copied_files,total_MiB:+(report.total_bytes/1048576).toFixed(2),excluded:excluded.length}));
})().catch(e=>{console.error(e);process.exitCode=1});
