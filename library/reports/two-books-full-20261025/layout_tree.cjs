// 使用与《超级骷髅兵》相同的Graphviz dot布局引擎。
const fs=require('node:fs'),path=require('node:path');
const {instance}=require(process.env.VIZ_MODULE||'@viz-js/viz');
(async()=>{
 const dir=path.join(__dirname,process.argv[2],'plot','whole-book');
 const viz=await instance(),model=JSON.parse(fs.readFileSync(path.join(dir,'layout-input.json'),'utf8'));
 const result=viz.renderJSON(model);
 fs.writeFileSync(path.join(dir,'layout.json'),JSON.stringify({engine:'Graphviz dot',version:viz.graphvizVersion,...result},null,2)+'\n');
})().catch(e=>{console.error(e);process.exitCode=1});
