const {chromium}=require('C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const {pathToFileURL}=require('node:url');const url=pathToFileURL('C:/Users/Administrator/Documents/ChatGPT/Novel/writing-vault/library/reports/super-skeleton/reading/plot/reader/index.html').href;
(async()=>{const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});try{
const p=await browser.newPage({viewport:{width:1440,height:1000}});await p.goto(url);await p.waitForFunction(()=>document.body.dataset.ready==='true');
for(const selector of ['#map','#map .openseadragon-canvas','#map-read']){
 await p.click('#map-read');await p.waitForTimeout(500);await p.locator(selector).focus();
 const before=await p.evaluate(()=>({z:plotMap.viewport.getZoom(true),y:plotMap.viewport.getCenter(true).y}));
 await p.keyboard.press('Equal');await p.waitForTimeout(900);await p.keyboard.press('ArrowDown');await p.waitForTimeout(500);
 console.log(selector,await p.evaluate(b=>({factor:plotMap.viewport.getZoom(true)/b.z,yChange:plotMap.viewport.getCenter(true).y-b.y}),before));
}
for(const v of ['1','9','18']){await p.selectOption('#map-location',v);await p.waitForTimeout(600);console.log('locate',v,await p.evaluate(n=>{const v=MAP_DATA.volumes.find(v=>String(v.number)===n),c=plotMap.viewport.viewportToImageCoordinates(plotMap.viewport.getCenter(true));return{expected:[v.x+v.width/2,v.y+v.height/2],actual:[c.x,c.y],error:document.getElementById('map-error').hidden===false}},v));}
await p.setViewportSize({width:320,height:480});await p.locator('#map-more summary').click();console.log('small',await p.evaluate(()=>({page:document.documentElement.scrollWidth,win:innerWidth,actions:[...document.querySelectorAll('.header-actions button,.header-actions summary,.header-actions select,.menu a')].map(e=>({text:e.textContent,rect:e.getBoundingClientRect().toJSON()}))})));
}finally{await browser.close()}})().catch(e=>{console.error(e);process.exitCode=1});
