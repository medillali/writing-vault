from pathlib import Path
import json,hashlib,sys
sys.stdout.reconfigure(encoding='utf-8')
R=Path(__file__).resolve().parents[2];P=Path(__file__).parent;L=R/'writing-vault';old=json.loads((P/'baseline-dirty.json').read_text(encoding='utf-8'))
current={n:hashlib.sha256((L/n).read_bytes()).hexdigest() for n in old};changed=[n for n in old if old[n]!=current[n]]
allowed={'library/sources/src-2a13958390274509b2af019f6b12d981/plot-graph.json','library/views/index.md'}
assert set(changed)<=allowed,changed
record={'reason':'其他任务在本轮期间继续更新其剧情图和总索引；两路径均不属于双书复制/暂存范围。本记录保存整合前指纹，原始baseline保留。','changed_since_start':changed,'fingerprints':current,'unrelated_files_written_by_this_task':0}
(P/'concurrent-preservation.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'audited_concurrent_paths':changed,'preserved_files':len(current)},ensure_ascii=False))
