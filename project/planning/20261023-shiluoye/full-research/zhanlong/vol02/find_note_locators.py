"""只在已经实际读完的笔记中辅助定位，不替代正文阅读。"""
import pathlib,json,sys
sys.stdout.reconfigure(encoding='utf-8');P=pathlib.Path(__file__).parent
for x in map(json.loads,(P/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines()):
 if any(t in json.dumps(x,ensure_ascii=False) for t in sys.argv[1:]):print(json.dumps(x,ensure_ascii=False))
