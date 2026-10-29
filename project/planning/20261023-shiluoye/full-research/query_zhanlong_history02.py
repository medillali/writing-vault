"""定向原文核查命中，按页完整显示，非全章阅读。"""
import re,sys
from pathlib import Path
from check_volume import WORK,read
sys.stdout.reconfigure(encoding='utf-8')
s=read(WORK/'zhanlong/source.json');lines=Path(s['normalized_path']).read_text(encoding='utf-8').splitlines()
queries=[('阳炎突破',505,843,r'阳炎境|突破.*阳炎'),('乘风首成',505,600,r'乘风斩|自创连招'),('旧案照护',505,1386,r'秦雨|秦蒙|若雨|王将'),('王权与通缉',505,530,r'罗雷|通缉|赦|青麟渊'),('南宫后会籍',453,1386,r'(南宫决|南宫灵).{0,20}(斩龙|史诗)|(斩龙|史诗).{0,20}(南宫决|南宫灵)'),('捡回旧物',490,1386,r'破雷|镇魂锤|龙骧战刀|寒铁剑.*补偿'),('骑兵规模',600,753,r'1000.{0,15}铁刃|铁刃.{0,15}1000|万.{0,5}铁刃'),('囚女权剑',315,1386,r'巴林|囚女|奴隶剑')]
i=int(sys.argv[1]);a=int(sys.argv[2]) if len(sys.argv)>2 else 0;z=int(sys.argv[3]) if len(sys.argv)>3 else a+30
queries += [('双刺客技能',754,780,r'不屈战魂|灵魂隐现'),('信号现场',754,968,r'甲骨文|12楼|十二楼|十二层'),('魏案终态',840,1386,r'魏凡.{0,30}(判|狱|死|逮|保释)|(判|狱|死|逮|保释).{0,30}魏凡'),('育龙与记忆',754,1386,r'流霜.{0,12}记忆|记忆.{0,12}流霜|百.{0,6}龙骑|千.{0,6}龙骑'),('细物归还',754,1386,r'执戟者战膝|镇月剑|盘古斧|罗恒')]
queries += [('银戈末击',1100,1180,r'击杀.{0,40}银戈|银戈.{0,25}(击杀|阵亡|死了|死去)'),('七主胜果',1180,1360,r'七.{0,12}主城|主城.{0,12}七|第三.{0,4}国战.{0,20}(结束|胜|赢)|国战结束')]
label,lo,hi,pat=queries[i];hits=[]
for c in s['chapters']:
 if lo<=int(c['chapter_id'][3:])<=hi:
  for n in range(c['start_line'],c['end_line']+1):
   if re.search(pat,lines[n-1]):hits.append((c['chapter_id'],n,lines[n-1]))
print('QUERY',i,label,lo,hi,'TOTAL',len(hits),'PAGE',a,z)
for cid,n,line in hits[a:z]:print(cid,f'L{n}',line)
print('END_QUERY_PAGE',len(hits[a:z]))
