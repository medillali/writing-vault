// 同时验收参考形式、图中文字与真实离线浏览操作。
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {pathToFileURL}=require('node:url'),{chromium}=require('playwright'),sharp=require('sharp');
const root=process.argv[2],mode=process.argv[3];
const save=(p,x)=>fs.writeFileSync(p,JSON.stringify(x,null,2)+'\n');
(async()=>{const browser=await chromium.launch({headless:true,channel:'chrome'});try{
 for(const folder of (process.argv.slice(4).length?process.argv.slice(4):['zeidan','leveling'])){
  const dir=path.join(root,folder),whole=path.join(dir,'plot','whole-book'),valid=path.join(dir,'validation');fs.mkdirSync(valid,{recursive:true});
  const m=JSON.parse(fs.readFileSync(path.join(whole,'manifest.json'),'utf8')),model=JSON.parse(fs.readFileSync(path.join(dir,'plot','topology.json'),'utf8'));
  const page=await browser.newPage({viewport:{width:mode==='svg'?m.width:1500,height:1000},deviceScaleFactor:1});
  const errors=[],network=[];page.on('pageerror',e=>errors.push(String(e)));page.on('request',r=>{if(/^https?:/.test(r.url()))network.push(r.url())});
  if(mode==='svg'){
   assert.equal(m.layout.engine,'Graphviz dot');assert.ok(m.forks.length&&m.junctions.length&&m.threads.length);
   await page.goto(pathToFileURL(path.join(whole,'tree.svg')).href);await page.evaluate(()=>document.fonts.ready);
   const layout=await page.evaluate(m=>{
    const texts=[...document.querySelectorAll('text')],ps=Object.entries(m.positions),overflow=[],overlaps=[],pierced=[],outsideCards=[];
    for(const t of texts){const b=t.getBBox();if(b.x<Number(t.dataset.left)-2||b.x+b.width>Number(t.dataset.right)+2||b.y+b.height>Number(t.dataset.bottom)+2)overflow.push(t.textContent)}
    for(let i=0;i<ps.length;i++)for(let j=i+1;j<ps.length;j++){const[a,p]=ps[i],[b,q]=ps[j];if(p.x<q.x+q.width-1&&q.x<p.x+p.width-1&&p.y<q.y+q.height-1&&q.y<p.y+p.height-1)overlaps.push([a,b])}
    for(const e of document.querySelectorAll('[data-kind=edge],[data-kind=annotation]'))for(const p of e.querySelectorAll('path:not([stroke=transparent])')){
     const len=p.getTotalLength();for(let i=3;i<len;i+=10){const q=p.getPointAtLength(i);for(const[id,b]of ps){if(id===e.dataset.from||id===e.dataset.to)continue;if(q.x>b.x+3&&q.x<b.x+b.width-3&&q.y>b.y+3&&q.y<b.y+b.height-3){pierced.push([e.id,id]);i=len;break}}}
    }
    for(const g of document.querySelectorAll('[data-kind=event],[data-kind=thread]')){const rb=g.querySelector('rect').getBBox();for(const t of g.querySelectorAll('text')){const b=t.getBBox();if(b.x<rb.x+8||b.x+b.width>rb.x+rb.width-8||b.y<rb.y+5||b.y+b.height>rb.y+rb.height-5)outsideCards.push([g.id,t.textContent])}}
    return{texts:texts.length,overflow,overlaps,pierced,outsideCards};
   },m);
   save(path.join(valid,'diagram-layout.json'),layout);
   assert.deepEqual(layout.overflow,[]);assert.deepEqual(layout.overlaps,[]);assert.deepEqual(layout.pierced,[]);assert.deepEqual(layout.outsideCards,[]);
   // 长图超过GPU纹理边界时，整页截图可能悄悄重复顶部。
   // 逐段渲染并核对64px重叠区；曲线的分段抗锯齿允许极小差异。
   const strips=[],seams=[],step=4096,overlap=64;let previous=null;
   for(let y=0;y<m.height;y+=step){
    const top=Math.max(0,y-overlap),height=Math.min(m.height,y+step)-top;
    await page.setViewportSize({width:m.width,height});
    await page.evaluate(({top,height,width,total})=>{const s=document.documentElement;s.setAttribute('width',width);s.setAttribute('height',height);s.setAttribute('viewBox',`0 ${top} ${width} ${height}`);s.style.width=width+'px';s.style.height=height+'px';const bg=s.querySelector(':scope>rect');bg.setAttribute('width',width);bg.setAttribute('height',total)},{top,height,width:m.width,total:m.height});
    const buffer=await page.screenshot({type:'png',timeout:60000});
    if(previous){const a=await sharp(previous).extract({left:0,top:(await sharp(previous).metadata()).height-overlap,width:m.width,height:overlap}).raw().toBuffer(),b=await sharp(buffer).extract({left:0,top:0,width:m.width,height:overlap}).raw().toBuffer();let delta=0,max=0;for(let i=0;i<a.length;i++){const d=Math.abs(a[i]-b[i]);delta+=d;max=Math.max(max,d)}const mean=delta/a.length;seams.push({y,mean_channel_delta:mean,max_channel_delta:max});assert.ok(mean<.2&&max<50,'接缝差异超出曲线抗锯齿范围：'+JSON.stringify(seams.at(-1)))}
    const skip=y-top;strips.push({input:await sharp(buffer).extract({left:0,top:skip,width:m.width,height:height-skip}).png().toBuffer(),left:0,top:y});previous=buffer;
   }
   await sharp({create:{width:m.width,height:m.height,channels:3,background:'#f7f9fc'},limitInputPixels:400000000}).composite(strips).png().toFile(path.join(whole,'tree.png'));
   save(path.join(valid,'raster-seams.json'),{strategy:'SVG原坐标分段渲染，避免超过16384像素的整页截图重复',step,overlap,seams});
   const image=sharp(path.join(whole,'tree.png'),{limitInputPixels:400000000});const dim=await image.metadata();assert.equal(dim.width,m.width);assert.equal(dim.height,m.height);
   await image.clone().resize({width:1900}).png().toFile(path.join(whole,'tree-preview.png'));
   // 局部严格裁自全图，保留连线、空间关系和原字体大小。
   const nodes=model.nodes,order=id=>nodes.find(n=>n.id===id).narrative_order;
   const picks={opening:m.forks.slice().sort((a,b)=>order(a)-order(b))[0],junction:m.junctions.slice().sort((a,b)=>Math.abs(order(a)-nodes[Math.floor(nodes.length*.4)].narrative_order)-Math.abs(order(b)-nodes[Math.floor(nodes.length*.4)].narrative_order))[0],turning:m.junctions.slice().sort((a,b)=>Math.abs(order(a)-nodes[Math.floor(nodes.length*.72)].narrative_order)-Math.abs(order(b)-nodes[Math.floor(nodes.length*.72)].narrative_order))[0],ending:nodes.at(-1).id};
   const crops=[];for(const[name,id]of Object.entries(picks)){
    const p=m.positions[id],width=Math.min(1100,m.width),height=Math.min(900,m.height);let cx=p.x+p.width/2,cy=p.y+p.height/2;
    if(name==='ending'){const nearby=m.threads.map(t=>m.positions[t.id]).filter(b=>Math.abs(b.x-p.x)<700&&Math.abs(b.y-p.y)<600).sort((a,b)=>Math.hypot(a.x-p.x,a.y-p.y)-Math.hypot(b.x-p.x,b.y-p.y))[0];if(nearby){const x=Math.min(p.x,nearby.x),y=Math.min(p.y,nearby.y),w=Math.max(p.x+p.width,nearby.x+nearby.width)-x,h=Math.max(p.y+p.height,nearby.y+nearby.height)-y;if(w+60<=width&&h+60<=height){cx=x+w/2;cy=y+h/2}}}
    const left=Math.max(0,Math.min(m.width-width,Math.round(cx-width/2))),top=Math.max(0,Math.min(m.height-height,Math.round(cy-height/2)));
    await image.clone().extract({left,top,width,height}).png().toFile(path.join(dir,'plot','map',name+'.png'));crops.push({name,id,left,top,width,height})
   }
   save(path.join(dir,'plot','map','previews.json'),{source:'../whole-book/tree.png',crops});
   console.log(JSON.stringify({folder,mode,width:m.width,height:m.height,events:m.events.length,forks:m.forks.length,junctions:m.junctions.length,valid:true}));
  }else{
   await page.goto(pathToFileURL(path.join(whole,'index.html')).href);await page.evaluate(()=>document.fonts.ready);
   assert.equal(await page.locator('[data-kind=event]').count(),model.nodes.length);assert.equal(await page.locator('[data-kind=edge]').count(),model.edges.length);
   assert.equal(await page.locator('#branch option').count(),model.threads.length+1);
   const event=model.nodes.find(n=>m.junctions.includes(n.id));await page.fill('#search',event.title);await page.click('#find');await page.locator('#'+event.id+' rect').first().click();
   assert.equal(await page.locator('#detail-title').innerText(),event.title);assert.match(await page.locator('#detail-evidence').innerText(),/ch-\d+/);assert.ok(await page.locator('#neighbors button').count()>=2);
   await page.screenshot({path:path.join(valid,'tree-event.png')});await page.locator('#neighbors button').first().click();assert.notEqual(await page.locator('#detail-title').innerText(),event.title);
   const hidden=model.threads.find(t=>t.kind==='hidden');await page.selectOption('#branch',hidden.id);assert.match(await page.locator('#detail-evidence').innerText(),/ch-\d+/);assert.ok(await page.locator('[data-kind=event].dim').count()>0);
   assert.equal(await page.locator('#'+event.id).count(),1);
   for(const kind of ['sequence','cause','reveal']){const edge=model.edges.find(e=>e.kind===kind);if(!edge)continue;await page.locator('#'+edge.id).focus();await page.keyboard.press('Enter');assert.match(await page.locator('#detail-label').innerText(),kind==='sequence'?/非因果/:/研究推断/)}
   await page.click('#mainline');assert.equal(await page.locator('#detail-title').innerText(),model.core_title);
   await page.click('#threads');assert.match(await page.locator('#notice').innerText(),/待回收或未明暗线/);
   await page.click('#junctions');assert.equal(await page.locator('[data-kind=event]:not(.dim)').count(),m.junctions.length);
   await page.selectOption('#volume',String(m.stages));assert.equal(await page.locator('[data-kind=event]:not(.dim)').count(),model.nodes.filter(n=>n.stage_number===m.stages).length);
   await page.click('#clear');assert.equal(await page.locator('.dim').count(),0);if(await page.locator('#close').isVisible())await page.click('#close');await page.click('#fit');
   const before=await page.locator('#canvas').getAttribute('style');await page.click('#plus');assert.notEqual(await page.locator('#canvas').getAttribute('style'),before);
   await page.click('#fit');await page.screenshot({path:path.join(valid,'tree-desktop.png')});
   const[svgDownload]=await Promise.all([page.waitForEvent('download'),page.click('#save-svg')]);const svg=fs.readFileSync(await svgDownload.path(),'utf8');assert.equal((svg.match(/data-kind="event"/g)||[]).length,model.nodes.length);
   await page.goto(pathToFileURL(path.join(dir,'plot','map','index.html')).href);await page.waitForFunction(()=>document.body.dataset.ready==='true');
   assert.equal(await page.locator('#map-location option').count(),m.stages+1);await page.selectOption('#map-location',String(m.stages));await page.waitForTimeout(450);
   const z=await page.evaluate(()=>plotMap.viewport.getZoom(true));await page.click('#zoom-in');await page.waitForTimeout(450);assert.ok(await page.evaluate(()=>plotMap.viewport.getZoom(true))>z);
   const center=await page.evaluate(()=>{const v=plotMap.viewport;v.panBy(new OpenSeadragon.Point(.025,.03),true);return{x:v.getCenter(true).x,y:v.getCenter(true).y}});await page.waitForTimeout(500);await page.reload();await page.waitForFunction(()=>document.body.dataset.ready==='true');
   const restored=await page.evaluate(()=>({x:plotMap.viewport.getCenter(true).x,y:plotMap.viewport.getCenter(true).y}));assert.ok(Math.abs(restored.x-center.x)<.01&&Math.abs(restored.y-center.y)<.01);
   await page.click('#focus-mode');assert.equal(await page.locator('body.focused').count(),1);await page.keyboard.press('Escape');assert.equal(await page.locator('body.focused').count(),0);
   for(const width of [360,390,768,1280,1600]){await page.setViewportSize({width,height:width<500?844:1000});await page.click('#map-home');await page.click('#map-read');await page.waitForTimeout(500);assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);assert.equal(await page.locator('#map-error:visible').count(),0);const opening=m.positions[model.threads[0].node_ids[0]],point=await page.evaluate(p=>{const v=plotMap.viewport,q=v.pixelFromPoint(v.imageToViewportCoordinates(p.x+p.width/2,p.y+p.height/2),true);return{x:q.x,y:q.y,w:innerWidth,h:innerHeight}},opening);assert.ok(Math.abs(point.x-point.w/2)<2&&Math.abs(point.y-point.h/2)<2,'全图后可读大小未定位开篇事件：'+JSON.stringify(point));if(width===390||width===1600)await page.screenshot({path:path.join(valid,width===390?'map-mobile.png':'map-desktop.png')})}
   const minib=await page.locator('#minimap').boundingBox();const c0=await page.evaluate(()=>plotMap.viewport.getCenter(true).y);await page.mouse.click(minib.x+minib.width*.5,minib.y+minib.height*.7);await page.waitForTimeout(500);assert.notEqual(await page.evaluate(()=>plotMap.viewport.getCenter(true).y),c0);
   await page.locator('#map-more summary').click();const[pngDownload]=await Promise.all([page.waitForEvent('download'),page.click('#download-png')]);assert.deepEqual(fs.readFileSync(await pngDownload.path()),fs.readFileSync(path.join(whole,'tree.png')));
   assert.deepEqual(errors,[]);assert.deepEqual(network,[]);
   save(path.join(valid,'browser.json'),{valid:true,reference_form:'超级骷髅兵：同一事件唯一，按关系分枝交汇；同图瓦片缩放',events:model.nodes.length,semantic_forks:m.forks.length,semantic_junctions:m.junctions.length,hidden_states:m.states,offline_external_requests:network.length,javascript_errors:errors.length,widths:[360,390,768,1280,1600],checks:['事件点击与章节行号','邻接事件导航','整书线聚焦','阅读衔接与因果区分','共享事件唯一','主线与暗线终态聚焦','交汇筛选','研究阶段定位','SVG下载','地图缩放','拖动位置恢复','小地图跳转','专注退出','五种宽度无横溢','PNG下载与全图逐字节相同'],limits:['手机截图来自浏览器视口模拟；真实手机手势仍待用户审阅','自动检查不能代替剧情关系解释与审美审阅']});
   console.log(JSON.stringify({folder,mode,valid:true}));
  }
  await page.close();
 }
}finally{await browser.close()}})().catch(e=>{console.error(e);process.exitCode=1});
