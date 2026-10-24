"""从版本化剧情图生成全书纵向图及复用既有离线地图。"""
from pathlib import Path
import json,sys,html,textwrap,subprocess,os,base64,io,math,re,hashlib,shutil
from PIL import Image
sys.stdout.reconfigure(encoding='utf-8')
O=Path(__file__).resolve().parent;V=O.parents[2];R=V.parent;CODE=V/'library/reports/super-skeleton/map'
NODE=Path.home()/'.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe';MODULES=NODE.parent.parent/'node_modules'
def dump(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def uri(raw,kind='png'):return f'data:image/{kind};base64,'+base64.b64encode(raw).decode()
def make_svg(folder,title):
 D=O/folder;G=json.loads((D/'plot/graph.json').read_text(encoding='utf-8'));out=D/'plot/whole-book';out.mkdir(parents=True,exist_ok=True)
 positions={};stages=[n for n in G['nodes'] if n['kind']=='arc'];y=220;W=2480
 positions['story']={'x':60,'y':40,'width':2050,'height':120,'volume':0}
 for i,st in enumerate(stages,1):
  group=[n for n in G['nodes'] if n.get('parent_id')==st['id']];positions[st['id']]={'x':60,'y':y,'width':360,'height':200,'volume':i}
  for j,n in enumerate(group):positions[n['id']]={'x':520+(j%3)*510,'y':y+(j//3)*270,'width':460,'height':200,'volume':i}
  y+=math.ceil(len(group)/3)*270+60
 H=y+100;esc=lambda x:html.escape(str(x),quote=True)
 parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><style>text{{font-family:"Microsoft YaHei",sans-serif}}.edge{{opacity:.45}}</style><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0L10,5L0,10z" fill="#8c6297"/></marker></defs><rect width="100%" height="100%" fill="#f7f5ee"/>']
 for st in stages:
  p=positions[st['id']];sy=p['y'];parts.append(f'<path d="M40,{sy}V{sy+200}H60" fill="none" stroke="#b8b6aa"/>')
  for n in G['nodes']:
   if n.get('parent_id')!=st['id']:continue
   q=positions[n['id']];x=q['x']+q['width']/2
   parts.append(f'<path d="M420,{sy+100}H450V{q["y"]-24}H{x}V{q["y"]}" fill="none" stroke="#cbcbbd" stroke-width="2"/>')
 for i,e in enumerate(G['edges']):
  a,b=positions[e['from']],positions[e['to']];x1=a['x']+a['width']/2;y1=a['y']+a['height'];x2=b['x']+b['width']/2;y2=b['y'];lane=2140+(i%24)*12
  path=f'M{x1},{y1}V{y1+15}H{lane}V{y2-16}H{x2}V{y2}'
  parts.append(f'<g id="{e["id"]}" data-kind="edge" data-from="{e["from"]}" data-to="{e["to"]}" class="edge"><title>{esc(e["kind"]+"："+e["label"]+"；"+e.get("summary",""))}</title><path d="{path}" fill="none" stroke="#8c6297" stroke-width="2" stroke-dasharray="7 5" marker-end="url(#arrow)"/></g>')
 def textlines(value,x,y,width,count,size,bottom):
  all_lines=textwrap.wrap(value,width=width,break_long_words=True,replace_whitespace=False);lines=all_lines[:count]
  if len(all_lines)>count:lines[-1]=lines[-1][:-1]+'…'
  return ''.join(f'<text x="{x}" y="{y+i*(size+9)}" font-size="{size}" fill="#29332f" data-left="{x}" data-right="{x+width*(size+1)}" data-bottom="{bottom}">{esc(t)}</text>' for i,t in enumerate(lines))
 for n in G['nodes']:
  p=positions[n['id']];x,y,w,h=[p[k] for k in ['x','y','width','height']];kind='event' if n['kind']=='scene' else n['kind'];fill='#ffffff' if kind=='event' else '#e6eee5'
  parts.append(f'<g id="{n["id"]}" data-kind="{kind}"><title>{esc(n["title"])}</title><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="#637966" stroke-width="2"/>')
  if n['kind']=='story':
   parts+= [textlines(title+' · 全书结构与伏笔',x+22,y+42,50,1,26,y+h),textlines('左列是研究阶段，中列是精选因果场景；浅线表示归属，紫色虚线表示有证据的铺垫与回应。完整详情见旁附剧情阅读器。',x+22,y+85,95,1,17,y+h)]
  else:
   parts.append(textlines(n['title'],x+18,y+34,15 if w==360 else 21,2,20,y+h-10))
   parts.append(textlines(n.get('summary',''),x+18,y+104,18 if w==360 else 24,2,16,y+h-10))
   es=n.get('evidence',[]);label=(f'阶段{p["volume"]} · '+(' / '.join(unique_ch(es)[:2])))
   parts.append(textlines(label,x+18,y+182,35,1,12,y+h-5))
  parts.append('</g>')
 parts.append('</svg>');(out/'tree.svg').write_text('\n'.join(parts),encoding='utf-8')
 dump(out/'manifest.json',{'title':title,'width':W,'height':H,'positions':positions,'nodes':len(G['nodes']),'scenes':sum(n['kind']=='scene' for n in G['nodes']),'relations':len(G['edges']),'stages':len(stages),'node_overlap':0,'edge_meaning':'结构线与阅读顺序不是因果；虚线只链接账本中有证据的设问和回应。'})
 return out
def unique_ch(es):return list(dict.fromkeys(e['chapter_id'] for e in es))
def make_map(folder,title):
 D=O/folder;out=D/'plot/whole-book';meta=json.loads((out/'manifest.json').read_text(encoding='utf-8'));raw=(out/'tree.png').read_bytes();im=Image.open(io.BytesIO(raw)).convert('RGB');width,height=im.size
 assert (width,height)==(meta['width'],meta['height']);hi=math.ceil(math.log2(max(width,height)));lo=hi-math.ceil(math.log2(max(width,height)/512));tiles={};checks=[]
 for level in range(lo,hi+1):
  factor=2**(hi-level);size=(math.ceil(width/factor),math.ceil(height/factor));scaled=im if level==hi else im.resize(size,Image.Resampling.LANCZOS)
  for x in range(math.ceil(size[0]/512)):
   for y in range(math.ceil(size[1]/512)):
    rect=(max(0,x*512-1),max(0,y*512-1),min(size[0],(x+1)*512+1),min(size[1],(y+1)*512+1));tile=scaled.crop(rect);buf=io.BytesIO();tile.save(buf,format='WEBP',lossless=True,method=4);payload=buf.getvalue();name=f'{level}/{x}/{y}';tiles[name]=uri(payload,'webp');checks.append({'key':name,'size':tile.size,'sha256':hashlib.sha256(payload).hexdigest()})
 positions=meta['positions'];volumes=[]
 for number in range(1,meta['stages']+1):
  key,p=next((key,p) for key,p in positions.items() if key.startswith('stage-') and p['volume']==number);volumes.append({'number':number,'event':key,**p})
 data={'width':width,'height':height,'tile_size':512,'overlap':1,'min_level':lo,'max_level':hi,'tiles':tiles,'start':positions['stage-01'],'volumes':volumes,'source_sha256':hashlib.sha256(raw).hexdigest(),'svg':(out/'tree.svg').read_text(encoding='utf-8'),'png':uri(raw)}
 engine=re.sub(r'//# sourceMappingURL=.*','',(CODE/'vendor/openseadragon.min.js').read_text(encoding='utf-8'));engine='/* OpenSeadragon license\n'+(CODE/'vendor/LICENSE.txt').read_text(encoding='utf-8')+'\n*/\n'+engine
 template=(CODE/'template.html').read_text(encoding='utf-8').replace('超级骷髅兵',title).replace('定位到集数','定位到研究阶段').replace('定位到某一集','定位到研究阶段').replace('蓝色主线　紫色暗线','浅线结构　紫色铺垫与回应').replace('https://github.com/medillali/writing-vault/blob/main/library/reports/super-skeleton/reading/plot/map.md','../../../README.md')
 app=(CODE/'app.js').read_text(encoding='utf-8').replace('超级骷髅兵',title).replace("'第'+v.number+'集'","'第'+v.number+'研究阶段'")
 for key,value in {'STYLE':(CODE/'style.css').read_text(encoding='utf-8'),'APP':app,'ENGINE':engine,'DATA':json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')}.items():template=template.replace(f'/* MAP_{key} */',value)
 target=D/'plot/map';target.mkdir(parents=True,exist_ok=True);(target/'index.html').write_text(template,encoding='utf-8');shutil.copy2(D/'plot/relations/index.html',target/'cards.html');dump(target/'manifest.json',{'engine':'OpenSeadragon 6.1.1','tile_format':'WebP lossless','tiles':checks,'source_png_sha256':data['source_sha256'],'html_sha256':hashlib.sha256(template.encode()).hexdigest(),'html_bytes':len(template.encode())})
 (D/'plot/README.md').write_text(f'# 《{title}》全书图\n\n[离线缩放地图](map/index.html) · [节点与证据](relations/index.html) · [PNG原图](whole-book/tree.png) · [SVG原图](whole-book/tree.svg)\n\n![](whole-book/tree-preview.png)\n\n图为研究组织方式，不是原著卷结构；全书全部章节记录见[逐单元笔记](../chapter-notes.md)。阶段未解状态以[结局核对](../ending-audit.md)为准。\n',encoding='utf-8')
if __name__=='__main__':
 selected=sys.argv[1:] or ['zeidan','leveling'];books=[(f,t) for f,t in [('zeidan','贼胆'),('leveling','网游之练级专家')] if f in selected]
 for folder,title in books:make_svg(folder,title)
 env={**os.environ,'NODE_PATH':str(MODULES)}
 subprocess.run([str(NODE),str(Path(__file__).with_name('render_full.cjs')),str(O),'svg',*selected],env=env,check=True)
 for folder,title in books:make_map(folder,title)
 subprocess.run([str(NODE),str(Path(__file__).with_name('render_full.cjs')),str(O),'views',*selected],env=env,check=True)
