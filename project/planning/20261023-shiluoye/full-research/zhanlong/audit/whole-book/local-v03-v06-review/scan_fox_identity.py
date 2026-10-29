from pathlib import Path
import json,hashlib,sys
sys.stdout.reconfigure(encoding='utf-8')
R=Path('C:/Users/Administrator/Documents/ChatGPT/Novel');A=Path(__file__).resolve().parent.parent;B=A.parents[1];F=R/'writing-vault/library/reports/zhanlong'
sid='src-20f2d16e3d1b472fa4b230ab0e1770c9';rev='61ab0b114c76446fda554abfafdac8c432cd88afaba7c2541f4473a3902134e3'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
paths=[]
for v in range(1,7):
 paths+=list((B/f'vol{v:02d}').glob('*.json'))+list((B/f'vol{v:02d}').glob('*.md'))+list((B/f'vol{v:02d}').glob('*.jsonl'))+list((B/f'vol{v:02d}').glob('*.py'))+list(F.glob(f'vol{v:02d}-*'))
for kind in ['characters','scenes','patterns']:
 for p in (R/'writing-vault/library'/kind).glob('*.json'):
  if sid in p.read_text(encoding='utf-8-sig'):paths.append(p)
for p in (R/'writing-vault/library/views').glob('*.md'):
 if p.stem=='chr-238cd5b220265eea9f053e12c12b7d59':paths.append(p)
hits=[]
def walk(x,keys,p):
 if isinstance(x,dict):
  for k,y in x.items():walk(y,keys+[k],p)
 elif isinstance(x,list):
  for i,y in enumerate(x):walk(y,keys+[i],p)
 elif isinstance(x,str) and '慕天' in x:hits.append(dict(path=p.relative_to(R).as_posix(),input_sha256=sha(p),field_path=keys,before=x,proposed_after=x.replace('狐狸／慕天','狐狸／刘庸').replace('慕天','刘庸')))
for p in sorted(set(paths)):
 try:
  if p.suffix=='.json':walk(json.loads(p.read_text(encoding='utf-8-sig')),[],p)
  else:
   for i,line in enumerate(p.read_text(encoding='utf-8-sig').splitlines(),1):
    if '慕天' in line:hits.append(dict(path=p.relative_to(R).as_posix(),input_sha256=sha(p),line=i,before=line,proposed_after=line.replace('狐狸／慕天','狐狸／刘庸').replace('慕天','刘庸')))
 except Exception as e:raise RuntimeError(str(p)) from e
src=R/f'writing-vault/private-sources/normalized/sources/{sid}/{rev}.txt';lines=src.read_text(encoding='utf-8-sig').splitlines()
out=dict(status='proposal_pending_primary_no_original_changed',issue='狐狸卡无证别名慕天',source_id=sid,revision=rev,reviewer='zongheng_vol05_full',scan_scope='stage六卷根json/md/jsonl/py、formal六卷根、SID关联canon卡及该人物readable；扫描不是原文逐章重读。',source_scan=dict(normalized_sha256=sha(src),literal_mu_tian_hits=sum('慕天' in x for x in lines),liu_yong_hits=[dict(line=i,text=x) for i,x in enumerate(lines,1) if '刘庸' in x]),changes=hits,interpretation='规范原文慕天零命中仅支持排查；本人本次实际读L8828—8908完整语境（含主L8865、厂主L8880明确姓名），L8972林资料也确认刘庸/琉璃狐。此为派生标题误加无证名，勿列源文姓名漂移或另拆实体。原冻结/已签池/历史回执均保留，未来优先使用经primary批准的外置解释层，不静默改原材料。',precise_evidence=[dict(source_id=sid,revision=rev,chapter_id='ch-0100',start_line=8864,end_line=8889,claim_kind='fact',access_level='targeted-source-context-reread'),dict(source_id=sid,revision=rev,chapter_id='ch-0101',start_line=8972,end_line=8972,claim_kind='fact',access_level='targeted-source-location')])
out['precise_evidence'][0]['chapter_id']='ch-0102';out['precise_evidence'][1]['chapter_id']='ch-0103'
p=A/'priority-corrections-fox-identity-proposal.json';p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
md=['# 狐狸无证别名最小外置提案','','待primary核源；不改冻结六卷、canonical、原题或已签池。未来引用旧材料时，以获批外置纠正层优先。历史import-result/asset-map仅列传播位置，保原字节作为导入历史。','',out['interpretation'],'']
for c in hits:md += ['- '+c['path']+' '+str(c.get('field_path',c.get('line')))+' SHA '+c['input_sha256'],'  - before：'+c['before'],'  - proposed after：'+c['proposed_after']]
p.with_suffix('.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
print(json.dumps(dict(json_sha256=sha(p),md_sha256=sha(p.with_suffix('.md')),changes=hits),ensure_ascii=False,indent=2))
