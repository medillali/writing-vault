"""从真实账本生成归属与派生复核记录，不增加阅读覆盖。"""
import json,hashlib
from pathlib import Path
P=Path(__file__).parent
N=[json.loads(s) for s in (P/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if s.strip()]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
data={'source_id':N[0]['source_id'],'revision':N[0]['revision'],'volume':4,'full_text_reading':[{'reader':'/root/zongheng_vol03_full','chapter_ids':[n['chapter_id'] for n in N],'raw_fragments':215,'body_units':214,'full_text_read':True,'notes':'卷题ch0754+正文0755—0968；55批每批2—4片即时四栏，读取各次1—2章BEGIN/END齐全。'}],'derived_material_review':{'reader':'/root/zongheng_vol03_full','material':'本人canonical四栏754—869在综合前逐项完整复核；870—968即此前逐章全文和手写四栏，综合按原记录取材；不新增任何正文覆盖。','source':str((P/'chapter-notes.jsonl').relative_to(P.parents[4])),'sha256':sha(P/'chapter-notes.jsonl')},'batches':[{'path':f.name,'sha256':sha(f)} for f in sorted(P.glob('batch[0-9][0-9][0-9].json'))],'raw_note_rows':len(N),'first_read_at':N[0]['read_at'],'last_read_at':N[-1]['read_at'],'unresolved_truncations':0,'status':'reading-complete-research-draft','boundary':'本卷由本代理亲读，不冒称个人亲读全部六卷；正式入库与文学批准由primary处理，用户审美另层。'}
assert len(data['batches'])==55 and len(N)==215
(P/'reading-attribution.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('reading-attribution.json written; 55 batches/215 rows preserved')
