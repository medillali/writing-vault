"""20项专项经真实逐项主审后的单独发布，不替代完整终点问题审计。"""
import hashlib,json,sys
from pathlib import Path
B=Path(__file__).resolve().parent;R=B.parents[2];D=B/'tianxia-wushuang';dest=R/'writing-vault/library/reports/tianxia-wushuang'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
expected={'cross-volume-focused-review.json':'00ca004028d616c4387f0f7df372146dfd9e183c3c91e000b3bed14573d5321b','cross-volume-focused-review.md':'7e2ead9a1a80388996b67af1a5b28fd66994509920171f8c3194355b6ca9d318'}
for n,h in expected.items():assert sha(D/n)==h
data=read(D/'cross-volume-focused-review.json');assert len(data['findings'])==20
for x in data['input_sha256_snapshot']:assert sha(R/x['path'])==x['sha256']
cf=next(x for x in data['findings'] if x['id']=='cf-17-distinct-medical-events')
assert cf['status']=='confirmed_retrospective_identity_with_separate_medical_chains'
assert 'L58565' in cf['verification_attribution']['primary']
for n in expected:(dest/n).write_bytes((D/n).read_bytes())
review=dict(reviewer='primary',status='reviewed_for_library_import',user_approval=False,findings_reviewed=20,
 scope='20项JSON结论/限制和完整MD逐项语义审阅；15正式输入SHA核对。root实际完整回读0695凭证确认林500CC供血，cf17由暂待核改明确身份回收，与晚期抗原分链。其他19项保持冻结稿。',
 input_sha256=expected,input_documents_verified=15,
 limits=['该专项不代替全部人物弧和历史/本地原子项终点评定。','未冒称由primary独自重读所有无双原文，未自动接受用户审美。'])
(dest/'audit/cross-volume-focused-review-primary.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8');print(json.dumps({'special_review':'20-findings-published','inputs_verified':15,'remaining':'全书人物弧与全问题终点审计'},ensure_ascii=False))
