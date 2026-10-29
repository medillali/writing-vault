"""沿用超级骷髅兵现有离线阅读器，替换书目专用内容与动态状态。"""
from pathlib import Path
base=Path(__file__).resolve().parents[3]
source=base/'writing-vault/library/reports/super-skeleton/whole_book_viewer.html'
target=base/'writing-vault/library/reports/zongheng-tianxia/atlas/tree/viewer.html'
s=source.read_text(encoding='utf-8')
s=s.replace('超级骷髅兵','网游之纵横天下').replace('跳到某一集','定位某一卷').replace('集数仅为标记','卷号仅为定位').replace('待回收暗线','全书线终态')
s=s.replace('Math.max(.025','Math.max(.008')
s=s.replace("n.summary+'\\n\\n'","(n.summary||'该事件为原图保留的场景记录，事实范围以以下章节证据为准。')+'\\n\\n'")
s=s.replace("(m?'暗线'+String(m.number).padStart(2,'0')+' · ':'剧情线 · ')","(m?'全书线'+String(m.number).padStart(2,'0')+' · ':'卷末阶段记录 · ')")
s=s.replace("t.question+'\\n\\n'+t.resolution_note","(t.question||'')+'\\n\\n'+(t.resolution_note||'本条保留对应卷末的阶段判断；不作为全书未知项。')")
s=s.replace("open:'未回收'","open:'未回收',unknown:'待核实'")
s=s.replace("+t.title.split(' · ').pop()", "+t.title.split(' · ').pop()")
start=s.index("document.getElementById('threads').onclick=")
end=s.index("document.getElementById('junctions').onclick",start)
s=s[:start]+"document.getElementById('threads').onclick=()=>{clear();panel.classList.remove('open');const ids=data.meta.threads.flatMap(t=>[t.id,t.anchor]);mark(ids);focusIds(ids);document.getElementById('notice').textContent='7条全书线：3条已回收、4条部分回收；安妮与明宇身份暗线均已回收。点击枝端状态框查看边界';};\n"+s[end:]
s=s.replace("o.textContent=({main:'主线',subplot:'支线',hidden:'暗线'}[t.kind])+' · '","o.textContent=(t.id.startsWith('editorial-')?'全书 · ':'卷末 · ')+({main:'主线',subplot:'支线',hidden:'暗线'}[t.kind])+' · '")
s=s.replace("(n.title+' '+n.summary)","(n.title+' '+(n.summary||''))")
s=s.replace("document.fonts.ready.then(fit);", "document.fonts.ready.then(fit);\n// 唯一书目key，避免同一浏览器误用其他书的视野。\nconst viewKey='novel-tree-src-2a13958390274509b2af019f6b12d981-v1';\ntry{const saved=JSON.parse(localStorage.getItem(viewKey));if(saved)document.fonts.ready.then(()=>{({scale,tx,ty}=saved);apply()});}catch(_){}\nwindow.addEventListener('beforeunload',()=>{try{localStorage.setItem(viewKey,JSON.stringify({scale,tx,ty}))}catch(_){}});")
s=s.replace("document.getElementById('save-svg').href", "document.getElementById('save-svg').download='纵横天下-全书分枝交汇图.svg';\ndocument.getElementById('save-svg').href")
s=s.replace(" clear();const el=document.getElementById(id);", " try{history.replaceState(null,'','#'+encodeURIComponent(id))}catch(_){}\n clear();const el=document.getElementById(id);")
s=s.replace("neighbors(id);if(focus)", "neighbors(id);characterLinks(id);if(focus)")
s=s.replace("function select(id,focus=false){", "function characterLinks(nid){for(const person of (data.character_links||{})[nid]||[]){const link=document.createElement('a');link.textContent='人物档案：'+person.name;link.href=person.href;link.style.cssText='display:block;margin:10px 0';document.getElementById('neighbors').append(link)}}\nfunction select(id,focus=false){")
s=s.replace("document.getElementById('mainline').onclick=()=>select(data.meta.core,true);", "document.getElementById('mainline').onclick=()=>{clear();const ids=data.reading_guide.node_ids,ge=new Set(Object.keys(data.reading_guide.edges));mark(ids,ge);focusIds(ids);detail('从谋生到组织与龙域责任 · 主干阅读衔接','31个转折事件 · 展示层，不是新增因果','沿书生目标与局势转折贯通整书。细蓝点划线只表示阅读衔接；原227条语义关系保持独立，不将阅读衔接计入起点、分枝或交汇。');document.getElementById('notice').textContent='主干阅读衔接：细蓝点划线，不表示因果';};")
s=s.replace("[data-kind=edge],[data-kind=annotation]", "[data-kind=edge],[data-kind=annotation],[data-kind=reading-order]")
s=s.replace("el.dataset.kind==='edge'", "['edge','reading-order'].includes(el.dataset.kind)")
s=s.replace(" else if(data.edges[id])", " else if(data.reading_guide.edges[id]){const e=data.reading_guide.edges[id];mark([e.from,e.to],new Set([id]));detail('主干阅读衔接 · '+data.nodes[e.from].title+' → '+data.nodes[e.to].title,'展示层 reading-order · 不表示因果','沿关键转折接续阅读；不属于原语义关系，不计起点、分枝或交汇。',evidence(e.evidence));if(focus)focusIds([e.from,e.to]);}\n else if(data.edges[id])")
s=s.replace("</script></body>", "// 允许人物档案以同一事件ID深链回地图，也支持同文件hash导航。\nfunction openHash(){const id=decodeURIComponent(location.hash.slice(1));if(data.nodes[id]||data.threads[id]||data.edges[id]||data.reading_guide.edges[id])select(id,true)}\ndocument.fonts.ready.then(openHash);window.addEventListener('hashchange',openHash);\n</script></body>")
target.write_text(s,encoding='utf-8')
print(target)
