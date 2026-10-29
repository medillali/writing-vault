"""保存新增明确后证之前版本，只定向修复天空回归两原子项。"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

here=Path(__file__).resolve().parent
jf=here/'adjudications-local-v06-part08.json'
old=json.loads(jf.read_text(encoding='utf-8'))
backup=here/'part08-before-sky-return.json'
if backup.exists():
    raise FileExistsError(backup)
backup.write_bytes(jf.read_bytes())
specfile=here/'spec-v06-part08.json'
spec=json.loads(specfile.read_text(encoding='utf-8'))
changes={
 457:'1199天空仍君分、1202尚余4天；1221系统已明卡琳九军重返天空且一小时前回中国（L97996—98022），七天条件实际兑现。不能将早君分冻结为终点，也不以王宫间接使用代替这条直接后证。',
 459:'1200七天回城仍预期，1202还有4天；1221正式系统/当章叙事明确卡琳九军重返天空、一小时前已回中国，终点已实际归城，不再留未找到回归时点的假pending。'
}
for row in spec:
    if row[0] in changes:
        row[1]='answered'
        row[3]=changes[row[0]]
        row[4]=[1199,1200,1202,1221]
specfile.write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
subprocess.run([sys.executable,str(here/'draft_batch.py'),specfile.name,'decisions-v06-part08.json'],check=True)
subprocess.run([sys.executable,str(here/'review_io.py'),'finalize','decisions-v06-part08.json'],check=True)
new=json.loads(jf.read_text(encoding='utf-8'))
delta=[]
for a,b in zip(old,new):
    if a!=b:
        delta.append({'candidate_id':a['candidate_id'],'before':a,'after':b})
assert len(delta)==2
(here/'part08-sky-return-delta.json').write_text(json.dumps({'reason':'本轮完整读1221派生note补明确归城回执；原读者是本审卷六前175片，不增加原文重读计数。','unchanged_other_items':58,'changed_items':delta,'new_json_sha256':hashlib.sha256(jf.read_bytes()).hexdigest()},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('changed 2; unchanged 58 verified')
