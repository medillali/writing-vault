// 渲染同一张全书图，并验证离线缩放、定位和详情交互。
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {pathToFileURL}=require('node:url');
const {chromium}=require('playwright');
const dir=path.join(__dirname,'reading','plot','whole-book');
const m=JSON.parse(fs.readFileSync(path.join(dir,'manifest.json'),'utf8'));
(async()=>{
 const browser=await chromium.launch({headless:true,...(process.env.PLOT_BROWSER_CHANNEL?{channel:process.env.PLOT_BROWSER_CHANNEL}:{})});
 try{
  const page=await browser.newPage({viewport:{width:m.width,height:1200},deviceScaleFactor:1});
  const errors=[];page.on('pageerror',e=>errors.push(String(e)));
  await page.goto(pathToFileURL(path.join(dir,'tree.svg')).href);await page.evaluate(()=>document.fonts.ready);
  const layout=await page.evaluate(()=>{
   const texts=[...document.querySelectorAll('text')];
   return {texts:texts.length,overflow:texts.flatMap(e=>{const b=e.getBBox();return b.x<Number(e.dataset.left)-2||b.x+b.width>Number(e.dataset.right)+2||b.y+b.height>Number(e.dataset.bottom)+2?[e.textContent]:[];})};
  });
  assert.deepEqual(layout.overflow,[]);
  await page.locator('svg').screenshot({path:path.join(dir,'tree.png'),timeout:60000});
  await page.setViewportSize({width:2600,height:1600});
  await page.evaluate(()=>{document.documentElement.style.width='2600px';document.documentElement.style.height='auto';});
  await page.locator('svg').screenshot({path:path.join(dir,'tree-preview.png'),timeout:60000});
  // 局部截图仅用于本地验收，避免把完整图缩小后误认为文字可读。
  await page.setViewportSize({width:1500,height:1000});
  const requests=[];page.on('request',r=>{if(/^https?:/.test(r.url()))requests.push(r.url())});
  await page.goto(pathToFileURL(path.join(dir,'index.html')).href);await page.evaluate(()=>document.fonts.ready);
  const [download]=await Promise.all([page.waitForEvent('download'),page.click('#save-svg')]);
  const exported=fs.readFileSync(await download.path(),'utf8');
  assert.match(exported,/xmlns="http:\/\/www.w3.org\/2000\/svg"/);
  assert.equal((exported.match(/data-kind="event"/g)||[]).length,77);
  assert.equal(await page.locator('[data-kind="event"]').count(),77);
  assert.equal(await page.locator('[data-kind="thread"]').count(),15);
  await page.selectOption('#volume','18');
  await page.locator('#v18-e07 rect').click();
  assert.equal(await page.locator('#detail-title').innerText(),'本源真相与创造者死亡');
  assert.match(await page.locator('#detail-evidence').innerText(),/ch-0202/);
  await page.screenshot({path:path.join(__dirname,'validation','whole-book-event.png')});
  await page.fill('#search','罗得');await page.click('#find');
  assert.match(await page.locator('#detail-title').innerText(),/罗得/);
  await page.click('#close');await page.click('#fit');
  await page.locator('#book-6e1451b9badd rect').first().click();
  assert.match(await page.locator('#detail-label').innerText(),/未回收/);
  assert.ok(await page.locator('[data-kind="event"].dim').count()>0);
  await page.click('#clear');assert.equal(await page.locator('.dim').count(),0);
  await page.click('#close');await page.click('#fit');
  await page.locator('#bridge-01 rect').click();assert.match(await page.locator('#detail-title').innerText(),/B01/);
  await page.click('#close');
  const before=await page.locator('#canvas').getAttribute('style');await page.click('#plus');
  assert.notEqual(await page.locator('#canvas').getAttribute('style'),before);
  const panBefore=await page.locator('#canvas').getAttribute('style');
  const box=await page.locator('#viewport').boundingBox();
  await page.mouse.move(box.x+12,box.y+12);await page.mouse.down();await page.mouse.move(box.x+112,box.y+65,{steps:5});await page.mouse.up();
  assert.notEqual(await page.locator('#canvas').getAttribute('style'),panBefore);
  await page.click('#threads');await page.click('#minus');await page.click('#mainline');await page.click('#fit');
  await page.screenshot({path:path.join(__dirname,'validation','whole-book-overview.png')});
  assert.deepEqual(errors,[]);assert.deepEqual(requests,[]);
  const result={images:['tree.png','tree-preview.png'],svg_text_lines:layout.texts,text_overflow:0,event_cards:77,hidden_threads:15,
   browser_checks:['standalone SVG download','event click and evidence','search','thread highlighting and unresolved state','clear highlighting','bridge details','zoom','pan','volume jump','section jump'],external_requests:0,javascript_errors:0};
  fs.writeFileSync(path.join(__dirname,'validation','whole-book-browser.json'),JSON.stringify(result,null,2)+'\n');
  console.log(JSON.stringify(result));
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
