"""完整输出人物语义，折叠重复文件指纹和逐证据来源身份。"""
from pathlib import Path
import hashlib,json,sys
B=Path(__file__).resolve().parent;R=B.parents[2];A=B/'zhanlong/audit/whole-book'
p=A/sys.argv[1];d=json.loads(p.read_text(encoding='utf-8'));s=json.loads((B/'zhanlong/source.json').read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for name,h in d.get('formal_input_sha256',{}).items():assert name.startswith('writing-vault/') and sha(R/name)==h,name
cs={c['chapter_id']:c for c in s['chapters']};a=int(sys.argv[2]) if len(sys.argv)>2 else 0;z=int(sys.argv[3]) if len(sys.argv)>3 else len(d['characters'])
print('BEGIN_CHARACTERS',p.name,sha(p),a,z,len(d['characters']))
for r in d['characters'][a:z]:
    out={k:v for k,v in r.items() if k not in {'evidence','stage_card_mapping'}}
    refs=[]
    for e in r['evidence']:
        c=cs[e['chapter_id']];assert e['source_id']==s['source_id'] and e['revision']==s['revision'] and c['start_line']<=e['start_line']<=e['end_line']<=c['end_line']
        refs.append(f"{e['chapter_id']} L{e['start_line']}—{e['end_line']} {e['claim_kind']}")
    out['evidence']=refs
    if 'stage_card_mapping' in r:out['stage_card_mapping']=[{k:v for k,v in m.items() if k in {'volume','index','title','asset_id'}} for m in r['stage_card_mapping']]
    print(json.dumps(out,ensure_ascii=False,separators=(',',':')))
print('END_CHARACTERS',p.name,a,z)
