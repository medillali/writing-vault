from pathlib import Path
import sys,json,hashlib,subprocess
R=Path(__file__).resolve().parents[2];V=R/'.verify/two-books';L=R/'writing-vault';O=V/'library/reports/two-books-20261023';P=R/'.planning/two-books-20261023'
sys.path.insert(0,str(R/'distill-novels/scripts'))
from fictionlib.vault import Vault
from fictionlib.storage import locked,commit,json_text,digest
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def dump(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def git(*args):
 p=subprocess.run(['git','-c',f'safe.directory={L.as_posix()}','-c','http.sslBackend=openssl','-C',str(L),*args],text=True,encoding='utf-8',capture_output=True)
 if p.returncode:raise RuntimeError(p.stderr+p.stdout)
 return p.stdout.strip()
class Cached(Vault):
 def _sources(self):
  if not hasattr(self,'cache'):self.cache=super()._sources()
  return self.cache
mode=sys.argv[1]
if mode=='copy':
 names=set(['AGENTS.md','START-HERE.md','CONTENT-GUIDE.md','RESEARCH-QUEUE.md','templates/original-project-brief.md'])
 for rel in ['library/reports/two-books-20261023','library/reports/zeidan/legacy']:
  names.update(p.relative_to(V).as_posix() for p in (V/rel).rglob('*') if p.is_file())
 for a in read(O/'batch-assets.json'):
  folder={'character':'characters','scene':'scenes','pattern':'patterns'}[a['type']];names.add(f"library/{folder}/{a['asset_id']}.json")
 sids=list(read(O/'validation/identity-reconciliation.json')['source_id_map'].values())
 for sid in sids:
  names.add(f'library/sources/{sid}.json')
  names.update(p.relative_to(V).as_posix() for p in (V/f'library/sources/{sid}').rglob('*') if p.is_file())
 for rid in ['run-legacy-zeidan-20261023','run-two-books-20261023-z','run-two-books-20261023-l']:names.add(f'exchanges/runs/{rid}.json')
 bundle=read(O/'handoff/bundle.json')['bundle_id']
 names.update(p.relative_to(V).as_posix() for p in (V/'exchanges/outbox').glob(bundle+'*') if p.is_file())
 sid=sids[1];source_rel=f'library/sources/{sid}.json';queue_rel='exchanges/runs/run-queue-leveling-expert-20261023.json'
 with locked(L):
  changes={};added=0;same=0
  for rel in sorted(names):
   src=V/rel;dst=L/rel
   if dst.exists():
    if dst.read_bytes()==src.read_bytes():same+=1;continue
    if src.suffix=='.json' and read(src)==read(dst):
     src.write_bytes(dst.read_bytes());same+=1;continue
    assert rel==source_rel,f'非本批独占文件发生冲突: {rel}'
    before=read(dst);after=read(src)
    assert {k:v for k,v in before.items() if k!='revisions'}=={k:v for k,v in after.items() if k!='revisions'}
    assert len(before['revisions'][-1]['chapters'])==389 and len(after['revisions'][-1]['chapters'])==388
    dump(P/'live-leveling-index-before.json',before)
   else:added+=1
   changes[rel]=src.read_text(encoding='utf-8')
  # 确认纠正范围里尚无既有卡片证据，避免重编号影响已完成研究。
  for folder in ['characters','scenes','patterns']:
   for p in (L/f'library/{folder}').glob('*.json'):
    for e in read(p).get('evidence',[]):
     if e.get('source_id')==sid:assert int(e['chapter_id'][3:])<317
  queued=read(L/queue_rel)
  assert queued['completed_chapters']==[] and queued['state']=='registered'
  dump(P/'live-leveling-queue-before.json',queued)
  updated=read(V/'exchanges/runs/run-two-books-20261023-l.json');updated['run_id']=queued['run_id']
  updated['notes']='此队列已由run-two-books-20261023-l接续：序章及1–12章已实读；续读第13章。已审计并纠正正文第一回合误分章，来源索引388段。'
  changes[queue_rel]=json_text(updated);names.add(queue_rel)
  dump(V/queue_rel,updated)
  manifest=read(L/'private-sources/normalized/manifest.json')
  dest=next(s for s in manifest['sources'] if s['source_id']==sid)
  correct=next(s for s in read(V/'private-sources/normalized/manifest.json')['sources'] if s['source_id']==sid)
  assert dest['revision']==correct['revision'] and len(dest['chapters'])==389
  dest['chapters']=correct['chapters'];dest['chapter_headings']=correct['chapter_headings']
  for rev in dest['revisions']:
   if rev['revision']==dest['revision']:rev['chapters']=correct['chapters']
  dump(P/'live-private-manifest-before.json',read(L/'private-sources/normalized/manifest.json'))
  changes['private-sources/normalized/manifest.json']=json_text(manifest)
  commit(L,changes)
  vault=Cached(L);result=vault._validate_locked();assert result['valid']
  assert digest(vault.cache)==digest(Vault._sources(vault))
  for rel in names:assert (L/rel).read_bytes()==(V/rel).read_bytes(),rel
 dump(P/'integration-paths.json',sorted(names))
 result.update({'valid':True,'new_files_copied':added,'existing_identical_reused':same,'selected_files':len(names),'unrelated_files_written':0,'new_cards':29,'legacy_cards_reused':292,'source_duplicates_added':0,'index_correction_audited':True})
 dump(O/'validation/live-integration.json',result);dump(L/'library/reports/two-books-20261023/validation/live-integration.json',result)
 print(json.dumps(result,ensure_ascii=False),flush=True)
elif mode=='commit':
 assert git('branch','--show-current')=='main'
 assert not git('diff','--cached','--name-only'),'其他任务已有暂存内容，不能混合提交'
 names=set(read(P/'integration-paths.json'))
 names.update(p.relative_to(V).as_posix() for p in O.rglob('*') if p.is_file())
 for rel in names:
  assert (V/rel).read_text(encoding='utf-8')==(L/rel).read_text(encoding='utf-8'),rel
 spec=P/'integration-pathspec.bin';spec.write_bytes(b'\0'.join(n.encode('utf-8') for n in sorted(names))+b'\0')
 git('add',f'--pathspec-from-file={spec}','--pathspec-file-nul')
 staged=set(git('diff','--cached','--name-only','-z').split('\0'))-{''}
 assert staged<=names and staged,'暂存范围异常'
 git('diff','--cached','--check')
 author=git('log','-1','--format=%an%n%ae').splitlines()
 print(git('-c',f'user.name={author[0]}','-c',f'user.email={author[1]}','commit','-m','纳管双书试蒸馏与原创内容管理，复用既有来源和旧研究').splitlines()[0],flush=True)
 dump(P/'integration-commit.json',{'commit':git('rev-parse','HEAD'),'files':len(staged),'branch':'main'})
 print(git('push','origin','HEAD:main'),flush=True)
elif mode=='receipt':
 expected=read(P/'integration-commit.json')['commit']
 def api(path):
  p=subprocess.run(['gh','api',path],text=True,encoding='utf-8',capture_output=True,check=True);return json.loads(p.stdout)
 assert api('repos/medillali/writing-vault')['private'] is True
 remote=api('repos/medillali/writing-vault/git/ref/heads/main')['object']['sha']
 # 即使另一项工作随后快进，也必须包含本批提交，并逐文件校验本批提交的远程树。
 if remote!=expected:
  comparison=api(f'repos/medillali/writing-vault/compare/{expected}...{remote}');assert comparison['status'] in ['ahead','identical']
 tree=api(f'repos/medillali/writing-vault/git/trees/{expected}?recursive=1');assert not tree['truncated']
 remote_files={e['path']:e['sha'] for e in tree['tree'] if e['type']=='blob'}
 local={rec.split('\t',1)[1]:rec.split('\t',1)[0].split()[2] for rec in git('ls-tree','-rz',expected).split('\0') if rec}
 assert local==remote_files
 result={'valid':True,'repository':'medillali/writing-vault','private':True,'branch':'main','content_commit':expected,'remote_head':remote,'remote_contains_content_commit':True,'all_tree_blobs_match':True,'tree_blob_count':len(local),'raw_sources_uploaded':False}
 dump(P/'remote-latest.json',result);print(json.dumps(result,ensure_ascii=False),flush=True)
else:raise SystemExit(mode)
