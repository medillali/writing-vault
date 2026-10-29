"""只核已完整读卡片的重复投影，避免把相同字段冒称新一轮原文阅读。"""
from check_volume import WORK,read
import sys,json
sys.stdout.reconfigure(encoding='utf-8')
v=int(sys.argv[1]);p=WORK/'zhanlong'/f'vol{v:02d}'
a=read(p/'analysis.json');c=read(p/'cards.json');g=read(p/'graph.json')
by={r['origin_key']:r for r in c}
field='stage_characters' if v==4 else 'major_character_states'
for r in a[field]:
 card=by[r['origin_key']];body=card['content']
 assert r['name']==card['title'] and r['stage_change']==body['stage_change'] and r['evidence']==card['evidence']
 if v==5:assert r['summary']==body['summary'] and r['relationships']==body['relationship_direction']
assert a['threads' if v==4 else 'plot_and_hidden_threads']==g['threads']
print(json.dumps({'volume':v,'character_projection_exact':len(a[field]),'thread_projection_exact':len(g['threads']),'scope':'重复投影逐值相等；语义审阅来自原卡/图的实际完整逐项阅读，不新增原文覆盖。'},ensure_ascii=False))
