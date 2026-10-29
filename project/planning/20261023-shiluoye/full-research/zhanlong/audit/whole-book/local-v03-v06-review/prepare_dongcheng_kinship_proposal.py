"""扫描六卷当前层与本书canon，生成最小亲缘外置提案；原件不改。"""
from pathlib import Path
import json,hashlib,re
H=Path(__file__).resolve().parent;A=H.parent;R=Path('C:/Users/Administrator/Documents/ChatGPT/Novel')
S=R/'.planning/20261023-shiluoye/full-research/zhanlong';F=R/'writing-vault/library/reports/zhanlong';L=R/'writing-vault/library'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
old='雷：亲妹/希望记忆重建';new='雷：同一收养家庭的义妹/家人；雷为东城风收养的故人之子，不以血缘亲妹作事实；希望记忆重建'
paths=[]
for v in range(1,7):
 paths += [p for p in (S/f'vol{v:02d}').glob('*') if p.suffix in ['.json','.jsonl','.md','.py']]
 paths += [p for p in F.glob(f'vol{v:02d}-*') if p.suffix in ['.json','.jsonl','.md']]
for p in (L/'characters').glob('*.json'):
 if 'src-20f2d16e3d1b472fa4b230ab0e1770c9' in p.read_text(encoding='utf-8-sig'):paths.append(p)
paths += [L/'views'/f'{p.stem}.md' for p in paths[:] if p.parent==L/'characters' and (L/'views'/f'{p.stem}.md').exists()]
hits=[];inputsha={}
def walk(x,path):
 if isinstance(x,str):
  if re.search('亲妹|亲兄妹|亲生妹妹|亲妹妹',x) and re.search('东城|苍雷|阿雷|雷：',x):hits.append(dict(file=current,path=path,value=x))
 elif isinstance(x,list):
  for i,y in enumerate(x):walk(y,path+[i])
 elif isinstance(x,dict):
  for k,y in x.items():walk(y,path+[k])
for p in dict.fromkeys(paths):
 current=p.relative_to(R).as_posix();inputsha[current]=sha(p)
 if p.suffix=='.json':walk(load(p),[])
 elif p.suffix=='.jsonl':
  for n,line in enumerate(p.read_text(encoding='utf-8-sig').splitlines()):
   if line.strip():walk(json.loads(line),['jsonl',n])
 else:
  for n,line in enumerate(p.read_text(encoding='utf-8-sig').splitlines(),1):
   if re.search('亲妹|亲兄妹|亲生妹妹|亲妹妹',line) and re.search('东城|苍雷|阿雷|雷：',line):hits.append(dict(file=current,path=['line',n],value=line))
changes=[]
for h in hits:
 if old not in h['value']:continue
 changes.append(dict(file=h['file'],input_sha256=inputsha[h['file']],field_path=h['path'],before=h['value'],proposed_after=h['value'].replace(old,new)))
out=dict(status='proposal_pending_primary_application',actual_reviewer='zongheng_vol05_full',scope='六卷stage当前根文件/正式volNN当前根文件/本书canon人物与对应readable；历史before/provenance快照不修改',source_check=dict(chapter_id='ch-0139',start_line=12116,end_line=12218,reading_scope='本裁定者本次实际完整读该章全部索引行；原首次读者归属不改，primary也已独立全文复核',precise_evidence=[dict(source_id='src-20f2d16e3d1b472fa4b230ab0e1770c9',revision='61ab0b114c76446fda554abfafdac8c432cd88afaba7c2541f4473a3902134e3',chapter_id='ch-0139',start_line=12149,end_line=12149,claim_kind='fact'),dict(source_id='src-20f2d16e3d1b472fa4b230ab0e1770c9',revision='61ab0b114c76446fda554abfafdac8c432cd88afaba7c2541f4473a3902134e3',chapter_id='ch-0139',start_line=12174,end_line=12181,claim_kind='fact')]),rationale='林读手机资料称风膝下一女月/另养子雷；风亲口说雷为故人子七岁双亲亡后自己养大。称同一收养家庭的义兄妹/家人，不以未明血缘亲妹作事实，不编同母异父等隐史。',changes=changes,scan=dict(input_files=len(inputsha),input_sha256=inputsha,all_qualifying_hits=hits,limits='普通妹妹/哥哥称谓不改；其他人物亲妹与本书无关不改；两池原题与历史readers不改'))
p=A/'priority-corrections-dongcheng-kinship-proposal.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
md=['# 雷月亲缘措辞最小外置提案','','原冻结文件不改。实际整章核raw139 L12116—12218；精确链L12149资料、L12181东城风自述。这里只纠明确血缘“亲妹”，普通妹妹称呼保留。','']
for c in changes:md += ['- '+c['file']+' '+str(c['field_path'])+' SHA '+c['input_sha256'],'  - before：'+c['before'],'  - after：'+c['proposed_after']]
p.with_suffix('.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
print(json.dumps(dict(proposal_sha256=sha(p),changes=changes,hits=len(hits),scanned=len(inputsha)),ensure_ascii=False))
