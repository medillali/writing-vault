"""仅补齐主审后装配/验证的冻结支持清单，不重建六核心。"""
import pathlib,json,hashlib,sys
P=pathlib.Path(__file__).parent;sys.stdout.reconfigure(encoding='utf-8')
def read(n):return json.loads((P/n).read_text(encoding='utf-8'))
def save(n,x):(P/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=read('freeze-manifest.json');assert m['status']=='draft-frozen-after-approved-primary-proposals'
assert all(h(P/n)==d for n,d in m['core_sha256'].items())
assert all(h(P/n)==d for n,d in m['support_sha256'].items())
replay=read('assembly-replay-validation.json');assert replay['status']=='passed' and replay['chapter_indexes_equal']
snapshot='review-corrections/after-approved-before-assembly-manifest.json';(P/snapshot).write_bytes((P/'freeze-manifest.json').read_bytes())
validation=read('validation.json');validation.update(approved_semantic_replay=True,report_exact_one_paragraph=True,current_assembly_entrypoint='assemble_approved_review.py',reading_and_chapter_indexes_unchanged=True)
save('validation.json',validation)
extra=['assemble_approved_review.py','assembly-replay-validation.json',snapshot,'review-corrections/assembly-source-before/manifest.json']
extra += ['review-corrections/assembly-source-before/'+n for n in read('review-corrections/assembly-source-before/manifest.json')['sha256']]
for n in set(list(m['support_sha256'])+extra):m['support_sha256'][n]=h(P/n)
m.update(status='draft-frozen-for-primary-final-recheck',assembly=dict(entrypoint='assemble_approved_review.py',method='重放主审前六核心+明确批准proposal；不运行旧手写生成器',proposal_sha256=h(P/'primary-review-proposal.json'),replay_validation='assembly-replay-validation.json'),notes='primary已批准10对象+report单段后受控合入；其余逐值不变，原notes/state/log和逐章索引不变。结构校验与获准重放passed，仍待primary最后复核/正式入库。')
save('freeze-manifest.json',m)
print(json.dumps(dict(status='frozen',manifest_sha256=h(P/'freeze-manifest.json'),merged_delta_sha256=h(P/'primary-review-merged-delta.json'),validation_sha256=h(P/'validation.json'),assembly_replay_sha256=h(P/'assembly-replay-validation.json'),core_sha256=m['core_sha256'],support_files=len(m['support_sha256'])),ensure_ascii=False))
