'use strict';
const claims={fact:'原文事实',inference:'研究推断',synthesis:'研究综合',plan:'计划'};
const knowledgeStates={unknown:'未知',suspects:'怀疑',knows:'知道',misbelieves:'误以为'};
const relations={cause:'因果',setup:'铺垫',reveal:'揭示',misdirection:'误导',reversal:'转折',payoff:'回收',echo:'主题呼应'};
const statuses={resolved:'已回收',partial:'部分回收',open:'未回收',unknown:'待核实',abandoned:'已放弃'};
const $=id=>document.getElementById(id),vp=$('viewport'),canvas=$('canvas'),svg=canvas.querySelector('svg'),panel=$('detail');
const guideIds=data.reading_guide.node_ids,notes=data.reading_notes.entries,viewKey='novel-tree-'+data.meta.source_id+'-v3';
let scale=1,tx=0,ty=0,currentId='',route=guideIds,routeId='main',routeIndex=-1,lastMainIndex=0,navHistory=[],historyIndex=-1,restoring=false;
let drag=null,dragged=false,gesture=null,pointers=new Map(),viewportSize={width:vp.clientWidth,height:vp.clientHeight};
const ordered=id=>data.meta.events.indexOf(id);
const titleOf=id=>notes[id]?.title||data.nodes[id]?.title||id;
function notice(text){$('notice').textContent=text}
function element(tag,text,className){const e=document.createElement(tag);if(text)e.textContent=text;if(className)e.className=className;return e}
function persist(){try{localStorage.setItem(viewKey,JSON.stringify({scale,tx,ty,id:currentId,routeId,lastMainIndex}))}catch(_){}}
function apply(){canvas.style.transform=`translate(${tx}px,${ty}px) scale(${scale})`;$('zoom').textContent=Math.round(scale*100)+'%';viewportSize={width:vp.clientWidth,height:vp.clientHeight};updateMini()}
function fitRect(x,y,w,h){const margin=24;scale=Math.max(.008,Math.min((vp.clientWidth-2*margin)/w,(vp.clientHeight-2*margin)/h,2));tx=(vp.clientWidth-w*scale)/2-x*scale;ty=(vp.clientHeight-h*scale)/2-y*scale;apply()}
function fit(){fitRect(0,0,data.meta.width,data.meta.height)}
function zoom(factor,x=vp.clientWidth/2,y=vp.clientHeight/2){const next=Math.max(.008,Math.min(3,scale*factor));tx=x-(x-tx)*next/scale;ty=y-(y-ty)*next/scale;scale=next;apply();persist()}
function focusIds(ids){const boxes=ids.map(id=>data.meta.positions[id]).filter(Boolean);if(!boxes.length)return;const x=Math.min(...boxes.map(b=>b.x)),y=Math.min(...boxes.map(b=>b.y));fitRect(x-65,y-65,Math.max(...boxes.map(b=>b.x+b.width))-x+130,Math.max(...boxes.map(b=>b.y+b.height))-y+130)}
function clear(){svg.querySelectorAll('.dim,.selected').forEach(e=>e.classList.remove('dim','selected'));notice('主干分枝 · 共享事件交汇；右下小地图可定位')}
function mark(ids,edgeIds=null){const keep=new Set(ids);svg.querySelectorAll('[data-kind=event],[data-kind=thread]').forEach(e=>e.classList.toggle('dim',!keep.has(e.id)));svg.querySelectorAll('[data-kind=edge],[data-kind=annotation],[data-kind=reading-order]').forEach(e=>e.classList.toggle('dim',edgeIds&&['edge','reading-order'].includes(e.dataset.kind)?!edgeIds.has(e.id):!(keep.has(e.dataset.from)&&keep.has(e.dataset.to))))}
function evidence(items){return [...new Set((items||[]).map(e=>`${data.chapters[e.chapter_id]?.title||e.chapter_id}\n${e.chapter_id} · L${e.start_line}—${e.end_line}`))].join('\n\n')}
function narrativeSection(title,text){const s=element('section');s.append(element('h3',title),element('p',text));$('detail-narrative').append(s)}
function detail(title,label,text,proof=''){
 panel.classList.add('open');$('detail-title').textContent=title;$('detail-label').textContent=label;$('detail-text').textContent=text;$('detail-evidence').textContent=proof;
 for(const id of ['neighbors','detail-narrative','branch-links'])$(id).replaceChildren();$('source-note').open=false;$('evidence-section').open=false;
 $('branch-section').hidden=true;$('neighbors-section').hidden=true;
}
function setRoute(id){routeId=id;route=id==='main'?guideIds:[...data.threads[id].node_ids].filter(n=>data.nodes[n]).sort((a,b)=>ordered(a)-ordered(b));routeIndex=route.indexOf(currentId)}
function updateReading(){
 const index=route.indexOf(currentId);if(index>=0)routeIndex=index;
 const isMain=routeId==='main';
 $('reading-progress').textContent=index>=0?`${index+1} / ${route.length} · ${isMain?'主干阅读':'剧情线阅读'}`:data.threads[currentId]?`剧情线 · ${route.length}个事件`:`分枝 · 主干${Math.max(1,guideIds.indexOf(route[routeIndex])+1)}步附近`;
 $('guide-prev').disabled=index<=0;$('guide-next').disabled=index>=route.length-1;
 $('return-main').hidden=isMain&&index>=0;$('guide-select').value=guideIds.includes(currentId)?currentId:'';
 $('guide-list').querySelectorAll('[data-event]').forEach(b=>{const selected=b.dataset.event===currentId;b.classList.toggle('current',selected);if(selected)b.setAttribute('aria-current','step');else b.removeAttribute('aria-current')});
 const selected=$('guide-list').querySelector('.current'),toc=$('toc');
 if(selected&&!toc.hidden){const a=toc.getBoundingClientRect(),b=selected.getBoundingClientRect();if(b.y<a.y+8)toc.scrollTop-=a.y+8-b.y;else if(b.bottom>a.bottom-8)toc.scrollTop+=b.bottom-a.bottom+8}
}
function eventButton(id,label){const b=element('button',label||titleOf(id));b.type='button';b.onclick=()=>select(id,true);return b}
function neighbors(nid){
 const items=Object.values(data.edges).filter(e=>e.from===nid||e.to===nid);
 for(const e of items){const incoming=e.to===nid,other=incoming?e.from:e.to,b=eventButton(other,(incoming?'来自：':'通向：')+titleOf(other)+' · '+relations[e.kind]);b.append(element('small',e.label));b.title=e.summary||e.label;$('neighbors').append(b)}
 for(const person of (data.character_links||{})[nid]||[]){const a=element('a','人物档案：'+person.name);a.href=person.href;$('neighbors').append(a)}
 $('neighbors-section').hidden=!$('neighbors').childElementCount;
}
function recordHistory(id){if(restoring||navHistory[historyIndex]===id)return;navHistory=navHistory.slice(0,historyIndex+1);navHistory.push(id);historyIndex=navHistory.length-1;$('go-back').disabled=historyIndex<=0}
function select(id,focus=false){
 if(!data.nodes[id]&&!data.threads[id]&&!data.edges[id]&&!data.reading_guide.edges[id])return;
 if(routeId==='main'&&guideIds.includes(id))lastMainIndex=guideIds.indexOf(id);
 if(innerWidth<=980){$('toc').hidden=true;$('toc-toggle').setAttribute('aria-expanded','false')}
 recordHistory(id);currentId=id;try{history.replaceState(null,'','#'+encodeURIComponent(id))}catch(_){}
 const wasOpen=panel.classList.contains('open');clear();document.getElementById(id)?.classList.add('selected');
 if(data.nodes[id]){
  const n=data.nodes[id],pos=data.meta.positions[id],links=Object.values(data.edges).filter(e=>e.from===id||e.to===id),note=notes[id];
  mark([id,...links.flatMap(e=>[e.from,e.to])],new Set(links.map(e=>e.id)));
  detail(titleOf(id),`${note?.stage?note.stage+' · ':''}${id} · ${note?'阅读综合':claims[n.claim_kind]||'研究记录'}`,n.summary||'',evidence(note?.evidence||n.evidence));
  if(note){narrativeSection('当时的处境',note.situation);narrativeSection('人物怎样行动',note.action);narrativeSection('这一步改变了什么',note.consequence)}
  else{narrativeSection('事件与变化',n.summary||'本事件保留原研究记录，具体范围见原文定位。');$('source-note').hidden=true}
  if(note)$('source-note').hidden=false;
  for(const k of n.knowledge||[])narrativeSection(`${data.observers[k.observer]||'观察者'} · ${knowledgeStates[k.state]||k.state}`,k.belief);
  for(const other of note?.branch_ids||[])$('branch-links').append(eventButton(other));
  $('branch-section').hidden=!$('branch-links').childElementCount;neighbors(id);
  if(focus||!wasOpen)fitRect(pos.x-105,pos.y-140,pos.width+210,pos.height+280);
  notice((guideIds.includes(id)?'主干 '+(guideIds.indexOf(id)+1)+'/31':'分枝事件')+' · '+n.title);
 }else if(data.threads[id]){
  const t=data.threads[id],m=data.meta.threads.find(x=>x.id===id);setRoute(id);
  const ids=[id,...t.node_ids,...t.edge_ids.flatMap(e=>[data.edges[e].from,data.edges[e].to])];
  detail(t.title,(m?'全书线 '+String(m.number).padStart(2,'0'):'卷末阶段记录')+' · '+statuses[t.status],t.question||'',evidence(t.evidence));
  narrativeSection('这条线追踪什么',t.question||t.title);narrativeSection('最后可靠状态',t.resolution_note||'保留对应阶段判断，不直接当作全书未解。');
  const list=element('section');list.append(element('h3','按事件继续读'));for(const nid of route){const b=eventButton(nid);b.classList.add('thread-event');list.append(b)}$('detail-narrative').append(list);$('source-note').hidden=true;mark(ids,new Set(t.edge_ids));if(focus)focusIds(ids);notice('已聚焦：'+t.title+'；共享事件保持原位');
 }else{
  const guide=!!data.reading_guide.edges[id],e=data.edges[id]||data.reading_guide.edges[id];mark([e.from,e.to],new Set([id]));
  detail((guide?'阅读衔接':relations[e.kind])+' · '+titleOf(e.from)+' → '+titleOf(e.to),guide?'展示层 reading-order · 不表示因果':`${e.from} → ${e.to} · ${claims[e.claim_kind]||'研究记录'}`,e.label,evidence(e.evidence));
  narrativeSection(guide?'只表示接续阅读':'这条关系为什么成立',guide?'两个事件沿主干接续阅读，不属于原语义关系，不计起点、分枝或交汇。':e.summary||e.label);
  $('neighbors').append(eventButton(e.from,'看来源：'+titleOf(e.from)),eventButton(e.to,'看去向：'+titleOf(e.to)));$('neighbors-section').hidden=false;$('source-note').hidden=true;if(focus)focusIds([e.from,e.to]);
 }
 updateReading();persist();
}
function startReading(index=0){setRoute('main');select(guideIds[Math.max(0,Math.min(guideIds.length-1,index))],true)}
function move(delta){let i=route.indexOf(currentId);if(i<0)i=routeIndex;select(route[Math.max(0,Math.min(route.length-1,i+delta))],true)}
function setupDirectory(){
 let stage='';guideIds.forEach((id,i)=>{const n=notes[id];if(n.stage!==stage){stage=n.stage;$('guide-list').append(element('div',stage,'stage'))}const b=eventButton(id);b.replaceChildren(element('span',String(i+1).padStart(2,'0'),'step-no'),element('span',titleOf(id)));b.dataset.event=id;b.onclick=()=>{setRoute('main');select(id,true)};$('guide-list').append(b);const o=element('option',String(i+1).padStart(2,'0')+' · '+titleOf(id));o.value=id;$('guide-select').append(o)});
 for(const t of data.meta.threads){const full=data.threads[t.id],b=element('button',full.title);b.append(element('small',statuses[t.status],t.status));b.onclick=()=>select(t.id,true);$('whole-thread-list').append(b)}
 for(const [label,threads] of [['全书剧情线',Object.values(data.threads).filter(t=>t.id.startsWith('editorial-'))],['分卷阶段记录',Object.values(data.threads).filter(t=>!t.id.startsWith('editorial-'))]]){const group=element('optgroup');group.label=label;for(const t of threads){const o=element('option',({main:'主线',subplot:'支线',hidden:'暗线'}[t.kind]||'线索')+' · '+t.title.split(' · ').pop());o.value=t.id;group.append(o)}$('branch').append(group)}
 data.volumes.forEach((v,i)=>{const o=element('option',v.title);o.value=i+1;$('volume').append(o)});
}
function setupMini(){
 const ns='http://www.w3.org/2000/svg',mini=$('minimap');mini.setAttribute('viewBox',`0 0 ${data.meta.width} ${data.meta.height}`);mini.style.aspectRatio=`${data.meta.width}/${data.meta.height}`;
 for(const id of data.meta.events){const p=data.meta.positions[id],r=document.createElementNS(ns,'rect');for(const k of ['x','y','width','height'])r.setAttribute(k,p[k]);r.setAttribute('fill',guideIds.includes(id)?'#3976bb':'#bfd0dd');mini.append(r)}
 const view=document.createElementNS(ns,'rect');view.id='minimap-view';mini.append(view);
 mini.onclick=e=>{e.stopPropagation();const b=mini.getBoundingClientRect(),x=(e.clientX-b.left)/b.width*data.meta.width,y=(e.clientY-b.top)/b.height*data.meta.height;tx=vp.clientWidth/2-x*scale;ty=vp.clientHeight/2-y*scale;apply();persist()};
}
function updateMini(){const box=$('minimap-view');if(!box)return;const x=Math.max(0,Math.min(data.meta.width,-tx/scale)),y=Math.max(0,Math.min(data.meta.height,-ty/scale)),w=Math.max(0,Math.min(data.meta.width-x,vp.clientWidth/scale)),h=Math.max(0,Math.min(data.meta.height-y,vp.clientHeight/scale));for(const [k,v] of Object.entries({x,y,width:w,height:h}))box.setAttribute(k,v)}
function find(){
 const term=$('search').value.trim(),box=$('search-results');if(!term){box.hidden=true;return}const lower=term.toLocaleLowerCase(),matches=data.meta.events.filter(id=>{
  const n=data.nodes[id],people=((data.character_links||{})[id]||[]).map(p=>p.name).join(' '),chapters=(n.evidence||[]).map(e=>(data.chapters[e.chapter_id]?.title||'')+' '+e.chapter_id).join(' ');
  return `${titleOf(id)} ${n.title} ${n.summary||''} ${people} ${chapters} ${JSON.stringify(notes[id]||{})}`.toLocaleLowerCase().includes(lower);
 });box.replaceChildren(element('div',matches.length?`找到 ${matches.length} 个事件，点选后定位`:'本图未找到：'+term,'result-count'));box.hidden=false;
 for(const id of matches){const n=data.nodes[id],b=eventButton(id);b.append(element('small',(n.evidence||[]).map(e=>data.chapters[e.chapter_id]?.short_title||e.chapter_id).filter((x,i,a)=>a.indexOf(x)===i).join(' · ')));b.onclick=()=>{select(id,true);box.hidden=true};box.append(b)}
 if(matches.length){select(matches[0],true);notice(`找到 ${matches.length} 个事件；结果清单可直接选择`)}else notice('本图未找到：'+term);
}
setupDirectory();setupMini();
$('save-svg').download='纵横天下-全书分枝交汇图.svg';$('save-svg').href=URL.createObjectURL(new Blob([svg.outerHTML],{type:'image/svg+xml;charset=utf-8'}));
$('guide-start').onclick=()=>startReading(0);$('guide-prev').onclick=()=>move(-1);$('guide-next').onclick=()=>move(1);$('return-main').onclick=()=>startReading(lastMainIndex);
$('guide-select').onchange=()=>{if($('guide-select').value){setRoute('main');select($('guide-select').value,true)}};
$('fit').onclick=()=>{clear();fit();persist()};$('mainline').onclick=()=>{clear();setRoute('main');mark(guideIds,new Set(Object.keys(data.reading_guide.edges)));detail('从谋生到组织与龙域责任 · 31个主要转折','主干阅读衔接 · 不新增因果','主干可逐步阅读；细蓝点划线只表示阅读顺序。');narrativeSection('怎样继续读','点击“从主干开始读”，或在左侧选一处。每步说明处境、行动与改变，相关分枝仍在同一张图。');focusIds(guideIds);updateReading();notice('主干阅读衔接：31个转折；细蓝点划线不表示因果')};
$('threads').onclick=()=>{clear();panel.classList.remove('open');const ids=data.meta.threads.flatMap(t=>[t.id,t.anchor]);mark(ids);focusIds(ids);notice('7条全书线：3条已回收、4条部分回收；安妮与明宇身份暗线均已回收。点击枝端框查看边界')};
$('junctions').onclick=()=>{clear();panel.classList.remove('open');mark(data.meta.junctions);fit();notice('金色标记为多路交汇；点击查看来源、选择与后果')};
$('branch').onchange=()=>{if($('branch').value)select($('branch').value,true)};
$('volume').onchange=()=>{if(!$('volume').value)return;clear();panel.classList.remove('open');const ids=data.meta.events.filter(id=>data.meta.positions[id].volume===Number($('volume').value));mark(ids);focusIds(ids)};
$('plus').onclick=()=>zoom(1.4);$('minus').onclick=()=>zoom(1/1.4);$('clear').onclick=clear;$('close').onclick=()=>{panel.classList.remove('open');apply()};
$('go-back').onclick=()=>{if(historyIndex<=0)return;historyIndex--;restoring=true;select(navHistory[historyIndex],true);restoring=false;$('go-back').disabled=historyIndex<=0};
$('toc-toggle').onclick=()=>{const hidden=!$('toc').hidden;$('toc').hidden=hidden;$('toc-toggle').setAttribute('aria-expanded',String(!hidden));apply()};
$('search-form').onsubmit=e=>{e.preventDefault();find()};document.addEventListener('click',e=>{if(!e.target.closest('#search-form'))$('search-results').hidden=true});
if(innerWidth<=980){$('toc').hidden=true;$('toc-toggle').setAttribute('aria-expanded','false')}
vp.addEventListener('wheel',e=>{e.preventDefault();const b=vp.getBoundingClientRect();zoom(Math.exp(-e.deltaY*.0015),e.clientX-b.left,e.clientY-b.top)},{passive:false});
vp.addEventListener('pointerdown',e=>{if(e.target.closest('#minimap-wrap')||e.button!==0)return;const b=vp.getBoundingClientRect();pointers.set(e.pointerId,{x:e.clientX-b.left,y:e.clientY-b.top});dragged=false;if(pointers.size===2){const [a,c]=[...pointers.values()],center={x:(a.x+c.x)/2,y:(a.y+c.y)/2};gesture={distance:Math.hypot(a.x-c.x,a.y-c.y),scale,x:(center.x-tx)/scale,y:(center.y-ty)/scale};drag=null}else{drag={x:e.clientX,y:e.clientY,tx,ty};vp.classList.add('drag')}});
vp.addEventListener('pointermove',e=>{if(!pointers.has(e.pointerId))return;const b=vp.getBoundingClientRect();pointers.set(e.pointerId,{x:e.clientX-b.left,y:e.clientY-b.top});if(gesture&&pointers.size===2){const [a,c]=[...pointers.values()];scale=Math.max(.008,Math.min(3,gesture.scale*Math.hypot(a.x-c.x,a.y-c.y)/Math.max(1,gesture.distance)));tx=(a.x+c.x)/2-gesture.x*scale;ty=(a.y+c.y)/2-gesture.y*scale;dragged=true;apply();return}if(!drag)return;const dx=e.clientX-drag.x,dy=e.clientY-drag.y;if(Math.abs(dx)+Math.abs(dy)>5){dragged=true;vp.setPointerCapture(e.pointerId)}tx=drag.tx+dx;ty=drag.ty+dy;apply()});
function endPointer(e){pointers.delete(e.pointerId);drag=null;if(pointers.size<2)gesture=null;vp.classList.remove('drag');if(vp.hasPointerCapture(e.pointerId))vp.releasePointerCapture(e.pointerId);persist()}
vp.addEventListener('pointerup',endPointer);vp.addEventListener('pointercancel',endPointer);
svg.addEventListener('click',e=>{if(dragged)return;const g=e.target.closest('[data-kind]');if(g)select(g.id)});
svg.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){const g=e.target.closest('[data-kind]');if(g){e.preventDefault();select(g.id,true)}}});
vp.addEventListener('dblclick',e=>{if(!e.target.closest('[data-kind]')&&!e.target.closest('#minimap-wrap'))fit()});
document.addEventListener('keydown',e=>{if(e.key==='Escape'){$('search-results').hidden=true;if(innerWidth<=980)$('toc').hidden=true;return}if(e.target.closest('input,select,textarea,[contenteditable=true]')||e.ctrlKey||e.metaKey||e.altKey)return;if(e.key==='ArrowRight'){e.preventDefault();move(1)}if(e.key==='ArrowLeft'){e.preventDefault();move(-1)}});
new ResizeObserver(()=>{const w=vp.clientWidth,h=vp.clientHeight;tx+=(w-viewportSize.width)/2;ty+=(h-viewportSize.height)/2;apply()}).observe(vp);
function openHash(){let id='';try{id=decodeURIComponent(location.hash.slice(1))}catch(_){}if(data.nodes[id]||data.threads[id]||data.edges[id]||data.reading_guide.edges[id]){select(id,true);return true}return false}
document.fonts.ready.then(()=>{
 let saved=null;try{saved=JSON.parse(localStorage.getItem(viewKey))}catch(_){}
 if(saved)lastMainIndex=Math.max(0,Math.min(guideIds.length-1,saved.lastMainIndex||0));
 let hash='';try{hash=decodeURIComponent(location.hash.slice(1))}catch(_){}
 if(saved&&hash===saved.id&&data.threads[saved.routeId])setRoute(saved.routeId);
 if(openHash())return;
 if(saved&&data.nodes[saved.id]){if(data.threads[saved.routeId])setRoute(saved.routeId);select(saved.id,true);return}
 startReading(0);
});
window.addEventListener('hashchange',openHash);window.addEventListener('beforeunload',persist);
