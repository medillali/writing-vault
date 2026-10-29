"""本卷未冻结笔记的字面收窄；保初稿批次与新增回读修订归属。"""
from pathlib import Path
import json
here=Path(__file__).resolve().parent
p=here/'chapter-notes.jsonl'
rows=[json.loads(s) for s in p.read_text(encoding='utf-8').splitlines()]
row=next(r for r in rows if r['chapter_id']=='ch-0518')
before=row['facts'][0]
old='本活动玩家死后24h禁上线'
new='原文说本次活动玩家挂掉就在24小时内无法上线，不在此独断为每人死亡后另计24小时'
assert old in before
row['facts'][0]=before.replace(old,new)
row['note_corrections']=[{'kind':'literal-scope-narrowing','reason':'0518原句为活动内24h表述；0528实见死亡后仅余4min即活动结束返场，原笔记擅加死后另计过强。未改当章事实进度，仅收窄规则转述。','later_chapter_id':'ch-0528','later_start_line':42831,'later_end_line':42836,'reader':'zongheng_vol05_full'}]
p.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows),encoding='utf-8')
(here/'note-corrections.json').write_text(json.dumps({'status':'unfrozen-own-note-correction','chapter_id':'ch-0518','before_fact':before,'after_fact':row['facts'][0],'basis':row['note_corrections'],'historical_batch_preserved':'batch0517-0520.json'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
