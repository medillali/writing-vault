import pathlib,json,sys
sys.stdout.reconfigure(encoding='utf-8')
root=pathlib.Path(__file__).resolve().parents[2]
s=json.loads((root/'.planning/20261023-shiluoye/zongheng-tianxia/source.json').read_text(encoding='utf-8'))
lines=pathlib.Path(s['normalized_path']).read_text(encoding='utf-8').splitlines()
for n in list(map(int,sys.argv[1:])) or [49]:
    c=s['chapters'][n]
    print(c['chapter_id'],c['title'],c['start_line'],c['end_line'])
    for i in range(c['start_line']-1,c['end_line']):print(f'L{i+1}: {lines[i]}')
