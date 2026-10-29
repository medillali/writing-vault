"""只接入已核准更正导航，不改变研究或整书验收状态。"""
from pathlib import Path
import json
B=Path(__file__).resolve().parent;R=B.parents[2]
report=R/'writing-vault/library/reports/zhanlong'
for relative,prefix in [('README.md','audit/'),('reading/README.md','../audit/')]:
    p=report/relative;data=p.read_bytes();text=data.decode('utf-8')
    if 'priority-corrections-wang-identity.md' not in text:
        needle=f'({prefix}priority-corrections-fox-identity.md)'
        assert text.count(needle)==1
        text=text.replace(needle,needle+f'、[王将与王翦分人]({prefix}priority-corrections-wang-identity.md)、[洛洵死亡时点]({prefix}priority-corrections-luoxun-timing.md)')
        p.write_bytes(text.encode('utf-8'))
    if (report/'audit/priority-corrections-xuyan-army.md').is_file() and 'priority-corrections-xuyan-army.md' not in text:
        needle=f'({prefix}priority-corrections-luoxun-timing.md)'
        assert text.count(needle)==1
        text=text.replace(needle,needle+f'、[徐焰所属军团]({prefix}priority-corrections-xuyan-army.md)')
        p.write_bytes(text.encode('utf-8'))
p=R/'writing-vault/library/reports/collection/catalog-config.json'
d=json.loads(p.read_text(encoding='utf-8'));entry=d['books']['src-20f2d16e3d1b472fa4b230ab0e1770c9'] if 'books' in d else d['sources']['src-20f2d16e3d1b472fa4b230ab0e1770c9']
for title,filename in [('王将与王翦独立身份及恋情归属核源纠正','priority-corrections-wang-identity.md'),('洛洵逼令与实际自刎时点核源纠正','priority-corrections-luoxun-timing.md')]:
    path='../zhanlong/audit/'+filename
    assert (report/'audit'/filename).is_file()
    if not any(x['path']==path for x in entry['additional_reports']):entry['additional_reports'].append({'title':title,'path':path})
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
extra='../zhanlong/audit/priority-corrections-xuyan-army.md'
if (report/'audit/priority-corrections-xuyan-army.md').is_file() and not any(x['path']==extra for x in entry['additional_reports']):
    entry['additional_reports'].append({'title':'徐焰所属狂雷军核源纠正','path':extra})
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'navigation_updated':True,'whole_book_acceptance_changed':False,'priority_documents':len(list((report/'audit').glob('priority-corrections*.md')))},ensure_ascii=False))
