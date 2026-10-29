(function(root){
 'use strict';
 const NS='http://www.w3.org/2000/svg',COLORS={core:'#2f629c',branch:'#287d78',hidden:'#795b9f'};
 function el(tag,attrs={},text){const e=document.createElementNS(NS,tag);for(const [k,v] of Object.entries(attrs))e.setAttribute(k,v);if(text!==undefined)e.textContent=text;return e;}
 function lines(title,width=279,size=20){const c=document.createElement('canvas').getContext('2d');c.font=`600 ${size}px "Microsoft YaHei", "PingFang SC", sans-serif`;const out=[];let line='';for(const ch of title){if(line&&c.measureText(line+ch).width>width){out.push(line);line=''}line+=ch;}if(line)out.push(line);return out;}
 class PlotGraph{
  constructor(model,onEvent,onEdge){
   this.model=model;this.onEvent=onEvent;this.onEdge=onEdge;this.vp=document.getElementById('graph-viewport');this.canvas=document.getElementById('graph-canvas');this.view={scale:1,tx:0,ty:0};this.points=new Map();this.moved=false;this.bind();
  }
  localLayout(center){
   const m=this.model,all=m.nearby(center,2),r=m.relations(center),first=new Set(m.nearby(center,1)),parents=new Set(r.incoming.map(e=>e.from));
   const groups=[[],[],[center],[],[]];
   all.filter(id=>id!==center).forEach(id=>{const col=first.has(id)?(parents.has(id)?1:3):(m.nodes[id].narrative_order<m.nodes[center].narrative_order?0:4);groups[col].push(id)});
   const max=Math.max(...groups.map(g=>g.length)),height=Math.max(600,max*200+80),positions={};
   groups.forEach((ids,col)=>m.sort(ids).forEach((id,i)=>positions[id]={x:40+col*410,y:40+(height-80-ids.length*200)/2+i*200,w:317,h:153}));
   return {width:2040,height,positions,paths:{}};
  }
  fallback(ids){const positions={};ids.forEach((id,i)=>positions[id]={x:40+(i%3)*390,y:40+Math.floor(i/3)*210,w:317,h:153});return {width:1180,height:Math.ceil(ids.length/3)*210+80,positions,paths:{}};}
  render(scope,ids,selected,view,read){
   this.selected=selected;this.ids=ids;this.read=read;this.scope=scope;
   this.layout=scope.kind==='nearby'?this.localLayout(scope.id):(this.model.data.layouts[scope.kind+':'+scope.id]||this.fallback(ids));
   const set=new Set(ids),svg=el('svg',{width:this.layout.width,height:this.layout.height,role:'group','aria-label':'事件与关系'}),defs=el('defs');
   Object.entries(COLORS).forEach(([k,c])=>{const marker=el('marker',{id:'reader-arrow-'+k,markerWidth:7,markerHeight:7,refX:6,refY:3.5,orient:'auto'});marker.append(el('path',{d:'M0,0 L7,3.5 L0,7 Z',fill:c}));defs.append(marker)});svg.append(defs);
   const edges=this.model.data.edges.filter(e=>set.has(e.from)&&set.has(e.to)),coreEdges=new Set(this.model.threads[this.model.data.core].edge_ids),darkEdges=new Set(this.model.data.threads.filter(t=>t.kind==='hidden').flatMap(t=>t.edge_ids));
   for(const e of edges){
    const a=this.layout.positions[e.from],b=this.layout.positions[e.to];if(!a||!b)continue;
    let d=this.layout.paths[e.id];
    if(!d){const right=b.x>a.x,ax=right?a.x+a.w:a.x,bx=right?b.x:b.x+b.w,ay=a.y+a.h/2,by=b.y+b.h/2;d=`M${ax},${ay} C${(ax+bx)/2},${ay} ${(ax+bx)/2},${by} ${bx},${by}`;}
    const category=coreEdges.has(e.id)?'core':darkEdges.has(e.id)?'hidden':'branch',g=el('g',{'data-edge':e.id,role:'button',tabindex:0,'aria-label':e.label});
    g.append(el('title',{},e.label),el('path',{d,fill:'none',stroke:'transparent','stroke-width':20}),el('path',{d,fill:'none',stroke:COLORS[category],'stroke-width':coreEdges.has(e.id)?3:2,'stroke-dasharray':e.kind==='cause'?'':e.kind==='echo'?'2 8':'8 6','marker-end':`url(#reader-arrow-${category})`}));
    g.addEventListener('click',()=>{if(!this.moved)this.onEdge(e.id)});g.addEventListener('keydown',ev=>{if(['Enter',' '].includes(ev.key)){ev.preventDefault();this.onEdge(e.id)}});
    g.addEventListener('focus',()=>{const path=g.querySelector('path'),p=path.getPointAtLength(path.getTotalLength()/2);this.focusPoint(p.x,p.y)});svg.append(g);
   }
   const coreNodes=new Set(this.model.threads[this.model.data.core].node_ids);
   for(const id of ids){
    const n=this.model.nodes[id],p=this.layout.positions[id];if(!p)continue;const r=this.model.relations(id),outside=r.incoming.concat(r.outgoing).filter(e=>!set.has(e.from)||!set.has(e.to)).length;
    const g=el('g',{transform:`translate(${p.x} ${p.y})`,'data-event':id,role:'button',tabindex:0,'aria-label':n.title});
    g.append(el('rect',{width:p.w,height:p.h,rx:13,fill:coreNodes.has(id)?'#eef4fc':'#fffefa',stroke:coreNodes.has(id)?'#96b0d0':'#a1beb0','stroke-width':1.2}));
    g.append(el('text',{x:18,y:25,'font-size':12,fill:'#61736c'},`第${+id.slice(1,3)}集 · ${id}${read.has(id)?' · 已读':''}`));
    if(r.parents.length>1){g.append(el('rect',{x:232,y:10,width:70,height:24,rx:5,fill:'#fff0df'}),el('text',{x:240,y:27,'font-size':12,fill:'#a25a25'},`交汇 ${r.parents.length}路`));}
    let titleLines=lines(n.title),size=20;if(titleLines.length>3){size=18;titleLines=lines(n.title,279,18);}
    titleLines.forEach((t,i)=>g.append(el('text',{x:18,y:57+i*25,'font-size':size,'font-weight':600,fill:'#203b35'},t)));
    g.append(el('text',{x:18,y:136,'font-size':11,fill:outside?'#a25a25':'#61736c'},outside?`${outside} 条关系在当前范围外 · 点击查看`:`${r.incoming.length} 条前置关系 · ${r.outgoing.length} 条后续关系`));
    g.append(el('title',{},n.summary));g.addEventListener('click',()=>{if(!this.moved)this.onEvent(id)});
    g.addEventListener('keydown',e=>{if(['Enter',' '].includes(e.key)){e.preventDefault();this.onEvent(id)}});
    g.addEventListener('focus',()=>{const b=g.getBoundingClientRect(),v=this.vp.getBoundingClientRect();if(b.right<v.left||b.left>v.right||b.bottom<v.top||b.top>v.bottom)this.readable(id)});svg.append(g);
   }
   this.canvas.replaceChildren(svg);this.svg=svg;this.highlight(selected);
   if(view&&Number.isFinite(view.scale)){this.view={...view};this.apply()}else this.readable(selected||scope.id||ids[0]);
  }
  highlight(id){
   if(!this.svg)return;const related=new Set(id?[id,...this.model.nearby(id,1)]:this.ids);
   this.svg.querySelectorAll('[data-event]').forEach(g=>{g.classList.toggle('muted',!!id&&!related.has(g.dataset.event));g.classList.toggle('active',g.dataset.event===id)});
   this.svg.querySelectorAll('[data-edge]').forEach(g=>{const e=this.model.data.edges.find(e=>e.id===g.dataset.edge);g.classList.toggle('muted',!!id&&e.from!==id&&e.to!==id)});
  }
  snapshot(){return {...this.view};}
  focusPoint(x,y){const {scale,tx,ty}=this.view,px=x*scale+tx,py=y*scale+ty;if(px<30||px>this.vp.clientWidth-30||py<30||py>this.vp.clientHeight-30){this.view={scale,tx:this.vp.clientWidth/2-x*scale,ty:this.vp.clientHeight/2-y*scale};this.apply()}}
  apply(){const {scale,tx,ty}=this.view;this.canvas.style.transform=`translate(${tx}px,${ty}px) scale(${scale})`;document.getElementById('graph-scale').textContent=Math.round(scale*100)+'%';}
  readable(id){const p=this.layout?.positions[id]||this.layout?.positions[this.ids?.[0]];if(!p)return;const scale=innerWidth<768?.84:1;this.view={scale,tx:(this.vp.clientWidth-p.w*scale)/2-p.x*scale,ty:Math.min(70,this.vp.clientHeight/5)-p.y*scale};this.apply();}
  fit(){if(!this.layout)return;const pts=this.ids.map(id=>this.layout.positions[id]).filter(Boolean);if(!pts.length)return;const x=Math.min(...pts.map(p=>p.x))-30,y=Math.min(...pts.map(p=>p.y))-30,w=Math.max(...pts.map(p=>p.x+p.w))-x+30,h=Math.max(...pts.map(p=>p.y+p.h))-y+30,scale=Math.min((this.vp.clientWidth-20)/w,(this.vp.clientHeight-20)/h,1.3);this.view={scale,tx:(this.vp.clientWidth-w*scale)/2-x*scale,ty:(this.vp.clientHeight-h*scale)/2-y*scale};this.apply();}
  zoom(factor,x=this.vp.clientWidth/2,y=this.vp.clientHeight/2){const v=this.view,next=Math.max(.001,Math.min(2.8,v.scale*factor));this.view={scale:next,tx:x-(x-v.tx)*next/v.scale,ty:y-(y-v.ty)*next/v.scale};this.apply();}
  bind(){
   document.getElementById('graph-readable').onclick=()=>this.readable(this.selected||this.scope?.id);
   document.getElementById('graph-fit').onclick=()=>this.fit();document.getElementById('graph-plus').onclick=()=>this.zoom(1.25);document.getElementById('graph-minus').onclick=()=>this.zoom(.8);
   this.vp.addEventListener('wheel',e=>{e.preventDefault();const b=this.vp.getBoundingClientRect();this.zoom(Math.exp(-e.deltaY*.0015),e.clientX-b.left,e.clientY-b.top)},{passive:false});
   this.vp.addEventListener('pointerdown',e=>{if(e.button!==0)return;this.points.set(e.pointerId,{x:e.clientX,y:e.clientY});this.moved=false;this.drag={x:e.clientX,y:e.clientY,...this.view};if(this.points.size===2){const [a,b]=[...this.points.values()];this.pinch={distance:Math.hypot(a.x-b.x,a.y-b.y),view:{...this.view}}}this.vp.classList.add('dragging')});
   this.vp.addEventListener('pointermove',e=>{if(!this.points.has(e.pointerId))return;this.points.set(e.pointerId,{x:e.clientX,y:e.clientY});if(this.points.size===2&&this.pinch){const [a,b]=[...this.points.values()],box=this.vp.getBoundingClientRect();this.view={...this.pinch.view};this.zoom(Math.hypot(a.x-b.x,a.y-b.y)/Math.max(1,this.pinch.distance),(a.x+b.x)/2-box.left,(a.y+b.y)/2-box.top);this.moved=true;this.vp.setPointerCapture(e.pointerId);return;}if(this.drag){const dx=e.clientX-this.drag.x,dy=e.clientY-this.drag.y;if(Math.abs(dx)+Math.abs(dy)>5){this.moved=true;this.vp.setPointerCapture(e.pointerId)}this.view={scale:this.drag.scale,tx:this.drag.tx+dx,ty:this.drag.ty+dy};this.apply()}});
   const end=e=>{this.points.delete(e.pointerId);this.pinch=null;this.drag=null;if(this.vp.hasPointerCapture(e.pointerId))this.vp.releasePointerCapture(e.pointerId);this.vp.classList.remove('dragging')};this.vp.addEventListener('pointerup',end);this.vp.addEventListener('pointercancel',end);
  }
 }
 root.PlotGraph=PlotGraph;
})(globalThis);
