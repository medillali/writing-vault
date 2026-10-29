import json,pathlib
b=pathlib.Path(__file__).resolve().parent
p=b/'chapter-notes.jsonl'
ns=[json.loads(x) for x in p.read_text(encoding='utf-8').splitlines()]
n=next(x for x in ns if x['chapter_id']=='ch-0669')
addition='回读补明L72570：系统特殊恢复75%物资军力后，书明确估十多万NPC至少可复七八万；未给逐兵实际复活清册，不把战时全灭写成战后全部永久损失。'
if addition not in n['facts']:n['facts'].append(addition)
n['audit_note']='主代理发现遗漏后，本代理完整回读raw0669原668核实L72568/72570，补明恢复例外；不改实际全文阅读归属。'
p.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in ns),encoding='utf-8')
