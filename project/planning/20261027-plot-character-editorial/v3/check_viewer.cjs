// 用实际离线阅读器验证读图路径，不以函数存在代替可用性。
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {pathToFileURL}=require('node:url');
const runtime=path.join(process.env.USERPROFILE,'.cache/codex-runtimes/codex-primary-runtime/dependencies');
const {chromium}=require(path.join(runtime,'node/node_modules/playwright'));
const root=path.resolve(__dirname,'../../..');
const dir=path.join(root,'writing-vault/library/reports/zongheng-tianxia/atlas/tree');
const url=pathToFileURL(path.join(dir,'index.html')).href;
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:path.join(process.env.LOCALAPPDATA,'ms-playwright/chromium_headless_shell-1228/chrome-headless-shell-win64/chrome-headless-shell.exe')});
 const context=await browser.newContext({viewport:{width:1600,height:1000}}),page=await context.newPage();
 page.setDefaultTimeout(4000);
 const errors=[],requests=[],results=[];
 page.on('pageerror',e=>errors.push(String(e)));page.on('request',r=>{if(/^https?:/.test(r.url()))requests.push(r.url())});
 async function check(name,fn){try{await fn();results.push({name,pass:true})}catch(e){results.push({name,pass:false,error:String(e.message).slice(0,500)})}}
 try{
  await page.goto(url);await page.evaluate(()=>document.fonts.ready);
  await check('主干从第1步开始，下一步解释处境、行动与变化',async()=>{
   assert.equal(await page.locator('#guide-start').count(),1,'缺少开始主干阅读入口');
   await page.click('#guide-start');assert.match(await page.locator('#reading-progress').innerText(),/1\s*\/\s*31/);
   assert.match(await page.locator('#detail-narrative').innerText(),/失业/);
   await page.click('#guide-next');assert.match(await page.locator('#reading-progress').innerText(),/2\s*\/\s*31/);
   assert.match(await page.locator('#detail-title').innerText(),/工作/);
  });
  await check('目录完整列出31步和7条全书线，末步仍保留未醒边界',async()=>{
   assert.equal(await page.locator('#guide-list [data-event]').count(),31,'主干目录缺失');
   assert.equal(await page.locator('#whole-thread-list button').count(),7);
   await page.selectOption('#guide-select','v8-v08-after');
   assert.match(await page.locator('#detail-narrative').innerText(),/无法确认苏醒/);
   assert.equal(await page.locator('#guide-next').isDisabled(),true);
  });
  await check('按人物检索，结果清单能定位同图事件',async()=>{
   await page.fill('#search','冰兰');await page.click('#find');
   assert.ok(await page.locator('#search-results button').count()>1,'没有可选的搜索结果清单');
   await page.locator('#search-results button').first().click();
   await page.click('#evidence-section summary');
   assert.match(await page.locator('#detail-evidence').innerText(),/第\d+章/);
   assert.ok(await page.locator('#neighbors a').count()>0);
  });
  await check('回到上个事件，不被全图定位打断',async()=>{
   await page.evaluate(()=>select('v1-gift',true));await page.evaluate(()=>select('v2-return',true));
   await page.click('#go-back');assert.match(await page.locator('#detail-label').innerText(),/v1-gift/);
  });
  await check('进入剧情线后可回到原来的主干转折',async()=>{
   await page.selectOption('#guide-select','v7-v07-industry');
   await page.selectOption('#branch','editorial-hidden-annie');
   await page.locator('#detail-narrative .thread-event').first().click();
   await page.click('#return-main');assert.match(await page.locator('#detail-label').innerText(),/v7-v07-industry/);
  });
  await check('直接选择主干目录会恢复31步阅读顺序',async()=>{
   await page.selectOption('#branch','editorial-hidden-annie');
   await page.locator('#guide-list [data-event="v8-v08-cleanse"]').click();
   assert.match(await page.locator('#reading-progress').innerText(),/29\s*\/\s*31/);
   await page.click('#guide-next');assert.match(await page.locator('#detail-label').innerText(),/v8-v08-endbattle/);
  });
  await check('刷新保留正在阅读的剧情线',async()=>{
   await page.selectOption('#branch','editorial-hidden-annie');
   await page.locator('#detail-narrative .thread-event').first().click();
   await page.reload();await page.evaluate(()=>document.fonts.ready);
   assert.match(await page.locator('#reading-progress').innerText(),/1\s*\/\s*4.*剧情线/);
  });
  await check('小地图随缩放更新，点击能移动视野',async()=>{
   assert.equal(await page.locator('#minimap-view').count(),1,'缺少当前位置小地图');
   const before=await page.locator('#minimap-view').getAttribute('width');await page.click('#plus');
   assert.notEqual(await page.locator('#minimap-view').getAttribute('width'),before);
   const old=await page.locator('#canvas').getAttribute('style');await page.locator('#minimap').click({position:{x:50,y:60}});
   assert.notEqual(await page.locator('#canvas').getAttribute('style'),old);
  });
  await check('重新打开后恢复到具体主干节点，深链接仍优先',async()=>{
   await page.selectOption('#guide-select','v7-v07-industry');await page.reload();await page.evaluate(()=>document.fonts.ready);
   assert.match(await page.locator('#detail-label').innerText(),/v7-v07-industry/);
   await page.goto(url+'#v8-v08-sacrifice');await page.evaluate(()=>document.fonts.ready);
   assert.match(await page.locator('#detail-label').innerText(),/v8-v08-sacrifice/);
   assert.match(await page.locator('#detail-narrative').innerText(),/不能.*提前认定/);
  });
  await check('事件深链接由画布定位，浏览器不额外滚动',async()=>{
   await page.goto(url+'#v8-v08-sacrifice');await page.evaluate(()=>document.fonts.ready);
   await page.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));
   assert.equal(await page.locator('#viewport').evaluate(e=>e.scrollTop),0,'原生锚点额外滚动了画布');
   const a=await page.locator('#viewport').boundingBox(),b=await page.locator('#v8-v08-sacrifice').boundingBox();
   assert.ok(Math.abs((a.y+a.height/2)-(b.y+b.height/2))<35,'选中事件未位于视野中央');
  });
  await check('目录中的当前位置随直接跳转可见',async()=>{
   const a=await page.locator('#toc').boundingBox(),b=await page.locator('#guide-list .current').boundingBox();
   assert.ok(b.y>=a.y&&b.y+b.height<=a.y+a.height,'当前转折在目录可见范围之外');
  });
  await page.screenshot({path:path.join(__dirname,'viewer-desktop.png')});
  await check('390px手机能读正文和导航，无页面横向溢出',async()=>{
   await page.setViewportSize({width:390,height:844});await page.goto(url+'#v2-zero');await page.evaluate(()=>document.fonts.ready);
   assert.match(await page.locator('#detail-narrative').innerText(),/零级/);
   assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
   assert.ok((await page.locator('#viewport').boundingBox()).height>=170);
   await page.screenshot({path:path.join(__dirname,'viewer-mobile.png')});
  });
  await check('手机选完目录项自动收起遮挡',async()=>{
   if(await page.locator('#toc').evaluate(e=>e.hidden))await page.click('#toc-toggle');
   await page.locator('#guide-list [data-event="v1-poor"]').click();
   assert.equal(await page.locator('#toc').evaluate(e=>e.hidden),true);
  });
  assert.deepEqual(errors,[]);assert.deepEqual(requests,[]);
  const result={results,passed:results.filter(x=>x.pass).length,failed:results.filter(x=>!x.pass).length,javascript_errors:errors,external_requests:requests};
  fs.writeFileSync(path.join(__dirname,'viewer-check.json'),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result));
  process.exitCode=result.failed?1:0;
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
