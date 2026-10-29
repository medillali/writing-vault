"""展示卷七主审后核修的具体内容与全部认知条。"""
import pathlib,json,sys
sys.stdout.reconfigure(encoding='utf-8')
folder=pathlib.Path(__file__).resolve().parent/'zongheng-tianxia/vol07'
def read(name):return json.loads((folder/name).read_text(encoding='utf-8'))
def compact(v):
    if isinstance(v,list):return [compact(x) for x in v]
    if isinstance(v,dict):
        if {'source_id','revision','chapter_id'}.issubset(v):return v['chapter_id']+f" L{v.get('start_line','?')}—{v.get('end_line','?')}"
        return {k:compact(x) for k,x in v.items()}
    return v
analysis=read('analysis.json');cards=read('cards.json');graph=read('graph.json')
mode=sys.argv[1]
if mode=='text':
    data={'dimensions':[x for group in analysis['dimensions'].values() for x in group if x['id'] in ['worldbuilding1','narrative1','dialogue4']],
          'cards':[x for x in cards if x['origin_key'].rsplit('/',1)[1] in ['shusheng','longhun','audan','sagelong','s4','aryan','split']],
          'edges':[x for x in graph['edges'] if x['id'] in ['v07-e-tank','v07-e-absence']],
          'seal_thread':[x for x in graph['threads'] if x['id']=='v07-t-seal']}
elif mode=='knowledge':data=[{'node':x['id'],'knowledge':x['knowledge']} for x in graph['nodes'] if x.get('knowledge')]
else:raise ValueError(mode)
print(json.dumps(compact(data),ensure_ascii=False,separators=(',',':')))
