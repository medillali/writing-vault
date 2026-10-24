// 为本批研究产物验证离线图、文字布局和地图交互。
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {pathToFileURL}=require('node:url'),{chromium}=require('playwright');
const root=process.argv[2],mode=process.argv[3];
(async()=>{const browser=await chromium.launch({headless:true,channel:'chrome'});try{
 for(const folder of (process.argv.slice(4).length?process.argv.slice(4):['zeidan','leveling'])){
  const dir=path.join(root,folder),whole=path.join(dir,'plot','whole-book'),m=JSON.parse(fs.readFileSync(path.join(whole,'manifest.json'),'utf8'));
  const page=await browser.newPage({viewport:{width:1500,height:1000},deviceScaleFactor:1});const errors=[],network=[];page.on('pageerror',e=>errors.push(String(e)));page.on('request',r=>{if(/^https?:/.test(r.url()))network.push(r.url())});
  if(mode==='svg'){
   await page.goto(pathToFileURL(path.join(whole,'tree.svg')).href);await page.evaluate(()=>document.fonts.ready);
   const layout=await page.evaluate(m=>{
    const overflow=[...document.querySelectorAll('text')].flatMap(t=>{const b=t.getBBox();return b.x+b.width>Number(t.dataset.right)+2||b.y+b.height>Number(t.dataset.bottom)+2?[t.textContent]:[]});
    const ps=Object.entries(m.positions),overlaps=[];for(let i=0;i<ps.length;i++)for(let j=i+1;j<ps.length;j++){const[a,p]=ps[i],[b,q]=ps[j];if(p.x<q.x+q.width&&q.x<p.x+p.width&&p.y<q.y+q.height&&q.y<p.y+p.height)overlaps.push([a,b])}
    const pierced=[];for(const e of document.querySelectorAll('[data-kind=edge]')){const p=e.querySelector('path'),len=p.getTotalLength();for(let i=3;i<len;i+=12){const q=p.getPointAtLength(i);for(const[id,b]of ps){if(id===e.dataset.from||id===e.dataset.to)continue;if(q.x>b.x+3&&q.x<b.x+b.width-3&&q.y>b.y+3&&q.y<b.y+b.height-3){pierced.push([e.id,id]);i=len;break}}}}
    const outsideCards=[];for(const g of document.querySelectorAll('[data-kind]:not([data-kind=edge])')){const r=g.querySelector('rect');if(!r)continue;const rb=r.getBBox();for(const t of g.querySelectorAll('text')){const b=t.getBBox();if(b.x<rb.x+8||b.x+b.width>rb.x+rb.width-8||b.y<rb.y+5||b.y+b.height>rb.y+rb.height-5)outsideCards.push([g.id,t.textContent])}}
    return{overflow,overlaps,pierced,outsideCards};
   },m);assert.deepEqual(layout.overflow,[]);assert.deepEqual(layout.overlaps,[]);assert.deepEqual(layout.pierced,[]);assert.deepEqual(layout.outsideCards,[]);
   await page.locator('svg').screenshot({path:path.join(whole,'tree.png'),timeout:60000});
   await page.evaluate(()=>{document.documentElement.style.width='1800px';document.documentElement.style.height='auto'});await page.locator('svg').screenshot({path:path.join(whole,'tree-preview.png'),timeout:60000});
   const result={valid:true,node_overlap:0,text_overflow:0,relations_through_unrelated_nodes:0,...m,nodes:undefined,positions:undefined};fs.mkdirSync(path.join(dir,'validation'),{recursive:true});fs.writeFileSync(path.join(dir,'validation','diagram-layout.json'),JSON.stringify(result,null,2)+'\n');
  }else{
   await page.goto(pathToFileURL(path.join(dir,'plot','map','index.html')).href);await page.waitForFunction(()=>document.body.dataset.ready==='true');
   assert.equal(await page.locator('#map-location option').count(),m.stages+1);await page.selectOption('#map-location',String(m.stages));await page.waitForTimeout(400);
   const before=await page.evaluate(()=>window.plotMap.viewport.getZoom());await page.click('#zoom-in');await page.waitForTimeout(400);assert.ok(await page.evaluate(()=>window.plotMap.viewport.getZoom())>before);
   await page.click('#map-home');await page.click('#map-read');await page.click('#focus-mode');assert.ok(await page.locator('body.focused').count());await page.keyboard.press('Escape');assert.equal(await page.locator('body.focused').count(),0);
   await page.screenshot({path:path.join(dir,'validation','map-desktop.png')});
   await page.setViewportSize({width:390,height:844});await page.click('#map-home');await page.click('#map-read');await page.screenshot({path:path.join(dir,'validation','map-mobile.png')});assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
   await page.goto(pathToFileURL(path.join(dir,'plot','relations','index.html')).href);const g=JSON.parse(fs.readFileSync(path.join(dir,'plot','graph.json'),'utf8'));await page.selectOption('#section',g.nodes.find(n=>n.kind==='arc').id);
   const first=g.nodes.find(n=>n.kind==='scene');await page.locator('#tree-canvas [data-node="'+first.id+'"]').click();assert.equal(await page.locator('#detail-title').innerText(),first.title);assert.match(await page.locator('#details').innerText(),/chapter_id/);
   if(g.threads.length){await page.selectOption('#section','');await page.selectOption('#thread',g.threads[0].id);assert.equal(await page.locator('#detail-title').innerText(),g.threads[0].title)}
   assert.deepEqual(errors,[]);assert.deepEqual(network,[]);fs.writeFileSync(path.join(dir,'validation','browser.json'),JSON.stringify({valid:true,offline_external_requests:network.length,javascript_errors:errors.length,desktop:true,mobile_width:390,checks:['地图载入','阶段定位','缩放','专注退出','手机无横溢','节点详情与证据','剧情线筛选']},null,2)+'\n');
  }
  console.log(JSON.stringify({folder,mode,valid:true}));await page.close();
 }
}finally{await browser.close()}})().catch(e=>{console.error(e);process.exitCode=1});
