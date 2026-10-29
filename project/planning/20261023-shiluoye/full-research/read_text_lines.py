"""按行显示本地文本；仅用于审阅，不改动来源或检查点。"""
import pathlib
import sys

sys.stdout.reconfigure(encoding="utf-8")
lines = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8").splitlines()
start = int(sys.argv[2]) if len(sys.argv) > 2 else 1
end = int(sys.argv[3]) if len(sys.argv) > 3 else len(lines)
for index in range(start - 1, min(end, len(lines))):
    print(f"{index + 1}: {lines[index]}")
