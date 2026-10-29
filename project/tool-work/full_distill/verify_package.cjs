const assert=require('assert');
const fs=require('fs');
const path=require('path');
const {pathToFileURL}=require('url');
const {chromium}=require('C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{
 const resultPath=path.join(__dirname,'review-package.json');
 const result=JSON.parse(fs.readFileSync(resultPath,'utf8'));
 const browser=await chromium.launch({channel:'msedge',headless:true});
 try{
  const page=await browser.newPage({viewport:{width:390,height:844}});
  const errors=[],requests=[];
  page.on('pageerror',e=>errors.push(String(e)));
  page.on('request',r=>{if(/^https?:/i.test(r.url()))requests.push(r.url());});
  await page.goto(pathToFileURL(result.entry).href);
  assert.equal(await page.locator('.progress-card.complete').count(),18);
  assert.equal(await page.locator('#synthesis .dimension-group').count(),9);
  assert(await page.locator('#question-ledger article').count()>0);
  await page.fill('#asset-search','黑龙');
  assert(await page.locator('#asset-cards .asset-card').count()>0);
  await page.click('#plot-link');
  assert(await page.locator('#tree-canvas [data-node]').count()>0);
  await page.click('#network');
  assert(await page.locator('#network-canvas').isVisible());
  assert.equal(errors.length,0,errors.join('\n'));
  assert.equal(requests.length,0,requests.join('\n'));
  Object.assign(result,{browser_check:'passed',mobile390:true,graph_relative_link:true,errors,remoteRequests:requests});
  fs.writeFileSync(resultPath,JSON.stringify(result,null,2));
  console.log(JSON.stringify(result,null,2));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
