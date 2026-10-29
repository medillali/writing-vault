"""卷五历史问题的定向核源，不把检索计为全章阅读。"""
from check_volume import WORK,read
from pathlib import Path
import re,sys
sys.stdout.reconfigure(encoding='utf-8')
S=read(WORK/'zhanlong/source.json');lines=Path(S['normalized_path']).read_text(encoding='utf-8').splitlines()
queries=[
 ('星辰戒',1180,1386,r'星辰戒'),
 ('龙域龙神',1180,1386,r'龙域|龙神'),
 ('新十五王',1180,1386,r'十五|15位|15名|点将|君王'),
 ('七曜联盟',1180,1386,r'七曜|同盟'),
 ('活口司法',1180,1386,r'日本人|活口|审讯|判刑|囚禁'),
 ('徐焰礼葬',987,1386,r'徐焰|礼葬|北迁'),
 ('唐心药',997,1386,r'唐心'),
 ('囚魂六王',1109,1386,r'囚魂|死契|六.{0,6}君王|君王.{0,6}六'),
 ('指定赠物',1111,1386,r'XTS|神将战膝|十五万|15万'),
 ('LV双手技能',1158,1386,r'LV|双手武|双手剑|双手精|包包|利刃空旋'),
 ('纸职位',1112,1386,r'副盟主|吕.{0,2}宾'),
 ('商业纪苑',1142,1386,r'巴黎|婉约|纪苑'),
 ('自废同老',1179,1386,r'自废|一起老|同老|废.{0,6}阳炎'),
 ('罗布列岛',1174,1386,r'罗布|列岛|夏叶.{0,10}军'),
 ('补给防线',1169,1386,r'龙晶箭|6000|六千|五十船|50艘|土城'),
 ('八转卡牌',1180,1386,r'八转|命运卡牌|净化'),
 ('转职神格',1180,1386,r'转职|八次|八阶|第八|九转'),
 ('具体赠物',982,1386,r'凯迪拉克|XTS|神将战膝|斗气化臂'),
 ('纸职位精读',1112,1386,r'纸上画魅.{0,30}(副盟|薪|吕)|(副盟|薪|吕).{0,30}纸上画魅|吕纯阳'),
]
i=int(sys.argv[1]);a=int(sys.argv[2]) if len(sys.argv)>2 else 0;z=int(sys.argv[3]) if len(sys.argv)>3 else a+25
label,lo,hi,pat=queries[i];hits=[]
for c in S['chapters']:
 if lo<=int(c['chapter_id'][3:])<=hi:
  for n in range(c['start_line'],c['end_line']+1):
   if re.search(pat,lines[n-1],re.I):hits.append((c['chapter_id'],n,lines[n-1]))
print('QUERY',i,label,lo,hi,'TOTAL',len(hits),'PAGE',a,z)
for cid,n,line in hits[a:z]:print(cid,f'L{n}',line)
print('END_QUERY_PAGE',len(hits[a:z]))
