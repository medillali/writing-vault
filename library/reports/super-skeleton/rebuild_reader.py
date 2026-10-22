"""从研究主档生成PC/手机共用的离线阅读页，不写回来源或人工笔记。"""
from pathlib import Path
import hashlib,json,sys
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
VAULT=HERE.parents[2]
SRC=HERE/'reader'
OUT=HERE/'reading/plot/reader'
SID='src-9ff09c395734410b856f77c77a652834'
GRAPH=VAULT/'library/sources'/SID/'plot-graph.json'

def dataset():
    g=json.loads(GRAPH.read_text(encoding='utf-8'))
    syn=json.loads((HERE/'book-synthesis.json').read_text(encoding='utf-8'))
    nodes=sorted((n for n in g['nodes'] if n['kind']=='event'),key=lambda n:n['narrative_order'])
    ranges=[(1,3),(4,6),(7,9),(10,12),(13,15),(16,17),(18,18)]
    stages=[]
    for i,((lo,hi),stage) in enumerate(zip(ranges,syn['stages']),1):
        stages.append({'id':f'stage-{i}','number':i,'title':stage['title'].split('：',1)[1],
            'range':f'第{lo}—{hi}集' if lo!=hi else f'第{lo}集','summary':stage['summary'],
            'evidence':stage['evidence'],'node_ids':[n['id'] for n in nodes if lo<=int(n['id'][1:3])<=hi]})
    wanted={c for n in nodes for c in n.get('characters',[])}|{k['observer'] for n in nodes for k in n.get('knowledge',[]) if k['observer']!='reader'}
    chars={}
    for f in (VAULT/'library/characters').glob('*.json'):
        card=json.loads(f.read_text(encoding='utf-8'))
        if card['asset_id'] in wanted:chars[card['asset_id']]={'name':card['content'].get('name',card['title']),'title':card['title'],'id':card['asset_id']}
    data={'title':'超级骷髅兵','source_id':SID,'revision':hashlib.sha256(GRAPH.read_bytes()).hexdigest(),
          'core':'book-37dd82abc178','nodes':nodes,'edges':g['edges'],'threads':[t for t in g['threads'] if t['id'].startswith('book-')],
          'stages':stages,'characters':chars,'research_status':'研究草稿 · 待审阅'}
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return data

def build():
    data=dataset()
    layouts=json.loads((OUT/'layouts.json').read_text(encoding='utf-8'))
    assert layouts['revision']==data['revision'],'布局与源数据不一致，请先运行layout_reader.cjs'
    data['layouts']=layouts['scopes']
    template=(SRC/'template.html').read_text(encoding='utf-8')
    raw=json.dumps(data,ensure_ascii=False).replace('<','\\u003c')
    html=template.replace('/* READER_STYLE */',(SRC/'style.css').read_text(encoding='utf-8'))
    html=html.replace('/* READER_DATA */',raw)
    for name in ('model','graph','app'):html=html.replace(f'/* READER_{name.upper()} */',(SRC/f'{name}.js').read_text(encoding='utf-8'))
    assert '/* READER_' not in html
    (OUT/'cards.html').write_text(html,encoding='utf-8')
    print(json.dumps({'events':len(data['nodes']),'relations':len(data['edges']),'threads':len(data['threads']),'stages':len(data['stages']),'bytes':len(html.encode('utf-8'))}))

if __name__=='__main__':
    dataset() if '--data' in sys.argv else build()
