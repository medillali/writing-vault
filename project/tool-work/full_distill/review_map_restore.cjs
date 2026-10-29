const {chromium}=require('C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('node:fs');
const root='C:/Users/Administrator/Documents/ChatGPT/Novel/writing-vault/library/reports/super-skeleton';
const {pathToFileURL}=require('node:url');const url=pathToFileURL(root+'/reading/plot/reader/index.html').href;
(async()=>{const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});try{
const c=await browser.newContext({viewport:{width:1440,height:1000}});let p=await c.newPage();
const open=async()=>{await p.goto(url);await p.waitForFunction(()=>document.body.dataset.ready==='true');await p.waitForTimeout(600)};
const state=()=>p.evaluate(()=>({imageZoom:plotMap.viewport.viewportToImageZoom(plotMap.viewport.getZoom(true)),zoom:plotMap.viewport.getZoom(true),center:plotMap.viewport.getCenter(true),storage:localStorage.getItem('plot-map-v1:'+MAP_DATA.source_sha256)}));
await open();await p.click('#map-read');await p.waitForTimeout(600);console.log('before',await state());await p.close();
p=await c.newPage();await p.setViewportSize({width:720,height:600});await open();console.log('reopened',await state());
console.log('svg',await p.evaluate(()=>({equalNormalized:MAP_DATA.svg===null,length:MAP_DATA.svg.length,start:MAP_DATA.svg.slice(0,70)})));
console.log('source-svg',{bytes:fs.readFileSync(root+'/reading/plot/whole-book/tree.svg').length,normalizedBytes:Buffer.byteLength(fs.readFileSync(root+'/reading/plot/whole-book/tree.svg','utf8').replace(/\r\n/g,'\n'))});
await p.selectOption('#map-location','18');await p.waitForTimeout(700);console.log('volume18',await state());
await p.click('#focus-mode');await p.keyboard.press('Escape');console.log('focus-after-escape',await p.evaluate(()=>({focused:document.body.classList.contains('focused'),active:document.activeElement.id})));
await p.locator('#map .openseadragon-canvas').focus();await p.keyboard.press('Escape');console.log('canvas-after-escape',await p.evaluate(()=>({active:document.activeElement.id||document.activeElement.className})));
await p.keyboard.press('ArrowDown');await p.waitForTimeout(500);console.log('after-arrow',await state());
}finally{await browser.close()}})().catch(e=>{console.error(e);process.exitCode=1});
