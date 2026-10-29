const fs=require('node:fs');
const {instance}=require('./package/dist/viz.cjs');
const file='C:/Users/Administrator/Documents/ChatGPT/Novel/writing-vault/library/sources/src-9ff09c395734410b856f77c77a652834/plot-graph.json';
const g=JSON.parse(fs.readFileSync(file,'utf8'));
const nodes=g.nodes.filter(n=>n.kind==='event'), ns=Object.fromEntries(nodes.map(n=>[n.id,n]));
const edges=g.edges.filter(e=>e.kind!=='echo');
const input={directed:true,graphAttributes:{rankdir:'TB',nodesep:'.6',ranksep:'.9',splines:'spline'},nodeAttributes:{shape:'box',fixedsize:true,width:4.7,height:2.3,label:''},nodes:nodes.map(n=>({name:n.id,attributes:{label:n.id}})),edges:edges.map(e=>({tail:e.from,head:e.to,attributes:{id:e.id,weight:e.kind==='cause'?5:1,constraint:ns[e.from].narrative_order<ns[e.to].narrative_order}}))};
(async()=>{const viz=await instance();const out=viz.renderJSON(input);fs.writeFileSync(__dirname+'/trial.json',JSON.stringify(out));fs.writeFileSync(__dirname+'/trial.svg',viz.renderString(input,{format:'svg'}));console.log(JSON.stringify({bb:out.bb,nodes:out.objects.length,edges:out.edges.length,sample:out.edges[0]}));})();
