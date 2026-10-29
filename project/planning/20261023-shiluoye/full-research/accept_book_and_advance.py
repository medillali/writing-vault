"""后两书全部正式研究、真实主审和独立审计验收后，才推进活动来源。"""
from pathlib import Path
import datetime, hashlib, json, runpy, sys
from validate_book_audit import validate

B=Path(__file__).resolve().parent; ROOT=B.parents[2]
sys.path.insert(0,str(ROOT/'distill-novels/scripts'))
from fictionlib.vault import Vault

def read(p):return json.loads(p.read_text(encoding='utf-8'))
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    slug=sys.argv[1]
    assert slug in {'tianxia-wushuang','zhanlong'}
    assert '--reviewed' in sys.argv,'仅整书语义审阅完成后执行'
    stage=B/slug; src=read(stage/'source.json')
    vault=ROOT/'writing-vault'; dest=vault/'library/reports'/slug
    collection=vault/'library/reports/collection'
    coverage=read(dest/'audit/full-reading-validation.json')
    assert coverage['status']=='passed' and coverage['source_id']==src['source_id']
    body=sum(v['body_units'] for v in src['volumes'])
    assert coverage['body_units']==body and coverage['indexed_segments']==len(src['chapters'])
    for name,digest in coverage['formal_input_sha256'].items():assert sha(dest/name)==digest,name
    synthesis=read(dest/'book-synthesis.json'); sr=read(dest/'audit/book-synthesis-review.json')
    assert len(synthesis['dimensions'])==9 and sum(map(len,synthesis['dimensions'].values()))==36
    assert sr['reviewer']=='primary' and sr['user_approval'] is False
    assert sha(dest/'book-synthesis.json')==sr['published_json_sha256']
    assert sha(dest/'book-synthesis.md')==sr['published_markdown_sha256']
    published=validate(ROOT,slug)
    # 验收页链接到这份实际独立核验结果；仅控制台输出不能替代可读回执。
    write(dest/'audit/whole-book/publication-validation.json',published)
    runpath=vault/'exchanges/runs'/f'run-deep-{slug}-20261025.json'
    run=read(runpath)
    assert run['source_id']==src['source_id'] and run['source_revision']==src['revision']
    assert set(run['completed_chapters'])=={c['chapter_id'] for c in src['chapters']} and not run['pending_chapters']
    assert run['completed_volumes']==[v['volume'] for v in src['volumes']]
    remaining=['三书及蜗牛材料统一比较管理','三书最终备份与实际恢复','用户审阅']
    if slug=='tianxia-wushuang':remaining.insert(0,'斩龙全量蒸馏')
    title={'tianxia-wushuang':'网游之天下无双','zhanlong':'斩龙'}[slug]
    receipt=dict(status='full-source-nine-dimensions-and-terminal-audit-complete',
        accepted_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        source_id=src['source_id'],source_revision=src['revision'],body_units=body,
        indexed_segments=len(src['chapters']),volumes=len(src['volumes']),
        volume_package_cards=coverage['cards'],source_total_cards=coverage['source_total_cards'],
        whole_book_synthesis_observations=36,whole_book_audit=published,
        review_status='draft',user_approval=False,remaining_project_work=remaining,
        remote_save='本任务未提交或推送；本地完成不等远程已保存')
    write(dest/'ACCEPTANCE.json',receipt)
    c=published['counts']
    (dest/'ACCEPTANCE.md').write_text(f'''# 《{title}》整书研究验收

{body}个正文阅读单元、含书首共{len(src['chapters'])}片段完成分工全文阅读与{len(src['volumes'])}卷九维研究。逐章记录保留真实读者归属；36条全书综合、{c['characters']}人物弧、{c['findings']}聚焦终态、{c['historical']}历史项与{c['local']}原子问题完成主代理审阅和独立发布核验，研究仍待用户审阅。

[全书入口](README.md) · [九维综合](book-synthesis.md) · [人物全弧](character-arcs.md) · [问题账本](question-ledger.md) · [独立发布核验](audit/whole-book/publication-validation.json) · [全文覆盖](audit/full-reading-validation.json) · [结构化验收](ACCEPTANCE.json)

分卷保留当时状态，终点判断独立叠加；未知不等作者遗漏。新分卷卡数与含旧卡的全源卡数分列于结构化验收，不重复累计。

本地整书研究完成不等三书统一管理或最终备份恢复已经完成；它们另行验收。本任务未提交或推送Git、未写入Space或ChatGPT记忆，个人审美及原创设定未自动填入。
''',encoding='utf-8')
    run.update(state='full-source-read-and-distilled',all_dimensions_complete=True,
        terminal_audit_complete=True,user_review_pending=True,
        book_acceptance=f'library/reports/{slug}/ACCEPTANCE.json',
        notes=f'{body}正文/{len(src["chapters"])}片段、{len(src["volumes"])}卷九维/全书综合/人物弧与问题终点审计均正式保存并主审；用户审阅待定。三书任务未完，本任务未推送Git。')
    Vault(vault).checkpoint(run)
    config=read(collection/'catalog-config.json'); book=config['books'][src['source_id']]
    book.update(task_state='completed_full_nine',note=f'{body}正文及书首已全文阅读，逐卷九维、全书综合和终态审计均正式验收；研究仍待用户审阅。本任务未推送Git，旧来源及人工评价保留。')
    extra={r['path']:r for r in book.get('additional_reports',[])}
    extra[f'../{slug}/ACCEPTANCE.md']={'title':'本地整书研究验收','path':f'../{slug}/ACCEPTANCE.md'}
    book['additional_reports']=list(extra.values())
    next_sid=read(B/'zhanlong/source.json')['source_id'] if slug=='tianxia-wushuang' else None
    config['active_source_id']=next_sid
    if next_sid:
        config['books'][next_sid].update(task_state='active',note='前两书整书研究已正式验收；现按六卷全量阅读全文，未读范围不标完成。')
    write(collection/'catalog-config.json',config)
    runpy.run_path(str(collection/'rebuild_catalog.py'),run_name='__main__')
    print(json.dumps(dict(book=slug,status=receipt['status'],active_source_id=next_sid,project_complete=False),ensure_ascii=False))

if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8');main()
