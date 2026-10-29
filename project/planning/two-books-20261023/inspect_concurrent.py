from pathlib import Path
import json
R=Path(__file__).resolve().parents[2];V=R/'writing-vault'
for p in (V/'library/sources').glob('*.json'):
    x=json.loads(p.read_text(encoding='utf-8'))
    print('SOURCE',p.name,x['title'],x['revision'],len(x['revisions'][-1]['chapters']))
for name in ['chr-zeidan-legacy-e0001.json']:
    x=json.loads((V/'library/characters'/name).read_text(encoding='utf-8'))
    print('ASSET',json.dumps(x,ensure_ascii=False)[:2800])
for p in (V/'exchanges/runs').glob('*20261023*'):
    x=json.loads(p.read_text(encoding='utf-8'))
    print('RUN',p.name, {k:v for k,v in x.items() if k not in ['completed_chapters','pending_chapters']})
print('REPORTS',[p.name for p in (V/'library/reports').iterdir()])
