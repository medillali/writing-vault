"""root实际核528全文/1178与1346等原文命中后，精准更新终评草稿。"""
from pathlib import Path
import json,copy,hashlib
B=Path(__file__).parent/'zhanlong';P=B/'audit/whole-book'
def read(q):return json.loads(q.read_text(encoding='utf-8'))
S=read(B/'source.json');C={int(c['chapter_id'][3:]):c for c in S['chapters']}
changes=[];out=P/'primary-history-precision-before';out.mkdir(exist_ok=True)
for name in ['adjudications-history-v02-batch001.json','adjudications-history-v02-batch002.json','adjudications-history-v03-batch001.json','adjudications-history-v03-batch002.json']:
 p=P/name;raw=p.read_bytes();rows=read(p);touched=False
 for r in rows:
  before=copy.deepcopy(r);cid=r['candidate_id']
  if cid=='v02-question-v02-q-escape':r['rationale']=r['rationale'].replace('528活动近结束时玩家实返','528主死后系统提示再等四分钟、结束后主出现/林牧实际复活')
  elif cid=='v02-thread-v02-t-promise':r['rationale']=r['rationale'].replace('528近终返场','528先等四分钟、结束后主出现/林牧复活')
  elif cid=='v03-question-v03-q-global':
   r['rationale']='844林亲述主昏迷导致斩龙放弃全球赛、天空玫瑰冠军/神话第二，不能把国内亚军搬作世界亚军。正式国战随后真开：919主第一战MVP，双城占领与临海委托/凡书失城分结；1346东城说明已拿七城、1347秦雯和1357燕赵的后述相互印证第三轮胜果，但不是每场全赢。'
   r['later_chapters']=[844,879,888,898,915,919,1090,1346,1347,1357]
  elif cid=='v03-thread-v03-t-zishu':
   r['rationale']='595—596有期限自愿约、607以后朋友关系与608留城育龙是真转变；1108百余蛋尚待孵、1146百余龙骑/1316数百实战确成。1178系统明确主末刀杀银戈，NPC主要输出和子舒的贡献分开，不记子舒独杀银戈；1360子舒再生臂实际舒展。608千匹普通练骑马全交仍无独立同批回执，不泛闭每个建设物料。'
   r['later_chapters']=[595,596,600,607,608,1108,1146,1177,1178,1316,1360]
  elif cid=='v03-thread-v03-t-national':r['later_chapters']=r['later_chapters']+[1346,1357]
  if r!=before:
   r['later_evidence']=[{k:S[k] for k in ['source_id','revision']}|{k:C[n][k] for k in ['chapter_id','start_line','end_line']}|{'claim_kind':'inference'} for n in r['later_chapters']]
   changes.append(dict(file=name,candidate_id=cid,before=before,after=copy.deepcopy(r)));touched=True
 if touched:
  assert not (out/name).exists();(out/name).write_bytes(raw);p.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert len(changes)==5
(P/'primary-history-precision-delta.json').write_text(json.dumps(dict(reviewer='primary',basis='root实际528全文，830—833/1178/1346—1347/1357定位命中，以及已全文读的末卷卡片语义。准确时点/末刀/后述渠道，保before。',changes=changes),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
note=dict(source_id=S['source_id'],revision=S['revision'],reader='primary',chapter_id='ch-0528',start_line=C[528]['start_line'],end_line=C[528]['end_line'],full_text_read=True,scope='root在本轮完整BEGIN-END重读528，无截断；重叠原始覆盖不新增正文数。',facts=['李牧、林先后游戏阵亡，主在最后五分钟继续战斗。','主后被问剑杀且爆寒铁等，界面提示再等四分钟，等待后主出现并有60分钟无敌，林与李牧随后复活。','池兄妹被伙伴保护到活动结束；寒铁小白取到、还林后林再亲赠小白，不能说主已拿回。'],research_correction='不能写尚余四分钟已经复活，也不能说每个人死后独立再禁24小时。')
(B/'primary-528-reread.json').write_text(json.dumps(note,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# 只核读者5批准的一项理由差，其余十九条与原真实已读输入逐值相同。
f=P/'adjudications-local-v03-batch001.json';old=P/'local-v03-v06-review/corrections/batch001-time/adjudications-local-v03-batch001.json'
if old.exists():
 a=read(old);z=read(f);diff=[(x,y) for x,y in zip(a,z) if x!=y];assert len(diff)==1
 x,y=diff[0];assert {k:v for k,v in x.items() if k!='rationale'}=={k:v for k,v in y.items() if k!='rationale'}
 assert '活动结束后三人实际复活' in y['rationale']
 print('APPROVED_READER_DELTA',y['candidate_id'],y['rationale'],hashlib.sha256(f.read_bytes()).hexdigest())
print('ROOT_PRECISION_CHANGES',len(changes))
