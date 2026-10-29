from pathlib import Path
import sys,json
sys.stdout.reconfigure(encoding='utf-8')
P=Path(__file__).parent
for name in ['book-synthesis.md','ending-audit.md']:
 lines=(P/name).read_text(encoding='utf-8').splitlines()
 for n,line in enumerate(lines,1):
  if any(x in line for x in ['**萧御**','**赵岚馨**','友谊决斗','同级友战']):print(name,n,line)
for name in ['integrated_notes','final_details','write_final_text']:
 for f in (P/'__pycache__').glob(name+'.*.pyc'):f.unlink()
