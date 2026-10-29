const {chromium}=require('C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('node:fs'),crypto=require('node:crypto');
const root='C:/Users/Administrator/Documents/ChatGPT/Novel/writing-vault/library/reports/super-skeleton';
const {pathToFileURL}=require('node:url');
const url=pathToFileURL(root+'/reading/plot/reader/index.html').href;
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
 try{
  const c=await browser.newContext({viewport:{width:1440,height:1000},acceptDownloads:true});
  const p=await c.newPage(); const errors=[];p.on('pageerror',e=>errors.push(String(e)));
  await p.goto(url);await p.waitForFunction(()=>document.body.dataset.ready==='true');
  await p.click('#map-read');await p.waitForTimeout(600);
  const state=()=>p.evaluate(()=>({imageZoom:plotMap.viewport.viewportToImageZoom(plotMap.viewport.getZoom(true)),zoom:plotMap.viewport.getZoom(true),center:plotMap.viewport.getCenter(true),focus:document.activeElement.id||document.activeElement.className,view:[innerWidth,innerHeight]}));
  console.log('read',await state());
  await p.locator('#map .openseadragon-canvas').focus();await p.keyboard.press('ArrowDown');await p.waitForTimeout(500);console.log('arrow',await state());
  await p.keyboard.press('Equal');await p.waitForTimeout(500);console.log('equal',await state());
  await p.keyboard.press('Minus');await p.waitForTimeout(500);console.log('minus',await state());
  await p.locator('#map-more summary').click();await p.keyboard.press('Escape');console.log('escape',await state());
  for(const type of ['png','svg']){
   await p.locator('#map-more summary').click();const pending=p.waitForEvent('download');await p.locator('#download-'+type).click();const d=await pending;const bytes=fs.readFileSync(await d.path());console.log('download',type,{name:d.suggestedFilename(),failure:await d.failure(),bytes:bytes.length,hash:hash(bytes),source:hash(fs.readFileSync(root+'/reading/plot/whole-book/tree.'+type))});
   await p.keyboard.press('Escape');
  }
  await p.click('#map-read');await p.waitForTimeout(600);const saved=await state();
  await p.setViewportSize({width:720,height:600});await p.reload();await p.waitForFunction(()=>document.body.dataset.ready==='true');await p.waitForTimeout(600);console.log('restore-narrow',{saved,restored:await state()});
  await p.setViewportSize({width:800,height:320});await p.locator('#map-more summary').click();console.log('short-menu',await p.evaluate(()=>({height:innerHeight,menu:document.querySelector('.menu').getBoundingClientRect().toJSON(),lastLink:document.querySelector('.menu a:last-of-type').getBoundingClientRect().toJSON(),lastLinkHit:document.elementFromPoint(680,310)?.outerHTML.slice(0,200)})));
  await p.screenshot({path:'C:/Users/Administrator/Documents/ChatGPT/Novel/distill-novels/work/full_distill/review_map_short.png'});
  console.log('errors',errors);await c.close();
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
