(function(){
 'use strict';
 const D=READER_DATA,M=PlotModel.createModel(D),$=id=>document.getElementById(id),mobile=()=>matchMedia('(max-width:767px)').matches;
 const REL={cause:'因果',setup:'铺垫',reveal:'揭示',reversal:'转折',payoff:'回收',echo:'呼应',misdirection:'误导'},CLAIM={fact:'原文事实',inference:'研究推断',synthesis:'研究综合',plan:'计划'},STATUS={open:'未回收',partial:'部分回收',resolved:'已回收'},KIND={main:'主线',subplot:'支线',hidden:'暗线'},KNOW={unknown:'未知',suspects:'怀疑',knows:'知道',misbelieves:'误以为'};
 const title=t=>t.title.split(' · ').pop();
 function h(tag,attrs={},...children){const e=document.createElement(tag);for(const [k,v] of Object.entries(attrs)){if(k.startsWith('on'))e.addEventListener(k.slice(2),v);else if(k==='class')e.className=v;else e.setAttribute(k,String(v));}for(const c of children.flat(Infinity)){if(c===undefined||c===null)continue;e.append(c instanceof Node?c:document.createTextNode(String(c)))}return e;}
 const badge=(text,cls='')=>h('span',{class:'badge '+cls},text);
 const button=(text,fn,attrs={})=>h('button',{type:'button',onclick:fn,...attrs},text);
 let noticeTimer;function notify(message){$('notice').textContent=message;clearTimeout(noticeTimer);noticeTimer=setTimeout(()=>{$('notice').textContent=''},9000)}
 let read=new Set(),bookmark=null,resume=null,storageWarned=false,navOpen=false;
 const storageKey='plot-reader-v1:'+D.source_id+':'+D.revision;
 function validState(s){
  if(!s||!s.scope||typeof s.scope.kind!=='string')return null;const p=s.scope;
  if(!['overview','stage','thread','character','nearby','search','junctions','unresolved'].includes(p.kind))return null;
  const known=(items,id)=>typeof id==='string'&&Object.hasOwn(items,id);
  if(p.kind==='stage'&&!known(M.stages,p.id)||p.kind==='thread'&&!known(M.threads,p.id)||p.kind==='character'&&!known(D.characters,p.id)||p.kind==='nearby'&&!known(M.nodes,p.id))return null;
  const out={scope:{kind:p.kind,id:typeof p.id==='string'?p.id:undefined,query:typeof p.query==='string'?p.query.slice(0,200):'',core:!!p.core,depth:p.depth===2?2:1},mode:s.mode==='map'?'map':'cards',selected:known(M.nodes,s.selected)?s.selected:null,detail:!!s.detail,detailEdge:D.edges.some(e=>e.id===s.detailEdge)?s.detailEdge:null,scroll:Number.isFinite(s.scroll)?Math.max(0,Math.min(s.scroll,100000)):0,detailScroll:Number.isFinite(s.detailScroll)?Math.max(0,Math.min(s.detailScroll,100000)):0,expanded:Array.isArray(s.expanded)?s.expanded.filter(v=>typeof v==='string'&&/^(card-threads-|relation-|stage-summary-)/.test(v)).slice(0,500):[],viewport:null};
  if(s.viewport&&['scale','tx','ty'].every(k=>Number.isFinite(s.viewport[k]))&&s.viewport.scale>=.001&&s.viewport.scale<=3)out.viewport={...s.viewport};
  if(!out.selected)out.detail=false;return out;
 }
 try{const saved=JSON.parse(localStorage.getItem(storageKey)||'null');if(saved){const packet=M.parseProgress(JSON.stringify(saved.progress));read=new Set(packet.read);bookmark=packet.bookmark;resume=validState(saved.state)}}catch{notify('此浏览器没有可恢复的有效进度；可继续阅读并导入备份。')}
 const initial={scope:mobile()?{kind:'stage',id:'stage-1',core:true}:{kind:'overview'},mode:'cards',selected:null,detail:false,detailEdge:null,scroll:0,detailScroll:0,expanded:[],viewport:null};
 const nav=new PlotModel.Navigation(initial),graph=new PlotGraph(M,id=>openEvent(id),id=>openEdge(id));
 const state=()=>nav.current;
 function capture(){const s=state();s.scroll=$('cards').scrollTop;s.detailScroll=$('detail-body').scrollTop;s.expanded=[...document.querySelectorAll('#cards details[open],#detail-body details[open],#scope-options details[open]')].map(el=>el.id);if(!$('graph').hidden)s.viewport=graph.snapshot();const active=document.activeElement?.closest('[data-event]');s.focusEvent=active?.dataset.event||null;}
 function progress(){return {version:1,source_id:D.source_id,revision:D.revision,read:[...read],bookmark};}
 function save(){try{localStorage.setItem(storageKey,JSON.stringify({progress:progress(),state:state()}))}catch{if(!storageWarned){storageWarned=true;notify('浏览器未允许保存进度。阅读仍可用，请通过“导出阅读进度”保留。')}}}
 function navigate(patch,{keepView=false}={}){capture();nav.go({...state(),scroll:0,detailScroll:0,expanded:[],viewport:keepView?state().viewport:null,detail:false,detailEdge:null,...patch});closeNav();render();save();}
 function back(){if(!nav.history.length)return;capture();nav.back();closeNav();render();save();}
 function openScope(scope){navigate({scope,mode:mobile()||['overview','search','junctions','unresolved'].includes(scope.kind)?'cards':'map',selected:null});}
 function openThread(id){const from=state().selected;openScope({kind:'thread',id});if(from&&M.threads[id].node_ids.includes(from))notify('已进入这条线；“返回刚才”可回到原交汇事件。');}
 function openEvent(id){if(!M.nodes[id])return;if(state().selected===id&&state().detail&&!state().detailEdge)return;const same=M.scopeIds(state().scope).includes(id)&&state().scope.kind!=='overview'&&state().scope.kind!=='unresolved';
  navigate({scope:same?state().scope:{kind:'nearby',id,depth:1},mode:same?state().mode:(mobile()?'cards':'map'),selected:id,detail:true,scroll:same?$('cards').scrollTop:0},{keepView:same});bookmark=id;save();}
 function openEdge(id){const e=D.edges.find(e=>e.id===id);if(!e)return;navigate({selected:e.to,detail:true,detailEdge:id,scroll:$('cards').scrollTop},{keepView:true});bookmark=e.to;save();}
 function localMap(id){navigate({scope:{kind:'nearby',id,depth:1},mode:'map',selected:id,detail:false});}
 function toggleRead(id){if(read.has(id))read.delete(id);else read.add(id);bookmark=id;capture();render();save();}
 function markButton(id){return button(read.has(id)?'✓ 已读':'标为已读',()=>toggleRead(id),{class:'read-toggle','data-action':'mark-read','aria-pressed':read.has(id),'aria-label':(read.has(id)?'取消已读：':'标为已读：')+M.nodes[id].title});}
 function proof(evidence){return h('ul',{class:'evidence'},(evidence||[]).map(e=>h('li',{},`${e.chapter_id} · L${e.start_line}—${e.end_line}`)));}
 function scopeLabel(s){if(s.kind==='overview')return '全书骨架';if(s.kind==='stage')return M.stages[s.id].title;if(s.kind==='thread')return title(M.threads[s.id]);if(s.kind==='character')return D.characters[s.id]?.name||'人物卡';if(s.kind==='nearby')return '局部关系 · '+M.nodes[s.id].title;if(s.kind==='search')return '搜索：'+s.query;if(s.kind==='junctions')return '多条剧情的交汇点';return '尚待回收的暗线';}
 function threadChips(id){return h('div',{class:'thread-chips'},M.memberships[id].map(tid=>button(KIND[M.threads[tid].kind]+' · '+title(M.threads[tid]),()=>openThread(tid),{'data-thread':tid})));}
 function eventCard(id){const n=M.nodes[id],r=M.relations(id);return h('article',{class:'event-card','data-event':id,'data-read':read.has(id)},
  h('div',{class:'card-meta'},h('div',{},h('span',{},`第${+id.slice(1,3)}集 · ${id}`),r.parents.length>1?badge('交汇 '+r.parents.length+'路','junction'):badge(CLAIM[n.claim_kind]||'研究记录')),markButton(id)),
  button(n.title,()=>openEvent(id),{class:'card-title','data-action':'event'}),h('p',{class:'card-summary'},n.summary),
  h('div',{class:'card-actions'},button(`前置 ${r.incoming.length}`,()=>openEvent(id)),button(`后续 ${r.outgoing.length}`,()=>openEvent(id)),button('查看关系',()=>localMap(id),{'data-action':'local-map'})),
  h('details',{class:'card-threads',id:'card-threads-'+id},h('summary',{},`${M.memberships[id].length} 条剧情线在此关联`),threadChips(id)));
 }
 function overview(){
  const intro=h('div',{class:'overview-intro'},h('p',{},'先看全书的走向，再进入一个阶段。你可以沿主线读，也可以从交汇事件进入另一条支线。'));
  const grid=h('div',{class:'stage-grid'});
  for(const s of D.stages){const junction=s.node_ids.filter(id=>M.relations(id).parents.length>1).sort((a,b)=>M.relations(b).parents.length-M.relations(a).parents.length)[0];
   grid.append(h('article',{class:'stage-tile','data-stage':s.id},button('',()=>openScope({kind:'stage',id:s.id}),{class:'stage-open'}),junction?h('div',{class:'stage-junction'},h('span',{},'关键交汇'),button(M.nodes[junction].title,()=>openEvent(junction))):null));
   const b=grid.lastChild.querySelector('.stage-open');b.append(h('span',{class:'stage-index'},String(s.number).padStart(2,'0')+' / '+s.range),h('h2',{},s.title),h('p',{},s.summary),h('span',{class:'tile-meta'},`${s.node_ids.length} 个事件 · 展开阅读 →`));
  }
  $('cards').replaceChildren(intro,grid);
 }
 function unresolved(){const list=h('div',{class:'event-list'});for(const t of D.threads.filter(t=>t.kind==='hidden'&&t.status!=='resolved'))list.append(h('article',{class:'thread-card','data-thread':t.id},badge(STATUS[t.status],t.status),h('h2',{},title(t)),h('p',{},t.question),button('沿这条暗线阅读 →',()=>openThread(t.id))));$('cards').replaceChildren(list);}
 function renderCards(ids){if(state().scope.kind==='overview')return overview();if(state().scope.kind==='unresolved')return unresolved();if(!ids.length){$('cards').replaceChildren(h('div',{class:'empty'},h('h2',{},'没有找到相关事件'),h('p',{},'试试人物名字、较短的关键词，或从剧情阶段重新进入。'),button('返回全书骨架',()=>openScope({kind:'overview'}))));return;}
  const list=h('div',{class:'event-list'});ids.forEach(id=>list.append(eventCard(id)));$('cards').replaceChildren(list);
 }
 function relationship(e,direction,visible){const other=direction==='incoming'?e.from:e.to;const outside=!visible.has(other),stage=M.stages[M.stageByNode[other]];
  return h('div',{class:'relation','data-direction':direction,'data-edge':e.id},badge(REL[e.kind]||e.kind),button(M.nodes[other].title,()=>openEvent(other),{'data-target':other}),outside?h('small',{},'范围外 · '+stage.range+' · '+stage.title):null,h('p',{},e.label),h('details',{id:'relation-'+e.id+'-'+direction},h('summary',{},(CLAIM[e.claim_kind]||'研究记录')+' · 查看关系依据'),proof(e.evidence)));
 }
 function renderDetail(ids){const s=state(),n=M.nodes[s.selected],panel=$('detail-panel');panel.hidden=!s.detail||!n;document.body.classList.toggle('has-detail',!panel.hidden);if(panel.hidden)return;
  const body=$('detail-body');body.replaceChildren();const stage=M.stages[M.stageByNode[n.id]],visible=new Set(ids);
  if(s.detailEdge){const e=D.edges.find(e=>e.id===s.detailEdge);body.append(badge(REL[e.kind]),h('h2',{id:'detail-title',tabindex:-1},M.nodes[e.from].title+' → '+M.nodes[e.to].title),h('p',{class:'detail-summary'},e.label),h('p',{class:'detail-stage'},CLAIM[e.claim_kind]),h('div',{class:'detail-controls'},button('读起点事件',()=>openEvent(e.from)),button('读终点事件',()=>openEvent(e.to))),proof(e.evidence));return;}
  const r=M.relations(n.id);body.append(h('p',{class:'detail-stage'},stage.range+' / '+stage.title),badge(CLAIM[n.claim_kind]||'研究记录'),h('h2',{id:'detail-title',tabindex:-1},n.title),h('p',{class:'detail-summary'},n.summary),h('div',{class:'detail-controls'},markButton(n.id),button('查看局部关系图',()=>localMap(n.id),{'data-action':'local-map'})));
  if(state().scope.kind==='thread'){const t=M.threads[state().scope.id];body.append(h('section',{class:'detail-section'},h('h3',{},'当前剧情线 · '+STATUS[t.status]),h('p',{},t.question),h('p',{class:'knowledge'},t.resolution_note.replace(/^已入库至第\d+集；最近关联事件在第\d+集。最新状态审计在第\d+集。/,''))));}
  body.append(h('section',{class:'detail-section'},h('h3',{},`前置关系 · 全部 ${r.incoming.length} 条`),r.incoming.length?r.incoming.map(e=>relationship(e,'incoming',visible)):h('p',{class:'knowledge'},'研究图中尚未记录前置关系。')));
  body.append(h('section',{class:'detail-section'},h('h3',{},`后续关系 · 全部 ${r.outgoing.length} 条`),r.outgoing.length?r.outgoing.map(e=>relationship(e,'outgoing',visible)):h('p',{class:'knowledge'},'研究图中尚未记录后续关系。')));
  body.append(h('section',{class:'detail-section'},h('h3',{},`经过这个事件的剧情线 · ${M.memberships[n.id].length}`),threadChips(n.id)));
  body.append(h('section',{class:'detail-section'},h('h3',{},'参与人物卡'),h('div',{class:'thread-chips'},(n.characters||[]).map(id=>button(D.characters[id]?.name||id,()=>openScope({kind:'character',id}),{title:D.characters[id]?.title||id})))));
  if(n.knowledge?.length)body.append(h('section',{class:'detail-section'},h('h3',{},'此时谁知道什么'),n.knowledge.map(k=>h('p',{class:'knowledge'},h('strong',{},(k.observer==='reader'?'读者':D.characters[k.observer]?.name||'人物')+' · '+(KNOW[k.state]||k.state)),k.belief))));
  body.append(h('section',{class:'detail-section'},h('h3',{},'原文定位 · '+n.id),proof(n.evidence)));
 }
 function renderHeader(ids){const s=state(),scope=s.scope,label=scopeLabel(scope);$('scope-title').textContent=label;
  $('breadcrumb').textContent=scope.kind==='overview'?'全书 / 结构导览':'全书 / '+(s.selected?M.stages[M.stageByNode[s.selected]].range+' / ':'')+({stage:'剧情阶段',thread:'剧情线',character:'人物卡',nearby:'事件周围',search:'查找',junctions:'交汇',unresolved:'暗线复核'}[scope.kind]||'阅读');
  $('scope-subtitle').textContent=scope.kind==='overview'?'七个阶段 · 点击进入局部结构':scope.kind==='unresolved'?'11条部分回收 · 3条未回收 · 状态截至全书终点':`${ids.length} 个事件 · ${ids.filter(id=>read.has(id)).length} 个已读`+(scope.core?' · 当前仅显示核心主线':'');
  $('back').disabled=!nav.history.length;$('mode-cards').setAttribute('aria-pressed',s.mode==='cards');$('mode-map').setAttribute('aria-pressed',s.mode==='map');
  const noMap=['overview','unresolved'].includes(scope.kind)||!ids.length;$('mode-map').disabled=noMap;
  $('scope-options').replaceChildren();if(scope.kind==='stage')$('scope-options').append(button(scope.core?'显示本阶段全部事件':'只读本阶段主线',()=>navigate({scope:{...scope,core:!scope.core},mode:'cards',selected:null})),h('details',{class:'stage-summary',id:'stage-summary-'+scope.id},h('summary',{},'阶段概览'),h('p',{},M.stages[scope.id].summary)));
  if(scope.kind==='thread'){const t=M.threads[scope.id];$('scope-options').append(badge(KIND[t.kind],t.kind),badge(STATUS[t.status],t.status));}
  $('expand-graph').hidden=scope.kind!=='nearby'||scope.depth===2;$('read-current').hidden=scope.kind!=='nearby';
  $('stage-select').value=scope.kind==='stage'?scope.id:'';$('thread-select').value=scope.kind==='thread'?scope.id:'';$('character-select').value=scope.kind==='character'?scope.id:'';
  document.querySelectorAll('#stage-nav [data-stage]').forEach(b=>b.classList.toggle('active',scope.kind==='stage'&&scope.id===b.dataset.stage));
 }
 function render(){const s=state(),ids=M.scopeIds(s.scope);renderHeader(ids);renderDetail(ids);const showMap=s.mode==='map'&&!['overview','unresolved'].includes(s.scope.kind)&&ids.length>0;
  $('cards').hidden=!!showMap;$('graph').hidden=!showMap;if(showMap)graph.render(s.scope,ids,s.selected,s.viewport,read);else renderCards(ids);
  for(const id of s.expanded||[]){const d=$(id);if(d)d.open=true;}
  applyModal();requestAnimationFrame(()=>{$('cards').scrollTop=s.scroll||0;$('detail-body').scrollTop=s.detailScroll||0;if(mobile()&&s.detail)$('detail-title')?.focus({preventScroll:true});else if(s.focusEvent){const b=document.querySelector('.event-card[data-event="'+CSS.escape(s.focusEvent)+'"] [data-action=event]');b?.focus({preventScroll:true});}});
 }
 function applyModal(){const detail=mobile()&&!$('detail-panel').hidden,modal=navOpen||detail;$('main').inert=modal;$('masthead').inert=modal;$('navigation').inert=detail;$('detail-panel').setAttribute('role',detail?'dialog':'complementary');$('detail-panel').setAttribute('aria-modal',String(detail));$('navigation').setAttribute('role',navOpen?'dialog':'navigation');$('navigation').setAttribute('aria-modal',String(navOpen));}
 function closeNav(){navOpen=false;document.body.classList.remove('nav-open');$('scrim').hidden=true;$('menu').setAttribute('aria-expanded','false');applyModal();}
 function toggleNav(){if(innerWidth>=1280){document.body.classList.toggle('nav-collapsed');return;}navOpen=!navOpen;document.body.classList.toggle('nav-open',navOpen);$('scrim').hidden=!navOpen;$('menu').setAttribute('aria-expanded',String(navOpen));applyModal();if(navOpen)$('search').focus();else $('menu').focus();}
 $('menu').onclick=toggleNav;$('nav-close').onclick=()=>{closeNav();$('menu').focus()};$('scrim').onclick=()=>{closeNav();$('menu').focus()};
 $('back').onclick=back;$('detail-back').onclick=back;$('detail-close').onclick=()=>{if(mobile()&&nav.history.length)return back();capture();state().detail=false;state().detailEdge=null;render();save()};
 $('home').onclick=()=>openScope({kind:'overview'});$('mode-cards').onclick=()=>navigate({mode:'cards',detail:false},{keepView:true});$('mode-map').onclick=()=>navigate({mode:'map',detail:false},{keepView:true});
 $('expand-graph').onclick=()=>navigate({scope:{...state().scope,depth:2},detail:false},{keepView:true});$('read-current').onclick=()=>openEvent(state().scope.id);
 $('search-form').onsubmit=e=>{e.preventDefault();const query=$('search').value.trim();if(query)openScope({kind:'search',query})};
 for(const s of D.stages){$('stage-select').append(h('option',{value:s.id},s.range+' · '+s.title));$('stage-nav').append(button('',()=>openScope({kind:'stage',id:s.id}),{'data-stage':s.id}));$('stage-nav').lastChild.append(h('span',{class:'number'},String(s.number).padStart(2,'0')),h('span',{},s.title,h('small',{},s.range+' · '+s.node_ids.length+'事件')));}
 for(const t of D.threads)$('thread-select').append(h('option',{value:t.id},KIND[t.kind]+' · '+title(t)));
 for(const [id,c] of Object.entries(D.characters).filter(([id])=>D.nodes.some(n=>n.characters?.includes(id))))$('character-select').append(h('option',{value:id},c.name+' · '+c.title));
 $('stage-select').onchange=()=>{if($('stage-select').value)openScope({kind:'stage',id:$('stage-select').value})};$('thread-select').onchange=()=>{if($('thread-select').value)openThread($('thread-select').value)};$('character-select').onchange=()=>{if($('character-select').value)openScope({kind:'character',id:$('character-select').value})};
 $('show-junctions').onclick=()=>openScope({kind:'junctions'});$('show-open').onclick=()=>openScope({kind:'unresolved'});
 $('export-progress').onclick=()=>{capture();save();const url=URL.createObjectURL(new Blob([JSON.stringify(progress(),null,2)],{type:'application/json'})),a=h('a',{href:url,download:'超级骷髅兵-阅读进度.json'});document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),2000)};
 $('import-progress').onchange=async()=>{const file=$('import-progress').files[0];if(!file)return;try{if(file.size>100000)throw new Error('进度文件过大，未导入');const packet=M.parseProgress(await file.text());read=new Set([...read,...packet.read]);bookmark=packet.bookmark;capture();save();render();notify('已合并阅读标记；可从“继续上次”回到导入位置。');if(bookmark){resume=null;showResume()}}catch(e){notify(e.message)}finally{$('import-progress').value=''}};
 function showResume(){if(!resume&&!bookmark)return;$('resume').hidden=false;$('resume').textContent='继续上次';$('resume').onclick=()=>{if(resume){navigate(validState(resume));resume=null}else if(bookmark)openEvent(bookmark);};}
 document.addEventListener('keydown',e=>{const modal=navOpen?$('navigation'):mobile()&&!$('detail-panel').hidden?$('detail-panel'):null;if(!modal)return;if(e.key==='Escape'){e.preventDefault();navOpen?closeNav():$('detail-close').click();return;}if(e.key==='Tab'){const items=[...modal.querySelectorAll('button:not(:disabled),input,select,a[href],summary,[tabindex="0"]')].filter(el=>el.getClientRects().length),first=items[0],last=items.at(-1);if(e.shiftKey&&(document.activeElement===first||!modal.contains(document.activeElement))){e.preventDefault();last?.focus()}else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first?.focus()}}});
 let saveTimer;for(const id of ['cards','detail-body'])$(id).addEventListener('scroll',()=>{clearTimeout(saveTimer);saveTimer=setTimeout(()=>{capture();save()},180)},{passive:true});
 window.addEventListener('pagehide',()=>{capture();save()});let lastMobile=mobile();window.addEventListener('resize',()=>{if(mobile()!==lastMobile){capture();lastMobile=mobile();if(lastMobile&&state().scope.kind==='overview')state().mode='cards';render()}else applyModal()});
 showResume();render();
})();
