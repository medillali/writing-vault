"""隔离目录中未发布的重复生成草稿移到规划档；不删除真实资料库或人工字段。"""
from pathlib import Path
import json,sys
P=Path(__file__).parent;R=P.parents[1];V=R/'.verify/two-books';O=V/'library/reports/two-books-full-20261025'
sys.stdout.reconfigure(encoding='utf-8')
for folder,key in [('leveling','l'),('zeidan','z')]:
 manifest=O/folder/'asset-manifest.json'
 if not manifest.exists():continue
 active={x['asset_id'] for x in json.loads(manifest.read_text(encoding='utf-8'))}
 for path in sorted((V/'library/characters').glob(f'chr-full-{key}-*.json')):
  aid=path.stem
  if aid in active:continue
  obj=json.loads(path.read_text(encoding='utf-8'));assert obj['review_status']=='draft' and not obj['user_notes'] and not obj['favorite'];assert obj['scope']=='source-analysis';assert obj['revision']==1
  candidates=[path,V/f'library/views/{aid}.md',O/folder/f'cards/{aid}.md']
  for src in candidates:
   if not src.exists():continue
   assert src.resolve().is_relative_to(V.resolve());dest=P/'superseded-unpublished-drafts'/src.relative_to(V);dest.parent.mkdir(parents=True,exist_ok=True);assert not dest.exists();src.replace(dest)
  print('归档未发布重复草稿',aid)
