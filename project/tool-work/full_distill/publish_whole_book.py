from pathlib import Path
from urllib.parse import unquote
from PIL import Image
import sys,json,hashlib,re,xml.etree.ElementTree as ET,zipfile
sys.dont_write_bytecode=True
from verify_plot_images import ROOT,VAULT,REPORT,GH,command,git
base='5f9548e0127cae5a23b6a3e6330e976130532b5a'
folder=REPORT/'reading/plot/whole-book'
m=json.loads((folder/'manifest.json').read_text(encoding='utf-8'))
gp=VAULT/'library/sources'/m['source_id']/'plot-graph.json'
g=json.loads(gp.read_text(encoding='utf-8'))
assert hashlib.sha256(gp.read_bytes()).hexdigest()==m['graph_sha256']
nodes={n['id']:n for n in g['nodes']}
edges={e['id']:e for e in g['edges']}
threads={t['id']:t for t in g['threads'] if t['id'].startswith('book-') and t['kind']=='hidden'}
assert len(m['events'])==len(set(m['events']))==77
assert set(int(n[1:3]) for n in m['events'])==set(range(1,19))
assert [nodes[n]['narrative_order'] for n in m['events']]==sorted(nodes[n]['narrative_order'] for n in m['events'])
assert len(m['bridges'])==12
for b in m['bridges']:
    e=edges[b['id']]
    assert e['from'] in m['events'] and e['to'] in m['events']
assert {t['id'] for t in m['threads']}==set(threads)
for t in m['threads']:
    source=threads[t['id']]
    assert t['status']==source['status']
    assert t['volumes']==sorted({int(n[1:3]) for n in source['node_ids']})
    assert set(source['node_ids'])&set(m['events']),t['id']
svg=ET.fromstring((folder/'tree.svg').read_text(encoding='utf-8'))
content=''.join(svg.itertext())
for nid in m['events']:
    assert nodes[nid]['title'] in content and nodes[nid]['summary'] in content
for b in m['bridges']:assert edges[b['id']]['label'] in content
for t in m['threads']:assert t['conclusion'] in content
with Image.open(folder/'tree.png') as im:
    assert im.size==(9740,5558)
    im.verify()
with Image.open(folder/'tree-preview.png') as im:
    assert im.size==(2600,1484)
    im.verify()
browser=json.loads((REPORT/'validation/whole-book-browser.json').read_text())
assert browser['text_overflow']==browser['javascript_errors']==browser['external_requests']==0
old=json.loads((REPORT/'validation/plot-images.json').read_text(encoding='utf-8'))
assert all(hashlib.sha256((REPORT/'reading/plot/images'/name).read_bytes()).hexdigest()==sha for name,sha in old['sha256'].items())
pages=json.loads((REPORT/'reading/manifest.json').read_text(encoding='utf-8'))['pages']
assert len(pages)==298
links=0
for name,sha in pages.items():
    p=REPORT/'reading'/name
    assert hashlib.sha256(p.read_bytes()).hexdigest()==sha
    for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
        if target.startswith(('http:','https:','#','mailto:')):continue
        target=unquote(target.split('#')[0])
        assert (p.parent/target).resolve().exists(),(name,target)
        links+=1
assert not git('diff',base,'--','library/sources','library/characters','library/scenes','library/patterns','history','books','exchanges').strip()
assert not git('diff','--cached','--name-only').strip()
assert git('branch','--show-current').strip()=='main'
assert git('remote','get-url','origin').strip()=='https://github.com/medillali/writing-vault.git'
git('diff','--check')
meta=json.loads(command([GH,'api','repos/medillali/writing-vault']))
assert meta['private'] and meta['owner']['login']=='medillali'
result={'selection':'关键脉络版','events':77,'total_events_in_research':163,'bridges':12,'hidden_threads':15,'dimensions':[9740,5558],'png_bytes':(folder/'tree.png').stat().st_size,'reading_pages':298,'valid_links':links,'old_49_images_unchanged':True,'source_and_notes_unchanged_from':base,'checks':'passed','browser':browser,'sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in folder.iterdir() if p.is_file()}}
(REPORT/'validation/whole-book.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in ['sha256','browser']},ensure_ascii=False),flush=True)
paths=['README.md','library/reports/super-skeleton/README.md','library/reports/super-skeleton/全书单图设计.md','library/reports/super-skeleton/rebuild_whole_book.py','library/reports/super-skeleton/render_whole_book.cjs','library/reports/super-skeleton/whole_book_viewer.html','library/reports/super-skeleton/rebuild_plot_images.py','library/reports/super-skeleton/rebuild_github_reading.py','library/reports/super-skeleton/reading','library/reports/super-skeleton/validation/whole-book.json','library/reports/super-skeleton/validation/whole-book-browser.json','library/reports/super-skeleton/validation/whole-book-event.png','library/reports/super-skeleton/validation/whole-book-overview.png']
git('add','--',*paths)
staged=[p for p in git('diff','--cached','--name-only','-z').split('\0') if p]
assert all(p in paths or p.startswith('library/reports/super-skeleton/reading/') for p in staged)
git('diff','--cached','--check')
print(git('commit','-m','docs: add a unified whole-book plot tree with zoomable reading').splitlines()[0],flush=True)
print(git('push','origin','main'),flush=True)
sha=git('rev-parse','HEAD').strip()
remote=json.loads(command([GH,'api','repos/medillali/writing-vault/commits/main']))['sha']
assert sha==remote
tree=json.loads(command([GH,'api',f'repos/medillali/writing-vault/git/trees/{sha}?recursive=1']))
assert not tree.get('truncated')
remote_files={p['path']:p['sha'] for p in tree['tree'] if p['type']=='blob'}
local_files={}
for line in git('ls-files','--stage','-z').split('\0'):
    if line:
        info,path=line.split('\t',1)
        local_files[path]=info.split()[1]
assert local_files==remote_files
assert not git('status','--porcelain').strip()
backup=ROOT/'backups/超级骷髅兵-全书一张图-20261022.zip'
with zipfile.ZipFile(backup,'w',zipfile.ZIP_DEFLATED) as z:
    for p in folder.iterdir():
        if p.is_file():z.write(p,p.name)
    z.writestr('阅读说明.txt','打开 index.html 可拖动、缩放、跳集、搜索，点击事件可查看摘要和证据。\n完整图片为 tree.png；tree.svg 可无损放大；tree-preview.png 是缩略预览。\n关键脉络版包括77个关键事件及全部15条暗线，未代替163个事件的完整索引。\n')
with zipfile.ZipFile(backup) as z:
    assert z.testzip() is None
    for p in folder.iterdir():
        if p.is_file():assert z.read(p.name)==p.read_bytes()
published={'head':sha,'remote_head':remote,'private':True,'remote_blobs':len(remote_files),'clean':True,'zip':str(backup)}
(ROOT/'distill-novels/work/full_distill/whole-book-published.json').write_text(json.dumps(published,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(published,ensure_ascii=False,indent=2))
