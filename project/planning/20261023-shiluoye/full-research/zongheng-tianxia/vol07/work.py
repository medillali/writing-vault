import json,pathlib,sys
sys.stdout.reconfigure(encoding='utf-8')
HERE=pathlib.Path(__file__).resolve().parent
SOURCE=json.loads((HERE.parent/'source.json').read_text(encoding='utf-8'))
if sys.argv[1]=='meta':
 v=next(v for v in SOURCE['volumes'] if v['volume']==7)
 print(json.dumps({k:v[k] for k in v if k!='units'},ensure_ascii=False))
 print(json.dumps({'unit_count':len(v['units']),'first_units':v['units'][:2],'last_units':v['units'][-2:],'first_chapters':SOURCE['chapters'][775:777],'last_chapter':SOURCE['chapters'][1059]},ensure_ascii=False))
elif sys.argv[1]=='commit':
 batch=json.loads((HERE/sys.argv[2]).read_text(encoding='utf-8'));old=[]
 if (HERE/'chapter-notes.jsonl').exists():old=[json.loads(x) for x in (HERE/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if x]
 existing={x['chapter_id'] for x in old}
 for item in batch:
  c=SOURCE['chapters'][item.pop('index')-1];assert c['chapter_id'] not in existing;old.append({**c,'full_text_read':True,**item})
 (HERE/'chapter-notes.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in old),encoding='utf-8')
 ids=[x['chapter_id'] for x in old]
 st={'source_id':SOURCE['source_id'],'revision':SOURCE['revision'],'volume':7,'status':'reading','read_chapter_ids':ids,'completed_count':len(ids),'next_chapter_id':f'ch-{int(ids[-1][3:])+1:04d}','pending_truncations':[],'current_volume_state':batch[-1]['state_changes'],'boundary':'阶段隔离，只据卷七已读；卷四至六未由本子代理阅读，不推造前史；待审阅草稿。'}
 (HERE/'reader-state.json').write_text(json.dumps(st,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('已保存',len(ids),'下一',int(ids[-1][3:])+1)
