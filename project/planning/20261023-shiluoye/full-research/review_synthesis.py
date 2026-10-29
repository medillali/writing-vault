"""按维度审整书新综合；固定上游全文仍保留在原JSON。"""
import pathlib,json,sys
sys.stdout.reconfigure(encoding='utf-8')
data=json.loads(pathlib.Path(sys.argv[1]).read_text(encoding='utf-8'))
for dimension in sys.argv[2].split(','):
    for row in data['dimensions'][dimension]:
        result={k:v for k,v in row.items() if k not in ['supporting_observations','evidence']}
        result['supporting_observations']=[{k:o.get(k) for k in ['volume','dimension','index_zero_based','observation_id']} for o in row['supporting_observations']]
        result['evidence_chapters']=list(dict.fromkeys(e['chapter_id'] for e in row.get('evidence',[])))
        print(json.dumps({'dimension':dimension,**result},ensure_ascii=False,separators=(',',':')))
