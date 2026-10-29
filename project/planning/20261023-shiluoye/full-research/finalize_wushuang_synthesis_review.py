"""主代理逐项读完36条并核修指定delta后的真实签收。"""
from pathlib import Path
import hashlib,json,sys
sys.stdout.reconfigure(encoding='utf-8')
B=Path(__file__).parent;d=B/'tianxia-wushuang'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
a=read(d/'book-synthesis-draft.json');dims=a['dimensions']
assert sha(d/'book-synthesis-draft.json')=='3e270c00e6ac14d25d62cc48faf9923040cc107cea0ed9b35e0283d2dc7c9c2d'
assert sha(d/'book-synthesis-draft.md')=='04864c47759b23ebded8a69a752984129e1fd6be7d469f3ef3a7b9299b1c585e'
targets=[('worldbuilding',3,'fact_summary'),('characters',2,'limits_and_counterevidence'),('characters',3,'limits_and_counterevidence'),('plot',2,'fact_summary'),('narrative',0,'fact_summary'),('pacing',1,'fact_summary'),('dialogue',2,'fact_summary'),('themes',2,'fact_summary'),('continuity',1,'fact_summary'),('continuity',3,'limits_and_counterevidence')]
for k,i,f in targets:print(json.dumps({'row':f'{k}.{i+1}','field':f,'value':dims[k][i][f]},ensure_ascii=False))
assert sum(map(len,dims.values()))==36
assert all('再以实际执行和状态变化检验，保不能被同一动作解决的残余' not in r['mechanism'] for rs in dims.values() for r in rs)
review=dict(reviewer='primary',status='reviewed_for_library_import',source_id=read(d/'source.json')['source_id'],user_approval=False,
 scope='primary逐项完整审36全书九维综合的主张、事实摘要、可迁移方法、适用反证、原创变换、后期检验；全部8卷已分别主审正式入库。继承证据的结构核验不冒充新增正文阅读。',
 corrections_verified=read(d/'book-synthesis-draft/primary-synthesis-delta-applied.json')['changes'],
 original_source_rechecks=['1455全文片段115228—115247：冰兰提问/心然向其谈爱陆之由，陆远未听。','0695已实际整章回读58512—58599：献血凭证58565—58569明确500CC林逸欣献予陆尘，与末卷抗原不同事件。'],
 remaining=['人物弧、全历史及本地原子问题终点审计尚需独立主审验收。','三书比较管理与最终备份恢复另验；用户审美未自动接受。'],
 input_sha256={n:sha(d/n) for n in ['book-synthesis-draft.json','book-synthesis-draft.md']})
(d/'primary-synthesis-review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('PRIMARY_36_SEMANTIC_REVIEW_PINNED')
