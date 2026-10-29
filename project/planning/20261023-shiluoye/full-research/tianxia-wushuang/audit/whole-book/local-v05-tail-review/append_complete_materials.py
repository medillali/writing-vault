import json,sys
from pathlib import Path
P=Path(__file__).parent;p=P/'material-read-log.json'
log=json.loads(p.read_text(encoding='utf-8'));raw=list(map(int,sys.argv[1:]));assert raw
log['complete_four_field_notes_read']=sorted(set(log['complete_four_field_notes_read'])|set(raw))
log.setdefault('supplemental_complete_notes_batches',[]).append({'chapters':raw,'method':'完整get输出后补登；不是关键词命中或全文覆盖。'})
p.write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(len(log['complete_four_field_notes_read']))
