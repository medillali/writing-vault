"""精确应用primary已批准的六处对象，禁止整包重生成。"""
import json,hashlib,copy
from pathlib import Path
P=Path(__file__).parent;D=P/'primary-delta';B=D/'before';B.mkdir(parents=True,exist_ok=True)
def digest(b):return hashlib.sha256(b).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
proposal=P/'continuity-proposal/before-after.json'
assert digest(proposal.read_bytes())=='1cb9ad3e1dc0c11616667fcbd1d78db314857fb58ff658c6d3d736d7fda5bee7'
q=json.loads(proposal.read_bytes());extra=json.loads((P/'primary-extra-proposal.json').read_bytes())
before_files={}
for name in ['analysis.json','cards.json','graph.json','build_research.py','research_characters.py','research_scenes.py','research_graph.py','read-log.json','chapter-notes.jsonl','reader-state.json','handoff.md']:
 raw=(P/name).read_bytes();assert not (B/name).exists();(B/name).write_bytes(raw);before_files[name]=digest(raw)
A=json.loads((B/'analysis.json').read_bytes());C=json.loads((B/'cards.json').read_bytes());oa=copy.deepcopy(A);oc=copy.deepcopy(C)
assert digest((B/'analysis.json').read_bytes())==q['analysis_before_sha256']
delta=[]
for i,r in enumerate(q['changes']):
 assert A['dimensions']['continuity'][i]==r['before']
 A['dimensions']['continuity'][i]=r['after'];delta.append({'file':'analysis.json','path':['dimensions','continuity',i],'before':r['before'],'after':r['after']})
assert A['source_anomalies'][31]['description']==extra['before']
A['source_anomalies'][31]['description']=extra['after'];delta.append({'file':'analysis.json','path':extra['path'],'before':extra['before'],'after':extra['after']})
peier=next(c for c in C if c['origin_key'].endswith('/character/peier'))
old='洛克女、欧西姐妹；主敬护，徐翊统军属她。';new='洛克之女、西奥多与欧恩之妹；主敬护，徐翊在其南征统下任元帅。'
assert peier['content']['relationships']==old
peier['content']['relationships']=new;delta.append({'file':'cards.json','origin_key':peier['origin_key'],'path':['content','relationships'],'before':old,'after':new})
# 去掉六处后其余对象必须完全等于原核心。
ta=copy.deepcopy(A);tc=copy.deepcopy(C)
ta['dimensions']['continuity']=oa['dimensions']['continuity']
ta['source_anomalies'][31]['description']=oa['source_anomalies'][31]['description']
next(c for c in tc if c['origin_key'].endswith('/character/peier'))['content']['relationships']=old
assert ta==oa and tc==oc
assert digest((P/'graph.json').read_bytes())==before_files['graph.json']
save(P/'analysis.json',A);save(P/'cards.json',C)
receipt={'status':'applied-primary-approved','proposal_sha256':digest(proposal.read_bytes()),'approved_by':'primary messages 2026-10-26: 四观察+source_anomalies31.description+佩儿relationships','before_files':before_files,'deltas':delta,'only_approved_objects_changed':True,'unchanged_core':['graph.json','read-log.json','chapter-notes.jsonl','reader-state.json'],'after':{n:digest((P/n).read_bytes()) for n in ['analysis.json','cards.json','graph.json']},'note':'未重跑builder，report读取精修后的JSON再导出；原装配脚本before齐，冻结后不得重跑。'}
save(D/'application-receipt.json',receipt)
save(P/'continuity-proposal/application-receipt.json',{'status':'applied-primary-approved','proposal_sha256':receipt['proposal_sha256'],'delta_receipt':'../primary-delta/application-receipt.json','analysis_after_sha256':receipt['after']['analysis.json']})
lines=['# 卷四primary指定修订精确差异','','状态：已按primary批准应用，未重生其他核心。','','- 4个continuity整观察（事实/推断证据含新增946/956四对象）。','- source_anomalies[31].description：968当前双武改已重铸的蝴蝶/镇岳，龙池是前态。','- 佩儿content.relationships：明确洛克之女/西奥多欧恩之妹。','','其他32九维、103张其余卡、佩儿其他字段、全图、readlog、原四栏、原reader与原逐章疑点全部未改。before核心、装配和清单均在before/，精确对象见application-receipt.json。','']
(D/'delta.md').write_text('\n'.join(lines),encoding='utf-8')
print(json.dumps({'after':receipt['after'],'delta_count':len(delta),'receipt_sha256':digest((D/'application-receipt.json').read_bytes())},ensure_ascii=False))
