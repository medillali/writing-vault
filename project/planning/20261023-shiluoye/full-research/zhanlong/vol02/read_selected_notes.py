import pathlib,json,sys
sys.stdout.reconfigure(encoding='utf-8')
p=pathlib.Path(__file__).parent
rows={int(x['chapter_id'].split('-')[1]):x for x in map(json.loads,(p/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines())}
for n in map(int,sys.argv[1:]):
 print(json.dumps(rows[n],ensure_ascii=False))
