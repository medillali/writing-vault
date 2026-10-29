from inspect import R,V,P,git
import json
def load(p):return json.loads(p.read_text(encoding='utf-8'))
for f in (V/'library/sources').glob('*.json'):
 x=load(f);print(json.dumps({'source':x.get('source_id'),'title':x.get('title'),'author':x.get('author'),'keys':list(x)},ensure_ascii=False))
for f in (V/'library/reports/super-skeleton/reading/plot').rglob('*manifest*.json'):
 x=load(f);print(f.relative_to(V).as_posix(),list(x) if isinstance(x,dict) else len(x))
