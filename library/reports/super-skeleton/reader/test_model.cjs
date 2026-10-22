const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const mod=path.join(__dirname,'model.js');
const api=fs.existsSync(mod)?require(mod):{};
const graph=JSON.parse(fs.readFileSync(path.join(__dirname,'../../../sources/src-9ff09c395734410b856f77c77a652834/plot-graph.json'),'utf8'));
const ranges=[[1,3],[4,6],[7,9],[10,12],[13,15],[16,17],[18,18]];
const data={source_id:'src-test',revision:'rev-test',core:'book-37dd82abc178',nodes:graph.nodes.filter(n=>n.kind==='event'),edges:graph.edges,threads:graph.threads.filter(t=>t.id.startsWith('book-')),stages:ranges.map(([lo,hi],i)=>({id:'stage-'+(i+1),title:'阶段'+(i+1),node_ids:graph.nodes.filter(n=>n.kind==='event'&&+n.id.slice(1,3)>=lo&&+n.id.slice(1,3)<=hi).map(n=>n.id)})),characters:{}};
test('提供共享事件与导航模型',()=>{assert.equal(typeof api.createModel,'function');assert.equal(typeof api.Navigation,'function');});
test('交汇保留全部关系，但同一来路不重复计算',()=>{
 if(!api.createModel)return assert.fail('阅读模型未实现');const m=api.createModel(data),r=m.relations('v10-e05');
 assert.equal(r.incoming.length,2);assert.equal(r.parents.length,1);
 assert.deepEqual(m.relations('v11-e02').incoming.map(e=>e.id).sort(),data.edges.filter(e=>e.to==='v11-e02').map(e=>e.id).sort());
});
test('支线共享事件身份且全部关系可跨范围追溯',()=>{
 if(!api.createModel)return assert.fail('阅读模型未实现');const m=api.createModel(data),scope={kind:'thread',id:'book-67592e865ba5'};
 assert.ok(m.scopeIds(scope).includes('v11-e02'));assert.equal(m.nodes['v11-e02'],data.nodes.find(n=>n.id==='v11-e02'));
 const near=m.nearby('v11-e02',1);assert.ok(near.includes('v10-e04'));assert.equal(near.length,new Set(near).size);
 assert.ok(m.nearby('v11-e02',2).length>near.length);
 assert.equal(m.scopeIds({kind:'search',query:'完全不存在的检索词'}).length,0);
});
test('返回恢复原范围、事件、滚动与图视窗，而非改走剧情前因',()=>{
 if(!api.Navigation)return assert.fail('导航历史未实现');const state={scope:{kind:'stage',id:'stage-4'},selected:'v11-e02',mode:'cards',scroll:721,expanded:['v11-e02'],viewport:{scale:1.1,tx:-123,ty:66}};
 const nav=new api.Navigation(state);nav.go({...state,scope:{kind:'thread',id:'book-67592e865ba5'},scroll:0});nav.go({...nav.current,selected:'v10-e04',scroll:500});
 nav.back();assert.equal(nav.current.scope.kind,'thread');nav.back();assert.deepEqual(nav.current,state);
});
test('进度导入只接受当前来源版本和事件ID，坏数据不影响原状态',()=>{
 if(!api.createModel)return assert.fail('进度校验未实现');const m=api.createModel(data);
 const packet={version:1,source_id:data.source_id,revision:data.revision,read:['v11-e02'],bookmark:'v11-e02'};
 assert.deepEqual(m.parseProgress(JSON.stringify(packet)).read,['v11-e02']);
 for(const bad of ['{',{...packet,source_id:'other'},{...packet,revision:'old'},{...packet,read:['unknown']},{...packet,bookmark:'unknown'},...['constructor','__proto__','toString'].flatMap(id=>[{...packet,read:[id]},{...packet,bookmark:id}]),{...packet,bookmark:['v11-e02']},{...packet,bookmark:{}}])assert.throws(()=>m.parseProgress(typeof bad==='string'?bad:JSON.stringify(bad)));
});
