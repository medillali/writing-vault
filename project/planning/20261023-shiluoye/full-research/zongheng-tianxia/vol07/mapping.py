import json,pathlib
H=pathlib.Path(__file__).resolve().parent;S=json.loads((H.parent/'source.json').read_text(encoding='utf-8'));D=json.loads(pathlib.Path('writing-vault/library/reports/collection/reading-units.json').read_text(encoding='utf-8'))[S['source_id']]
print(json.dumps({'keys':list(D),'meta':{k:v for k,v in D.items() if not isinstance(v,(list,dict))}},ensure_ascii=True))
for k,v in D.items():
 if isinstance(v,list):
  selected=[u for u in v if isinstance(u,dict) and any(776<=int(x[3:])<=1060 for x in u.get('segment_ids',[]) if x.startswith('ch-'))]
  print(json.dumps({'key':k,'selected':len(selected),'multi_segments':[u for u in selected if len(u['segment_ids'])>1],'nonbody':[u for u in selected if u.get('kind')!='body']},ensure_ascii=True))
