import pathlib,json,sys,re
sys.stdout.reconfigure(encoding='utf-8')
root=pathlib.Path(__file__).resolve().parents[2]
old=root.parent/'Chinese Novel'
print('OLD BOOKS')
for p in (old/'books').iterdir():
    if p.is_dir():
        print(p.name, [q.name for q in p.iterdir()])
print('OLD ZEIDAN MANIFEST')
j=json.loads((old/'books/zeidan/manifest.json').read_text(encoding='utf-8'))
print(json.dumps({k:(v[:2] if isinstance(v,list) else v) for k,v in j.items()},ensure_ascii=False)[:14000])
for slug in ['tianxia-wushuang','zongheng-tianxia','zhanlong']:
    s=json.loads((root/'.planning/20261023-shiluoye'/slug/'source.json').read_text(encoding='utf-8'))
    t=pathlib.Path(s['normalized_path']).read_text(encoding='utf-8').splitlines()
    print(slug,'AUTHOR NOTES')
    hits=[i for i,l in enumerate(t) if any(x in l for x in ['新书《斩龙》','新书，书名','新书书名','纵横天下》','天下无双》'])]
    for i in hits:
        if i<400 or i>len(t)-400:print(i+1,t[i])
