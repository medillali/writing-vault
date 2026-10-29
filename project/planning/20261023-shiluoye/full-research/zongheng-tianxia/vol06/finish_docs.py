from pathlib import Path
b=Path(__file__).resolve().parent
prefix='C:/Users/Administrator/Documents/ChatGPT/Novel/.planning/20261023-shiluoye/full-research/zongheng-tianxia/vol06/'
for name in ['report.md','handoff.md']:
 p=b/name
 p.write_text(p.read_text(encoding='utf-8').replace(prefix,''),encoding='utf-8')
assert all((b/n).exists() for n in ['read-log.json','chapter-notes.jsonl','reader-state.json','analysis.json','cards.json','graph.json','report.md','handoff.md'])
