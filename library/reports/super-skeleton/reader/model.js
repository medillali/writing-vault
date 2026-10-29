(function(root){
 'use strict';
 const copy=value=>JSON.parse(JSON.stringify(value));
 function createModel(data){
  const index=items=>Object.assign(Object.create(null),Object.fromEntries(items.map(item=>[item.id,item])));
  const nodes=index(data.nodes),threads=index(data.threads);
  const stages=index(data.stages),stageByNode=Object.create(null);
  data.stages.forEach(s=>s.node_ids.forEach(id=>stageByNode[id]=s.id));
  const memberships=Object.create(null),incoming=Object.create(null),outgoing=Object.create(null);
  data.nodes.forEach(n=>{memberships[n.id]=[];incoming[n.id]=[];outgoing[n.id]=[]});
  data.threads.forEach(t=>t.node_ids.forEach(id=>{if(memberships[id])memberships[id].push(t.id)}));
  data.edges.forEach(e=>{if(nodes[e.from]&&nodes[e.to]){incoming[e.to].push(e);outgoing[e.from].push(e)}});
  const sort=ids=>[...new Set(ids)].filter(id=>nodes[id]).sort((a,b)=>nodes[a].narrative_order-nodes[b].narrative_order);
  function relations(id){return {incoming:incoming[id]||[],outgoing:outgoing[id]||[],parents:sort((incoming[id]||[]).filter(e=>e.kind!=='echo').map(e=>e.from)),children:sort((outgoing[id]||[]).filter(e=>e.kind!=='echo').map(e=>e.to))};}
  function nearby(id,depth=1){let all=new Set(nodes[id]?[id]:[]),front=[id];for(let i=0;i<Math.min(2,Math.max(0,depth));i++){const next=[];front.forEach(n=>(incoming[n]||[]).concat(outgoing[n]||[]).forEach(e=>{for(const k of [e.from,e.to])if(!all.has(k)){all.add(k);next.push(k)}}));front=next;}return sort(all);}
  function scopeIds(scope){
   if(scope.kind==='stage')return sort(stages[scope.id]?.node_ids||[]).filter(id=>!scope.core||threads[data.core].node_ids.includes(id));
   if(scope.kind==='thread')return sort(threads[scope.id]?.node_ids||[]);
   if(scope.kind==='character')return sort(data.nodes.filter(n=>(n.characters||[]).includes(scope.id)).map(n=>n.id));
   if(scope.kind==='nearby')return nearby(scope.id,scope.depth||1);
   if(scope.kind==='search'){const q=(scope.query||'').trim().toLocaleLowerCase();return q?sort(data.nodes.filter(n=>(n.id+' '+n.title+' '+n.summary+' '+(n.characters||[]).map(id=>data.characters[id]?.name||'').join(' ')).toLocaleLowerCase().includes(q)).map(n=>n.id)):[];}
   if(scope.kind==='junctions')return sort(data.nodes.filter(n=>relations(n.id).parents.length>1).map(n=>n.id));
   return sort(data.nodes.map(n=>n.id));
  }
  function parseProgress(raw){
   if(typeof raw!=='string'||raw.length>100000)throw new Error('进度文件过大或格式不正确');
   let p;try{p=JSON.parse(raw)}catch{throw new Error('进度文件不是有效JSON')}
   if(!p||p.version!==1||p.source_id!==data.source_id||p.revision!==data.revision)throw new Error('这份进度属于另一部书或另一版本，未导入');
   const known=id=>typeof id==='string'&&Object.hasOwn(nodes,id);
   if(!Array.isArray(p.read)||p.read.length>data.nodes.length||p.read.some(id=>!known(id)))throw new Error('进度包含未知事件，未导入');
   if(p.bookmark!==null&&p.bookmark!==undefined&&!known(p.bookmark))throw new Error('阅读位置不是当前书的事件');
   return {version:1,source_id:data.source_id,revision:data.revision,read:[...new Set(p.read)],bookmark:p.bookmark||null};
  }
  return {data,nodes,threads,stages,stageByNode,memberships,relations,nearby,scopeIds,sort,parseProgress};
 }
 class Navigation{
  constructor(state){this.current=copy(state);this.history=[];}
  go(state){this.history.push(copy(this.current));if(this.history.length>40)this.history.shift();this.current=copy(state);}
  back(){if(this.history.length)this.current=this.history.pop();return this.current;}
 }
 const api={createModel,Navigation};if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.PlotModel=api;
})(globalThis);
