from pathlib import Path
import shutil
base=Path(__file__).resolve().parents[3]
d=base/'writing-vault/library/reports/zongheng-tianxia/atlas/tree'
for name in ['tree.svg','manifest.json','layout.json','layout-input.json']:
    target=d/('semantic-only-'+name)
    if not target.exists():shutil.copyfile(d/name,target)
