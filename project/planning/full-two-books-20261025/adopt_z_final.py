from build_full import *
import shutil,re
batches('z');src=P/'z-final';dest=O/'zeidan'
required=['book-synthesis.md','book-synthesis.json','ending-audit.md','ending-audit.json','terminal-question-map.json','causal-relations.json']
assert all((src/n).exists() for n in required),'全书综合与终态文件尚未定稿'
report=load(src/'book-synthesis.json');assert len(report['dimensions'])==9 and all(report['dimensions'].values())
assert report.get('collective_actual_read_units',463)==463
for name in required+['characters-final.json','threads.json','identity-links.json']:
 f=src/name
 if not f.exists():continue
 if f.suffix=='.md':
  body=f.read_text(encoding='utf-8');assert not any(x in body for x in ['本稿不能作为全书已完证明','等待341–390','待末段报告补齐'])
  body=re.sub(r'(ch-\d{4}):L(\d+)[–-](\d+)',lambda m:f'[{m[1]} L{m[2]}–{m[3]}](chapter-index.md#{m[1]})',body)
  write(dest/name,body)
 else:shutil.copy2(f,dest/name)
print('贼胆最终综合、终态审计及身份边界已并入阅读成品。')
