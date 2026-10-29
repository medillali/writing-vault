from pathlib import Path
from collections import defaultdict
import json
b=Path(__file__).resolve().parents[3]
d=b/'writing-vault/library/reports/zongheng-tianxia/atlas/tree'
m=json.loads((d/'manifest.json').read_text(encoding='utf-8'))
rows=defaultdict(list)
for nid,p in m['positions'].items():rows[p['y']].append((nid,p['x']))
print('Rows:',len(rows),'Max events:',max(len(x) for x in rows.values()))
print('Extreme:',sorted([(len(v),k,min(x for n,x in v),max(x for n,x in v)) for k,v in rows.items()],reverse=True)[:12])
print('Yranges:',sorted([(k,len(v)) for k,v in rows.items()])[:10])
print('roots',len(m['roots']),'junctions',len(m['junctions']),'forks',len(m['forks']))
g=json.loads((d/'layout.json').read_text(encoding='utf-8'))
ns={n['name']:n for n in g['objects'] if 'pos' in n and not n['name'].startswith('_')}
es={e['id']:e for e in m['links']}
hits=[]
for e in g['edges']:
    if e['id'].startswith('_order'):continue
    found=False
    for draw in e.get('_draw_',[]):
        if draw['op'] not in ['b','B']:continue
        pts=draw['points']
        for j in range(0,len(pts)-1,3):
            a,b,c,z=pts[j:j+4]
            for k in range(101):
                t=k/100;u=1-t;x=u**3*a[0]+3*u*u*t*b[0]+3*u*t*t*c[0]+t**3*z[0];y=u**3*a[1]+3*u*u*t*b[1]+3*u*t*t*c[1]+t**3*z[1]
                for nid,n in ns.items():
                    if nid in [es[e['id']]['from'],es[e['id']]['to']]:continue
                    nx,ny=map(float,n['pos'].split(','));w,h=float(n['width'])*72,float(n['height'])*72
                    if nx-w/2+3<x<nx+w/2-3 and ny-h/2+3<y<ny+h/2-3:
                        hits.append([e['id'],nid]);found=True;break
                if found:break
            if found:break
        if found:break
print('Original graphviz card pierce:',hits)
