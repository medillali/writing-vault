"""定向显示卷六已要求修订的完整内容，供主代理复核。"""
from pathlib import Path
import json,sys
B=Path(__file__).parent/'tianxia-wushuang/vol06'
def read(n):return json.loads((B/n).read_text(encoding='utf-8'))
def short(v):
    if isinstance(v,list):return [short(x) for x in v]
    if isinstance(v,dict):
        if {'source_id','revision','chapter_id'}<=v.keys():return v['chapter_id']
        return {k:short(x) for k,x in v.items() if k not in ['source_id','revision','tags','scope','review_status','user_notes','favorite']}
    return v
cards=read('cards.json');cards=cards.get('cards',[]) if isinstance(cards,dict) else cards
graph=read('graph.json');analysis=read('analysis.json')
result={'cards':[c for c in cards if any(c['origin_key'].endswith(x) for x in ['/character/sansheng','/character/wenhen','/scene/kalan-rescue','/scene/wild-city'])],
    'nodes':[n for n in graph['nodes'] if n['id'] in ['wild-city','three-souls']],
    'issue022':analysis['issue_log'][21],'corrections':read('primary-corrections.json')}
sys.stdout.reconfigure(encoding='utf-8');print(json.dumps(short(result),ensure_ascii=False,separators=(',',':')))
