"""仅展示来源规划元数据，不能据此计作正文阅读。"""
import pathlib,json,sys
sys.stdout.reconfigure(encoding='utf-8')
base=pathlib.Path(__file__).resolve().parent
for slug in sys.argv[1:]:
    source=json.loads((base/slug/'source.json').read_text(encoding='utf-8'))
    volumes=[]
    for volume in source['volumes']:
        segments=[s for unit in volume['units'] for s in unit['segments']]
        volumes.append({'volume':volume['volume'],'body_units':volume['body_units'],
                        'segments':len(segments),'first':segments[0]['chapter_id'],'last':segments[-1]['chapter_id']})
    print(json.dumps({'book':slug,'source_id':source['source_id'],'revision':source['revision'],'volumes':volumes},ensure_ascii=False))
