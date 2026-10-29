(function(){
 'use strict';
 const D=MAP_DATA,$=id=>document.getElementById(id),key='plot-map-v1:'+D.source_sha256;
 let timer,noticeTimer,opened=false,storageWarned=false;
 function notice(message){$('map-notice').textContent=message;clearTimeout(noticeTimer);noticeTimer=setTimeout(()=>{$('map-notice').textContent=''},5000)}
 const viewer=OpenSeadragon({id:'map',showNavigationControl:false,showNavigator:true,navigatorId:'minimap',navigatorAutoFade:false,navigatorMaintainSizeRatio:false,navigatorDisplayRegionColor:'#d07a2e',navigatorBorderColor:'transparent',
  drawer:'canvas',preserveImageSizeOnResize:true,animationTime:matchMedia('(prefers-reduced-motion:reduce)').matches?0:.25,blendTime:0,visibilityRatio:.85,constrainDuringPan:true,minZoomImageRatio:.8,maxZoomPixelRatio:3,maxImageCacheCount:40,imageLoaderLimit:4,showZoomControl:false,showFullPageControl:false,showHomeControl:false,
  gestureSettingsMouse:{clickToZoom:false,dblClickToZoom:true,scrollToZoom:true},gestureSettingsTouch:{pinchToZoom:true,clickToZoom:false,dblClickToZoom:true,dragToPan:true},
  tileSources:{width:D.width,height:D.height,tileSize:D.tile_size,tileOverlap:D.overlap,minLevel:D.min_level,maxLevel:D.max_level,getTileUrl:(l,x,y)=>D.tiles[l+'/'+x+'/'+y]}
 });
 // 仅暴露查看器本身，方便本机与浏览器验证，不包含凭据或远程服务。
 window.plotMap=viewer;
 function save(){if(!opened)return;try{const vp=viewer.viewport,c=vp.getCenter(true),z=vp.getZoom(true);localStorage.setItem(key,JSON.stringify({x:c.x,y:c.y,z,imageZoom:vp.viewportToImageZoom(z)}))}catch{if(!storageWarned){storageWarned=true;notice('当前浏览器无法记住位置；地图仍可正常浏览。')}}}
 function zoom(factor){viewer.viewport.zoomBy(factor);viewer.viewport.applyConstraints()}
 function readable(point){const vp=viewer.viewport,center=point||vp.getCenter(true),scale=innerWidth<500?.88:1.1;vp.zoomTo(vp.imageToViewportZoom(scale),center,true);vp.panTo(center,true);vp.applyConstraints(true);}
 $('zoom-in').onclick=()=>zoom(1.4);$('zoom-out').onclick=()=>zoom(1/1.4);
 $('map-home').onclick=()=>{viewer.viewport.goHome();$('map-location').value=''};
 $('map-read').onclick=()=>{const vp=viewer.viewport,small=vp.viewportToImageZoom(vp.getZoom(true))<.2;readable(small?vp.imageToViewportCoordinates(D.start.x+D.start.width/2,D.start.y+D.start.height/2):null)};
 function focus(on){document.body.classList.toggle('focused',on);$('exit-focus').hidden=!on;if(!on)$('focus-mode').focus();else $('exit-focus').focus()}
 $('focus-mode').onclick=()=>focus(true);$('exit-focus').onclick=()=>focus(false);
 $('map-fullscreen').hidden=!document.fullscreenEnabled;
 $('map-fullscreen').onclick=async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await document.documentElement.requestFullscreen()}catch{notice('当前窗口未允许全屏；可用“专注”扩大看图空间。')}};
 document.addEventListener('fullscreenchange',()=>{$('map-fullscreen').textContent=document.fullscreenElement?'退出全屏':'全屏'});
 for(const v of D.volumes){const option=document.createElement('option');option.value=v.number;option.textContent='第'+v.number+'集';$('map-location').append(option)}
 $('map-location').onchange=()=>{const v=D.volumes.find(v=>String(v.number)===$('map-location').value);if(v)readable(viewer.viewport.imageToViewportCoordinates(v.x+v.width/2,v.y+v.height/2))};
 // 下载数据由内嵌图块或原SVG生成，离线包中也无需访问原文件路径。
 $('download-svg').onclick=e=>{e.preventDefault();download(new Blob([D.svg],{type:'image/svg+xml'}),'超级骷髅兵-全书图.svg')};
 $('download-png').onclick=e=>{e.preventDefault();downloadURI(D.png,'超级骷髅兵-全书图.png')};
 function downloadURI(url,name){const a=document.createElement('a');a.href=url;a.download=name;document.body.append(a);a.click();a.remove()}
 function download(blob,name){const url=URL.createObjectURL(blob);downloadURI(url,name);setTimeout(()=>URL.revokeObjectURL(url),2000)}
 viewer.addHandler('open',()=>{
  let saved;try{saved=JSON.parse(localStorage.getItem(key)||'null')}catch{}
  if(saved&&['x','y','z'].every(k=>Number.isFinite(saved[k]))&&saved.x>=0&&saved.x<=1&&saved.y>=0&&saved.y<=D.height/D.width&&saved.z>0){const vp=viewer.viewport,target=Number.isFinite(saved.imageZoom)&&saved.imageZoom>0?vp.imageToViewportZoom(saved.imageZoom):saved.z,z=Math.max(vp.getMinZoom(),Math.min(vp.getMaxZoom(),target));vp.zoomTo(z,null,true);vp.panTo(new OpenSeadragon.Point(saved.x,saved.y),true);vp.applyConstraints(true)}
  opened=true;document.body.dataset.ready='true';$('map-loading').hidden=true;
 });
 viewer.addHandler('viewport-change',()=>{$('map-scale').textContent=Math.round(viewer.viewport.viewportToImageZoom(viewer.viewport.getZoom(true))*100)+'%';clearTimeout(timer);timer=setTimeout(save,350)});
 viewer.addHandler('open-failed',()=>{$('map-loading').hidden=true;$('map-error').hidden=false});
 viewer.addHandler('tile-load-failed',()=>{$('map-error').hidden=false;$('map-error').textContent='部分图块未能载入，请重新打开完整HTML文件。'});
 window.addEventListener('pagehide',save);
 document.addEventListener('pointerdown',e=>{if(!$('map-more').contains(e.target))$('map-more').open=false});
 document.addEventListener('keydown',e=>{if(e.key==='Escape'){if(document.body.classList.contains('focused'))focus(false);else if($('map-more').open){$('map-more').open=false;$('map-more').querySelector('summary').focus()}} if(e.ctrlKey||e.metaKey||e.altKey||['INPUT','SELECT','TEXTAREA'].includes(e.target.tagName))return;if(e.key==='+'||e.key==='='){e.preventDefault();e.stopPropagation();zoom(1.4)}if(e.key==='-'){e.preventDefault();e.stopPropagation();zoom(1/1.4)}if(e.key==='0'){e.preventDefault();e.stopPropagation();viewer.viewport.goHome()}},true);
})();
