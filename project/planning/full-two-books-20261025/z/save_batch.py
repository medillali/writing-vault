from pathlib import Path
import json,sys
P=Path(__file__).parent
books=json.loads((P.parent/'sources.json').read_text(encoding='utf-8'))
data=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
for u in data['units']:
    m=books['z']['units'][u['ordinal']-1]
    u['unit_id']=m['unit_id'];u['title']=m['title']
data['source_key']='z';data['source_id']=books['z']['source_id'];data['source_revision']=books['z']['revision']
Path(sys.argv[1]).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
