from pathlib import Path
import json,sys,os
R=Path(__file__).resolve().parents[2];P=Path(__file__).parent;V=R/'.verify/two-books'
sys.stdout.reconfigure(encoding='utf-8')
if sys.argv[1]=='batches':
 for folder in ['z','z-b','l-a','l-b']:
  f=sorted((P/folder).glob('batch-*.json'))[0];b=json.loads(f.read_text(encoding='utf-8'))
  print(folder,'keys',list(b),'units0',b['units'][0], 'char0',b['characters'][0],'scene0',b['scenes'][0],'thread0',b['threads'][0],'q0',b['questions'][0])
elif sys.argv[1]=='map':
 for folder in [R/'writing-vault',R/'distill-novels',R/'.planning']:
  for f in folder.rglob('*'):
   if f.is_file() and any(t in f.name for t in ['rebuild_map','rebuild_plot','layout_whole','render_whole']):print(f.relative_to(R))
 print('ENV', {k:v for k,v in os.environ.items() if k.startswith(('VIZ_MODULE','PLOT_BROWSER'))})
elif sys.argv[1]=='front':
 s=json.loads((P/'sources.json').read_text(encoding='utf-8'))
 for key,b in s.items():
  print(key,list(b),b.get('chapters',[])[:2])
  lines=Path(b['normalized_path']).read_text(encoding='utf-8').splitlines()
  for c in b['chapters']:
   if c['chapter_id']=='ch-0001':print('\n'.join(f'L{i+1}: {lines[i]}' for i in range(c['start_line']-1,c['end_line'])))
