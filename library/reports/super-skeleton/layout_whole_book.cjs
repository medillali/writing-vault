// 只计算关系拓扑坐标；中文换行与图片样式由 Python 生成器处理。
const fs=require('node:fs'),path=require('node:path');
const {instance}=require(process.env.VIZ_MODULE||'@viz-js/viz');
const dir=path.join(__dirname,'reading','plot','whole-book');
(async()=>{
 const viz=await instance();
 const result=viz.renderJSON(JSON.parse(fs.readFileSync(path.join(dir,'layout-input.json'),'utf8')));
 fs.writeFileSync(path.join(dir,'layout.json'),JSON.stringify({engine:'Graphviz dot',version:viz.graphvizVersion,...result},null,2)+'\n');
 console.log(JSON.stringify({bounds:result.bb,nodes:result.objects.length,edges:result.edges.length}));
})().catch(e=>{console.error(e);process.exitCode=1});
