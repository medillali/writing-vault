"""保存已发生的主代理原文复读范围；不改变原读者或唯一覆盖数。"""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent;R=B.parents[2];s=json.loads((B/'zhanlong/source.json').read_text(encoding='utf-8'));cs={c['chapter_id']:c for c in s['chapters']}
rows=[]
for n in [499,500,1067,1358]:
    c=cs[f'ch-{n:04d}'];rows.append(dict(chapter_id=c['chapter_id'],start_line=c['start_line'],end_line=c['end_line'],full_text_read=True,actual_reader='primary',unique_coverage_increment=0))
for n,a,z in [(445,37035,37045),(999,74066,74078),(1000,74083,74100),(1199,87370,87386),(1155,84350,84360),(1001,74200,74212),(1041,76714,76720)]:
    c=cs[f'ch-{n:04d}'];assert c['start_line']<=a<=z<=c['end_line'];rows.append(dict(chapter_id=c['chapter_id'],start_line=a,end_line=z,full_text_read=False,actual_reader='primary',unique_coverage_increment=0))
p=R/'writing-vault/library/reports/zhanlong/audit/primary-rereads/identity-and-terminal-addendum-20261026.json';assert not p.exists()
d=dict(status='actual-primary-reread-ranges-recorded',source_id=s['source_id'],revision=s['revision'],purpose='王将与王翦分人、洛洵死亡分期、徐焰军团与死亡、弗雷报告渠道及火犁名词边界核对。1358已在前回执记前段，本次补齐全章；不改旧回执字节。',ranges=rows,full_chapters=4,limited_ranges=7,unique_coverage_increment=0,limits='仅记录实际工具输出已阅范围，不冒主代理个人全书重读；820/821本轮再次全文复核已在先前回执计过，不重复增唯一覆盖。')
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()),ensure_ascii=False))
