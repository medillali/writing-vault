"""按真实关系生成多起点、分枝、共享交汇的全书图，不用集数构造父子树。"""
from pathlib import Path
from collections import Counter
import hashlib
import json
import math
import sys
sys.dont_write_bytecode = True
import tree_style as p

HERE = Path(__file__).resolve().parent
TEAL, JUNCTION = '#147d8b', '#b86a23'
NW, HEADER, PAD = 366, 510, 90

def configure(folder):
    global OUT, CORE, ns, events, threads, ts, hidden, hno, core_nodes, core_edges, hidden_edges, edges, structural, pairs, incoming, outgoing, roots, forks, junctions, TIME_LABELS
    data=json.loads((HERE/folder/'plot/topology.json').read_text(encoding='utf-8'))
    p.G=data; p.NODES={n['id']:n for n in data['nodes']}; p.EDGES={e['id']:e for e in data['edges']}
    p.VAULT=HERE.parents[2];p.SID=data['source_id'];p.VOLUMES=data['stages'];p.TITLE=data['title'];p.CORE_TITLE=data['core_title']
    p.GRAPH_PATH=HERE/folder/'plot/graph.json';p.GAPS={t['id']:t.get('display_note',t['resolution_note']) for t in data['threads']}
    OUT=HERE/folder/'plot/whole-book';CORE='book-main';ns=p.NODES
    events=sorted(data['nodes'],key=lambda n:n['narrative_order']);threads=data['threads'];ts={t['id']:t for t in threads}
    hidden=[t for t in threads if t['kind']=='hidden'];hno={t['id']:i+1 for i,t in enumerate(hidden)}
    core_nodes=set(ts[CORE]['node_ids']);core_edges=set(ts[CORE]['edge_ids'])
    hidden_edges={eid for t in hidden for eid in t['edge_ids']};edges=data['edges']
    # 阅读衔接只组织主干，不参与语义分枝与交汇的计数。
    structural=[e for e in edges if e['kind'] not in ('echo','sequence')]
    pairs={(e['from'],e['to']) for e in structural};incoming=Counter(b for a,b in pairs);outgoing=Counter(a for a,b in pairs)
    roots=[n['id'] for n in events if not incoming[n['id']]];forks=[n['id'] for n in events if outgoing[n['id']]>1];junctions=[n['id'] for n in events if incoming[n['id']]>1]
    TIME_LABELS={}

def size(n):
    if n['id'] in hno:
        return NW, 95+p.text_height(p.title(n),NW-40,26,True)+p.text_height(p.GAPS[n['id']],NW-40,23)
    return NW, 83+p.text_height(n['title'],NW-40,29,True)


def endpoint(t):
    return max(t['node_ids'],key=lambda nid:ns[nid]['narrative_order'])


def prepare():
    OUT.mkdir(parents=True,exist_ok=True)
    nodes=[]
    for n in events+hidden:
        w,h=size(n)
        nodes.append({'name':n['id'],'attributes':{'width':w/72,'height':h/72}})
    links=[]
    for e in edges:
        forward=ns[e['from']]['narrative_order']<ns[e['to']]['narrative_order']
        links.append({'tail':e['from'],'head':e['to'],'attributes':{
            'id':e['id'],'constraint':forward and e['kind']!='echo',
            'weight':6 if e['id'] in core_edges and e['kind']!='echo' else (3 if e['kind']=='cause' else 1)}})
    for t in hidden:
        links.append({'tail':endpoint(t),'head':t['id'],'attributes':{'id':'state-'+t['id'],'weight':2}})
    # 只约束大致阅读进度，避免第18集的独立起点浮到开篇附近。
    # 不画时间链，也不以这些隐形约束生成剧情关系。
    ranks={}
    for n in events:
        prev=[ranks[e['from']]+1 for e in edges if e['kind']!='echo' and e['to']==n['id'] and e['from'] in ranks]
        ranks[n['id']]=max([(p.vol(n)-1)*2]+prev)
    for t in hidden:ranks[t['id']]=ranks[endpoint(t)]+1
    subgraphs=[]
    for level in range(max(ranks.values())+1):
        anchor=f'_rank{level}'
        nodes.append({'name':anchor,'attributes':{'shape':'point','width':0,'height':0,'style':'invis'}})
        subgraphs.append({'name':f'r{level}','graphAttributes':{'rank':'same'},
                          'nodes':[{'name':anchor}]+[{'name':nid} for nid,r in ranks.items() if r==level]})
        if level:links.append({'tail':f'_rank{level-1}','head':anchor,'attributes':{'id':f'_order{level}','style':'invis','weight':0}})
    model={'directed':True,'graphAttributes':{'rankdir':'TB','nodesep':'.8','ranksep':'1.05','splines':'spline','outputorder':'edgesfirst'},
           'nodeAttributes':{'shape':'box','fixedsize':True,'label':''},'nodes':nodes,'edges':links,'subgraphs':subgraphs}
    (OUT/'layout-input.json').write_bytes((json.dumps(model,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
    print(f'布局输入：{len(events)}个事件、{len(structural)}条语义关系、{len(hidden)}个暗线终态。')


class Map(p.SVG):
    def group(self,**attrs):
        self.parts.append('<g '+' '.join(f'{k.replace("_","-")}="{p.esc(v)}"' for k,v in attrs.items())+'>')
    def end(self):self.parts.append('</g>')
    def tooltip(self,s):self.parts.append('<title>'+p.esc(s)+'</title>')


def bounds(ids,positions):
    boxes=[positions[i] for i in ids]
    x=min(b['x'] for b in boxes);y=min(b['y'] for b in boxes)
    return {'x':x-35,'y':y-35,'width':max(b['x']+b['width'] for b in boxes)-x+70,
            'height':max(b['y']+b['height'] for b in boxes)-y+70}


def render():
    layout=json.loads((OUT/'layout.json').read_text(encoding='utf-8'))
    _,_,gw,gh=map(float,layout['bb'].split(','))
    width,height=math.ceil(gw+2*PAD),math.ceil(gh+HEADER+140)
    positions={}
    for n in layout['objects']:
        if n['name'] not in ns and n['name'] not in hno:continue
        x,y=map(float,n['pos'].split(','));w=float(n['width'])*72;h=float(n['height'])*72
        positions[n['name']]={'x':round(x-w/2+PAD,2),'y':round(gh-y-h/2+HEADER,2),
                              'width':round(w,2),'height':round(h,2),
                              'volume':p.vol(ns[n['name']]) if n['name'] in ns else None}
    assert set(positions)=={n['id'] for n in events+hidden}
    s=Map(width)
    s.rect(0,0,width,16,p.BLUE,p.BLUE,0)
    s.text(80,48,f'《{p.TITLE}》 · 剧情分枝与交汇',width-160,82,p.INK,True)
    s.text(80,162,f'从“{p.CORE_TITLE}”出发，旁支另起，在共享事件处交汇，再继续分枝。',width-160,39,p.MUTED)
    s.text(80,230,f'{len(events)}个事件 / {len(roots)}个图内起点 / {len(forks)}个分枝点 / {len(junctions)}个交汇点 / {len(hidden)}条暗线终点复核',width-160,32,p.INK)
    legend=[(p.BLUE,'蓝色 · 核心成长主线'),(TEAL,'青色 · 其他剧情枝线'),(p.PURPLE,'紫色 · 暗线关系'),(JUNCTION,'金色节点标记 · 多路交汇')]
    for i,(c,label) in enumerate(legend):
        x=80+i*850;s.path(f'M {x} 328 H {x+90}',c,7);s.text(x+112,300,label,700,28,c,True)
    s.text(80,365,'实线为因果，虚线为铺垫、揭示、转折或回收；蓝色细点线仅为主干阅读衔接，不代表因果，也不计入交汇。',width-160,27,p.MUTED)
    s.text(80,416,'整体沿阅读进度向下展开，研究阶段只是位置提示；同一事件只画一次。暗线状态框取全书终点复核，不是新增剧情。',width-160,27,p.MUTED)
    links_meta=[]
    for el in sorted((e for e in layout['edges'] if not e['id'].startswith('_order')),key=lambda el: (0 if el['id'] in p.EDGES and p.EDGES[el['id']]['kind']=='echo' else 1)):
        eid=el['id'];state=eid.startswith('state-');e=p.EDGES.get(eid)
        if state:
            t=ts[eid[6:]];color=p.STATE[t['status']][1];stroke=2.5;dash='5 9';opacity=.8
        else:
            color=p.BLUE if eid in core_edges else p.PURPLE if eid in hidden_edges else TEAL
            stroke=2.5 if e['kind']=='sequence' else 5 if eid in core_edges else 3
            dash='' if e['kind']=='cause' else '2 11' if e['kind'] in ('echo','sequence') else '11 8'
            opacity=.4 if e['kind'] in ('echo','sequence') else .85
        s.group(id=eid,data_kind='annotation' if state else 'edge',data_from=endpoint(t) if state else e['from'],
                data_to=t['id'] if state else e['to'],data_relation='state' if state else e['kind'],
                tabindex=0 if not state else -1,role='button' if not state else 'group',
                aria_label='暗线终点注记' if state else p.REL[e['kind']][0]+'：'+e['label'])
        for draw in el.get('_draw_',[]):
            if draw['op'] not in ('b','B'):continue
            points=[(round(x+PAD,2),round(gh-y+HEADER,2)) for x,y in draw['points']]
            d='M '+','.join(map(str,points[0]))+' C '+' '.join(','.join(map(str,pt)) for pt in points[1:])
            s.parts.append(f'<path d="{d}" stroke="transparent" stroke-width="18" fill="none" pointer-events="stroke"/>')
            s.path(d,color,stroke,dash,not state,opacity)
        if e:s.tooltip(p.REL[e['kind']][0]+' · '+p.CLAIM[e['claim_kind']]+'\n'+e['label']+'\n'+p.evidence(e))
        s.end()
        links_meta.append({'id':eid,'from':endpoint(t) if state else e['from'],'to':t['id'] if state else e['to'],
                           'kind':'annotation' if state else e['kind'],'core':eid in core_edges})
    for n in events:
        nid=n['id'];b=positions[nid];x,y,w,h=(b[k] for k in ('x','y','width','height'))
        memberships=[t['id'] for t in threads if nid in t['node_ids']]
        darks=[hno[t] for t in memberships if t in hno]
        color=p.BLUE if nid in core_nodes else TEAL
        s.group(id=nid,data_kind='event',data_volume=p.vol(n),data_threads=','.join(memberships),
                data_junction=str(nid in junctions).lower(),data_root=str(nid in roots).lower(),
                tabindex=0,role='button',aria_label=n['title'])
        s.rect(x,y,w,h,'#edf4ff' if nid in core_nodes else 'white',color,18)
        mark='起点' if nid in roots else ('交汇 '+str(incoming[nid])+'路' if nid in junctions else '分枝' if nid in forks else '')
        s.text(x+18,y+12,f'阶段{p.vol(n):02d} · {n["label_id"]}',w-140,18,color)
        if mark:
            fill='#fff0df' if nid in junctions else '#e9f4f4'
            s.rect(x+w-123,y+9,108,30,fill,fill,8)
            s.text(x+w-113,y+10,mark,96,18,JUNCTION if nid in junctions else color,True)
        end=s.text(x+20,y+49,n['title'],w-40,29,p.INK,True)
        suffix=TIME_LABELS.get(nid) or ('暗线 '+ ' / '.join(f'{i:02}' for i in darks) if darks else p.CLAIM[n['claim_kind']])
        assert end<=y+h-30,(nid,end,y+h)
        s.text(x+20,y+h-29,suffix,w-40,18,p.PURPLE if darks else p.MUTED)
        s.tooltip(n['summary']+'\n'+p.evidence(n));s.end()
    for t in hidden:
        b=positions[t['id']];x,y,w,h=(b[k] for k in ('x','y','width','height'))
        label,color,fill=p.STATE[t['status']]
        s.group(id=t['id'],data_kind='thread',data_thread=hno[t['id']],tabindex=0,role='button',aria_label=p.title(t))
        s.rect(x,y,w,h,fill,color,22)
        yy=s.text(x+20,y+12,f'暗线 {hno[t["id"]]:02d} · {label}',w-40,23,color,True)
        yy=s.text(x+20,yy+8,p.title(t),w-40,26,p.INK,True)
        yy=s.text(x+20,yy+10,p.GAPS[t['id']],w-40,23,color)
        s.text(x+20,y+h-29,'全书终点复核 · 点击查看问题范围',w-40,17,p.MUTED)
        assert yy<=y+h-29,(t['id'],yy,y+h)
        s.tooltip(t['question']+'\n'+p.conclusion(t));s.end()
    s.text(80,height-92,'研究草稿待审阅 · 全部事件与原始关系可回查 · 交汇依据已有推进关系，起点不推断为绝对无前因 · 原文事实与研究推断分开保存',width-160,27,p.MUTED)
    colors={p.BLUE,p.PURPLE,TEAL,p.GREEN,p.AMBER,p.RED}
    defs=''.join(f'<marker id="a{c[1:]}" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L6,3 L0,6 Z" fill="{c}"/></marker>' for c in sorted(colors))
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" aria-label="{p.esc(p.TITLE)}多起点剧情树"><title>{p.esc(p.TITLE)}：分枝与交汇</title><defs>{defs}</defs><rect width="100%" height="100%" fill="#f7f9fc"/><g font-family="Microsoft YaHei, Noto Sans CJK SC, sans-serif">'+''.join(s.parts)+'</g></svg>'
    (OUT/'tree.svg').write_bytes(svg.encode('utf-8'))
    meta={'version':2,'width':width,'height':height,'selection':'全事件分枝交汇版','title':p.TITLE,'stages':len(p.VOLUMES),'reference':{'book':'超级骷髅兵','form':'蓝色主干、青色枝线、紫色暗线、共享交汇、枝端终态；同版式离线地图'},'semantic_edges_total':sum(e['kind']!='sequence' for e in edges),'echo_relations':sum(e['kind']=='echo' for e in edges),'semantic_relations':len(structural),'reading_links':sum(e['kind']=='sequence' for e in edges),'source_id':p.SID,
          'graph_sha256':hashlib.sha256(p.GRAPH_PATH.read_bytes()).hexdigest(),
          'events':[n['id'] for n in events],'edges':[e['id'] for e in edges],'positions':positions,'links':links_meta,
          'threads':[{'id':t['id'],'number':hno[t['id']],'status':t['status'],'anchor':endpoint(t),'conclusion':p.conclusion(t)} for t in hidden],
          'roots':roots,'forks':forks,'junctions':junctions,'core':CORE,'time_labels':TIME_LABELS,
          'volume_bounds':{str(v):bounds([n['id'] for n in events if p.vol(n)==v],positions) for v in range(1,len(p.VOLUMES)+1)},
          'thread_bounds':{t['id']:bounds(t['node_ids'],positions) for t in threads},
          'layout':{'engine':layout['engine'],'version':layout['version'],'direction':'按关系自上而下分枝；无阶段父子结构','sequence':'蓝色细点线为主干阅读衔接，非因果，不计交汇',
                    'echo':'显示但不决定层级','back_references':'保留原方向，不强制为向下推进'},
          'states':dict(Counter(t['status'] for t in hidden))}
    (OUT/'manifest.json').write_bytes((json.dumps(meta,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
    observers={'reader':'读者'}
    for path in (p.VAULT/'library/characters').glob('*.json'):
        card=json.loads(path.read_text(encoding='utf-8'));observers[card['asset_id']]=card['content'].get('name',card['title'])
    data={'meta':meta,'nodes':{n['id']:n for n in events},'threads':ts,'volumes':p.VOLUMES,'edges':p.EDGES,'observers':observers}
    raw=json.dumps(data,ensure_ascii=False).replace('<','\\u003c')
    template=(HERE/'tree-viewer.html').read_text(encoding='utf-8')
    (OUT/'index.html').write_bytes(template.replace('BOOK_TITLE',p.TITLE).replace('<!-- TREE_SVG -->',svg).replace('/* TREE_DATA */',raw).encode('utf-8'))
    return meta
    print(json.dumps({k:meta[k] for k in ('width','height','states')}))

