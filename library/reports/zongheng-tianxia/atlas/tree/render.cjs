// 与超级骷髅兵一致：实际浏览器渲染SVG，并验证同一张图的离线交互。
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {pathToFileURL}=require('node:url');
const {chromium}=require('playwright');
const dir=__dirname,m=JSON.parse(fs.readFileSync(path.join(dir,'manifest.json'),'utf8'));
(async()=>{
 const browser=await chromium.launch({headless:true,...(process.env.PLOT_BROWSER_EXE?{executablePath:process.env.PLOT_BROWSER_EXE}:{})});
 try{
  const page=await browser.newPage({viewport:{width:m.width,height:1200},deviceScaleFactor:1});
  const errors=[],requests=[];page.on('pageerror',e=>errors.push(String(e)));page.on('request',r=>{if(/^https?:/.test(r.url()))requests.push(r.url())});
  await page.goto(pathToFileURL(path.join(dir,'tree.svg')).href);await page.evaluate(()=>document.fonts.ready);
  const layout=await page.evaluate(m=>{
   const texts=[...document.querySelectorAll('text')];
   const overflow=texts.flatMap(e=>{const b=e.getBBox();return b.x<Number(e.dataset.left)-2||b.x+b.width>Number(e.dataset.right)+2||b.y+b.height>Number(e.dataset.bottom)+2?[e.textContent]:[];});
   const cards=Object.entries(m.positions),overlaps=[];
   for(let i=0;i<cards.length;i++)for(let j=i+1;j<cards.length;j++){
    const [ai,a]=cards[i],[bi,b]=cards[j];if(a.x<b.x+b.width-1&&b.x<a.x+a.width-1&&a.y<b.y+b.height-1&&b.y<a.y+a.height-1)overlaps.push([ai,bi]);
   }
   const pierced=[];
   for(const g of document.querySelectorAll('[data-kind=edge],[data-kind=annotation],[data-kind=reading-order]')){
    for(const p of g.querySelectorAll('path:not([stroke=transparent])')){
     const len=p.getTotalLength();for(let k=4;k<len;k+=7){const q=p.getPointAtLength(k);for(const [id,b] of cards){if(id===g.dataset.from||id===g.dataset.to)continue;if(q.x>b.x+3&&q.x<b.x+b.width-3&&q.y>b.y+3&&q.y<b.y+b.height-3){pierced.push([g.id,id]);k=len;break;}}}
    }
   }
   return {texts:texts.length,overflow,overlaps,pierced};
  },m);
  fs.writeFileSync(path.join(dir,'layout-check.json'),JSON.stringify(layout,null,2)+'\n');
  assert.deepEqual(layout.overflow,[],'文字溢出');assert.deepEqual(layout.overlaps,[],'卡片重叠');assert.deepEqual(layout.pierced,[],'关系穿过无关卡片');
  await page.locator('svg').screenshot({path:path.join(dir,'tree.png'),timeout:60000});
  await page.setViewportSize({width:1800,height:1600});
  await page.evaluate(m=>{document.documentElement.style.width='1800px';document.documentElement.style.height=(1800*m.height/m.width)+'px'},m);
  await page.locator('svg').screenshot({path:path.join(dir,'tree-preview.png'),timeout:60000});
  const selected=['v8-v08-sacrifice','v8-v08-cleanse','v8-v08-endbattle','v8-v08-wsl','v8-v08-durability'].map(id=>m.positions[id]);
  const cx=Math.min(...selected.map(p=>p.x))-100,cy=Math.min(...selected.map(p=>p.y))-120;
  const crop={x:Math.max(0,cx),y:Math.max(0,cy),width:Math.max(...selected.map(p=>p.x+p.width))-cx+100,height:Math.max(...selected.map(p=>p.y+p.height))-cy+120};
  const cropHeight=Math.ceil(crop.height*1800/crop.width);
  await page.setViewportSize({width:1800,height:cropHeight});
  await page.evaluate(c=>{const s=document.documentElement;s.setAttribute('viewBox',`${c.x} ${c.y} ${c.width} ${c.height}`);s.style.width='1800px';s.style.height=(c.height*1800/c.width)+'px'},crop);
  await page.locator('svg').screenshot({path:path.join(dir,'tree-junction-preview.png'),timeout:60000});
  // 第二个相同坐标窗口：开篇主干分枝，而非另绘一张小流程图。
  const opening={x:Math.max(0,m.positions['v1-gift'].x-600),y:Math.max(0,m.positions['v1-gift'].y-280),width:1800,height:1550};
  await page.setViewportSize({width:1800,height:1550});
  await page.evaluate(c=>{const s=document.documentElement;s.setAttribute('viewBox',`${c.x} ${c.y} ${c.width} ${c.height}`);s.style.width='1800px';s.style.height='1550px'},opening);
  await page.locator('svg').screenshot({path:path.join(dir,'tree-opening-preview.png'),timeout:60000});
  await page.setViewportSize({width:1600,height:1050});
  await page.goto(pathToFileURL(path.join(dir,'index.html')).href);await page.evaluate(()=>document.fonts.ready);
  const [download]=await Promise.all([page.waitForEvent('download'),page.click('#save-svg')]);
  const exported=fs.readFileSync(await download.path(),'utf8');assert.match(exported,/xmlns="http:\/\/www.w3.org\/2000\/svg"/);
  assert.equal((exported.match(/data-kind="event"/g)||[]).length,m.events.length);
  assert.equal(await page.locator('[data-kind=event]').count(),m.events.length);
  assert.equal(await page.locator('[data-kind=edge]').count(),m.edges.length);
  assert.equal(await page.locator('[data-kind=reading-order]').count(),30);
  assert.equal(await page.locator('[data-kind=thread]').count(),7);
  await page.fill('#search','安妮');await page.click('#find');assert.match(await page.locator('#detail-narrative').innerText(),/安妮/);await page.click('#evidence-section summary');assert.match(await page.locator('#detail-evidence').innerText(),/ch-/);
  await page.evaluate(()=>select('v8-v08-bloodroar',true));
  await page.locator('#v8-v08-bloodroar rect').first().click();
  await page.click('#evidence-section summary');
  assert.match(await page.locator('#detail-evidence').innerText(),/ch-/);assert.ok(await page.locator('#neighbors button').count()>0);
  await page.screenshot({path:path.join(dir,'browser-event-evidence.png')});
  const title=await page.locator('#detail-title').innerText();await page.locator('#neighbors button').first().click();assert.notEqual(await page.locator('#detail-title').innerText(),title);
  await page.selectOption('#branch','editorial-hidden-annie');assert.match(await page.locator('#detail-label').innerText(),/已回收/);
  await page.selectOption('#branch','editorial-hidden-mentor');assert.match(await page.locator('#detail-label').innerText(),/已回收/);
  await page.evaluate(()=>select('editorial-mentor-identity',true));
  await page.locator('#editorial-mentor-identity').focus();await page.keyboard.press('Enter');
  assert.match(await page.locator('#detail-label').innerText(),/editorial-mentor-missing → v8-v08-bloodroar/);
  await page.click('#threads');assert.match(await page.locator('#notice').innerText(),/3条已回收、4条部分回收/);
  assert.equal(await page.locator('[data-kind=thread]:not(.dim)').count(),7);
  await page.click('#junctions');assert.equal(await page.locator('[data-kind=event]:not(.dim)').count(),m.junctions.length);
  await page.selectOption('#volume','8');assert.equal(await page.locator('[data-kind=event]:not(.dim)').count(),m.events.filter(id=>m.positions[id].volume===8).length);
  await page.click('#mainline');assert.match(await page.locator('#detail-title').innerText(),/谋生到组织与龙域责任/);
  assert.equal(await page.locator('[data-kind=event]:not(.dim)').count(),31);
  assert.equal(await page.locator('[data-kind=reading-order]:not(.dim)').count(),30);
  await page.evaluate(()=>select('reading-order-01',true));assert.match(await page.locator('#detail-label').innerText(),/不表示因果/);
  await page.click('#clear');assert.equal(await page.locator('.dim').count(),0);await page.click('#close');await page.click('#fit');
  const before=await page.locator('#canvas').getAttribute('style');await page.click('#plus');assert.notEqual(await page.locator('#canvas').getAttribute('style'),before);
  const panBefore=await page.locator('#canvas').getAttribute('style'),box=await page.locator('#viewport').boundingBox();
  await page.mouse.move(box.x+12,box.y+12);await page.mouse.down();await page.mouse.move(box.x+112,box.y+65,{steps:5});await page.mouse.up();assert.notEqual(await page.locator('#canvas').getAttribute('style'),panBefore);
  await page.click('#fit');await page.screenshot({path:path.join(dir,'browser-overview.png')});
  await page.goto(pathToFileURL(path.join(dir,'index.html')).href+'#v8-v08-bloodroar');await page.evaluate(()=>document.fonts.ready);
  assert.equal(await page.locator('#v8-v08-bloodroar.selected').count(),1);assert.match(await page.locator('#detail-title').innerText(),/明宇/);
  await page.goto(pathToFileURL(path.join(dir,'index.html')).href+'#v1-gift');
  await page.evaluate(()=>document.fonts.ready);
  const snowDossier=page.locator('#neighbors a[href="../characters/character-arc-02.md"]');
  assert.equal(await snowDossier.count(),1);assert.match(await snowDossier.innerText(),/凌雪/);
  assert.ok(fs.existsSync(path.resolve(dir,await snowDossier.getAttribute('href'))));
  await page.goto(pathToFileURL(path.join(dir,'index.html')).href+'#v8-v08-sacrifice');
  await page.evaluate(()=>document.fonts.ready);
  assert.equal(await page.locator('#neighbors a[href="../characters/character-arc-07.md"]').count(),1);
  assert.deepEqual(errors,[]);assert.deepEqual(requests,[]);
  const result={images:['tree.png','tree-preview.png','tree-junction-preview.png','tree-opening-preview.png'],dimensions:{width:m.width,height:m.height},svg_text_lines:layout.texts,text_overflow:0,node_overlap:0,edges_through_unrelated_nodes:0,event_cards:m.events.length,edges:m.edges.length,display_reading_order_links:30,whole_book_threads:7,terminal_states:m.states,external_requests:0,javascript_errors:0,browser_checks:['standalone SVG download','event click and chapter-line evidence','neighbor navigation','search','Annie resolved','Mingyu resolved','edge keyboard and original direction','terminal states','junction focus','volume locator','31 main reading nodes','30 display reading-order links explicitly non-causal','clear','zoom','pan','event ID deep link'],preview_crops:{junction:crop,opening}};
  result.browser_checks.push('event-to-character dossier links');
  fs.writeFileSync(path.join(dir,'browser-check.json'),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result));
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
