import json
from pathlib import Path
r=Path(__file__).parent
p=r/'chapter-notes.jsonl'
ns=[json.loads(x) for x in p.read_text(encoding='utf-8').splitlines()]
for n in ns:
    if n['chapter_id']=='ch-0417':
        n['facts']=[x.replace('冰茶因孵扣级不在榜','冰茶未列此榜，原因未本章展示') for x in n['facts']]
    if n['chapter_id']=='ch-0413':
        msg='冰茶口述已练小龙龟，但前文蛋需150孵、此后仍明确145，资格/时序不一致；不能凭未列榜反推一次实际扣级。'
        if msg not in n['unresolved']:n['unresolved'].append(msg)
p.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in ns),encoding='utf-8')
for bn,cid in [('batch043.json',413),('batch044.json',417)]:
    p=r/bn
    vs=json.loads(p.read_text(encoding='utf-8'))
    live=next(n for n in ns if int(n['chapter_id'][3:])==cid)
    target=next(n for n in vs if n['index']==cid)
    for k in ['facts','inferences','state_changes','unresolved']:target[k]=live[k]
    p.write_text(json.dumps(vs,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('corrected qualified statements in notes and batch snapshots')
