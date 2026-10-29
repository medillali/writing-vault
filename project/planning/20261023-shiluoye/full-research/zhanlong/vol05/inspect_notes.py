"""派生笔记回读/定位辅助；不计新增原文阅读。"""
import pathlib,json,sys
sys.stdout.reconfigure(encoding='utf-8');P=pathlib.Path(__file__).parent
rows=[json.loads(s) for s in (P/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines()]
args=sys.argv[1:]
if args==['--titles']:
 for n in rows:print(n['chapter_id'],n['title'])
elif not args:
 print(json.dumps({'count':len(rows),'source_anomaly_rows':sum(bool(n.get('source_anomalies')) for n in rows),'unresolved_rows':sum(bool(n['unresolved']) for n in rows)},ensure_ascii=False))
else:
 ids={int(a) for a in args}
 for n in rows:
  if int(n['chapter_id'].split('-')[1]) in ids:print(json.dumps(n,ensure_ascii=False))
