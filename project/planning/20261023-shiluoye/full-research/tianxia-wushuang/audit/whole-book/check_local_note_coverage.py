"""区分analysis中已收逐章索引与notes未暴露在analysis的原未决，不改候选池。"""
import pathlib,json,sys,collections
sys.stdout.reconfigure(encoding='utf-8');H=pathlib.Path(__file__).resolve().parent;B=H.parents[1]
pool=json.loads((H/'local-question-pool.json').read_text(encoding='utf-8'))
out=[]
for v in range(1,9):
 notes=[json.loads(l) for l in (B/f'vol{v:02d}/chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if l.strip()]
 indexed={x['original_record'].get('chapter_id') for x in pool['candidates'] if x['volume']==v and x['original_field'] in ['chapter_unresolved_index','local_historical_questions'] and isinstance(x['original_record'],dict)}
 missing=[n for n in notes if n.get('unresolved') and n['chapter_id'] not in indexed]
 out.append(dict(volume=v,notes_with_unresolved=sum(bool(n.get('unresolved')) for n in notes),chapters_represented_by_explicit_analysis_local_index=len(indexed),notes_not_represented_by_explicit_local_index=len(missing),unresolved_strings_missing=sum(len(n['unresolved']) if isinstance(n['unresolved'],list) else 1 for n in missing),first_missing=[n['chapter_id'] for n in missing[:3]]))
(H/'local-note-coverage-check.json').write_text(json.dumps(dict(note='只核机械候选范围，不取正文、不改变已冻结ID。source_anomaly引用某章不等保全该章全部unresolved。',volumes=out),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out,ensure_ascii=False))
