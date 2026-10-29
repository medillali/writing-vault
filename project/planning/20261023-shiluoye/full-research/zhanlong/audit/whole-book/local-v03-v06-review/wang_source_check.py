from pathlib import Path
import json,sys
sys.stdout.reconfigure(encoding='utf-8')
R=Path('C:/Users/Administrator/Documents/ChatGPT/Novel');B=Path(__file__).resolve().parent.parent.parents[1];s=json.loads((B/'source.json').read_text(encoding='utf-8'));ch={int(c['chapter_id'][3:]):c for c in s['chapters']};lines=(R/f"writing-vault/private-sources/normalized/sources/{s['source_id']}/{s['revision']}.txt").read_text(encoding='utf-8-sig').splitlines()
for n in map(int,sys.argv[1:]):
 c=ch[n];print(f'BEGIN raw{n} L{c["start_line"]}—{c["end_line"]} targeted name contexts, not chapter reread')
 chosen=set()
 for i in range(c['start_line']-1,c['end_line']):
  if any(t in lines[i] for t in ['王将','王翦','若雨','卫戍','寒羽','凌烈','天尘']):chosen.update(range(max(c['start_line']-1,i-1),min(c['end_line'],i+2)))
 for i in sorted(chosen):print(f'L{i+1}: '+lines[i])
 print('END targeted contexts')
