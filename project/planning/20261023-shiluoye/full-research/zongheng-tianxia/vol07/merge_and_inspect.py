import json,pathlib,sys
sys.stdout.reconfigure(encoding='utf-8')
p=pathlib.Path(__file__).parent
load=lambda f:[json.loads(x) for x in f.read_text(encoding='utf-8').splitlines() if x]
if sys.argv[1]=='merge':
 a=load(p/'chapter-notes.jsonl');b=load(p.parent/'vol07-primary-tail'/'chapter-notes.jsonl')
 assert len(a)==175 and len(b)==110
 assert [r['chapter_id'] for r in a]==[f'ch-{i:04d}' for i in range(776,951)]
 assert [r['chapter_id'] for r in b]==[f'ch-{i:04d}' for i in range(951,1061)]
 assert all(r['full_text_read'] for r in a+b)
 (p/'personal-reader-state.json').write_text((p/'reader-state.json').read_text(encoding='utf-8'),encoding='utf-8')
 for r in a:r['reader']='zongheng_vol03_full'
 out=a+b
 (p/'chapter-notes.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in out),encoding='utf-8')
 source=json.loads((p.parent/'source.json').read_text(encoding='utf-8'))
 st={'source_id':source['source_id'],'revision':source['revision'],'volume':7,'status':'researching','read_chapter_ids':[r['chapter_id'] for r in out],'completed_count':285,'complete_volume_read':True,'next_chapter_id':None,'pending_truncations':[],'reader_assignments':[{'reader':'zongheng_vol03_full','first':'ch-0776','last':'ch-0950','count':175},{'reader':'primary','first':'ch-0951','last':'ch-1060','count':110,'notes_from':'../vol07-primary-tail/chapter-notes.jsonl'}],'current_volume_state':b[-1]['state_changes'],'boundary':'全285由两实际读者分段全文读取，本子代理只亲读175；研究草稿待文学审查，不等全书完成。'}
 (p/'reader-state.json').write_text(json.dumps(st,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print('合并285，175+110，顺序/无缺口/无重复/完整标记通过')
elif sys.argv[1]=='notes':
 a,b=map(int,sys.argv[2:4])
 for r in load(p/'chapter-notes.jsonl'):
  if a<=int(r['chapter_id'][3:])<=b: print(json.dumps(r,ensure_ascii=False))
elif sys.argv[1]=='schema':
 for name in ['analysis.json','graph.json','read-log.json']:
  d=json.loads((p.parent/'vol03'/name).read_text(encoding='utf-8')); print(name,list(d));
  if name=='graph.json':print(json.dumps({k:v[:2] for k,v in d.items() if isinstance(v,list)},ensure_ascii=False))
  if name=='analysis.json':print(json.dumps({k:(list(v) if isinstance(v,dict) else type(v).__name__) for k,v in d.items()},ensure_ascii=False));print(json.dumps(d['dimensions']['style'],ensure_ascii=False))
