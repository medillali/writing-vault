"""按小批输出主读尾段完整四栏派生笔记；不生成阅读事实。"""
import pathlib, json, sys
sys.stdout.reconfigure(encoding='utf-8')
v = pathlib.Path(__file__).resolve().parent
rows = [json.loads(x) for x in (v.parent/'primary-vol02-tail'/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if x]
for row in rows[int(sys.argv[1]):int(sys.argv[2])]:
    print(json.dumps(row, ensure_ascii=False))
