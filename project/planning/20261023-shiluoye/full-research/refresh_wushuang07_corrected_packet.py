"""唯一异常纠正后刷新验证与输入快照，保旧快照为研究历史。"""
from pathlib import Path
import hashlib,json
from check_volume import load_and_check
B=Path(__file__).parent;D=B/'tianxia-wushuang/vol07'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
*_,r=load_and_check('tianxia-wushuang',7)
v=read(D/'validation.json');v.update(r);v['literary_review']='primary_correction_reread_complete';write(D/'validation.json',v)
p=D/'delivery-freeze.json';old=read(p)
archive=D/'delivery-freeze-before-raw1305-correction.json';assert not archive.exists();archive.write_bytes(p.read_bytes())
new=dict(old);new.update(status='primary_reviewed_corrected_packet_snapshot',note='原十几分钟为研究误读；primary完整核源后纠为分盟规模口径。原输入快照另存，原笔记与卡图未动。')
new['files']={name:hashlib.sha256((D/name).read_bytes()).hexdigest() for name in old['files']}
new['files']['primary-corrections.json']=hashlib.sha256((D/'primary-corrections.json').read_bytes()).hexdigest();write(p,new)
print(json.dumps(r))
