import json
from pathlib import Path
P=Path(__file__).parent
S=json.loads((P.parent/'source.json').read_text(encoding='utf-8'));SID,REV=S['source_id'],S['revision']
N=[json.loads(x) for x in (P/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()];CH={int(x['chapter_id'][3:]):x for x in N}
def R(n):return json.loads((P/n).read_text(encoding='utf-8'))
def W(n,v):(P/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def origin(kind,key):return SID+'/full-20261025/vol08/'+kind+'/'+key
def ev(ids,kind='fact'):
 return [dict(source_id=SID,revision=REV,chapter_id=CH[i]['chapter_id'],start_line=CH[i]['start_line'],end_line=CH[i]['end_line'],claim_kind=kind,source_reader=CH[i]['reader']) for i in dict.fromkeys(ids)]
