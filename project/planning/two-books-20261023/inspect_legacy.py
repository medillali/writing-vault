from pathlib import Path
import json
R=Path(__file__).resolve().parents[2]
D=R.parent/'Chinese Novel/books/zeidan/distillation'
for name in ['entities','scenes','threads']:
    d=json.loads((D/f'{name}.json').read_text(encoding='utf-8'))
    print(name,len(d),'keys',sorted({k for x in d for k in x}))
    print('first',json.dumps(d[0],ensure_ascii=False))
    print('last',json.dumps(d[-1],ensure_ascii=False)[:1200])
    print('with_facts',sum(bool(x.get('facts')) for x in d),'with_evidence',sum(bool(x.get('evidence')) for x in d))
