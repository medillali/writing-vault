"""生成自足的OpenSeadragon全书地图；不改研究数据和原图。"""
from pathlib import Path
import base64,hashlib,io,json,math,re,sys
from PIL import Image
HERE=Path(__file__).resolve().parent
SOURCE=HERE/'reading/plot/whole-book'
OUT=HERE/'reading/plot/reader'
CODE=HERE/'map'
Image.MAX_IMAGE_PIXELS=150_000_000

def uri(raw,kind='png'):return 'data:image/'+kind+';base64,'+base64.b64encode(raw).decode()
def build():
    raw=(SOURCE/'tree.png').read_bytes();meta=json.loads((SOURCE/'manifest.json').read_text(encoding='utf-8'))
    im=Image.open(io.BytesIO(raw)).convert('RGB');width,height=im.size
    assert (width,height)==(meta['width'],meta['height'])
    hi=math.ceil(math.log2(max(width,height)));lo=hi-math.ceil(math.log2(max(width,height)/512));tiles={};checks=[]
    for level in range(lo,hi+1):
        factor=2**(hi-level);size=(math.ceil(width/factor),math.ceil(height/factor))
        scaled=im if level==hi else im.resize(size,Image.Resampling.LANCZOS)
        for x in range(math.ceil(size[0]/512)):
            for y in range(math.ceil(size[1]/512)):
                rect=(max(0,x*512-1),max(0,y*512-1),min(size[0],(x+1)*512+1),min(size[1],(y+1)*512+1))
                tile=scaled.crop(rect);b=io.BytesIO();tile.save(b,format='WEBP',lossless=True,method=4);payload=b.getvalue();name=f'{level}/{x}/{y}'
                tiles[name]=uri(payload,'webp');checks.append({'key':name,'size':tile.size,'sha256':hashlib.sha256(payload).hexdigest()})
        print('level',level,'ready',flush=True)
    positions=meta['positions'];volumes=[]
    for number in range(1,19):
        candidates=[(k,p) for k,p in positions.items() if p['volume']==number];key,p=sorted(candidates)[0];volumes.append({'number':number,'event':key,**p})
    data={'width':width,'height':height,'tile_size':512,'overlap':1,'min_level':lo,'max_level':hi,'tiles':tiles,
          'start':positions['v01-e01'],'volumes':volumes,'source_sha256':hashlib.sha256(raw).hexdigest(),
          'svg':(SOURCE/'tree.svg').read_text(encoding='utf-8'),'png':uri(raw)}
    # 全PNG只作为下载数据，不提交给图像解码器；画布按需解码图块。
    engine=(CODE/'vendor/openseadragon.min.js').read_text(encoding='utf-8');engine=re.sub(r'//# sourceMappingURL=.*','',engine)
    engine='/* OpenSeadragon third-party license\n'+(CODE/'vendor/LICENSE.txt').read_text(encoding='utf-8')+'\n*/\n'+engine
    html=(CODE/'template.html').read_text(encoding='utf-8')
    for key,value in {'STYLE':(CODE/'style.css').read_text(encoding='utf-8'),'APP':(CODE/'app.js').read_text(encoding='utf-8'),'ENGINE':engine,'DATA':json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')}.items():html=html.replace(f'/* MAP_{key} */',value)
    OUT.mkdir(parents=True,exist_ok=True);(OUT/'index.html').write_bytes(html.encode('utf-8'))
    manifest={'engine':'OpenSeadragon 6.1.1','tile_format':'WebP lossless','width':width,'height':height,'tile_size':512,'overlap':1,'min_level':lo,'max_level':hi,'tiles':checks,
              'source_png_sha256':data['source_sha256'],'source_svg_sha256':hashlib.sha256((SOURCE/'tree.svg').read_bytes()).hexdigest(),
              'html_bytes':len(html.encode()),'html_sha256':hashlib.sha256(html.encode()).hexdigest()}
    (OUT/'map-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'tiles':len(tiles),'html_bytes':manifest['html_bytes'],'levels':[lo,hi]}))

if __name__=='__main__':build()
