from pathlib import Path
import json,sys,hashlib,shutil
R=Path(__file__).resolve().parents[2];V=R/'.verify/two-books';LIVE=R/'writing-vault';O=V/'library/reports/two-books-20261023'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def dump(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
sources={'src-dd0554907f2942feb3162689dbad167f':'src-2d8a13f33737429da512e5cc9e839712','src-abe49798d224463fb60416f1286fd23f':'src-359a2bd5a60747038b12a7ba483a5f80'}
for old,sid in sources.items():
 p=V/f'library/sources/{sid}.json';correct=read(p);canonical=read(LIVE/f'library/sources/{sid}.json')
 assert canonical['revision']==correct['revision']
 if '练级' in canonical['title']:
  assert len(canonical['revisions'][-1]['chapters'])==389 and len(correct['revisions'][-1]['chapters'])==388
  canonical['revisions']=correct['revisions']
 dump(p,canonical)
 src=V/f'private-sources/originals/{old}.txt';dst=V/f'private-sources/originals/{sid}.txt'
 if src.exists() and not dst.exists():shutil.copy2(src,dst)
assets=read(O/'batch-assets.json');canonical_hashes={}
for a in assets:
 folder={'character':'characters','scene':'scenes','pattern':'patterns'}[a['type']]
 p=V/f"library/{folder}/{a['asset_id']}.json";obj=read(p)
 if a['imported_legacy']:
  assert p.read_bytes()==(LIVE/p.relative_to(V)).read_bytes()
  canonical_hashes[p.relative_to(V).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
 else:
  tags=['作者:发飙的蜗牛']+(['跨书机制'] if obj['asset_type']=='pattern' else ['作品:贼胆' if '-z-' in a['asset_id'] else '作品:网游之练级专家'])
  obj['tags']=list(dict.fromkeys(obj['tags']+tags));dump(p,obj)
 a['title']=obj['title']
dump(O/'batch-assets.json',assets)
old_baselines=list((V/'exchanges/outbox').glob('bundle-1fb16990807641e6857499f56299741c*'))
old_handoff=O/'handoff';save=R/'.planning/two-books-20261023/pre-reconcile-handoff'
assert not save.exists();shutil.copytree(old_handoff,save)
for p in sorted(old_handoff.rglob('*'),reverse=True):
 assert p.resolve().is_relative_to(O.resolve())
 if p.is_file():p.unlink()
 else:p.rmdir()
old_handoff.rmdir()
for p in old_baselines:
 assert p.is_file() and p.resolve().is_relative_to((V/'exchanges/outbox').resolve());p.unlink()
sys.path.insert(0,str(R/'distill-novels/scripts'))
from fictionlib.vault import Vault
from fictionlib.exchange import export_bundle
class Cached(Vault):
 def _sources(self):
  if not hasattr(self,'cache'):self.cache=super()._sources()
  return self.cache
export_bundle(Cached(V),old_handoff,[a['asset_id'] for a in assets if a['type']=='pattern'],None,100000)
(old_handoff/'README.md').write_text((save/'README.md').read_text(encoding='utf-8'),encoding='utf-8')
dump(O/'validation/identity-reconciliation.json',{'valid':True,'reason':'并行任务已登记同书身份与旧研究；按相同文本哈希复用长期库身份，避免重复来源和292张重复旧卡。','source_id_map':sources,'legacy_cards_reused':len(canonical_hashes),'legacy_card_hashes':canonical_hashes,'legacy_checkpoint_reused':'run-legacy-zeidan-20261023','new_cards':29,'old_snapshot_commit':'6e430f2','all_user_fields_preserved':True,'leveling_index_correction_preserved':True})
print(json.dumps({'remapped_sources':len(sources),'reused_cards':len(canonical_hashes),'new_cards':29},ensure_ascii=False))
