from pathlib import Path
import json,subprocess,difflib,hashlib,sys
sys.stdout.reconfigure(encoding='utf-8');R=Path(__file__).resolve().parents[2];V=R/'writing-vault';P=Path(__file__).parent
def git(*args,raw=False):
 x=subprocess.run(['git','-c',f'safe.directory={V.as_posix()}','-C',str(V),*args],capture_output=True,check=True).stdout
 return x if raw else x.decode('utf-8').strip()
assert not git('diff','--cached','--name-only'),'有其他暂存内容，须先分离'
prefix='**[按书名、作者、小说类型浏览书库](书库/README.md)** · **[全书剧情地图](书库/全书剧情地图/README.md)**\n\n'
before=(V/'README.md').read_bytes()
if before.startswith(prefix.encode()):
 before=before[len(prefix.encode()):];assert before==(P/'README-before-navigation.bin').read_bytes()
else:
 assert not (P/'README-before-navigation.bin').exists(),'README在整合期间被其他任务更新，先审查'
 (P/'README-before-navigation.bin').write_bytes(before);(V/'README.md').write_bytes(prefix.encode()+before)
head=git('show','HEAD:README.md',raw=True).decode('utf-8');patch=''.join(difflib.unified_diff(head.splitlines(True),(prefix+head).splitlines(True),fromfile='a/README.md',tofile='b/README.md'))
(P/'readme-navigation.patch').write_bytes(patch.encode('utf-8'));git('apply','--cached','--check',str(P/'readme-navigation.patch'));git('apply','--cached',str(P/'readme-navigation.patch'))
for filename in ['START-HERE.md','AGENTS.md']:
 assert not git('diff','--name-only','--',filename),'已有其他修改：'+filename
 f=V/filename;body=f.read_text(encoding='utf-8');(P/(filename+'.before')).write_text(body,encoding='utf-8')
 if filename=='START-HERE.md':body=body.replace('- **[贼胆', '- **[书库：按书名、作者、类型浏览](书库/README.md)**，或直接进入[全书剧情地图](书库/全书剧情地图/README.md)。\n- **[贼胆',1)
 else:body+='\n- Git书目导航入口为`书库/README.md`，书名、作者、类型目录由`书库/catalog.json`和`书库/重建目录.py`维护。这里只索引已发布研究范围；不把建档或未提交续读标成全书完成。全书地图集中在`书库/全书剧情地图/README.md`。\n'
 f.write_text(body,encoding='utf-8')
receipt={'root_readme_staged_patch_only':True,'preserved_readme_remainder_sha256':hashlib.sha256(before).hexdigest(),'prefix':prefix,'changed_existing_documents':['README.md','START-HERE.md','AGENTS.md']}
(P/'integration.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(receipt,ensure_ascii=False))
