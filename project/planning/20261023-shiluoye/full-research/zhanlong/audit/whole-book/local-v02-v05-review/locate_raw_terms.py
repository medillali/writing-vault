"""只定向定位原文词句，不声明整章/整书已重读。"""
from save_manual_batch import B,read
import pathlib,re,sys,bisect
sys.stdout.reconfigure(encoding='utf-8')
s=read(B/'source.json');lines=pathlib.Path(s['normalized_path']).read_text(encoding='utf-8').splitlines();starts=[x['start_line'] for x in s['chapters']]
patterns=[re.compile(x) for x in sys.argv[1:]]
for no,line in enumerate(lines,1):
    if any(p.search(line) for p in patterns):
        c=s['chapters'][bisect.bisect_right(starts,no)-1];print(c['chapter_id'],f'L{no}:',line)
