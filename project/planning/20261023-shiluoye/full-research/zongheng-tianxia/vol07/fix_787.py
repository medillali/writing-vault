import json,pathlib
p=pathlib.Path(__file__).parent/'chapter-notes.jsonl'
ns=[json.loads(x) for x in p.read_text(encoding='utf-8').splitlines()]
for n in ns:
 if n['chapter_id']=='ch-0787':
  n['facts']=[s.replace('大师给击杀野兽2700只的村庄任务','大师给难度2700的击杀野兽村庄任务') for s in n['facts']]
  n['state_changes']=[s.replace('2700野兽任务','难度2700野兽任务') for s in n['state_changes']]
p.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in ns),encoding='utf-8')
