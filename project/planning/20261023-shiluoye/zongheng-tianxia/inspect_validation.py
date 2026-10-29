import pathlib,sys
sys.stdout.reconfigure(encoding='utf-8')
for name in ['graph.py','vault.py']:
 p=pathlib.Path('distill-novels/scripts/fictionlib')/name
 lines=p.read_text(encoding='utf-8').splitlines()
 print('\nFILE',name)
 for i,l in enumerate(lines):
  if (name=='graph.py' and 26<=i<123) or (name=='vault.py' and 127<=i<202): print(i+1,l)
