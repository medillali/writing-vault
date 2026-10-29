// 复用超级骷髅兵的 Viz.js / Graphviz dot 离线布局流程。
const fs=require('node:fs'),path=require('node:path');
const {instance}=require(process.env.VIZ_MODULE||'@viz-js/viz');
(async()=>{
 const viz=await instance();
 const result=viz.renderJSON(JSON.parse(fs.readFileSync(path.join(__dirname,'layout-input.json'),'utf8')));
 fs.writeFileSync(path.join(__dirname,'layout.json'),JSON.stringify({engine:'Graphviz dot',version:viz.graphvizVersion,...result},null,2)+'\n');
 console.log(JSON.stringify({bounds:result.bb,nodes:result.objects.length,edges:result.edges.length}));
})().catch(e=>{console.error(e);process.exitCode=1});
