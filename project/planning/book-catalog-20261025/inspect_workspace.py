from pathlib import Path
import sys,json,subprocess,collections
sys.stdout.reconfigure(encoding='utf-8');R=Path(__file__).resolve().parents[2];V=R/'writing-vault';P=Path(__file__).parent
def git(*args):return subprocess.run(['git','-c',f'safe.directory={V.as_posix()}','-C',str(V),*args],capture_output=True,check=True).stdout.decode('utf-8')
tracked=set(git('ls-files','-z').split('\0'))-{''};cfg=json.loads((V/'library/reports/collection/catalog-config.json').read_text(encoding='utf-8'))
print('HEAD',git('rev-parse','HEAD').strip());print('collection config tracked', 'library/reports/collection/catalog-config.json' in tracked)
for sid,b in cfg['books'].items():
 d=V/'library/sources'/sid;files=list(d.glob('*.json'));meta=[]
 for f in files:
  if f.name=='plot-graph.json':continue
  x=json.loads(f.read_text(encoding='utf-8'));meta.append({'file':f.name,'keys':list(x)[:18],'title':x.get('title'),'kind':x.get('kind'),'genre':x.get('genre'),'author':x.get('author')})
 runs=[]
 for f in (V/'exchanges/runs').glob('*.json'):
  x=json.loads(f.read_text(encoding='utf-8'))
  if x.get('source_id')==sid:runs.append({'run_id':x.get('run_id'),'state':x.get('state'),'completed':len(x.get('completed_chapters',[])),'tracked':f.relative_to(V).as_posix() in tracked})
 report=(V/'library/reports/collection'/b.get('report','missing')).resolve();print(json.dumps({'source_id':sid,'title':b['title'],'author':b['author'],'task_state':b['task_state'],'metadata':meta,'runs':runs,'report_exists':report.exists(),'report_tracked':report.relative_to(V).as_posix() in tracked if report.is_relative_to(V) else False},ensure_ascii=False))
for k in ['zeidan','leveling']:
 d=V/'library/reports/two-books-full-20261025'/k;g=json.loads((d/'plot/graph.json').read_text(encoding='utf-8'));print('MAP',k,{'coverage':g['coverage'],'nodes':len(g['nodes']),'relations':len(g['edges']),'png_bytes':(d/'plot/whole-book/tree.png').stat().st_size,'html_bytes':(d/'plot/map/index.html').stat().st_size})
print('rootfiles',sorted(p.name for p in V.iterdir() if p.is_file()));print('other_ag~',list(V.rglob('AGENTS.md'))[:10])
