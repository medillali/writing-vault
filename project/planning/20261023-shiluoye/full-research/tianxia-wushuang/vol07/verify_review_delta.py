import json,pathlib,hashlib,sys
sys.stdout.reconfigure(encoding='utf-8');H=pathlib.Path(__file__).resolve().parent
read=lambda n:json.loads((H/n).read_text(encoding='utf-8'))
a,c,g=read('analysis.json'),read('cards.json'),read('graph.json')
for k,es in a['dimensions'].items():
 assert len(es)==5
 for e in es:
  assert len(e['mechanism'])>=2 and len(e['limits_and_counterevidence'])>=2,(k,e['title'])
assert len({json.dumps(e['mechanism'],ensure_ascii=False) for es in a['dimensions'].values() for e in es})==45
assert len({json.dumps(e['limits_and_counterevidence'],ensure_ascii=False) for es in a['dimensions'].values() for e in es})==45
assert hashlib.sha256((H/'chapter-notes.jsonl').read_bytes()).hexdigest()=='5fcedf147fb7d937a9fc0ac329fb04925b70d4e61aa04e83cbb39f131b8be10a'
bad=['林小萌','神农6分','神农六分','六城军团合作','银色龙骑','雷鸣／风吟者','杀兵放19魂','神级玩家全MISS','主真付公证十万','凝视控北林','解盟与解禁名','百骑蛋结界已起','1454心说爱主','1454爱语','1454已听心说爱','1454读者知主未听','自伤龙战','筹修油药','旧逐日靴','故意宣心已死']
for n in ['analysis.json','cards.json','graph.json','report.md','handoff.md']:
 s=(H/n).read_text(encoding='utf-8')
 for b in bad:assert b not in s,(n,b)
delta=read('primary-review-delta.json');delta.update(status='draft_all_received_corrections_applied_pending_primary_review',dimensions_with_independent_mechanism=45,dimensions_with_limits_and_counterevidence=45,original_notes_preserved=True,current_core_sha256={n:hashlib.sha256((H/n).read_bytes()).hexdigest() for n in ['analysis.json','cards.json','graph.json']})
delta['corrections']=[x for x in delta['corrections'] if not x.startswith('图renew')]
delta['corrections'].append('图renew经1311全文复核改knows：心明确问再装病几天、主答应，只指当下陪伴，不倒推早伤/97%假；sulun改陆suspects/苏伦真实所知unknown，反证错误不证明有意说谎')
delta['independently_full_chapter_reread_this_delta']=list(dict.fromkeys(delta['independently_full_chapter_reread_this_delta']+['ch-1311']))
(H/'primary-review-delta.json').write_text(json.dumps(delta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(status='targeted_delta_checked_not_frozen',dimensions=45,cards=len(c),nodes=len(g['nodes']),edges=len(g['edges']),threads=len(g['threads']),core_sha256=delta['current_core_sha256'],notes_preserved=True),ensure_ascii=False))
