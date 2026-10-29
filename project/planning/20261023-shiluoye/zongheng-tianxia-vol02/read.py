import json, pathlib, sys
sys.stdout.reconfigure(encoding='utf-8')
base=pathlib.Path(__file__).resolve().parent
src=json.loads((base.parent/'zongheng-tianxia/source.json').read_text(encoding='utf-8-sig'))
data=src if src.get('normalized_path') else next(x for x in src['revisions'] if x['revision']==src['revision'])
chapters=data.get('chapters',src.get('chapters'))
if sys.argv[1]=='meta':
    print(json.dumps({'source_id':src['source_id'],'revision':src['revision'],'chapters':[c for c in chapters[50:101]]},ensure_ascii=False,indent=2))
else:
    lines=pathlib.Path(data['normalized_path']).read_text(encoding='utf-8').splitlines()
    for n in range(int(sys.argv[1]),int(sys.argv[2])+1):
        c=chapters[n]
        print('\n=== '+json.dumps(c,ensure_ascii=False)+' ===')
        for i in range(c['start_line']-1,c['end_line']):
            print(f'{i+1}: {lines[i]}')
        print('=== FULL CHAPTER END ===')
