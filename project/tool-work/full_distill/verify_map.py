import sys
sys.dont_write_bytecode=True
from pathlib import Path
import base64,hashlib,io,json,math,re,zipfile
from urllib.parse import unquote
from PIL import Image
from verify_plot_images import ROOT,VAULT,REPORT,GH,command,git
BASE='ca64b73379d524a28b12db1047c9ef016a758305'
Image.MAX_IMAGE_PIXELS=150_000_000
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify():
    folder=REPORT/'reading/plot/reader';text=(folder/'index.html').read_text(encoding='utf-8')
    data=json.loads(re.search(r'const MAP_DATA=(.*?);</script>',text,re.S).group(1));manifest=read(folder/'map-manifest.json')
    assert digest(folder/'index.html')==manifest['html_sha256']
    original=Image.open(REPORT/'reading/plot/whole-book/tree.png').convert('RGB')
    expected=[];pixel_checks=0
    for level in range(data['min_level'],data['max_level']+1):
        f=2**(data['max_level']-level);w,h=math.ceil(original.width/f),math.ceil(original.height/f)
        for x in range(math.ceil(w/512)):
            for y in range(math.ceil(h/512)):expected.append(f'{level}/{x}/{y}')
    assert set(expected)==set(data['tiles']) and len(expected)==589
    for item in manifest['tiles']:
        raw=base64.b64decode(data['tiles'][item['key']].split(',',1)[1]);assert hashlib.sha256(raw).hexdigest()==item['sha256']
        image=Image.open(io.BytesIO(raw));assert list(image.size)==item['size']
        level,x,y=map(int,item['key'].split('/'))
        if level==data['max_level']:
            rect=(max(0,x*512-1),max(0,y*512-1),min(original.width,(x+1)*512+1),min(original.height,(y+1)*512+1))
            assert image.convert('RGB').tobytes()==original.crop(rect).tobytes();pixel_checks+=1
    assert pixel_checks==434
    assert hashlib.sha256(base64.b64decode(data['png'].split(',',1)[1])).hexdigest()==digest(REPORT/'reading/plot/whole-book/tree.png')
    assert data['svg']==(REPORT/'reading/plot/whole-book/tree.svg').read_text(encoding='utf-8')
    assert (REPORT/'map/vendor/LICENSE.txt').read_text(encoding='utf-8') in text
    for preview in read(REPORT/'reading/plot/map/previews.json'):
        x,y,w,h=preview['original_rect'];im=Image.open(REPORT/'reading/plot/map'/preview['file']).convert('RGB')
        assert im.tobytes()==original.crop((x,y,x+w,y+h)).tobytes()
    protected=['library/sources','library/characters','library/scenes','library/patterns','history','books','exchanges','library/reports/super-skeleton/reading/plot/whole-book','library/reports/super-skeleton/reading/plot/images']
    assert not git('diff',BASE,'--',*protected).strip()
    unrelated=git('ls-files','--others','--exclude-standard','--',*protected).splitlines()
    excluded={name:digest(VAULT/name) for name in unrelated}
    assert digest(folder/'cards.html')==read(REPORT/'validation/reader-integrity.json')['standalone_html_sha256']
    results={'whole_image':[original.width,original.height],'tiles':589,'lossless_native_tiles_pixel_verified':pixel_checks,'preview_crops_pixel_verified':4,
        'tracked_source_files_unchanged_from':BASE,'untracked_source_files_excluded':excluded,'html_sha256':manifest['html_sha256'],'full_license_embedded':True,'original_card_reader_preserved':True,
        'codex_in_app_browser':'localhost actual drag and wheel zoom verified','public_website_deployed':False,'real_mobile_device_verified':False}
    # 先建立核验入口，再验证包含该链接的阅读页面。
    result=REPORT/'validation/map-integrity.json';result.write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    pages=read(REPORT/'reading/manifest.json')['pages'];links=0
    assert len(pages)==300
    for name,sha in pages.items():
        p=REPORT/'reading'/name;assert digest(p)==sha
        for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
            if target.startswith(('http:','https:','#','mailto:')):continue
            target=unquote(target.split('#')[0]);assert (p.parent/target).resolve().exists(),(name,target);links+=1
    results.update(reading_pages=len(pages),valid_local_links=links)
    result.write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    git('diff','--check')
    meta=json.loads(command([GH,'api','repos/medillali/writing-vault','--jq','{full_name,private}']))
    assert meta=={'full_name':'medillali/writing-vault','private':True}
    return results

def package():
    path=ROOT/'backups/超级骷髅兵-地图阅读器-20261023.zip'
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
        z.write(REPORT/'reading/plot/reader/index.html','打开全书地图.html')
        z.write(REPORT/'reading/plot/reader/cards.html','cards.html')
        z.write(REPORT/'map/vendor/LICENSE.txt','OpenSeadragon-LICENSE.txt')
        z.writestr('使用说明.txt','解压后用浏览器打开“打开全书地图.html”。拖动平移，滚轮或双指缩放；左下小地图可跳转，右下“可读大小”看清文字。\n更多菜单可保存PNG、SVG。卡片页可选。页面离线可用，不上传数据。\nCodex也可打开此文件；本机HTTP预览方式见私有GitHub说明页。GitHub仓库页不运行HTML，请下载后打开。\n')
    with zipfile.ZipFile(path) as z:assert z.testzip() is None
    return {'path':str(path),'bytes':path.stat().st_size,'sha256':digest(path)}

if __name__=='__main__':print(json.dumps({'integrity':verify(),'package':package()},ensure_ascii=False,indent=2))
