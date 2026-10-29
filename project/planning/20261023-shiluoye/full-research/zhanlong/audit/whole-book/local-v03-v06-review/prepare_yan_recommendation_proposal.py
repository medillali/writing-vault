"""仅写外置提案与定向扫描凭据，不改被冻结阅读或正式文件。"""
from pathlib import Path
import json,hashlib,datetime
H=Path(__file__).resolve().parent;A=H.parent;B=A.parents[1];R=B.parents[3];F=R/'writing-vault/library/reports/zhanlong'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def walk(x,path=()):
 if isinstance(x,dict):
  for k,v in x.items():yield from walk(v,path+(k,))
 elif isinstance(x,list):
  for i,v in enumerate(x):yield from walk(v,path+(i,))
 elif isinstance(x,str) and '百里宁' in x:yield {'path':list(path),'value':x}
files=[p for p in list((B/'vol06').glob('*'))+list(F.glob('vol06-*'))+list((R/'writing-vault/library/characters').glob('*.json')) if p.is_file() and p.suffix in ['.json','.jsonl','.md']]
scan=[];changes=[]
old='L86858—86870李请燕援右/燕要下军会荐百里宁长风统领，李口允须功勋达，是交换承诺非实任。斩龙7万多全到/活动无人可调NPC协战无重炮，主先借船不等违禁带战军。'
new='L86858—86870李请燕援右；燕请求主在下次军团会议举荐燕本人接替年迈百里宁、担任长风军统领，李答允以功勋达到为条件；此时只是举荐承诺，非百里宁被新荐、也非燕已经实任。斩龙7万多全到/活动无人可调NPC协战无重炮，主先借船不等违禁带战军。'
for p in files:
 hits=[]
 if p.suffix=='.json':hits=list(walk(read(p)))
 elif p.suffix=='.jsonl':
  for i,l in enumerate(p.read_text(encoding='utf-8').splitlines()):
   if l.strip():
    row=json.loads(l)
    for hit in walk(row):hits.append({'jsonl_index':i,'chapter_id':row.get('chapter_id'),'reader':row.get('reader'),**hit})
 else:hits=[{'line':i,'value':l} for i,l in enumerate(p.read_text(encoding='utf-8').splitlines(),1) if '百里宁' in l]
 scan.append({'path':p.relative_to(R).as_posix(),'sha256':sha(p),'hits':hits})
 for hit in hits:
  if hit['value']==old:changes.append({'file':p.relative_to(R).as_posix(),'input_sha256':sha(p),**{('field_path' if k=='path' else k):v for k,v in hit.items() if k!='value'},'before':old,'proposed_after':new})
assert len(changes)==3
source=read(B/'source.json')
e=lambda n,s,t:{'source_id':source['source_id'],'revision':source['revision'],'chapter_id':f'ch-{n:04d}','start_line':s,'end_line':t,'claim_kind':'fact'}
proposal={'status':'proposal_only_pending_primary_overlay','actual_reviewer':'zongheng_vol05_full','created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'correction_kind':'research-subject-object-correction','subject':'1192燕请求举荐自己取代百里宁，原短句把被荐对象误归百里宁','changes':changes,'evidence':[e(1192,86857,86870)],'later_outcome_evidence':[e(1234,89535,89546),e(1244,90159,90170)],'later_outcome_scope':'1234主临战任燕代理统领；1244正式升任且佩徽，不倒写1192已任。这两条仅本次实核补充，不改历史阶段。','reading_attribution':'1192/1234/1244原全文初读均本代理；本次实际定向原文重核。root另已实核1192 L86860—69批准事实判别；正式优先overlay由root保存。','unchanged_policy':'不改三个冻结原件、其他正确百里宁句、分卷analysis/cards/readable/canonical人物卡及任何已签终评。','scan_summary':{'files':len(scan),'hits':sum(len(x['hits']) for x in scan),'true_correction_fields':3,'other_hits':'1229牺牲师长/燕职位机会的推断正确，不改；扫描未发现analysis/cards/readable/canonical其他百里宁误荐句。'},'scan_inputs':scan}
out=A/'priority-corrections-yan-recommendation-proposal.json'
if out.exists():assert read(out)['status']=='proposal_only_pending_primary_overlay'
out.write_text(json.dumps(proposal,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
md=['# 燕赵无双举荐对象纠正提案','', '只提案，不改冻结原件。root已核1192事实判别，正式priority层由root保存。','', '原文raw1192 L86864—65：燕求主荐燕自己接年迈百里宁的长风统领位；旧简句误写成荐百里宁。三处同源短句分别在stage批/合并notes/formal notes。','', '后证由本代理本次实际源行复核：raw1234 L89535—46临战代理；raw1244 L90159—70正式升任/佩徽。不能倒写1192已经实任。','']
for c in changes:md += ['- '+c['file']+'；定位：'+str({k:v for k,v in c.items() if k in ['field_path','jsonl_index','chapter_id','reader']}),'  - input SHA256：'+c['input_sha256'],'  - before：'+c['before'],'  - proposed_after：'+c['proposed_after'],'']
md+=['扫描全部候选文件SHA/路径及命中保同名JSON；仅上列三字段需改。1229正确推断不改。终评和原池均不改。']
(A/'priority-corrections-yan-recommendation-proposal.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
print(json.dumps({'proposal':out.name,'sha256':sha(out),'changes':len(changes),'scanned_files':len(scan),'other_correct_hits':sum(len(x['hits']) for x in scan)-3},ensure_ascii=False))
