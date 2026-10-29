"""本次双端阅读器交付检查；不改写研究主档。"""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import hashlib,json,re,zipfile
from urllib.parse import unquote
from verify_plot_images import ROOT,VAULT,REPORT,GH,command,git
BASE='a22937b9d38e26b4770c7b31f352a93f757aa30b'
OUT=REPORT/'reading/plot/reader'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def verify():
    data=read(OUT/'data.json');graph=read(VAULT/'library/sources'/data['source_id']/'plot-graph.json')
    assert {n['id']:n for n in data['nodes']}=={n['id']:n for n in graph['nodes'] if n['kind']=='event'}
    assert data['edges']==graph['edges']
    assert data['threads']==[t for t in graph['threads'] if t['id'].startswith('book-')]
    assert data['revision']==sha(VAULT/'library/sources'/data['source_id']/'plot-graph.json')
    assert len(data['nodes'])==163 and len(data['edges'])==265 and len(data['threads'])==46
    assert len(data['stages'])==7 and sum(len(s['node_ids']) for s in data['stages'])==163
    layouts=read(OUT/'layouts.json');assert layouts['revision']==data['revision'] and len(layouts['scopes'])==53
    for kind,items in [('stage',data['stages']),('thread',data['threads'])]:
        for item in items:assert set(layouts['scopes'][kind+':'+item['id']]['positions'])==set(item['node_ids'])
    source_paths=['library/sources','library/characters','library/scenes','library/patterns','history','books','exchanges']
    old_pictures=['library/reports/super-skeleton/reading/plot/images','library/reports/super-skeleton/reading/plot/whole-book']
    assert not git('diff',BASE,'--',*source_paths,*old_pictures,'library/reports/super-skeleton/book-synthesis.json').strip()
    assert not git('ls-files','--others','--exclude-standard','--',*source_paths,*old_pictures).strip()
    pages=read(REPORT/'reading/manifest.json')['pages'];assert len(pages)==299
    local_links=0
    docs=[REPORT/'reading'/n for n in pages]+[VAULT/'README.md',REPORT/'README.md']
    for name,digest in pages.items():assert sha(REPORT/'reading'/name)==digest
    for p in docs:
        for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
            if target.startswith(('http:','https:','#','mailto:')):continue
            target=unquote(target.split('#')[0]);assert (p.parent/target).resolve().exists(),(p,target)
            local_links+=1
    assert not re.findall(r'<script[^>]+src=',(OUT/'index.html').read_text(encoding='utf-8'))
    assert git('remote','get-url','origin').strip()=='https://github.com/medillali/writing-vault.git'
    meta=json.loads(command([GH,'api','repos/medillali/writing-vault','--jq','{full_name,private,default_branch}']))
    assert meta['private'] and meta['full_name']=='medillali/writing-vault'
    git('diff','--check')
    result={'events':163,'relations':265,'threads':46,'stages':7,'layout_scopes':53,'source_graph_sha256':data['revision'],
        'reading_pages':len(pages),'valid_local_links':local_links,'source_notes_history_and_old_images_unchanged_from':BASE,
        'private_destination':meta['full_name'],'standalone_html_sha256':sha(OUT/'index.html'),'validation':'passed'}
    (REPORT/'validation/reader-integrity.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return result

def package():
    dest=ROOT/'backups/超级骷髅兵-PC手机阅读器-20261022.zip';dest.parent.mkdir(exist_ok=True)
    instructions='''《超级骷髅兵》PC／手机剧情阅读器

PC：解压后，用Chrome、Edge等现代浏览器打开“打开阅读器.html”。
手机：需使用能运行本地HTML脚本的浏览器；聊天附件预览或文件管理器可能不能运行。本次已验证手机布局与模拟触摸，尚未完成真实手机及私有网页部署验收。

PC从七个阶段进入局部关系图；手机先读核心主线事件卡片。
点击事件可查全部前因和后续。点击支线后，“返回刚才”恢复原位置。
阅读进度与文件→导出／导入JSON，可在设备间携带已读标记和书签。
图片目录提供全书SVG和PNG，不依赖专用阅读器。

本包不含原小说TXT。研究内容仍为待审阅草稿。
阅读器离线可用，GitHub图片说明链接需要登录私有仓库。
项目入口：https://github.com/medillali/writing-vault/blob/main/library/reports/super-skeleton/reading/plot/reader.md
'''
    with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED) as z:
        z.write(OUT/'index.html','打开阅读器.html');z.writestr('使用说明.txt',instructions)
        for ext in ['svg','png']:z.write(REPORT/f'reading/plot/whole-book/tree.{ext}',f'图片/全书树图.{ext}')
    with zipfile.ZipFile(dest) as z:
        assert z.testzip() is None and z.read('打开阅读器.html')==(OUT/'index.html').read_bytes()
        assert len(z.namelist())==4
    return {'path':str(dest),'bytes':dest.stat().st_size,'sha256':sha(dest)}

if __name__=='__main__':
    print(json.dumps({'integrity':verify(),'package':package()},ensure_ascii=False,indent=2))
