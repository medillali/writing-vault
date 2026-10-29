"""将较长索引片段拆为有限原行阅读；不自动记录整片已读。"""
import json
import pathlib
import sys

sys.stdout.reconfigure(encoding="utf-8")
base = pathlib.Path(__file__).resolve().parent
book, cid, start, end = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
source = json.loads((base / book / "source.json").read_text(encoding="utf-8"))
chapter = next(c for c in source["chapters"] if c["chapter_id"] == cid)
assert chapter["start_line"] <= start <= end <= chapter["end_line"]
assert end - start < 150
lines = pathlib.Path(source["normalized_path"]).read_text(encoding="utf-8").splitlines()
print(f"BEGIN PART {book} {cid} L{start}—{end}; 整片L{chapter['start_line']}—{chapter['end_line']}")
for n in range(start, end + 1):
    print(f"L{n}: {lines[n - 1]}")
print(f"END PART {cid} L{end}")
