from pathlib import Path
import json,re,sys
R=Path(__file__).resolve().parents[2];V=R/'.verify/two-books';p=V/'private-sources/normalized/manifest.json'
m=json.loads(p.read_text(encoding='utf-8'))
s=next(x for x in m['sources'] if '练级专家' in x['title'])
bad=[c for c in s['chapters'] if c['title'] not in ['章前内容','序章'] and not re.match(r'^第\d+章',c['title'])]
print('FALSE_HEADINGS',json.dumps(bad,ensure_ascii=False))
if '--apply' not in sys.argv:raise SystemExit(0)
assert len(bad)==1 and bad[0]['title'].startswith('第一回合的交手')
correct=[]
for c in s['chapters']:
    if c in bad:
        correct[-1]['end_offset']=c['end_offset'];correct[-1]['end_line']=c['end_line']
    else:correct.append(dict(c))
for i,c in enumerate(correct,1):c['chapter_id']=f'ch-{i:04}'
s['chapters']=correct;s['chapter_headings']=[c['title'] for c in correct]
for rev in s['revisions']:
    if rev['revision']==s['revision']:rev['chapters']=correct
p.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# 该source记录仅是本次隔离worktree的新建临时记录，尚无Git提交。
# 删除这一个新记录后，通过正式导入重新登记审核过的索引，避免直接覆盖主档。
sid=s['source_id'];record=V/f'library/sources/{sid}.json'
assert record.resolve().is_relative_to(V.resolve())
import subprocess
git=['git','-c',f'safe.directory={V.as_posix()}','-C',str(V)]
assert subprocess.run(git+['cat-file','-e',f'HEAD:library/sources/{sid}.json'],capture_output=True).returncode!=0
record.unlink()
sys.path.insert(0,str(R/'distill-novels/scripts'))
from library import execute,parser
print(execute(parser().parse_args(['--vault',str(V),'sources-import','--file',str(p)])))
audit={'issue':'正文第一回合被识别为回标题','source_id':sid,'revision':s['revision'],'original_segments':389,'corrected_segments':len(correct),'false_start_line':bad[0]['start_line'],'merged_into_previous_chapter':correct[316]['title'],'method':'人工核验标题后并入上一章节；正文及其SHA不变；首轮实读段ID不变。','production_tool_changed':False}
out=V/'library/reports/two-books-20261023/validation/chapter-index-correction.json';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(audit,ensure_ascii=False))
