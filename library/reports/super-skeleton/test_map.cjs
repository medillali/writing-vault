const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict'),crypto=require('node:crypto');
const {pathToFileURL}=require('node:url'),{chromium}=require('playwright');
const url=pathToFileURL(path.join(__dirname,'reading/plot/reader/index.html')).href;
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:process.env.PLOT_BROWSER_EXE});
 const errors=[],network=[];
 try{
  for(const mobile of [false,true]){
   const context=await browser.newContext({viewport:mobile?{width:390,height:844}:{width:1440,height:1000},isMobile:mobile,hasTouch:mobile});
   const p=await context.newPage();p.on('pageerror',e=>errors.push(String(e)));p.on('request',r=>{if(/^https?:/.test(r.url()))network.push(r.url())});
   await p.goto(url);assert.equal(await p.locator('#map').count(),1,'默认入口应是整张地图');
   await p.waitForFunction(()=>document.body.dataset.ready==='true');
   await p.waitForFunction(()=>plotMap.world.getItemAt(0).getFullyLoaded());
   assert.equal(await p.locator('#minimap').isVisible(),true);
   assert.equal(await p.evaluate(()=>plotMap.world.getItemCount()),1,'整本书是一张连续图');
   const home=await p.evaluate(()=>plotMap.viewport.getZoom(true));
   await p.click('#zoom-in');await p.waitForFunction(z=>plotMap.viewport.getZoom(true)>z,home);
   await p.click('#map-home');await p.waitForFunction(z=>Math.abs(plotMap.viewport.getZoom(true)-z)<.001,home);
   await p.click('#map-read');await p.waitForFunction(()=>plotMap.viewport.viewportToImageZoom(plotMap.viewport.getZoom(true))>.6);
   if(!mobile){
    const z=await p.evaluate(()=>plotMap.viewport.getZoom(true));await p.mouse.move(700,400);await p.mouse.wheel(0,-180);
    await p.waitForFunction(z=>plotMap.viewport.getZoom(true)>z,z);
    await p.click('#focus-mode');assert.equal(await p.locator('.map-header').isVisible(),false);await p.click('#exit-focus');
    await p.locator('#map').focus();await p.keyboard.press('Escape');
    assert.equal(await p.evaluate(()=>document.activeElement.id),'map','普通画布按Escape不应抢走焦点');
    const keyZoom=await p.evaluate(()=>plotMap.viewport.getZoom(true));await p.locator('#map').focus();await p.keyboard.press('-');
    await p.waitForFunction(z=>plotMap.viewport.getZoom(true)<z,keyZoom);
    await p.click('#map-read');await p.locator('#map .openseadragon-canvas').focus();
    const canvasZoom=await p.evaluate(()=>plotMap.viewport.getZoom(true));await p.keyboard.press('Equal');
    await p.waitForTimeout(600);assert.ok(Math.abs((await p.evaluate(()=>plotMap.viewport.getZoom(true)))/canvasZoom-1.4)<.01,'画布焦点下键盘缩放只处理一次');
    await p.locator('#map-more summary').click();
    for(const ext of ['png','svg']){
     const [download]=await Promise.all([p.waitForEvent('download'),p.click('#download-'+ext)]);
     const actual=fs.readFileSync(await download.path()),expected=fs.readFileSync(path.join(__dirname,'reading/plot/whole-book/tree.'+ext));
     if(ext==='png')assert.deepEqual(crypto.createHash('sha256').update(actual).digest(),crypto.createHash('sha256').update(expected).digest());
     else assert.equal(actual.toString().replaceAll('\r\n','\n'),expected.toString().replaceAll('\r\n','\n'));
    }
    await p.locator('#map-more summary').click();
   }
   const box=await p.locator('#map').boundingBox();
   const before=await p.evaluate(()=>({x:plotMap.viewport.getCenter(true).x,y:plotMap.viewport.getCenter(true).y}));
   if(!mobile){await p.mouse.move(box.x+box.width*.5,box.y+box.height*.55);await p.mouse.down();await p.mouse.move(box.x+box.width*.5-160,box.y+box.height*.55-120,{steps:8});await p.mouse.up();}
   else{
    const cdp=await context.newCDPSession(p),x=190,y=420;
    await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x,y,id:1}]});
    await cdp.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:x-80,y:y-80,id:1}]});
    await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});
    const zoom=await p.evaluate(()=>plotMap.viewport.getZoom(true));
    await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:140,y:400,id:1},{x:230,y:400,id:2}]});
    await cdp.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:100,y:400,id:1},{x:270,y:400,id:2}]});
    await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});
    await p.waitForFunction(z=>plotMap.viewport.getZoom(true)>z*1.2,zoom);
   }
   await p.waitForFunction(b=>Math.abs(plotMap.viewport.getCenter(true).x-b.x)+Math.abs(plotMap.viewport.getCenter(true).y-b.y)>.001,before);
   await p.click('#map-read');await p.waitForFunction(()=>plotMap.world.getItemAt(0).getFullyLoaded());
   await p.screenshot({path:path.join(__dirname,'validation/map-'+(mobile?'mobile':'desktop')+'.png')});
   const mini=await p.locator('#minimap').boundingBox(),previous=await p.evaluate(()=>plotMap.viewport.getCenter(true).y);
   await p.mouse.click(mini.x+mini.width/2,mini.y+mini.height*.8);
   await p.waitForFunction(y=>Math.abs(plotMap.viewport.getCenter(true).y-y)>.02,previous);
   await p.waitForTimeout(500);
   const saved=await p.evaluate(()=>({x:plotMap.viewport.getCenter(true).x,y:plotMap.viewport.getCenter(true).y,z:plotMap.viewport.getZoom(true)}));
   await p.reload();await p.waitForFunction(()=>document.body.dataset.ready==='true');
   await p.waitForFunction(s=>Math.abs(plotMap.viewport.getCenter(true).x-s.x)<.001&&Math.abs(plotMap.viewport.getCenter(true).y-s.y)<.001&&Math.abs(plotMap.viewport.getZoom(true)-s.z)<.001,saved);
   for(const width of mobile?[320,390,768]:[1024,1440]){await p.setViewportSize({width,height:900});assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),true);}
   assert.equal(await p.locator('#map-error').isVisible(),false);
   if(!mobile){
    await p.click('#map-read');const pixelZoom=await p.evaluate(()=>plotMap.viewport.viewportToImageZoom(plotMap.viewport.getZoom(true)));
    await p.close();const narrow=await context.newPage();await narrow.setViewportSize({width:720,height:900});await narrow.goto(url);
    await narrow.waitForFunction(()=>document.body.dataset.ready==='true');
    const restored=await narrow.evaluate(()=>plotMap.viewport.viewportToImageZoom(plotMap.viewport.getZoom(true)));
    assert.ok(Math.abs(restored-pixelZoom)<.01,'换窄窗口后仍保持文字的像素缩放');
   }
   await context.close();
  }
  assert.deepEqual(errors,[]);assert.deepEqual(network,[]);
  fs.writeFileSync(path.join(__dirname,'validation/map-browser.json'),JSON.stringify({desktop:true,mobile_emulation:true,checks:['single whole-book image','zoom and home','readable size','mouse drag','touch drag and pinch','minimap navigation','restore location and zoom','pixel zoom preserved across window widths','Escape preserves canvas focus','keyboard zoom processed once','original PNG and SVG downloads','five viewport widths','offline'],errors,network,physical_phone_verified:false},null,2)+'\n');
  console.log('全图缩放、拖动、缩略导航与位置恢复通过');
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
