from pathlib import Path
import shutil,sys,os
sys.stdout.reconfigure(encoding='utf-8')
print('dot',shutil.which('dot'))
base=Path.home()/'.cache/codex-runtimes/codex-primary-runtime/dependencies/node'
for p in ['node_modules/@viz-js/viz','node_modules/playwright','node_modules/sharp']:print(p,(base/p).exists())
for p in [Path.home()/'.cache/ms-playwright',Path.home()/'AppData/Local/ms-playwright',Path('C:/Program Files/Google/Chrome/Application/chrome.exe'),Path('C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe')]:
 print(p,p.exists());
 if p.is_dir():print([x.name for x in p.iterdir()])
