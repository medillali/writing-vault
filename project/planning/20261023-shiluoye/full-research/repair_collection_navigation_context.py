"""保旧正式字节，补旧短名入口并登记不可改写历史MD的原导航上下文。"""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent;R=B.parents[2];V=R/'writing-vault';C=V/'library/reports/collection'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
src=B/'zongheng-tianxia/vol07/review-changes.md';dest=V/'library/reports/zongheng-tianxia/review-changes.md';assert not dest.exists();dest.write_bytes(src.read_bytes());assert sha(src)==sha(dest)
p=V/'library/reports/tianxia-wushuang/report.md';assert not p.exists();p.write_text('# 早期交接报告短名入口\n\n卷一与卷二的原交接均使用阶段目录内短名`report.md`。正式库按卷保存报告，本入口保留旧交接字节并明确分卷，不能把两卷并成一份报告。\n\n- [卷一九维报告](vol01.md)\n- [卷二九维报告](vol02.md)\n- [本书正式入口](README.md)\n',encoding='utf-8')
base='library/reports/tianxia-wushuang';folder=base+'/audit/synthesis-revisions/before-identity-guild-field-fix';corr=base+'/audit/research-corrections'
definitions=[(corr+'/before-scale-book-synthesis.md',{'book-synthesis.json':corr+'/before-scale-book-synthesis.json'}),(corr+'/before-scale-cross-volume-focused-review.md',{'cross-volume-focused-review.json':corr+'/before-scale-cross-volume-focused-review.json'}),(folder+'/01-book-synthesis-draft.md',{'book-synthesis-draft.json':folder+'/00-book-synthesis-draft.json'}),(folder+'/04-book-synthesis.md',{'book-synthesis.json':folder+'/03-book-synthesis.json'}),(folder+'/07-ACCEPTANCE.md',{'ACCEPTANCE.json':folder+'/06-ACCEPTANCE.json','book-synthesis.md':folder+'/04-book-synthesis.md'})]
entries=[]
for name,overrides in definitions:
    assert (V/name).is_file()
    entries.append({'archive_path':name,'sha256':sha(V/name),'original_navigation_base':base,'exact_snapshot_targets':{k:{'path':v,'sha256':sha(V/v)} for k,v in overrides.items()},'role':'immutable_historical_source_not_current_navigation','boundary':'历史MD原字节不改；相对链接按原上下文解释，若有对应旧JSON使用准确旧版本，不能以快照所在目录当原目录。'})
target=C/'qa/historical-markdown-contexts.json';assert not target.exists();target.write_text(json.dumps({'schema_version':1,'entries':entries,'current_navigation_files_exempted':False,'original_archives_unchanged':True},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=C/'三书最终验收.md';text=p.read_text(encoding='utf-8')
for old,new in [("{'character': 153, 'scene': 207, 'pattern': 72}",'432'),("{'character': 295, 'scene': 364, 'pattern': 92}",'751'),("{'character': 271, 'scene': 300, 'pattern': 78}",'649')]:assert text.count(old)==1;text=text.replace(old,new)
p.write_text(text,encoding='utf-8')
print(json.dumps({'added_current_short_name_entries':2,'historical_markdown_contexts':len(entries),'original_frozen_files_changed':0},ensure_ascii=False))
