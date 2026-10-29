"""定向查词定位，打印命中不代表亲读整章或自动得出终评。"""
import json,re,sys
from check_volume import WORK,read
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
s=read(WORK/'zhanlong/source.json');lines=Path(s['normalized_path']).read_text(encoding='utf-8').splitlines()
queries=[
 ('旧师与NPC冉闵',252,1386,r'卡尔|卡特|武悼|冉闵.{0,15}罗林|罗林.{0,15}冉闵'),
 ('细账物件',252,1386,r'圣魂盾|冰壶|空虚扇|500块|500元|五百块|五百元'),
 ('雄霸改革',243,1386,r'小猪.{0,20}(副盟|积分)|(副盟|积分).{0,20}小猪'),
 ('日常邀约',252,1386,r'洛阳|实习|西溪'),
 ('细装补偿',252,400,r'(阿雷|倾浅).{0,15}(补偿|戒指)|(补偿|戒指).{0,15}(阿雷|倾浅)'),
 ('亲友阴谋',262,264,r'汪泽诚|布斯特'),
]
i=int(sys.argv[1]);label,a,z,pattern=queries[i];print('QUERY',i,label,a,z,pattern)
count=0
for c in s['chapters']:
 if a<=int(c['chapter_id'][3:])<=z:
  for n in range(c['start_line'],c['end_line']+1):
   if re.search(pattern,lines[n-1]):print(c['chapter_id'],f'L{n}',lines[n-1]);count+=1
print('QUERY_END',count)
