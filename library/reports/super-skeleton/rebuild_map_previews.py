"""从同一全书原图裁切GitHub可读预览，保留原坐标及连线。"""
from pathlib import Path
from PIL import Image
import json
HERE=Path(__file__).resolve().parent
ROOT=HERE/'reading/plot'
Image.MAX_IMAGE_PIXELS=150_000_000
im=Image.open(ROOT/'whole-book/tree.png').convert('RGB')
meta=json.loads((ROOT/'whole-book/manifest.json').read_text(encoding='utf-8'))
out=ROOT/'map';out.mkdir(exist_ok=True)
result=[]
for name,node,label in [('opening','v01-e03','主线开始分枝'),('junction','v04-e08','中前段的多线交汇'),('sea-emperor','v11-e02','海皇危机交汇'),('ending','v18-e07','终局分枝与暗线')]:
    p=meta['positions'][node];x=round(max(0,min(im.width-1100,p['x']+p['width']/2-550)));y=round(max(0,min(im.height-900,p['y']+p['height']/2-450)))
    im.crop((x,y,x+1100,y+900)).save(out/(name+'.png'),optimize=True)
    result.append({'file':name+'.png','anchor':node,'label':label,'original_rect':[x,y,1100,900]})
(out/'previews.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('4个原坐标局部预览已生成')
