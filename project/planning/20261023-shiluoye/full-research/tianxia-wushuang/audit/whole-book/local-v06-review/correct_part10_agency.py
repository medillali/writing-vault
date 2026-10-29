"""落实primary三项施为边界反馈，保留全部其余57项原值。"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path
here=Path(__file__).resolve().parent
jf=here/'adjudications-local-v06-part10.json'
old=json.loads(jf.read_text(encoding='utf-8'))
backup=here/'part10-before-agency.json'
if backup.exists(): raise FileExistsError(backup)
backup.write_bytes(jf.read_bytes())
f=here/'spec-v06-part10.json'
spec=json.loads(f.read_text(encoding='utf-8'))
changes={
592:'1259所述救赎承诺在1265被当前借体者吞魂背约反证，1268明确明宇借林浅身体；原林浅是否真悔、1259当时由谁发言未独立证实。往史仍为NPC自述，不全客观化或跨书改史。',
594:'1265三魂确交、SS奖实得，但当前王子身体/借体者捏碎吞魂背约，主承诺帮助救赎未实现；不把系统完成等作三师和解，亦无证宣魂永久湮灭。',
595:'1262艾听陆转述悔意而停止攻击、自刎后主才拾魂，残血不直接等于得魂；第三1264杀圣魔林再取，后证均有明确取得步骤。不由借体者后来背约倒证原王子独立悔意必假。'
}
for row in spec:
    if row[0] in changes: row[3]=changes[row[0]]
f.write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
subprocess.run([sys.executable,str(here/'draft_batch.py'),f.name,'decisions-v06-part10.json'],check=True)
subprocess.run([sys.executable,str(here/'review_io.py'),'finalize','decisions-v06-part10.json'],check=True)
new=json.loads(jf.read_text(encoding='utf-8'))
delta=[]
for a,b in zip(old,new):
    if a!=b:
        assert {k for k in a if a[k]!=b[k]}=={'rationale'}
        delta.append({'candidate_id':a['candidate_id'],'before_rationale':a['rationale'],'after_rationale':b['rationale']})
assert len(delta)==3
(here/'part10-agency-delta.json').write_text(json.dumps({'primary_requested':True,'changed_items':delta,'unchanged_other_items':57,'all_statuses_and_evidence_unchanged':True,'new_json_sha256':hashlib.sha256(jf.read_bytes()).hexdigest()},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('changed only 3 rationales; unchanged other 57 and all statuses/evidence verified')
