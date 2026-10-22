// 渲染全书拓扑图，检查文字、节点遮挡及离线阅读交互。
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {pathToFileURL}=require('node:url');
const {chromium}=require('playwright');
const dir=path.join(__dirname,'reading','plot','whole-book');
const m=JSON.parse(fs.readFileSync(path.join(dir,'manifest.json'),'utf8'));
(async()=>{
 const browser=await chromium.launch({headless:true,...(process.env.PLOT_BROWSER_EXE?{executablePath:process.env.PLOT_BROWSER_EXE}:process.env.PLOT_BROWSER_CHANNEL?{channel:process.env.PLOT_BROWSER_CHANNEL}:{})});
 try{
  const page=await browser.newPage({viewport:{width:m.width,height:1200},deviceScaleFactor:1});
  const errors=[];page.on('pageerror',e=>errors.push(String(e)));
  await page.goto(pathToFileURL(path.join(dir,'tree.svg')).href);await page.evaluate(()=>document.fonts.ready);
  const layout=await page.evaluate(m=>{
   const texts=[...document.querySelectorAll('text')];
   const overflow=texts.flatMap(e=>{const b=e.getBBox();return b.x<Number(e.dataset.left)-2||b.x+b.width>Number(e.dataset.right)+2||b.y+b.height>Number(e.dataset.bottom)+2?[e.textContent]:[];});
   const cards=Object.entries(m.positions),overlaps=[];
   for(let i=0;i<cards.length;i++)for(let j=i+1;j<cards.length;j++){
    const [ai,a]=cards[i],[bi,b]=cards[j];if(a.x<b.x+b.width-1&&b.x<a.x+a.width-1&&a.y<b.y+b.height-1&&b.y<a.y+a.height-1)overlaps.push([ai,bi]);
   }
   const pierced=[];
   for(const g of document.querySelectorAll('[data-kind=edge],[data-kind=annotation]')){
    for(const p of g.querySelectorAll('path:not([stroke=transparent])')){
     const len=p.getTotalLength();for(let k=4;k<len;k+=10){const q=p.getPointAtLength(k);for(const [id,b] of cards){if(id===g.dataset.from||id===g.dataset.to)continue;if(q.x>b.x+3&&q.x<b.x+b.width-3&&q.y>b.y+3&&q.y<b.y+b.height-3){pierced.push([g.id,id]);k=len;break;}}}
    }
   }
   return {texts:texts.length,overflow,overlaps,pierced};
  },m);
  assert.deepEqual(layout.overflow,[]);assert.deepEqual(layout.overlaps,[]);assert.deepEqual(layout.pierced,[]);
  await page.locator('svg').screenshot({path:path.join(dir,'tree.png'),timeout:60000});
  await page.setViewportSize({width:2600,height:1600});
  await page.evaluate(()=>{document.documentElement.style.width='2600px';document.documentElement.style.height='auto'});
  await page.locator('svg').screenshot({path:path.join(dir,'tree-preview.png'),timeout:60000});
  // 同一张图的局部取景，展示独立起点接入主线与继续分枝。
  await page.setViewportSize({width:1800,height:1400});
  await page.evaluate(()=>{const s=document.documentElement;s.setAttribute('viewBox','2200 2630 2000 1560');s.style.width='1800px';s.style.height='1404px';});
  await page.locator('svg').screenshot({path:path.join(dir,'tree-junction-preview.png'),timeout:60000});
  await page.setViewportSize({width:1600,height:1050});
  const requests=[];page.on('request',r=>{if(/^https?:/.test(r.url()))requests.push(r.url())});
  await page.goto(pathToFileURL(path.join(dir,'index.html')).href);await page.evaluate(()=>document.fonts.ready);
  const [download]=await Promise.all([page.waitForEvent('download'),page.click('#save-svg')]);
  const exported=fs.readFileSync(await download.path(),'utf8');
  assert.match(exported,/xmlns="http:\/\/www.w3.org\/2000\/svg"/);
  assert.equal((exported.match(/data-kind="event"/g)||[]).length,163);
  assert.equal(await page.locator('[data-kind=event]').count(),163);
  assert.equal(await page.locator('[data-kind=edge]').count(),265);
  assert.equal(await page.locator('[data-kind=thread]').count(),15);
  assert.equal(await page.locator('#branch option').count(),47);
  await page.fill('#search','本源真相');await page.click('#find');
  await page.locator('#v18-e07 rect').first().click();
  assert.equal(await page.locator('#detail-title').innerText(),'本源真相与创造者死亡');
  assert.match(await page.locator('#detail-evidence').innerText(),/ch-0202/);
  assert.ok(await page.locator('#neighbors button').count()>=3);
  await page.screenshot({path:path.join(__dirname,'validation','whole-book-event.png')});
  await page.locator('#neighbors button').first().click();
  assert.notEqual(await page.locator('#detail-title').innerText(),'本源真相与创造者死亡');
  await page.selectOption('#branch','book-6e1451b9badd');
  assert.match(await page.locator('#detail-label').innerText(),/未回收/);
  assert.equal(await page.locator('#v04-e04.dim').count(),0);
  assert.equal(await page.locator('#cross-roder-01.dim').count(),0);
  assert.ok(await page.locator('[data-kind=event].dim').count()>0);
  // 点选线条本身，核验原方向与语义，键盘同样可访问。
  await page.locator('#cross-roder-01').focus();await page.keyboard.press('Enter');
  assert.match(await page.locator('#detail-title').innerText(),/揭示/);
  assert.match(await page.locator('#detail-label').innerText(),/v04-e04 → v05-e05/);
  await page.selectOption('#branch','book-67592e865ba5');
  assert.equal(await page.locator('#v11-e02.dim').count(),0);
  assert.equal(await page.locator('#v11-e02').count(),1);
  await page.click('#mainline');assert.match(await page.locator('#detail-title').innerText(),/自由存在/);
  await page.click('#threads');assert.match(await page.locator('#notice').innerText(),/11条部分回收、3条未回收/);
  assert.equal(await page.locator('[data-kind=thread]:not(.dim)').count(),14);
  await page.click('#junctions');assert.equal(await page.locator('[data-kind=event]:not(.dim)').count(),m.junctions.length);
  await page.selectOption('#volume','18');assert.equal(await page.locator('[data-kind=event]:not(.dim)').count(),9);
  await page.fill('#search','罗得');await page.click('#find');assert.match(await page.locator('#detail-title').innerText(),/罗得/);
  await page.click('#clear');assert.equal(await page.locator('.dim').count(),0);
  await page.click('#close');await page.click('#fit');
  const before=await page.locator('#canvas').getAttribute('style');await page.click('#plus');assert.notEqual(await page.locator('#canvas').getAttribute('style'),before);
  const panBefore=await page.locator('#canvas').getAttribute('style');const box=await page.locator('#viewport').boundingBox();
  await page.mouse.move(box.x+12,box.y+12);await page.mouse.down();await page.mouse.move(box.x+112,box.y+65,{steps:5});await page.mouse.up();
  assert.notEqual(await page.locator('#canvas').getAttribute('style'),panBefore);
  await page.click('#fit');await page.screenshot({path:path.join(__dirname,'validation','whole-book-overview.png')});
  assert.deepEqual(errors,[]);assert.deepEqual(requests,[]);
  const result={images:['tree.png','tree-preview.png','tree-junction-preview.png'],svg_text_lines:layout.texts,text_overflow:0,node_overlap:0,edges_through_unrelated_nodes:0,event_cards:163,edges:265,hidden_threads:15,thread_choices:46,
   browser_checks:['standalone SVG download','event click and evidence','neighbor navigation','search','thread highlighting','edge keyboard details','shared junction node identity','mainline focus','unresolved status focus','junction focus','volume focus','clear highlighting','zoom','pan'],external_requests:0,javascript_errors:0};
  fs.writeFileSync(path.join(__dirname,'validation','whole-book-browser.json'),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result));
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
