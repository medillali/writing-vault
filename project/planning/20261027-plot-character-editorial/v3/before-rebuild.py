"""《纵横天下》全书分枝交汇图；正式JSON只读，Graphviz布局与中文绘制分开。"""
from pathlib import Path
from collections import Counter
from functools import lru_cache
import hashlib
import html
import json
import math
import re
import sys
from bisect import bisect_right

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
VAULT = HERE.parents[4]
SID = 'src-2a13958390274509b2af019f6b12d981'
GRAPH_PATH = VAULT/'library/sources'/SID/'plot-graph.json'
G = json.loads(GRAPH_PATH.read_text(encoding='utf-8'))
NS = {n['id']: n for n in G['nodes']}
ES = {e['id']: e for e in G['edges']}
EVENTS = [n for n in G['nodes'] if n['kind'] in ('event', 'scene')]
GROUPS = [n for n in G['nodes'] if n['kind'] not in ('event', 'scene')]
THREADS = G['threads']
TS = {t['id']: t for t in THREADS}
WHOLE = [t for t in THREADS if t['id'].startswith('editorial-')]
WNO = {t['id']: i+1 for i,t in enumerate(WHOLE)}
CORE = 'editorial-livelihood-duty'
GUIDE_CANDIDATES='v1-poor,v1-team,v1-v1c12,v1-v1c39,v2-move,v2-zero,v2-return,v3-v03-token,v3-v03-reject_bet,v4-v04-exile,v4-v04-firstcity,v4-v04-hushou,v5-v05-scene-korea,v6-v06-scene-dragon-gate,v6-v06-scene-china-final,v6-v06-scene-defend-capital,v6-v06-scene-refuse-duke,v7-v07-relevel,v7-v07-qingfeng,v7-v07-split,v7-v07-destroy,v7-v07-industry,v7-v07-aryan,v7-v07-dal,v8-v08-father,v8-v08-bloodroar,v8-v08-sacrifice,v8-v08-wsl,v8-v08-cleanse,v8-v08-endbattle,v8-v08-after'.split(',')
INK, MUTED, BLUE, PURPLE, TEAL, GOLD = '#172b46', '#51637a', '#2563a6', '#7850b5', '#147d8b', '#b86a23'
GREEN, AMBER, RED = '#087f65', '#a5650b', '#bf3b42'
STATE = {'resolved': ('已回收', GREEN, '#e6f5ef'), 'partial': ('部分回收', AMBER, '#fff3dc'), 'open': ('未回收', RED, '#fcecef'), 'unknown': ('待核实', PURPLE, '#f2edfa')}
REL = {'cause':'因果', 'setup':'铺垫', 'reveal':'揭示', 'reversal':'转折', 'payoff':'回收', 'echo':'主题呼应'}
CLAIM = {'fact':'原文事实', 'inference':'研究推断', 'synthesis':'研究综合', 'plan':'计划'}
NW, PAD, HEADER = 390, 90, 480


def vol(n):
    nid = n['id']
    while not re.match(r'^v[1-8]-', nid):
        parent = NS[nid].get('parent_id')
        if not parent:
            return 7 if n['id']=='editorial-mentor-missing' else 0
        nid = parent
    return int(nid[1])


def order(n):
    return (vol(n), n.get('narrative_order', 0), n['id'])


EVENTS.sort(key=order)
ORDER = {n['id']: i for i,n in enumerate(EVENTS)}
assert all(nid in ORDER for nid in GUIDE_CANDIDATES)
GUIDE_IDS=sorted(GUIDE_CANDIDATES,key=lambda nid:ORDER[nid])
GUIDE_NO={nid:i+1 for i,nid in enumerate(GUIDE_IDS)}
GUIDE_EDGES=[{'id':f'reading-order-{i+1:02}','from':a,'to':b,'kind':'reading-order','label':'主干阅读衔接；不表示因果，不计语义分枝／交汇','claim_kind':'synthesis','evidence':NS[a].get('evidence',[])+NS[b].get('evidence',[])} for i,(a,b) in enumerate(zip(GUIDE_IDS,GUIDE_IDS[1:]))]
GE={e['id']:e for e in GUIDE_EDGES}
CORE_NODES = {nid for t in THREADS if t['kind']=='main' for nid in t['node_ids']}
CORE_NODES.update(GUIDE_IDS)
CORE_EDGES = {eid for t in THREADS if t['kind']=='main' for eid in t['edge_ids']}
HIDDEN_NODES = {nid for t in THREADS if t['kind']=='hidden' for nid in t['node_ids']}
HIDDEN_EDGES = {eid for t in THREADS if t['kind']=='hidden' for eid in t['edge_ids']}
PAIRS = {(e['from'],e['to']) for e in G['edges'] if e['kind']!='echo'}
INCOMING, OUTGOING = Counter(b for a,b in PAIRS), Counter(a for a,b in PAIRS)
ROOTS = [n['id'] for n in EVENTS if not INCOMING[n['id']]]
FORKS = [n['id'] for n in EVENTS if OUTGOING[n['id']]>1]
JUNCTIONS = [n['id'] for n in EVENTS if INCOMING[n['id']]>1]


def esc(s):
    return html.escape(str(s), quote=True)


@lru_cache(maxsize=32)
def font(size, bold=False):
    from PIL import ImageFont
    for path in [Path('C:/Windows/Fonts')/('msyhbd.ttc' if bold else 'msyh.ttc'), Path('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')]:
        if path.exists():
            return ImageFont.truetype(str(path),size)
    raise RuntimeError('需要本机微软雅黑或Noto CJK字体。')


def wrap(s, width, size=26, bold=False):
    lines=[]
    for paragraph in str(s).split('\n'):
        line=''
        for char in re.findall(r'[A-Za-z0-9][A-Za-z0-9_.:–/\-]*|.',paragraph):
            if line and font(size,bold).getlength(line+char)>width-8:
                lines.append(line);line=char
            else:
                line+=char
        lines.append(line)
    return lines


def th(s,w,size=26,bold=False):
    return len(wrap(s,w,size,bold))*math.ceil(size*1.48)


def evidence(n):
    return '；'.join(f"{e['chapter_id']} L{e['start_line']}—{e['end_line']}" for e in n.get('evidence',[]))


def endpoint(t):
    return max(t['node_ids'],key=lambda nid:ORDER[nid])


def size(n):
    if n['id'] in WNO:
        return NW,112+th(n['title'],NW-40,25,True)+th(n.get('resolution_note',''),NW-40,21)
    return NW,95+th(n['title'],NW-40,27,True)


def prepare():
    assert len({n['id'] for n in EVENTS})==len(EVENTS)
    assert all(e[k] in ORDER for e in G['edges'] for k in ('from','to'))
    nodes=[{'name':n['id'],'attributes':{'width':size(n)[0]/72,'height':size(n)[1]/72}} for n in EVENTS+WHOLE]
    links=[]
    for e in G['edges']:
        forward=ORDER[e['from']]<ORDER[e['to']]
        links.append({'tail':e['from'],'head':e['to'],'attributes':{'id':e['id'],'constraint':forward and e['kind']!='echo','weight':8 if e['id'] in CORE_EDGES and e['kind']!='echo' else 3 if e['kind']=='cause' else 1}})
    for e in GUIDE_EDGES:
        links.append({'tail':e['from'],'head':e['to'],'attributes':{'id':e['id'],'constraint':True,'weight':12}})
    for t in WHOLE:
        links.append({'tail':endpoint(t),'head':t['id'],'attributes':{'id':'state-'+t['id'],'weight':2}})
    # 与超级骷髅兵相同，隐形进度约束只调整阅读位置，不新增剧情边或交汇。
    # 以全书事件序号每6个一档，避免没有已存关系的后期事件浮到开篇。
    ranks={}
    for i,n in enumerate(EVENTS):
        prior=[ranks[a]+1 for a,b in PAIRS|{(e['from'],e['to']) for e in GUIDE_EDGES} if b==n['id'] and a in ranks]
        ranks[n['id']]=max([i//6]+prior)
    for t in WHOLE:
        ranks[t['id']]=ranks[endpoint(t)]+1
    subgraphs=[]
    for level in range(max(ranks.values())+1):
        anchor=f'_rank{level}'
        nodes.append({'name':anchor,'attributes':{'shape':'point','width':0,'height':0,'style':'invis'}})
        subgraphs.append({'name':f'r{level}','graphAttributes':{'rank':'same'},'nodes':[{'name':anchor}]+[{'name':nid} for nid,r in ranks.items() if r==level]})
        if level:
            links.append({'tail':f'_rank{level-1}','head':anchor,'attributes':{'id':f'_order{level}','style':'invis','weight':0}})
    model={'directed':True,'graphAttributes':{'rankdir':'TB','nodesep':'.65','ranksep':'.95','splines':'spline','outputorder':'edgesfirst'},'nodeAttributes':{'shape':'box','fixedsize':True,'label':''},'nodes':nodes,'edges':links,'subgraphs':subgraphs}
    (HERE/'layout-input.json').write_text(json.dumps(model,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'events':len(EVENTS),'semantic_relations':len(G['edges']),'display_reading_order_links':len(GUIDE_EDGES),'terminal_notes':len(WHOLE),'removed_groups':len(GROUPS),'ranks':max(ranks.values())+1}))


class SVG:
    def __init__(self):self.parts=[]
    def group(self,**attrs):self.parts.append('<g '+' '.join(f'{k.replace("_","-")}="{esc(v)}"' for k,v in attrs.items())+'>')
    def end(self):self.parts.append('</g>')
    def tooltip(self,s):self.parts.append('<title>'+esc(s)+'</title>')
    def rect(self,x,y,w,h,fill='white',stroke='#d9e2ed',radius=14):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
    def path(self,d,color=BLUE,width=3,dash='',arrow=False,opacity=1):
        marker=f' marker-end="url(#a{color[1:]})"' if arrow else ''
        self.parts.append(f'<path d="{d}" stroke="{color}" stroke-width="{width}" fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="{dash}" opacity="{opacity}"{marker}/>')
    def text(self,x,y,text,width,size=26,color=INK,bold=False):
        yy=y
        for line in wrap(text,width,size,bold):
            self.parts.append(f'<text x="{x}" y="{yy+size}" font-size="{size}" font-weight="{700 if bold else 400}" fill="{color}" data-left="{x}" data-right="{x+width}" data-bottom="{yy+math.ceil(size*1.48)}">{esc(line)}</text>')
            yy+=math.ceil(size*1.48)
        return yy


def bounds(ids,positions,pad=35):
    boxes=[positions[i] for i in ids]
    x=min(b['x'] for b in boxes);y=min(b['y'] for b in boxes)
    return {'x':x-pad,'y':y-pad,'width':max(b['x']+b['width'] for b in boxes)-x+2*pad,'height':max(b['y']+b['height'] for b in boxes)-y+2*pad}


def compact_geometry(layout,gh):
    """逐层单调压缩空白；节点宽度与上下关系不变，所有边使用同一连续变换。

    稀疏独立起点使dot原坐标横跨2.7万像素。每个层带内压缩节点间空白，
    两层之间连续插值，保留Graphviz的左右次序、拓扑路径及卡片避让。
    """
    rows={};boxes={}
    for n in layout['objects']:
        if n['name'] not in ORDER and n['name'] not in WNO:continue
        x,y=map(float,n['pos'].split(','));w=float(n['width'])*72;h=float(n['height'])*72;cy=gh-y
        box={'x':x-w/2,'y':cy-h/2,'width':w,'height':h,'cy':cy}
        boxes[n['name']]=box;rows.setdefault(cy,[]).append(box)
    full=max(sum(b['width'] for b in row)+90*(len(row)-1) for row in rows.values())
    bands=[]
    for cy,row in sorted(rows.items()):
        row.sort(key=lambda b:b['x']);span=sum(b['width'] for b in row)+90*(len(row)-1);xx=(full-span)/2;src=[];dst=[]
        for b in row:
            src.extend([b['x'],b['x']+b['width']]);dst.extend([xx,xx+b['width']]);xx+=b['width']+90
        bands.append({'top':min(b['y'] for b in row),'bottom':max(b['y']+b['height'] for b in row),'source_x':src,'target_x':dst})
    assert all(a['bottom']<b['top'] for a,b in zip(bands,bands[1:]))
    def row_x(band,x):
        a,b=band['source_x'],band['target_x'];i=bisect_right(a,x)-1
        if i<0:return b[0]+(x-a[0])*.12
        if i>=len(a)-1:return b[-1]+(x-a[-1])*.12
        return b[i]+(x-a[i])*(b[i+1]-b[i])/(a[i+1]-a[i])
    def fx(x,y):
        for i,band in enumerate(bands):
            if y<=band['bottom']:
                if y>=band['top'] or i==0:return row_x(band,x)
                prev=bands[i-1];f=(y-prev['bottom'])/(band['top']-prev['bottom'])
                return (1-f)*row_x(prev,x)+f*row_x(band,x)
        return row_x(bands[-1],x)
    draws={}
    for e in layout['edges']:
        if e['id'].startswith('_order'):continue
        paths=[]
        for draw in e.get('_draw_',[]):
            if draw['op'] not in ('b','B'):continue
            pts=[(x,gh-y) for x,y in draw['points']];sample=[]
            for j in range(0,len(pts)-1,3):
                a,b,c,d=pts[j:j+4]
                def mapped(t):
                    u=1-t;x=u**3*a[0]+3*u*u*t*b[0]+3*u*t*t*c[0]+t**3*d[0];y=u**3*a[1]+3*u*u*t*b[1]+3*u*t*t*c[1]+t**3*d[1]
                    return fx(x,y),y
                def refine(t0,p0,t1,p1,depth=0):
                    tm=(t0+t1)/2;pm=mapped(tm);q1=mapped((t0+tm)/2);q3=mapped((tm+t1)/2)
                    dx,dy=p1[0]-p0[0],p1[1]-p0[1];length=max(math.hypot(dx,dy),.001)
                    error=max(abs(dx*(q[1]-p0[1])-dy*(q[0]-p0[0]))/length for q in [q1,pm,q3])
                    if depth<19 and (error>.08 or abs(dy)>5 or abs(dx)>30):
                        refine(t0,p0,tm,pm,depth+1);refine(tm,pm,t1,p1,depth+1)
                    else:sample.append(p1)
                p0,p1=mapped(0),mapped(1)
                if not sample:sample.append(p0)
                refine(0,p0,1,p1)
            paths.append(sample)
        draws[e['id']]=paths
    xs=[fx(b['x'],b['cy']) for b in boxes.values()]+[fx(b['x']+b['width'],b['cy']) for b in boxes.values()]+[x for paths in draws.values() for pts in paths for x,y in pts]
    left,right=min(xs),max(xs)
    positions={nid:{'x':round(fx(b['x'],b['cy'])-left+PAD,2),'y':round(b['y']+HEADER,2),'width':round(b['width'],2),'height':round(b['height'],2),'volume':vol(NS[nid]) if nid in NS else None} for nid,b in boxes.items()}
    geometry={eid:[[(round(x-left+PAD,2),round(y+HEADER,2)) for x,y in pts] for pts in paths] for eid,paths in draws.items()}
    return positions,geometry,math.ceil(right-left+2*PAD),bands


def render():
    layout=json.loads((HERE/'layout.json').read_text(encoding='utf-8'))
    _,_,gw,gh=map(float,layout['bb'].split(','))
    positions,geometry,width,compact_bands=compact_geometry(layout,gh)
    height=math.ceil(gh+HEADER+140)
    assert set(positions)==set(ORDER)|set(WNO)
    s=SVG();s.rect(0,0,width,15,BLUE,BLUE,0)
    s.text(80,45,'《网游之纵横天下》 · 全书分枝与交汇',width-160,72,INK,True)
    s.text(80,151,'从谋生、结盟到组织与龙域责任；旁支另起，共享事件处交汇，再向后分枝。',width-160,35,MUTED)
    s.text(80,214,f'{len(EVENTS)}个唯一事件／场景 · {len(G["edges"])}条原关系 · {len(ROOTS)}个图内起点 · {len(FORKS)}个分枝点 · {len(JUNCTIONS)}个交汇点 · 7条全书线终态',width-160,29,INK)
    for i,(c,label) in enumerate([(BLUE,'主线'),(TEAL,'旁线'),(PURPLE,'暗线'),(GOLD,'共享事件交汇')]):
        x=80+i*670;s.path(f'M{x} 303 H{x+80}',c,6);s.text(x+100,278,label,530,28,c,True)
    s.text(80,333,'因果实线；铺垫／揭示／转折／回收虚线；主题呼应细点线。细蓝点划线是31个转折的阅读衔接，不表示因果。',width-160,26,MUTED)
    s.text(80,377,'阅读衔接不计语义起点／分枝／交汇；共享事件才是交汇。卷号只作定位；枝端全书终态不覆盖早期人物认知。',width-160,26,MUTED)
    links_meta=[]
    for el in sorted((e for e in layout['edges'] if not e['id'].startswith('_order')),key=lambda el:0 if el['id'] in ES and ES[el['id']]['kind']=='echo' else 1):
        eid=el['id'];state=eid.startswith('state-');guide=eid in GE;e=ES.get(eid) or GE.get(eid)
        if state:
            t=TS[eid[6:]];color=PURPLE if t['kind']=='hidden' else STATE[t['status']][1];stroke=2;dash='5 9';opacity=.75
        elif guide:
            color=BLUE;stroke=2.6;dash='3 7 13 7';opacity=.78
        else:
            color=BLUE if eid in CORE_EDGES else PURPLE if eid in HIDDEN_EDGES else TEAL
            stroke=4.5 if eid in CORE_EDGES else 3;dash='' if e['kind']=='cause' else '2 11' if e['kind']=='echo' else '11 8';opacity=.36 if e['kind']=='echo' else .86
        a,b=(endpoint(t),t['id']) if state else (e['from'],e['to'])
        s.group(id=eid,data_kind='annotation' if state else 'reading-order' if guide else 'edge',data_from=a,data_to=b,data_relation='state' if state else e['kind'],tabindex=-1 if state else 0,role='group' if state else 'button',aria_label='全书终态注记' if state else ('阅读衔接' if guide else REL[e['kind']])+'：'+e['label'])
        for pts in geometry[eid]:
            d='M '+','.join(map(str,pts[0]))+' L '+' '.join(','.join(map(str,p)) for p in pts[1:])
            s.parts.append(f'<path d="{d}" stroke="transparent" stroke-width="18" fill="none" pointer-events="stroke"/>')
            s.path(d,color,stroke,dash,not state and not guide,opacity)
        if e:s.tooltip(('阅读衔接，不表示因果' if guide else REL[e['kind']])+' · '+CLAIM[e['claim_kind']]+'\n'+e['label']+'\n'+evidence(e))
        s.end();links_meta.append({'id':eid,'from':a,'to':b,'kind':'annotation' if state else e['kind'],'core':eid in CORE_EDGES})
    for n in EVENTS:
        nid=n['id'];b=positions[nid];x,y,w,h=(b[k] for k in ('x','y','width','height'))
        members=[t['id'] for t in THREADS if nid in t['node_ids']]
        full=[WNO[t] for t in members if t in WNO]
        color=BLUE if nid in CORE_NODES else PURPLE if nid in HIDDEN_NODES else TEAL
        s.group(id=nid,data_kind='event',data_volume=vol(n),data_threads=','.join(members),data_junction=str(nid in JUNCTIONS).lower(),data_root=str(nid in ROOTS).lower(),tabindex=0,role='button',aria_label=n['title'])
        s.rect(x,y,w,h,'#edf4ff' if nid in CORE_NODES else '#f8f4ff' if nid in HIDDEN_NODES else 'white',color,17)
        mark='起点' if nid in ROOTS else f'交汇{INCOMING[nid]}路' if nid in JUNCTIONS else '分枝' if nid in FORKS else ''
        s.text(x+17,y+11,f'卷{vol(n)} · {nid}',w-130,16,color)
        if mark:
            fill='#fff0df' if nid in JUNCTIONS else '#e9f4f4';s.rect(x+w-113,y+8,99,28,fill,fill,7);s.text(x+w-105,y+9,mark,90,17,GOLD if nid in JUNCTIONS else color,True)
        end=s.text(x+20,y+47,n['title'],w-40,27,INK,True)
        assert end<=y+h-35,(nid,end,y+h)
        suffix=('主干阅读 '+str(GUIDE_NO[nid]).zfill(2)+' · ' if nid in GUIDE_NO else '')+('全书线 '+' / '.join(f'{i:02}' for i in full) if full else CLAIM[n['claim_kind']])
        s.text(x+20,y+h-29,suffix,w-40,17,PURPLE if nid in HIDDEN_NODES else MUTED)
        s.tooltip(n.get('summary','')+'\n'+evidence(n));s.end()
    for t in WHOLE:
        b=positions[t['id']];x,y,w,h=(b[k] for k in ('x','y','width','height'));label,color,fill=STATE[t['status']]
        s.group(id=t['id'],data_kind='thread',data_thread=WNO[t['id']],tabindex=0,role='button',aria_label=t['title'])
        s.rect(x,y,w,h,fill,PURPLE if t['kind']=='hidden' else color,20)
        yy=s.text(x+20,y+12,f'全书线 {WNO[t["id"]]:02} · {label}',w-40,22,color,True)
        yy=s.text(x+20,yy+8,t['title'],w-40,25,INK,True)
        yy=s.text(x+20,yy+10,t.get('resolution_note',''),w-40,21,color)
        s.text(x+20,y+h-29,'全书终点复核 · 非新增剧情事件',w-40,16,MUTED)
        assert yy<=y+h-30,(t['id'],yy,y+h)
        s.tooltip(t.get('question','')+'\n'+t.get('resolution_note',''));s.end()
    s.text(80,height-85,'来源事实与研究推断分开 · 全部原事件及关系可回查 · 研究解释待用户审阅 · 图内起点不推断为故事世界绝对无前因',width-160,26,MUTED)
    colors={BLUE,PURPLE,TEAL,GREEN,AMBER,RED}
    defs=''.join(f'<marker id="a{c[1:]}" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L6,3 L0,6 Z" fill="{c}"/></marker>' for c in colors)
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" aria-label="纵横天下多起点剧情树"><title>网游之纵横天下：分枝与交汇</title><defs>{defs}</defs><rect width="100%" height="100%" fill="#f7f9fc"/><g font-family="Microsoft YaHei, Noto Sans CJK SC, sans-serif">'+''.join(s.parts)+'</g></svg>'
    (HERE/'tree.svg').write_text(svg,encoding='utf-8')
    meta={'version':1,'source_id':SID,'title':'网游之纵横天下','graph_revision':G['revision'],'graph_sha256':hashlib.sha256(GRAPH_PATH.read_bytes()).hexdigest(),'width':width,'height':height,'events':[n['id'] for n in EVENTS],'edges':[e['id'] for e in G['edges']],'positions':positions,'links':links_meta,'roots':ROOTS,'forks':FORKS,'junctions':JUNCTIONS,'core':CORE,'time_labels':{'v1-locked':'先见结果','v1-rescue':'倒叙解释','v1-poor':'补叙困境'},'threads':[{'id':t['id'],'number':WNO[t['id']],'status':t['status'],'anchor':endpoint(t),'kind':t['kind'],'conclusion':t.get('resolution_note','')} for t in WHOLE],'states':dict(Counter(t['status'] for t in WHOLE)),'removed_group_nodes':[{'id':n['id'],'kind':n['kind'],'title':n['title']} for n in GROUPS],'original_node_kinds':dict(Counter(n['kind'] for n in G['nodes'])),'original_edge_kinds':dict(Counter(e['kind'] for e in G['edges'])),'volume_bounds':{str(v):bounds([n['id'] for n in EVENTS if vol(n)==v],positions) for v in range(1,9)},'layout':{'engine':layout['engine'],'version':layout['version'],'direction':'按真实关系分枝与共享事件交汇；不使用卷/阶段父子结构','invisible_order_constraints':'每6个事件的阅读位置档，只用于布局，不绘线，不计因果/交汇','echo':'保留原方向和细点线，不计入分枝交汇','parent_edges_drawn':0,'semantic_edges_added':0},'source_snapshots':{'events':EVENTS,'edges':G['edges'],'whole_book_threads':WHOLE}}
    meta['layout']['compact_geometry']={'method':'Graphviz逐层单调连续横向变换，仅压缩空白','original_width':gw,'final_width':width,'card_width_preserved':True,'bands':compact_bands}
    meta['reading_guide']={'node_ids':GUIDE_IDS,'edges':GUIDE_EDGES,'semantic':False,'label':'蓝色主干阅读衔接；不表示因果，不计入语义起点、分枝与交汇','acyclic':all(ORDER[e['from']]<ORDER[e['to']] for e in GUIDE_EDGES)}
    (HERE/'manifest.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    observers={'reader':'读者'}
    for path in (VAULT/'library/characters').glob('*.json'):
        card=json.loads(path.read_text(encoding='utf-8'));observers[card['asset_id']]=card.get('content',{}).get('name',card.get('title',card['asset_id']))
    person_file=HERE/'character-links.json'
    person_links=json.loads(person_file.read_text(encoding='utf-8')) if person_file.exists() else {}
    data={'meta':meta,'nodes':{n['id']:n for n in EVENTS},'threads':TS,'volumes':[n for n in G['nodes'] if n['kind']=='volume'],'edges':ES,'observers':observers,'character_links':person_links,'reading_guide':{'node_ids':GUIDE_IDS,'edges':GE}}
    raw=json.dumps(data,ensure_ascii=False).replace('<','\\u003c')
    template=(HERE/'viewer.html').read_text(encoding='utf-8')
    (HERE/'index.html').write_text(template.replace('<!-- TREE_SVG -->',svg).replace('/* TREE_DATA */',raw),encoding='utf-8')
    print(json.dumps({k:meta[k] for k in ['width','height','states']},ensure_ascii=False))


if __name__=='__main__':
    prepare() if '--prepare' in sys.argv else render()
