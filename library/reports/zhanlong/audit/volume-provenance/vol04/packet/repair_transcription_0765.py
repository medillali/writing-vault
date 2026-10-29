"""清理本代理手写草稿的两处表述，不改原文/阅读状态事实。"""
import json
from pathlib import Path
P=Path(__file__).parent
p=P/'batch001.json';x=json.loads(p.read_text(encoding='utf-8'))
for n in x['notes']:
 n['facts']=[s.replace('她姐弟首发现（双月姐妹）','她与妹妹首发现') for s in n['facts']]
p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=P/'chapter-notes.jsonl';rows=[json.loads(s) for s in p.read_text(encoding='utf-8').splitlines() if s.strip()]
for n in rows:
 if n['chapter_id']=='ch-0755':n['facts']=[s.replace('她姐弟首发现（双月姐妹）','她与妹妹首发现') for s in n['facts']]
p.write_text(''.join(json.dumps(n,ensure_ascii=False)+'\n' for n in rows),encoding='utf-8')
for filename in ('batch003.json','reader-state.json'):
 p=P/filename;x=json.loads(p.read_text(encoding='utf-8'));key=x['current_state']['protagonist']
 x['current_state']['protagonist']=key.replace('643魅仅由+100条件推不当新面板','新魅力只据任职+100条件而未重列面板，不自行改算')
 p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('two handwriting fragments cleaned; source and coverage unchanged')
