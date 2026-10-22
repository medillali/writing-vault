"""将全书主线、选定跨集关系和全部暗线放进同一张时间树图。"""
from pathlib import Path
import hashlib
import html
import json
import math
import re
import sys
sys.dont_write_bytecode = True
import rebuild_plot_images as p

HERE = Path(__file__).resolve().parent
OUT = HERE/'reading/plot/whole-book'
# 展示选择是阅读层，不修改研究图；编号对应原有事件。
PICKS = {1:[1,3,5,10],2:[1,4,6,8,9],3:[3,4,5,8],4:[3,4,6,8,9],5:[1,2,4,8],
         6:[1,5,6,9],7:[2,5,6,7],8:[2,5,7,9],9:[1,3,5,7,8],10:[4,6,8,9],
         11:[1,2,3,9],12:[1,3,5,6],13:[2,3,6,8],14:[2,6,8,9],15:[1,4,6,9],
         16:[3,5,7,8],17:[2,4,5,7,9],18:[1,6,7,8,9]}
BRIDGES = ['cross-memory-01','cross-redemption-02','cross-mark-02','cross-children-02',
           'cross-autonomy-03','cross-seal-01','cross-return-01','cross-corpse-plan-01',
           'cross-relics-01','cross-v16-betrayal','cross-v17-chaos','cross-v18-return']
BRIDGE_TITLES = ['记忆完整融合，未继承魔力','救赎真义：净化而非恢复人身','亡灵印记的发出者得到确认',
                 '黑大从自主萌芽到完全觉醒','自由宣言与强制转生的矛盾','外封解除之后才有真正脱困',
                 '放逐与失联以实体返场收束','回归后暂禁活尸方案','遗物追索通向失落帝国',
                 '共同使命被用于骗取夺体机会','夺体危机在混沌之灵阶段逆转','红月开启后子民灵魂跨界归来']
STAGES = [(1,3,'求生与同伴'),(4,6,'照护与觉醒'),(7,9,'自由与领地'),(10,12,'海皇与龙岛'),
          (13,15,'放逐与遗产'),(16,17,'夺体与假旗'),(18,18,'本源与归来')]
START, STEP, WIDTH = 680, 440, 9740
NODE_W, NODE_H, ROW = 366, 238, 278
EVENT_TOP = 1030
NODE_X = lambda v: START + (v-1)*STEP + 48
CENTER = lambda v: START + (v-1)*STEP + 224
ns = p.NODES
threads = sorted(p.THREADS,key=lambda t:(min(ns[n]['narrative_order'] for n in t['node_ids']),t['id']))
thread_no = {t['id']:i+1 for i,t in enumerate(threads)}
selected = sorted([ns[f'v{v:02d}-e{e:02d}'] for v,es in PICKS.items() for e in es],key=lambda n:n['narrative_order'])
positions = {}
TIME_LABELS = {'v09-e05':'跨段聚合','v14-e06':'缺席期回叙','v17-e05':'神史回叙'}


class Map(p.SVG):
    def start_group(self, **attrs):
        self.parts.append('<g '+ ' '.join(f'{k.replace("_","-")}="{p.esc(v)}"' for k,v in attrs.items())+'>')

    def end_group(self):
        self.parts.append('</g>')

    def tooltip(self, s):
        self.parts.append('<title>'+p.esc(s)+'</title>')


def tree():
    s = Map(WIDTH)
    s.rect(0,0,WIDTH,16,p.BLUE,p.BLUE,0)
    s.text(80,50,'《超级骷髅兵》 · 全书一张图',4500,92,p.INK,True)
    s.text(80,180,'从左到右读集数，从上到下读每集枝条；跨集关系与15条暗线共用同一时间轴。',6500,38,p.MUTED)
    s.text(80,254,f'7个阶段 / 18集 / {len(selected)}个关键事件 / 15条暗线 · 蓝线为结构与顺序，彩色桥为已有研究关系。',7200,32,p.MUTED)
    s.text(80,320,'图中内容包含结局。旧史与回叙依揭示顺序保留；完整摘要、认知边界和证据可在缩放页点击事件查看。',8400,30,p.MUTED)
    s.rect(80,420,510,198,'#eaf1fb','#b9cfe9')
    s.text(108,443,'黑龙的核心追求',454,44,p.BLUE,True)
    s.text(108,513,'生存 → 交流与同伴\n→ 自由存在与共处',454,34,p.INK)
    s.path(f'M 590 519 H {START-22} V 642 H {CENTER(18)}',p.BLUE,6)
    for i,(lo,hi,label) in enumerate(STAGES):
        left=START+(lo-1)*STEP+10
        width=(hi-lo+1)*STEP-30
        s.start_group(id=f'stage-{i+1}', data_volume=lo)
        s.rect(left,420,width,198,'#eaf1fb','#b9cfe9')
        s.text(left+24,440,f'阶段 {i+1:02d} · 第{lo}—{hi}集' if lo!=hi else f'阶段 {i+1:02d} · 第{lo}集',width-48,30,p.BLUE,True)
        s.text(left+24,499,label,width-48,49,p.INK,True)
        s.end_group()
        mid=left+width/2
        s.path(f'M {mid} 618 V 642',p.BLUE,4)
    for v in range(1,19):
        x=START+(v-1)*STEP
        cx=CENTER(v)
        s.path(f'M {cx} 642 V 704',p.BLUE,4)
        s.start_group(id=f'volume-{v:02d}',data_volume=v,data_kind='volume')
        s.rect(x+10,710,420,206,'white','#b9cfe9')
        s.text(x+32,727,f'{v:02d} / '+p.VOLUMES[v-1]['title'].split(' ',1)[-1],376,36,p.INK,True)
        s.text(x+32,792,p.SHORT[v-1],376,29,p.MUTED)
        s.tooltip(p.VOLUMES[v-1]['summary'])
        s.end_group()
        if v<18:s.path(f'M {cx} 956 H {CENTER(v+1)-20}',p.BLUE,4,arrow=True)
        s.circle(cx,956,12,p.BLUE)
        s.path(f'M {cx} 916 V 956 H {x+24} V {EVENT_TOP+len(PICKS[v])*ROW-88}',p.BLUE,3)
        vn=sorted((n for n in selected if p.vol(n)==v),key=lambda n:n['narrative_order'])
        for idx,n in enumerate(vn):
            ny=EVENT_TOP+idx*ROW
            memberships=[thread_no[t['id']] for t in threads if n['id'] in t['node_ids']]
            positions[n['id']]={'x':NODE_X(v),'y':ny,'width':NODE_W,'height':NODE_H,'volume':v}
            s.path(f'M {x+24} {ny+47} H {NODE_X(v)}',p.BLUE,3)
            s.circle(x+24,ny+47,7,p.BLUE)
            s.start_group(id=n['id'],data_kind='event',data_volume=v,data_threads=','.join(map(str,memberships)),tabindex=0,role='button',aria_label=n['title'])
            s.rect(NODE_X(v),ny,NODE_W,NODE_H,'white','#cddaea')
            yy=s.text(NODE_X(v)+18,ny+13,n['id']+' · '+TIME_LABELS.get(n['id'],p.CLAIM.get(n.get('claim_kind'),'研究记录')),NODE_W-36,23,p.BLUE)
            yy=s.text(NODE_X(v)+18,yy+11,n['title'],NODE_W-36,30,p.INK,True)
            if yy>ny+NODE_H-43:raise ValueError('事件标题溢出 '+n['id'])
            if memberships:s.text(NODE_X(v)+18,ny+NODE_H-38,'暗线 '+ ' / '.join(f'{x:02d}' for x in memberships),NODE_W-36,21,p.PURPLE)
            else:s.text(NODE_X(v)+18,ny+NODE_H-38,'主线转折 / 关系变化',NODE_W-36,21,p.MUTED)
            s.tooltip(n['summary']+'\n'+p.evidence(n))
            s.end_group()
    # 跨集桥独立占用通道；标签与回收性质直接印在图上。
    bridge_top=EVENT_TOP+5*ROW+94
    s.text(80,bridge_top-50,'跨集关系桥',520,46,p.INK,True)
    s.text(80,bridge_top+25,'沿B编号追踪前后联系。\n它们是精选研究关系，\n不是新增剧情。',520,30,p.MUTED)
    lanes=[]
    bridge_meta=[]
    for i,(eid,label) in enumerate(zip(BRIDGES,BRIDGE_TITLES),1):
        e=p.EDGES[eid]
        a,b=positions[e['from']],positions[e['to']]
        x1=a['x']+a['width']+9+(i%3)*5
        x2=b['x']+b['width']+9+(i%3)*5
        lo,hi=sorted((x1,x2))
        lane=next((j for j,end in enumerate(lanes) if end<lo-55),len(lanes))
        if lane==len(lanes):lanes.append(hi)
        else:lanes[lane]=hi
        by=bridge_top+lane*134
        color=p.REL[e['kind']][1]
        s.start_group(id=f'bridge-{i:02d}',data_kind='bridge')
        s.path(f'M {a["x"]+a["width"]} {a["y"]+NODE_H-60} H {x1} V {by} Q {x1} {by+20} {x1+20} {by+20} H {x2-20} Q {x2} {by+20} {x2} {by} V {b["y"]+NODE_H-60} H {b["x"]+b["width"]+3}',color,3.2,'10 9',True,.8)
        tw=min(max(400,hi-lo-38),950)
        tx=(x1+x2-tw)/2
        s.rect(tx,by-26,tw,100,'white',color,13)
        s.text(tx+14,by-17,f'B{i:02d} · {p.REL[e["kind"]][0]} · '+label,tw-28,28,color,True)
        s.tooltip(e['label']+'\n判断：'+p.CLAIM.get(e.get('claim_kind'),'研究记录'))
        s.end_group()
        bridge_meta.append({'id':eid,'number':i,'label':label,'lane':lane})
    thread_top=bridge_top+len(lanes)*134+140
    s.text(80,thread_top-32,'15条暗线 · 沿同一主线时间轴追踪',5500,52,p.INK,True)
    s.text(80,thread_top+48,'相同编号连接事件枝条与暗线轨道。圆点内是该集关联事件数；虚线尾端表示问题仍悬置，不代表空白期间持续发生事件。',8600,30,p.MUTED)
    axis_y=thread_top+130
    for v in range(1,19):
        s.text(CENTER(v)-35,axis_y,f'{v:02d}集',132,30,p.BLUE,True)
        s.path(f'M {CENTER(v)} {axis_y+51} V {axis_y+110+15*144}', '#dee6f1',2)
    s.text(START+18*STEP+70,axis_y,'第18集终点复核',870,34,p.MUTED,True)
    track_meta=[]
    for i,t in enumerate(threads,1):
        y=axis_y+76+(i-1)*144
        st,color,fill=p.STATE[t['status']]
        s.start_group(id=t['id'],data_kind='thread',data_thread=i,tabindex=0,role='button',aria_label=p.title(t))
        s.rect(64,y,WIDTH-128,128,'white','#e0e6ef')
        s.text(86,y+13,f'{i:02d} · '+p.title(t),552,29,p.INK,True)
        vols=sorted({p.vol(ns[n]) for n in t['node_ids']})
        dots=[]
        for j,v in enumerate(vols):
            x=CENTER(v);py=y+60+(8 if j%2 else -8)
            count=sum(p.vol(ns[n])==v for n in t['node_ids'])
            dots.append((x,py))
            if j:
                px,prev=dots[-2]
                s.path(f'M {px} {prev} C {(px+x)/2} {prev-28} {(px+x)/2} {py+28} {x} {py}',p.PURPLE,4,'10 8')
            s.circle(x,py,22,p.PURPLE)
            s.text(x-8,py-16,str(count),48,22,'white',True)
        ex,ey=dots[-1]
        end=START+18*STEP+38
        s.path(f'M {ex+25} {ey} C {ex+70} {ey} {end-100} {y+60} {end-15} {y+60}',color,4,'12 10' if t['status']!='resolved' else '',True)
        s.rect(end,y+11,WIDTH-end-86,106,fill,fill)
        s.text(end+20,y+17,st+' · '+p.GAPS[t['tracking_key']],WIDTH-end-126,28,color,True)
        s.tooltip(t['question']+'\n'+p.conclusion(t))
        s.end_group()
        track_meta.append({'id':t['id'],'number':i,'status':t['status'],'volumes':vols,'y':y,'question':t['question'],'conclusion':p.conclusion(t)})
    height=axis_y+76+15*144+136
    s.text(80,height-98,'阅读导图 / 精选事件不等于全事件索引 · 回收结论针对各线问题范围 · 原始资料、人物笔记与版本历史保持独立',WIDTH-160,30,p.MUTED)
    colors={p.BLUE,p.PURPLE,p.GREEN,p.AMBER,p.RED}|{c for _,c in p.REL.values()}
    defs=''.join(f'<marker id="a{c[1:]}" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L8,4 L0,8 Z" fill="{c}"/></marker>' for c in sorted(colors))
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" viewBox="0 0 {WIDTH} {height}" aria-label="超级骷髅兵全书时间树"><title>超级骷髅兵全书时间树</title><defs>{defs}</defs><rect width="100%" height="100%" fill="#f4f7fc"/><g font-family="Microsoft YaHei, Noto Sans CJK SC, sans-serif">'+''.join(s.parts)+'</g></svg>'
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'tree.svg').write_text(svg,encoding='utf-8')
    meta={'width':WIDTH,'height':height,'selection':'关键脉络版','source_id':p.SID,'graph_sha256':hashlib.sha256(p.GRAPH_PATH.read_bytes()).hexdigest(),
          'events':[n['id'] for n in selected],'positions':positions,'bridges':bridge_meta,'threads':track_meta,'thread_top':thread_top,
          'stages':STAGES,'event_top':EVENT_TOP,'start':START,'step':STEP,'time_labels':TIME_LABELS}
    (OUT/'manifest.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    write_viewer(svg,meta)
    write_readme(meta)
    print(json.dumps({'events':len(selected),'bridges':len(bridge_meta),'hidden_threads':len(threads),'width':WIDTH,'height':height},ensure_ascii=False))


def write_viewer(svg,meta):
    observers={'reader':'读者'}
    for path in (p.VAULT/'library/characters').glob('*.json'):
        card=json.loads(path.read_text(encoding='utf-8'))
        observers[card['asset_id']]=card['content'].get('name',card['title'])
    data={'meta':meta,'nodes':{n['id']:n for n in selected},'threads':{t['id']:t for t in threads},'volumes':p.VOLUMES,
          'edges':{eid:p.EDGES[eid] for eid in BRIDGES},'observers':observers}
    raw=json.dumps(data,ensure_ascii=False).replace('<','\\u003c')
    template=(HERE/'whole_book_viewer.html').read_text(encoding='utf-8')
    (OUT/'index.html').write_text(template.replace('<!-- TREE_SVG -->',svg).replace('/* TREE_DATA */',raw),encoding='utf-8')


def write_readme(meta):
    (HERE/'reading/plot/whole-book.md').write_text(f'''# 全书一张树形图

[返回图片目录](images.md) · [全部事件与证据](README.md)

**从左向右贯穿18集，向下展开每集关键事件。** 七阶段、{len(selected)}个关键事件、12座跨集关系桥和全部15条暗线在同一张图中。

[打开完整PNG](whole-book/tree.png) · [打开SVG矢量图](whole-book/tree.svg) · [离线缩放页面](whole-book/index.html)

![全书时间树预览](whole-book/tree-preview.png)

预览用于看整体布局；阅读文字请打开原图放大。要使用拖动、滚轮缩放、跳集、事件搜索和暗线聚焦，请下载`whole-book/index.html`后用浏览器打开。该页面已内嵌全部图片与研究摘要，不需要服务器或网络；GitHub不直接运行仓库内HTML。

- 蓝色树干与枝条：结构归属和阅读顺序，不自动代表因果。
- B01—B12：既有研究中的精选跨集关系，图上标注回收、揭示、呼应或转折；点击可看完整说明。
- 暗线01—15：事件上的编号对应底部轨道。圆点中的数字为该集关联事件数，结尾标明已回收、部分回收或未回收。
- 回叙保留在读者获知的位置；第14集缺席期回叙和第17集神史不会被改写为当时新发生的事。
- 本图为关键脉络版，不替代163个事件的完整索引。旧49张分图和全部文字资料继续保留。

生成源：`rebuild_whole_book.py`与`whole_book_viewer.html`。研究图的哈希、事件选择、跨集桥和暗线映射见[单图清单](whole-book/manifest.json)。
''',encoding='utf-8')


if __name__=='__main__':tree()
