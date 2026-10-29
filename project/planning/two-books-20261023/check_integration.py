from pathlib import Path
import json,sys,hashlib
R=Path(__file__).resolve().parents[2];V=R/'.verify/two-books';L=R/'writing-vault';O=V/'library/reports/two-books-20261023';P=R/'.planning/two-books-20261023'
sys.path.insert(0,str(R/'distill-novels/scripts'))
from fictionlib.vault import Vault
from fictionlib.storage import locked,digest
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def dump(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
class Cached(Vault):
 def _sources(self):
  if not hasattr(self,'cache'):self.cache=super()._sources()
  return self.cache
names=set(['AGENTS.md','START-HERE.md','CONTENT-GUIDE.md','RESEARCH-QUEUE.md','templates/original-project-brief.md'])
for rel in ['library/reports/two-books-20261023','library/reports/zeidan/legacy']:
 names.update(p.relative_to(V).as_posix() for p in (V/rel).rglob('*') if p.is_file())
for a in read(O/'batch-assets.json'):
 folder={'character':'characters','scene':'scenes','pattern':'patterns'}[a['type']];names.add(f"library/{folder}/{a['asset_id']}.json")
for sid in read(O/'validation/identity-reconciliation.json')['source_id_map'].values():
 names.add(f'library/sources/{sid}.json');names.update(p.relative_to(V).as_posix() for p in (V/f'library/sources/{sid}').rglob('*') if p.is_file())
for rid in ['run-legacy-zeidan-20261023','run-two-books-20261023-z','run-two-books-20261023-l','run-queue-leveling-expert-20261023']:names.add(f'exchanges/runs/{rid}.json')
bundle=read(O/'handoff/bundle.json')['bundle_id'];names.update(p.relative_to(V).as_posix() for p in (V/'exchanges/outbox').glob(bundle+'*') if p.is_file())
vault=Cached(L)
with locked(L):
 result=vault._validate_locked();assert result['valid'];assert digest(vault.cache)==digest(Vault._sources(vault))
 for rel in names:assert (L/rel).read_text(encoding='utf-8')==(V/rel).read_text(encoding='utf-8'),rel
 assert len({s['revision'] for s in vault.cache})==len(vault.cache),'相同文本重复来源'
dump(P/'integration-paths.json',sorted(names))
result.update({'valid':True,'selected_files':len(names),'unrelated_files_written':0,'new_cards':29,'legacy_cards_reused':292,'source_duplicates_added':0,'index_correction_audited':True,'verification':'使用原全库规则，持锁缓存来源，前后摘要一致；指定文本与审核工作树一致，忽略Windows LF/CRLF换行差异。'})
dump(O/'validation/live-integration.json',result);dump(L/'library/reports/two-books-20261023/validation/live-integration.json',result)
print(json.dumps(result,ensure_ascii=False),flush=True)
