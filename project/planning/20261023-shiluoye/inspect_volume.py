import pathlib,json,sys
sys.stdout.reconfigure(encoding='utf-8')
root=pathlib.Path(__file__).resolve().parents[2];work=root/'.planning/20261023-shiluoye/zongheng-tianxia'
if '--vol2' in sys.argv:
    work=work.parent/'zongheng-tianxia-vol02';sys.argv.remove('--vol2')
def read(name):return json.loads((work/name).read_text(encoding='utf-8'))
analysis=read('analysis.json');cards=read('cards.json');cards=cards['cards'] if isinstance(cards,dict) else cards;g=read('graph.json')
mode=sys.argv[1] if len(sys.argv)>1 else 'dimensions'
if mode=='dimensions':
    for name,data in analysis['dimensions'].items():
        print('\nDIMENSION',name)
        if isinstance(data,list):
            print(json.dumps(data,ensure_ascii=False));continue
        for o in data.get('observations',[]):print(o['claim_kind'],o['claim'])
        print('LIMITS',data.get('evidence_limits'))
        print('CONTROLS',data.get('transfer_controls'))
elif mode=='cards':
    def compact(x):
        if isinstance(x,dict):
            if {'chapter_id','start_line','end_line'}.issubset(x):return x['chapter_id']+f" L{x['start_line']}—{x['end_line']}"
            return {k:compact(v) for k,v in x.items() if k!='phase_scope'}
        if isinstance(x,list):return [compact(v) for v in x]
        return x
    for c in cards:
        if len(sys.argv)>2 and sys.argv[2] not in c['origin_key']:continue
        print('\nCARD',c['origin_key'],c['asset_type'],c['title'])
        print(json.dumps(compact(c['content']),ensure_ascii=False))
elif mode=='graph':
    edges={e['id']:e for e in g['edges']}
    for t in g['threads']:
        for eid in t['edge_ids']:
            e=edges[eid]
            if e['from'] not in t['node_ids'] or e['to'] not in t['node_ids']:print('OUTSIDE_THREAD',t['id'],eid,e['from'],e['to'])
    for n in g['nodes']:
        if n.get('knowledge'):print(n['id'],n['title'],json.dumps(n['knowledge'],ensure_ascii=False))
elif mode=='other':
    print('keys',list(analysis))
    for k,v in analysis.items():
        if k not in ['source_id','revision','dimensions','characters','scenes','patterns','threads','read_chapter_ids']:print(k,json.dumps(v,ensure_ascii=False))
