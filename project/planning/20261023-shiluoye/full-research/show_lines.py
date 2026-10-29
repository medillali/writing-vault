"""显示文件的限定行段。"""
import pathlib,sys
sys.stdout.reconfigure(encoding='utf-8')
lines=pathlib.Path(sys.argv[1]).read_text(encoding='utf-8').splitlines()
start=int(sys.argv[2]);end=int(sys.argv[3])
print('\n'.join(f'{i+1}: {s}' for i,s in enumerate(lines) if start<=i+1<=end))
