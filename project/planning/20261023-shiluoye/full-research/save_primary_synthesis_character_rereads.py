"""保存主代理实际核源范围；复读不增加全文唯一覆盖。"""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent;R=B.parents[2];source=json.loads((B/'zhanlong/source.json').read_text(encoding='utf-8'))
cs={c['chapter_id']:c for c in source['chapters']}
full=[(139,12116,12218),(1262,91320,91389),(820,63066,63118),(821,63119,63175),(1357,97621,97678),(1359,97756,97823)]
parts=[(257,22394,22418),(258,22424,22449),(356,30280,30309),(965,72015,72043),(102,8859,8885),(103,8967,8977),(1358,97679,97703),(1366,98258,98275)]
rows=[]
for isfull,entries in [(True,full),(False,parts)]:
    for raw,a,z in entries:
        cid=f'ch-{raw:04d}';c=cs[cid];assert c['start_line']<=a<=z<=c['end_line']
        if isfull:assert (a,z)==(c['start_line'],c['end_line'])
        rows.append(dict(chapter_id=cid,start_line=a,end_line=z,full_text_read=isfull,actual_reader='primary',unique_coverage_increment=0))
d=dict(status='actual-primary-reread-ranges-recorded',source_id=source['source_id'],revision=source['revision'],purpose='综合与人物主审的材料名称、责任归属、收养链、姓名和时点核对；不修改首次全文读者归属。',ranges=rows,full_chapters=6,limited_ranges=8,unique_coverage_increment=0,limits='这是本次已发生阅读的范围记录，不由脚本生成文学结论；不宣主代理独自读完原文全书。')
p=R/'writing-vault/library/reports/zhanlong/audit/primary-rereads/synthesis-and-character-crosschecks-20261026.json';assert not p.exists()
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(full_chapters=6,limited_ranges=8,unique_coverage_increment=0,sha256=hashlib.sha256(p.read_bytes()).hexdigest()),ensure_ascii=False))
