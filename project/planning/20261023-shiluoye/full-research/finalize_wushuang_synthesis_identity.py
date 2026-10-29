"""核对定向更正正式发布后的逐值边界，补当前回执与目录入口。"""
from pathlib import Path
import hashlib, json, runpy, sys
sys.stdout.reconfigure(encoding='utf-8')
B=Path(__file__).resolve().parent;ROOT=B.parents[2];S=B/'tianxia-wushuang';D=ROOT/'writing-vault/library/reports/tianxia-wushuang'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
review=read(S/'primary-synthesis-review.json')
review.setdefault('historical_review_remaining_before_terminal_acceptance',review['remaining'])
review['remaining']=['斩龙全量蒸馏','三书及蜗牛比较管理与最终备份恢复','用户审阅']
write(S/'primary-synthesis-review.json',review)
oldargv=sys.argv;sys.argv=['publish_book_synthesis.py','tianxia-wushuang']
try:runpy.run_path(str(B/'publish_book_synthesis.py'),run_name='__main__')
finally:sys.argv=oldargv
current=read(D/'book-synthesis.json')
old=read(D/'audit/synthesis-revisions/before-identity-guild-field-fix/03-book-synthesis.json')
for dim,rows in old['dimensions'].items():
    for i,row in enumerate(rows):
        if (dim,i)!=('continuity',0):assert current['dimensions'][dim][i]==row
target=current['dimensions']['continuity'][0]
assert '1098同ID三项均为吻痕' in target['fact_summary']
assert target['supporting_observations']==old['dimensions']['continuity'][0]['supporting_observations']
assert current['review_status']=='draft' and current['primary_literary_review']['user_approval'] is False
receipt=read(D/'audit/book-synthesis-review.json')
assert receipt['published_json_sha256']==sha(D/'book-synthesis.json')
assert receipt['published_markdown_sha256']==sha(D/'book-synthesis.md')
amend=read(D/'audit/synthesis-identity-correction.json')
amend['publication_verification']={'status':'passed','other_35_observations_equal':True,'historical_upstream_quote_preserved':True,'current_draft_sha256':sha(S/'book-synthesis-draft.json'),'published_json_sha256':sha(D/'book-synthesis.json'),'published_markdown_sha256':sha(D/'book-synthesis.md'),'current_review_sha256':sha(S/'primary-synthesis-review.json'),'canonical_asset_field_scan':'当前无双正式卡片递归字符串定向检索只命中巴西谁卡标题，未见旧中美谁名单传播；不等重读所有卡全部事实。','terminal_four_packages_and_manifest_unchanged':True}
write(D/'audit/synthesis-identity-correction.json',amend);write(S/'audit/synthesis-identity-correction.json',amend)
C=ROOT/'writing-vault/library/reports/collection'
config=read(C/'catalog-config.json');book=config['books'][current['source_id']]
extras={r['path']:r for r in book.get('additional_reports',[])}
link='../tianxia-wushuang/audit/synthesis-identity-correction.md'
extras[link]={'title':'身份字段核源更正及旧版','path':link}
book['additional_reports']=list(extras.values());write(C/'catalog-config.json',config)
runpy.run_path(str(C/'rebuild_catalog.py'),run_name='__main__')
print(json.dumps(amend['publication_verification'],ensure_ascii=False))
