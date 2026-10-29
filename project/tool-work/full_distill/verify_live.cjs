const assert=require('assert');
const fs=require('fs');
const path=require('path');
const {pathToFileURL}=require('url');
const {chromium}=require('C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const vault=path.resolve(__dirname,'../../../writing-vault');
const output=path.join(vault,'library/views/超级骷髅兵全书审查.html');
const n=Number(process.argv[2]);
assert(n>=1&&n<=18);
(async()=>{
 const browser=await chromium.launch({channel:'msedge',headless:true});
 try{
  const page=await browser.newPage({viewport:{width:1440,height:1000}});
  const errors=[],requests=[];
  const readability=[];
  async function checkReadable(label,canvas){
   const sample=await page.locator(canvas+' [data-node]').filter({visible:true}).first().evaluate(el=>{
    const text=el.querySelector('text'),m=text.getScreenCTM();
    return {fontPixels:parseFloat(getComputedStyle(text).fontSize)*Math.hypot(m.a,m.b),canvasWidth:el.closest('svg').getBoundingClientRect().width};
   });
   assert(sample.fontPixels>=12,`${label}: ${sample.fontPixels}px`);
   readability.push({label,...sample});
  }
  page.on('pageerror',e=>errors.push(String(e)));
  page.on('request',r=>{if(/^https?:/i.test(r.url()))requests.push(r.url());});
  await page.goto(pathToFileURL(output).href);
  await page.waitForSelector('[data-ready="true"]');
  assert.equal(await page.locator('[data-volume]').count(),18);
  for(let i=1;i<=18;i++)assert.match(await page.locator(`[data-volume="${i}"]`).innerText(),i<=n?/已完成/:/尚未入库/);
  if(n===18){
   const ledger=JSON.parse(fs.readFileSync(path.join(vault,'library/reports/super-skeleton/question-ledger.json'),'utf8'));
   assert.equal(await page.locator('#question-ledger article.chapter-note').count(),ledger.entries.length);
   assert.equal(await page.locator('#synthesis .dimension-group').count(),9);
   assert(await page.locator('#synthesis .analysis-item').count()>=27);
   await page.locator('#question-ledger > details').first().locator('summary').first().click();
   assert.match(await page.locator('#question-ledger').innerText(),/已有答案/);
   await page.locator('#question-ledger > details').first().locator('summary').first().click();
  }
  const fullCount=await page.locator('#asset-cards .asset-card').count();
  await page.fill('#asset-search','黑龙');
  const filtered=await page.locator('#asset-cards .asset-card').count();
  assert(filtered>0&&filtered<fullCount);
  await page.fill('#asset-search','');
  await page.selectOption('#asset-type','scene');
  assert(await page.locator('#asset-cards .asset-card').count()>0);
  await page.selectOption('#asset-type','');
  await page.selectOption('#asset-volume',String(n));
  assert(await page.locator('#asset-cards .asset-card').count()>0);
  await page.selectOption('#asset-volume','');
  await page.locator('#dimension-evidence details.evidence').first().click();
  assert.match(await page.locator('#dimension-evidence').innerText(),/ch-\d+/);
  await page.evaluate(()=>window.scrollTo(0,0));
  await page.screenshot({path:path.join(__dirname,`live-${String(n).padStart(2,'0')}-desktop.png`)});
  await page.setViewportSize({width:390,height:844});
  await page.evaluate(()=>window.scrollTo(0,0));
  assert(await page.evaluate(()=>document.documentElement.scrollWidth<=document.documentElement.clientWidth));
  await page.screenshot({path:path.join(__dirname,`live-${String(n).padStart(2,'0')}-mobile.png`)});
  if(n===18){
   const section=page.locator('#question-ledger > details').first();
   await section.locator('summary').first().click();
   await section.scrollIntoViewIfNeeded();
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=document.documentElement.clientWidth));
   await page.screenshot({path:path.join(__dirname,'live-18-ledger-mobile.png')});
  }
  const graph=await page.locator('#plot-link').getAttribute('href');
  await page.goto(new URL(graph,pathToFileURL(output)).href);
  assert(await page.locator('#tree-canvas [data-node]').count()>0);
  await checkReadable('mobile-full-tree','#tree-canvas');
  await page.selectOption('#section',`vol-${String(n).padStart(2,'0')}`);
  await page.locator('#tree-canvas [data-node]').filter({visible:true}).last().click();
  assert.notEqual(await page.locator('#detail-title').innerText(),'从一个节点开始');
  await page.click('#network');
  assert(await page.locator('#network-canvas').isVisible());
  await checkReadable('mobile-volume-network','#network-canvas');
  await page.screenshot({path:path.join(__dirname,'live-18-graph-mobile.png')});
  const opts=await page.locator('#thread option').evaluateAll(xs=>xs.map(x=>x.value));
  assert(opts.length>2);
  await page.selectOption('#thread',opts[2]);
  if(n===18){
   const graphData=JSON.parse(await page.locator('#graph-data').textContent());
   const bookThread=graphData.threads.find(t=>t.id.startsWith('book-')&&t.edge_ids.some(id=>id.startsWith('cross-')));
   assert(bookThread);
   await page.selectOption('#section','');
   await page.selectOption('#thread',bookThread.id);
   assert(await page.locator('#network-canvas .relation').filter({visible:true}).count()>0);
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=document.documentElement.clientWidth));
   await page.setViewportSize({width:1440,height:1000});
   await checkReadable('desktop-book-thread','#network-canvas');
   const memberCount=bookThread.node_ids.length;
   assert.equal(await page.locator('#network-canvas [data-node]').filter({visible:true}).count(),memberCount);
   await page.screenshot({path:path.join(__dirname,'live-18-network.png')});
  }
  assert.equal(errors.length,0,errors.join('\n'));
  assert.equal(requests.length,0,requests.join('\n'));
  const result={volumes:n,assets:fullCount,searchMatches:filtered,desktop:true,mobile390:true,graph:true,readability,errors,remoteRequests:requests};
  fs.writeFileSync(path.join(__dirname,`live-${String(n).padStart(2,'0')}-qa.json`),JSON.stringify(result,null,2));
  console.log(JSON.stringify(result,null,2));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
