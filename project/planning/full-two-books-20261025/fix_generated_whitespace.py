from pathlib import Path
import sys,json
sys.stdout.reconfigure(encoding='utf-8');R=Path(__file__).resolve().parents[2];P=Path(__file__).parent;V=R/'.verify/two-books';L=R/'writing-vault';O=V/'library/reports/two-books-full-20261025'
changed=[]
def save(p,data):
 old=p.read_bytes();dst=L/p.relative_to(V);assert dst.read_bytes()==old,'本批文件被外部改动'
 if old!=data:p.write_bytes(data);dst.write_bytes(data);changed.append(p.relative_to(V).as_posix())
for p in O.rglob('plot.md'):save(p,(p.read_text(encoding='utf-8').rstrip()+'\n').encode('utf-8'))
p=O/'rebuild-full.py';body=p.read_text(encoding='utf-8');assert ' for a in cards:\n' in body
body=body.replace(' for a in cards:\n'," # 既有图生成器的段尾空行统一为一个换行。\n for md in (dest/'plot').rglob('plot.md'):write(md,md.read_text(encoding='utf-8'))\n for a in cards:\n",1)
save(p,body.encode('utf-8'));print(json.dumps({'owned_generated_files_normalized':len(changed)},ensure_ascii=False))
