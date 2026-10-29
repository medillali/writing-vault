"""发布经主代理文学审阅的整书综合，仍保留用户待审阅状态。"""
import pathlib,json,hashlib,datetime,sys,copy
sys.stdout.reconfigure(encoding='utf-8')
base=pathlib.Path(__file__).resolve().parent;root=base.parents[2];slug=sys.argv[1]
stage=base/slug;vault=root/'writing-vault';dest=vault/'library/reports'/slug
def read(p):return json.loads(p.read_text(encoding='utf-8'))
data=read(stage/'book-synthesis-draft.json');md=(stage/'book-synthesis-draft.md').read_text(encoding='utf-8')
assert slug in {'zongheng-tianxia','tianxia-wushuang','zhanlong'},'仅支持本项目已登记三书'
review=None
if slug!='zongheng-tianxia':
    # 后续作品的发布必须签收本书最终稿，不能沿用纵横的主审描述。
    review=read(stage/'primary-synthesis-review.json')
    assert review.get('reviewer')=='primary' and review.get('status')=='reviewed_for_library_import'
    assert review.get('source_id')==read(stage/'source.json')['source_id']
    for name in ['book-synthesis-draft.json','book-synthesis-draft.md']:
        assert hashlib.sha256((stage/name).read_bytes()).hexdigest()==review['input_sha256'][name],name
    coverage=read(dest/'audit/full-reading-validation.json')
    assert coverage['status']=='passed'
    assert coverage['body_units']==sum(v['body_units'] for v in read(stage/'source.json')['volumes'])
    for name,digest in coverage['formal_input_sha256'].items():
        assert hashlib.sha256((dest/name).read_bytes()).hexdigest()==digest,name
assert data['validation']['observations']==36 and len(data['dimensions'])==9
assert all(row['claim_kind']=='synthesis' for rows in data['dimensions'].values() for row in rows)
checked=[]
for group in data['upstream_documents']:
    for doc in group['documents']:
        if doc['exists']:
            path=root/doc['path'];assert path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest()==doc['sha256'],doc['path']
            checked.append(doc['path'])
data=copy.deepcopy(data)
data.update(status='literary-reviewed-user-review-pending',review_status='draft',overview=md.splitlines()[2],overview_claim_kind='synthesis')
data['primary_literary_review']={'reviewer':'primary','reviewed_observations':36,'user_approval':False,
    'verified_corrections':['艾兰复明就业与林克/米拉/达芙妮死亡分对象','幕后劳动措辞','丁舒升原名与误称边界','426分卷卡与含旧6张的432全源卡分开'],
    'limits':'本次通过综合文学审阅，独立人物弧与全历史问题终点审计另验，研究未成为用户审美或原创正典。'}
if review:
    data['primary_literary_review']={**review,'reviewed_observations':36,'user_approval':False}
dest.mkdir(parents=True,exist_ok=True)
(dest/'book-synthesis.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
md=md.replace('(book-synthesis-draft.json)','(book-synthesis.json)')
md+='\n\n## 主代理审阅记录\n\n36条跨卷综合已经逐条审阅，事实误配与措辞已核修；上游正式文件哈希经发布时复核。研究仍待用户审阅，不自动收藏或写入原创设定。全书人物弧、历史问题及终点复核另列，不由本综合代替。\n\n[返回本书入口](README.md) · [疑点终点账本](question-ledger.md)\n'
# 问题账本尚未发布时不提前生成断链；终点发布会再加入口。
md=md.replace(' · [疑点终点账本](question-ledger.md)','')
(dest/'book-synthesis.md').write_text(md,encoding='utf-8')
remaining=['人物全弧审计','全历史问题终点审计','整书及三书最终验收','用户审阅']
terminal_validation=dest/'audit/whole-book/publication-validation.json'
if terminal_validation.exists() and read(terminal_validation).get('status')=='published-audit-validation-passed':
    remaining=['三书比较管理与最终备份恢复','用户审阅']
receipt={'status':'passed-for-research-library','reviewer':'primary','user_approval':False,'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'observations':36,'input_documents_verified':len(checked),'source_draft_sha256':hashlib.sha256((stage/'book-synthesis-draft.json').read_bytes()).hexdigest(),'published_json_sha256':hashlib.sha256((dest/'book-synthesis.json').read_bytes()).hexdigest(),'published_markdown_sha256':hashlib.sha256((dest/'book-synthesis.md').read_bytes()).hexdigest(),'remaining':remaining}
(dest/'audit/book-synthesis-review.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(receipt,ensure_ascii=False))
