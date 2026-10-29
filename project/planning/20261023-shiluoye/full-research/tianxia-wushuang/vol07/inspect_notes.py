import json,pathlib,sys
sys.stdout.reconfigure(encoding='utf-8')
H=pathlib.Path(__file__).resolve().parent
lo=int(sys.argv[1]);hi=int(sys.argv[2])
for l in (H/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines():
 n=json.loads(l);i=int(n['chapter_id'][3:])
 if lo<=i<=hi:
  print(n['chapter_id'],n['title'],n['start_line'],n['end_line'])
  print(' | '.join(n['state_changes']))
  print('未明：'+' | '.join(n['unresolved']))
