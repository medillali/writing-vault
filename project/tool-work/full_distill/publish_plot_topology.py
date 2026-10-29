from pathlib import Path
from collections import Counter
from urllib.parse import unquote
from PIL import Image
import sys,json,hashlib,re,xml.etree.ElementTree as ET,zipfile
sys.dont_write_bytecode=True
from verify_plot_images import ROOT,VAULT,REPORT,GH,command,git

BASE='99c54c95f58e3da7d68fdd460018086b64581340'
folder=REPORT/'reading/plot/whole-book'
m=json.loads((folder/'manifest.json').read_text(encoding='utf-8'))
gp=VAULT/'library/sources'/m['source_id']/'plot-graph.json'
g=json.loads(gp.read_text(encoding='utf-8'))
assert hashlib.sha256(gp.read_bytes()).hexdigest()==m['graph_sha256']
nodes={n['id']:n for n in g['nodes'] if n['kind']=='event'}
edges={e['id']:e for e in g['edges']}
threads={t['id']:t for t in g['threads'] if t['id'].startswith('book-')}
hidden={tid:t for tid,t in threads.items() if t['kind']=='hidden'}
assert len(m['events'])==len(set(m['events']))==163 and set(m['events'])==set(nodes)
assert len(m['edges'])==len(set(m['edges']))==265 and set(m['edges'])==set(edges)
assert {t['id'] for t in m['threads']}==set(hidden)
assert {t['id']:t['status'] for t in m['threads']}=={tid:t['status'] for tid,t in hidden.items()}
assert m['states']==dict(Counter(t['status'] for t in hidden.values()))
pairs={(e['from'],e['to']) for e in edges.values() if e['kind']!='echo'}
inc,out=Counter(b for a,b in pairs),Counter(a for a,b in pairs)
assert set(m['roots'])=={n for n in nodes if not inc[n]}
assert set(m['junctions'])=={n for n in nodes if inc[n]>1}
assert set(m['forks'])=={n for n in nodes if out[n]>1}
assert 'v04-e04' in m['roots'] and 'v11-e02' in m['junctions']
svg=ET.fromstring((folder/'tree.svg').read_text(encoding='utf-8'))
groups={e.attrib['id']:e for e in svg.iter() if 'id' in e.attrib and 'data-kind' in e.attrib}
assert set(e.attrib['id'] for e in groups.values() if e.attrib['data-kind']=='event')==set(nodes)
assert not any(e.attrib.get('data-kind')=='volume' for e in svg.iter())
for eid,e in edges.items():
    el=groups[eid]
    assert el.attrib['data-kind']=='edge'
    assert el.attrib['data-from']==e['from'] and el.attrib['data-to']==e['to']
    assert el.attrib['data-relation']==e['kind']
    assert e['label'] in ''.join(el.itertext())
for nid,n in nodes.items():
    text=''.join(groups[nid].itertext())
    assert n['title'] in text and n['summary'] in text
for t in m['threads']:
    assert t['anchor']==max(hidden[t['id']]['node_ids'],key=lambda nid:nodes[nid]['narrative_order'])
    assert t['conclusion'] in ''.join(groups[t['id']].itertext())
html=(folder/'index.html').read_text(encoding='utf-8')
embedded=json.loads(re.search(r'const data=(.+);\nconst claims=',html,re.S).group(1))
assert embedded['nodes']==nodes and embedded['edges']==edges and embedded['threads']==threads
browser=json.loads((REPORT/'validation/whole-book-browser.json').read_text())
assert all(browser[k]==0 for k in ['text_overflow','node_overlap','edges_through_unrelated_nodes','javascript_errors','external_requests'])
assert browser['event_cards']==163 and browser['edges']==265 and browser['thread_choices']==46
# 本任务有意生成约1亿像素的大图，仅对明确的本地生成文件提高检查上限。
Image.MAX_IMAGE_PIXELS=130_000_000
for name,expected in [('tree.png',(m['width'],m['height'])),('tree-preview.png',(2600,round(m['height']*2600/m['width']))),('tree-junction-preview.png',(1800,1404))]:
    with Image.open(folder/name) as im:
        assert abs(im.width-expected[0])<=1 and abs(im.height-expected[1])<=1
        im.verify()
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
        assert (p.parent/unquote(target.split('#')[0])).resolve().exists(),(name,target)
        links+=1
assert not git('diff',BASE,'--','library/sources','library/characters','library/scenes','library/patterns','history','books','exchanges').strip()
assert not git('diff','--cached','--name-only').strip()
assert git('branch','--show-current').strip()=='main'
assert git('remote','get-url','origin').strip()=='https://github.com/medillali/writing-vault.git'
git('diff','--check')
repo=json.loads(command([GH,'api','repos/medillali/writing-vault']))
assert repo['private'] and repo['owner']['login']=='medillali'
result={'selection':m['selection'],'events':163,'relations':265,'independent_origins':len(m['roots']),'forks':len(m['forks']),'junctions':len(m['junctions']),'hidden_threads':15,'dimensions':[m['width'],m['height']],'png_bytes':(folder/'tree.png').stat().st_size,'reading_pages':298,'valid_links':links,'old_49_images_unchanged':True,'source_and_notes_unchanged_from':BASE,'checks':'passed','browser':browser,'sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in folder.iterdir() if p.is_file()}}
(REPORT/'validation/whole-book.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in ['sha256','browser']},ensure_ascii=False),flush=True)
if '--publish' not in sys.argv:sys.exit(0)
remote_before=json.loads(command([GH,'api','repos/medillali/writing-vault/commits/main']))['sha']
assert remote_before==git('rev-parse','HEAD').strip()==BASE
paths=['README.md','library/reports/super-skeleton/README.md','library/reports/super-skeleton/全书单图设计.md','library/reports/super-skeleton/rebuild_whole_book.py','library/reports/super-skeleton/rebuild_plot_topology.py','library/reports/super-skeleton/layout_whole_book.cjs','library/reports/super-skeleton/render_whole_book.cjs','library/reports/super-skeleton/whole_book_viewer.html','library/reports/super-skeleton/rebuild_plot_images.py','library/reports/super-skeleton/rebuild_github_reading.py','library/reports/super-skeleton/reading','library/reports/super-skeleton/validation/whole-book.json','library/reports/super-skeleton/validation/whole-book-browser.json','library/reports/super-skeleton/validation/whole-book-event.png','library/reports/super-skeleton/validation/whole-book-overview.png']
git('add','--',*paths)
staged=[p for p in git('diff','--cached','--name-only','-z').split('\0') if p]
assert all(p in paths or p.startswith('library/reports/super-skeleton/reading/') for p in staged)
git('diff','--cached','--check')
print(git('commit','-m','docs: reshape full-book plot as branching and converging event graph').splitlines()[0],flush=True)
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
        info,path=line.split('\t',1);local_files[path]=info.split()[1]
assert local_files==remote_files
assert not git('status','--porcelain').strip()
backup=ROOT/'backups/超级骷髅兵-分枝交汇全图-20261022.zip'
with zipfile.ZipFile(backup,'w',zipfile.ZIP_DEFLATED) as z:
    for p in folder.iterdir():
        if p.is_file():z.write(p,p.name)
    z.writestr('阅读说明.txt','打开 index.html 可缩放拖动、搜索、选择任一剧情线聚焦，并沿事件的来源与去向继续阅读。\n完整图片 tree.png，矢量图 tree.svg；tree-preview.png 为全图预览，tree-junction-preview.png 为同图局部。\n163个事件、265条原关系。15条暗线状态使用全书终点复核；不是新剧情事件。\n')
with zipfile.ZipFile(backup) as z:
    assert z.testzip() is None
    for p in folder.iterdir():
        if p.is_file():assert z.read(p.name)==p.read_bytes()
published={'head':sha,'remote_head':remote,'private':True,'remote_blobs':len(remote_files),'clean':True,'zip':str(backup)}
(ROOT/'distill-novels/work/full_distill/plot-topology-published.json').write_text(json.dumps(published,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(published,ensure_ascii=False,indent=2))
