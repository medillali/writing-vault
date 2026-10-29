"""模型完成指定材料阅读后显式登记；此脚本不打开小说正文或制造阅读记录。"""
import json,sys,hashlib
from pathlib import Path
from datetime import datetime,timezone
sys.stdout.reconfigure(encoding='utf-8');P=Path(__file__).parent;B=P.parent;ROOT=P.parents[4];v=int(sys.argv[1]);D=B/f'vol{v:02d}'
assert v in [6,7,8]
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
p=P/'late-material-read-log.json'
data=read(p) if p.exists() else dict(reader='/root/zongheng_vol03_full',record_kind='research_material_reading_not_new_original_fulltext',full_original_book_read_by_synthesizer=False,volumes=[],complete_volumes=[],original_fulltext_scopes=[dict(volume=3,raw_first='ch-0229',raw_last='ch-0606',segments=378,body_units=376),dict(volume=8,raw_first='ch-1573',raw_last='ch-1609',segments=37,body_units=37)])
a=read(D/'analysis.json');state=read(D/'reader-state.json');assert state['complete_volume']
files=['analysis.json','handoff.md']
if v==6:files+=['primary-corrections.json','reading-attribution.json']
if v==7:files+=['primary-review-delta.json']
if v==8:files+=['cards.json','graph.json','reader-merge-validation.json']
assert all((D/n).is_file() for n in ['analysis.json','cards.json','graph.json','report.md','handoff.md','validation.json'])
documents=[dict(path=(D/n).relative_to(ROOT).as_posix(),sha256=hashlib.sha256((D/n).read_bytes()).hexdigest()) for n in files]
if v==7:
 formal=ROOT/'writing-vault/library/reports/tianxia-wushuang/vol07-analysis.json'
 assert read(formal)['dimensions']==a['dimensions']
 documents.append(dict(path=formal.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(formal.read_bytes()).hexdigest()))
row=dict(volume=v,source_reader=state.get('reader'),documents=documents,dimensions={d:len(rows) for d,rows in a['dimensions'].items()},reading_method='已完整显示阅读九维全部fact/inference/mechanism/limits字段，继承证据定位；handoff完整读，不冒认该卷原文亲读。' if v!=8 else '本代理构造并逐项研究全部36九维/81卡/图；primary68条逐章笔记此前分批完整阅读，尾37片本人原文亲读。',full_dimension_text_read=True,unresolved_output_truncations=0,new_original_fulltext_reads=0,recorded_at=datetime.now(timezone.utc).isoformat())
if v==7:row['reading_method']='已重新完整读取正式vol07-analysis全部45条fact/inference及90条独立mechanism/limits字段；完整读取最终handoff及primary-review-delta，旧预读稿已撤回。正式与暂存九维逐项等同，不冒认原文亲读。'
data['volumes']=[x for x in data['volumes'] if x['volume']!=v]+[row];data['volumes'].sort(key=lambda x:x['volume']);data['complete_volumes']=[x['volume'] for x in data['volumes']];data['status']='late_stage_materials_fully_read' if data['complete_volumes']==[6,7,8] else 'waiting_remaining_late_stage_materials'
p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(status=data['status'],complete_volumes=data['complete_volumes']),ensure_ascii=False))
