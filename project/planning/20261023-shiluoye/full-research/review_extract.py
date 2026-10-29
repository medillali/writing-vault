"""压缩重复定位字段以便审阅全部研究文本，不替代原文阅读或证据验证。"""
import pathlib,json,sys
root=pathlib.Path(__file__).resolve().parent
book,volume,section=sys.argv[1],int(sys.argv[2]),sys.argv[3]
directory=root/book/f'vol{volume:02d}'
def compact(value):
    if isinstance(value,list):return [compact(x) for x in value]
    if isinstance(value,dict):
        if {'source_id','revision','chapter_id'}.issubset(value):
            return value['chapter_id']+f" L{value.get('start_line','?')}—{value.get('end_line','?')}"+((' '+value['claim_kind']) if value.get('claim_kind') else '')
        return {k:compact(v) for k,v in value.items() if k not in ['source_id','revision','read_chapter_ids','completed_chapter_ids','pending_chapter_ids']}
    return value
def read(name):return json.loads((directory/name).read_text(encoding='utf-8'))
if section=='dimensions':data=read('analysis.json')['dimensions']
elif section=='keys':data={k:(len(v) if isinstance(v,(list,dict)) else str(v)[:150]) for k,v in read('analysis.json').items()}
elif section=='analysis':data={k:v for k,v in read('analysis.json').items() if k not in ['dimensions']}
elif section=='cards':data=read('cards.json')
elif section=='graph':data=read('graph.json')
elif section.startswith('graph:'):data=read('graph.json')[section.split(':',1)[1]]
elif section.startswith('analysis:'):data=read('analysis.json')[section.split(':',1)[1]]
elif section.startswith('cards:'):
    cards=read('cards.json');cards=cards['cards'] if isinstance(cards,dict) else cards
    data=[c for c in cards if c['asset_type']==section.split(':',1)[1]]
else:raise ValueError(section)
if len(sys.argv)>4 and isinstance(data,list):data=data[int(sys.argv[4]):int(sys.argv[5]) if len(sys.argv)>5 else None]
sys.stdout.reconfigure(encoding='utf-8')
print(json.dumps(compact(data),ensure_ascii=False,separators=(',',':')))
