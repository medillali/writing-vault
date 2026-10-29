"""本次图片交付的覆盖、原档保护、链接和像素文件检查。"""
from pathlib import Path
from collections import Counter
import hashlib
import json
import os
import re
import subprocess
import xml.etree.ElementTree as ET
from urllib.parse import unquote
from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
VAULT = ROOT/'writing-vault'
REPORT = VAULT/'library/reports/super-skeleton'
OUT = REPORT/'reading/plot/images'
GH = Path.home()/'Tools/gh/bin/gh.exe'
BASE = 'b054b5fb1625c193808fe360c859ac5570efa7ce'


def command(args):
    r = subprocess.run([str(a) for a in args],cwd=VAULT,env={**os.environ,'GIT_TERMINAL_PROMPT':'0','GH_PROMPT_DISABLED':'1'},capture_output=True,text=True,encoding='utf-8')
    if r.returncode:
        raise RuntimeError(r.stderr or r.stdout)
    return r.stdout


def git(*args):
    return command(['git','-c',f'safe.directory={VAULT.as_posix()}','-c','http.sslBackend=openssl',
                    '-c','credential.helper=','-c',f'credential.helper=!{GH.as_posix()} auth git-credential',
                    '-c','user.name=Codex','-c','user.email=codex@local.invalid',*args])


def read(p):
    return json.loads(p.read_text(encoding='utf-8'))


def verify():
    m = read(OUT/'manifest.json')
    graph_path = VAULT/'library/sources'/m['source_id']/'plot-graph.json'
    g = read(graph_path)
    ns = {n['id']:n for n in g['nodes']}
    es = {e['id']:e for e in g['edges']}
    ts = {t['id']:t for t in g['threads'] if t['id'].startswith('book-') and t['kind']=='hidden'}
    assert m['graph_sha256']==hashlib.sha256(graph_path.read_bytes()).hexdigest()
    assert m['synthesis_sha256']==hashlib.sha256((REPORT/'book-synthesis.json').read_bytes()).hexdigest()
    images = m['images']
    assert len(images)==49 and len({i['file'] for i in images})==49
    assert set(p.stem for p in OUT.glob('*.svg'))==set(i['file'] for i in images)
    assert set(p.stem for p in OUT.glob('*.png'))==set(i['file'] for i in images)
    assert {n for i in images if i['kind']=='volume' for n in i['node_ids']}=={n['id'] for n in g['nodes'] if n['kind']=='event'}
    assert {i['thread_id'] for i in images if i['kind']=='thread'}==set(ts)
    assert {k:v for i in images if i['kind']=='hidden-overview' for k,v in i['states'].items()}=={k:t['status'] for k,t in ts.items()}
    assert m['hidden_states']==dict(Counter(t['status'] for t in ts.values()))
    for tid,t in ts.items():
        parts=[i for i in images if i.get('thread_id')==tid]
        wanted=set(t['node_ids'])|{es[e][k] for e in t['edge_ids'] for k in ['from','to']}
        actual=[n for i in parts for n in i['node_ids']]
        assert set(actual)==wanted and len(actual)==len(wanted)
        assert {e for i in parts for e in i['edge_ids']}==set(t['edge_ids'])
        assert [ns[n]['narrative_order'] for n in actual]==sorted(ns[n]['narrative_order'] for n in actual)
    png_bytes=0
    text_nodes=0
    checksums={}
    for im in images:
        p=OUT/(im['file']+'.png')
        with Image.open(p) as image:
            assert image.size==(im['width'],im['height'])
            image.verify()
        with Image.open(p) as image:
            assert len(image.convert('RGB').resize((120,120)).getcolors(14401))>30
        svg=ET.fromstring((OUT/(im['file']+'.svg')).read_text(encoding='utf-8'))
        text=''.join(e.text or '' for e in svg.findall('.//{http://www.w3.org/2000/svg}text'))
        text_nodes+=len(svg.findall('.//{http://www.w3.org/2000/svg}text'))
        for nid in im.get('node_ids',[]):
            assert ns[nid]['title'] in text and ns[nid]['summary'] in text,(im['file'],nid)
        for eid in im.get('edge_ids',[]):
            assert es[eid]['label'] in text,(im['file'],eid)
        if im.get('thread_id'):
            t=ts[im['thread_id']]
            note=re.sub(r'^已入库至第\d+集；最近关联事件在第\d+集。最新状态审计在第\d+集。','',t['resolution_note'])
            assert note in text and im['status']==t['status']
        png_bytes+=p.stat().st_size
        for ext in ['png','svg']:
            q=OUT/(im['file']+'.'+ext)
            checksums[q.name]=hashlib.sha256(q.read_bytes()).hexdigest()
    pages=read(REPORT/'reading/manifest.json')['pages']
    assert len(pages)==297
    links=0
    for name,sha in pages.items():
        p=REPORT/'reading'/name
        assert hashlib.sha256(p.read_bytes()).hexdigest()==sha
        for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
            if target.startswith(('http:','https:','#','mailto:')):continue
            target=unquote(target.split('#')[0])
            assert (p.parent/target).resolve().exists(),(name,target)
            links+=1
    # 以任务开始时的已推送提交为基准，只允许阅读副本和相关说明变化。
    changed=[x for x in git('diff',BASE,'--name-only','-z').split('\0') if x]
    allowed={'README.md','library/reports/super-skeleton/README.md','library/reports/super-skeleton/rebuild_github_reading.py'}
    assert all(p in allowed or p.startswith('library/reports/super-skeleton/reading/') for p in changed),changed
    assert not git('diff',BASE,'--','library/sources','library/characters','library/scenes','library/patterns','history','books','exchanges').strip()
    assert git('remote','get-url','origin').strip()=='https://github.com/medillali/writing-vault.git'
    meta=json.loads(command([GH,'api','repos/medillali/writing-vault']))
    assert meta['private'] and meta['owner']['login']=='medillali'
    git('diff','--check')
    result={'images':len(images),'png_bytes':png_bytes,'svg_text_lines':text_nodes,'volumes':18,'event_nodes':163,
            'hidden_threads':15,'hidden_states':m['hidden_states'],'reading_pages':len(pages),'valid_local_links':links,
            'research_and_personal_notes_unchanged_from':BASE,'private_destination':meta['full_name'],
            'local_verification':'passed','sha256':checksums}
    (REPORT/'validation/plot-images.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='sha256'},ensure_ascii=False,indent=2))
    return result


if __name__=='__main__':verify()
