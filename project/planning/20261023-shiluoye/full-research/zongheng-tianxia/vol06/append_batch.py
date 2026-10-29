import json,pathlib,sys
b=pathlib.Path(__file__).resolve().parent
existing={json.loads(x)['chapter_id'] for x in (b/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()}
data=json.loads((b/sys.argv[1]).read_text(encoding='utf-8'))
assert not (existing&{n['chapter_id'] for n in data})
with (b/'chapter-notes.jsonl').open('a',encoding='utf-8') as f:
 for n in data:f.write(json.dumps(n,ensure_ascii=False)+'\n')
