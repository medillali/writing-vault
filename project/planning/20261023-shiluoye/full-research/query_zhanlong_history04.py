"""卷四历史终审的定向原文定位，不自动判定或记全章阅读。"""
from check_volume import WORK,read
from pathlib import Path
import re,sys
sys.stdout.reconfigure(encoding='utf-8')
S=read(WORK/'zhanlong/source.json');lines=Path(S['normalized_path']).read_text(encoding='utf-8').splitlines()
queries=[
 ('洛洵旧疑',969,1386,r'洛洵.{0,40}(侄|孩|毒|谋|武信)|(侄|孩|毒|武信).{0,40}洛洵'),
 ('羽平伤龙',834,1386,r'羽平'),
 ('PaPa营业',961,1386,r'PAPA'),
 ('仙人果酒',967,1386,r'仙人果|仙人醉'),
 ('裴案',969,1386,r'裴赢'),
 ('墓碑',889,1386,r'墓碑|立碑|佩儿之墓'),
 ('艾尔莎',969,1386,r'艾尔莎'),
 ('神殿原批',969,1386,r'神殿.{0,35}(8000|2000|一万|八千|两千)|(8000|2000|一万|八千|两千).{0,35}神殿'),
 ('新矿结果',969,975,r'火神矛|魔山|矿'),
 ('建制新将',969,1010,r'20W|二十万|20万|莫文|万夫长'),
]
i=int(sys.argv[1]);a=int(sys.argv[2]) if len(sys.argv)>2 else 0;z=int(sys.argv[3]) if len(sys.argv)>3 else a+30
label,lo,hi,pat=queries[i];hits=[]
for c in S['chapters']:
 if lo<=int(c['chapter_id'][3:])<=hi:
  for n in range(c['start_line'],c['end_line']+1):
   if re.search(pat,lines[n-1],re.I):hits.append((c['chapter_id'],n,lines[n-1]))
print('QUERY',i,label,lo,hi,'TOTAL',len(hits),'PAGE',a,z)
for cid,n,line in hits[a:z]:print(cid,f'L{n}',line)
print('END_QUERY_PAGE',len(hits[a:z]))
