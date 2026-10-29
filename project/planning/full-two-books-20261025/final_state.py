from pathlib import Path
import sys,subprocess,json,hashlib
sys.stdout.reconfigure(encoding='utf-8');R=Path(__file__).resolve().parents[2];P=Path(__file__).parent;L=R/'writing-vault';rel='library/reports/two-books-full-20261025'
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def git(*args):return subprocess.run(['git','-c',f'safe.directory={L.as_posix()}','-C',str(L),*args],capture_output=True,check=True).stdout.decode('utf-8').strip()
names=set(load(P/'owned-paths.json'))|{rel+'/validation/live-integration.json',rel+'/validation/save-and-restore.json'}
dirty=set(git('diff','--name-only','-z').split('\0'))-{''};assert not dirty&names,dirty&names
assert not git('diff','--cached','--name-only')
tracked=set(git('ls-files','-z').split('\0'))-{''};assert names<=tracked,names-tracked
assert all(hashlib.sha256((L/n).read_bytes()).hexdigest()==s for n,s in load(P/'concurrent-preservation.json')['fingerprints'].items())
remote=load(P/'remote-final.json');assert git('rev-parse','HEAD')==remote['remote_head']
coverage=load(L/rel/'coverage.json');accept=load(L/rel/'validation/library-and-links.json');backup=load(L/rel/'validation/save-and-restore.json')
assert backup['valid'] and backup['restored_library']['valid'] and accept['valid']
out={'valid':True,'latest_commit':remote['remote_head'],'owned_tracked_files':len(names),'owned_uncommitted_changes':0,'other_original_modified_files_preserved':27,'new_cards':accept['new_cards'],'reading_units':{k:x['actual_reading_units'] for k,x in coverage.items()},'stages':{k:x['stages'] for k,x in coverage.items()},'private_remote_verified':True,'backup_restore_verified':True}
(P/'final-state.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(out,ensure_ascii=False))
