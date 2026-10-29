// 预先布局各阶段和剧情线，离线浏览器只负责显示，不依赖网络或布局运行时。
const fs=require('node:fs'),path=require('node:path');
const {instance}=require(process.env.VIZ_MODULE||'@viz-js/viz');
const {createModel}=require('./reader/model.js');
const dir=path.join(__dirname,'reading/plot/reader'),data=JSON.parse(fs.readFileSync(path.join(dir,'data.json'),'utf8')),model=createModel(data);
(async()=>{
 const viz=await instance(),scopes={};
 const wanted=[...data.stages.map(s=>({kind:'stage',id:s.id})),...data.threads.map(t=>({kind:'thread',id:t.id}))];
 for(const scope of wanted){
  const ids=model.scopeIds(scope),set=new Set(ids),edges=data.edges.filter(e=>set.has(e.from)&&set.has(e.to));
  const raw=viz.renderJSON({directed:true,graphAttributes:{rankdir:'TB',ranksep:'.75',nodesep:'.5',splines:'spline'},nodeAttributes:{shape:'box',label:'',width:4.4,height:2.12,fixedsize:true},nodes:ids.map(id=>({name:id})),edges:edges.map(e=>({tail:e.from,head:e.to,attributes:{id:e.id,weight:e.kind==='cause'?4:1,constraint:e.kind!=='echo'&&model.nodes[e.from].narrative_order<model.nodes[e.to].narrative_order}}))});
  const [,,w,h]=raw.bb.split(',').map(Number),positions={},paths={};
  for(const n of raw.objects){const [x,y]=n.pos.split(',').map(Number);positions[n.name]={x:x-158.5+35,y:h-y-76.5+35,w:317,h:153};}
  for(const e of raw.edges||[]){paths[e.id]=(e._draw_||[]).filter(x=>x.op==='b').map(d=>{const pts=d.points.map(([x,y])=>[x+35,h-y+35]);return 'M '+pts[0].join(',')+' C '+pts.slice(1).map(p=>p.join(',')).join(' ')}).join(' ');}
  scopes[scope.kind+':'+scope.id]={width:w+70,height:h+70,positions,paths};
 }
 fs.writeFileSync(path.join(dir,'layouts.json'),JSON.stringify({revision:data.revision,engine:viz.graphvizVersion,scopes},null,2)+'\n');console.log(JSON.stringify({scopes:Object.keys(scopes).length,engine:viz.graphvizVersion}));
})().catch(e=>{console.error(e);process.exitCode=1});
