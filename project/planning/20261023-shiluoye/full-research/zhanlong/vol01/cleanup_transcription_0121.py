"""仅清理已存手写笔记两处草稿缩写，不改变事实或阅读计数。"""
import json
from pathlib import Path
P=Path(__file__).parent
fixes={'ch-0099':('后895系统','后L8595系统'),'ch-0121':('三友34?此段仍30余','三友此段仍30余')}
for filename in ('batch025.json','batch030.json'):
 p=P/filename; x=json.loads(p.read_text(encoding='utf-8'))
 for n in x['notes']:
  if n['chapter_id'] in fixes:
   old,new=fixes[n['chapter_id']];n['facts']=[v.replace(old,new) for v in n['facts']]
 p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=P/'chapter-notes.jsonl';rows=[json.loads(s) for s in p.read_text(encoding='utf-8').splitlines() if s.strip()]
for n in rows:
 if n['chapter_id'] in fixes:
  old,new=fixes[n['chapter_id']];n['facts']=[v.replace(old,new) for v in n['facts']]
p.write_text(''.join(json.dumps(n,ensure_ascii=False)+'\n' for n in rows),encoding='utf-8')
print('cleaned two transcription fragments; coverage unchanged')
