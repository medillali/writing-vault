from pathlib import Path
from PIL import Image
import json, math
Image.MAX_IMAGE_PIXELS=400_000_000
O=Path('.verify/tree-maps-20261025/library/reports/two-books-full-20261025')
for f in ('zeidan','leveling'):
 d=O/f/'plot';m=json.loads((d/'whole-book/manifest.json').read_text(encoding='utf-8'));pre=json.loads((d/'map/previews.json').read_text(encoding='utf-8'))
 e=next(c for c in pre['crops'] if c['name']=='ending');p=m['positions'][e['id']]
 nearby=[m['positions'][t['id']] for t in m['threads'] if abs(m['positions'][t['id']]['x']-p['x'])<700 and abs(m['positions'][t['id']]['y']-p['y'])<600]
 if nearby:
  b=min(nearby,key=lambda b:math.hypot(b['x']-p['x'],b['y']-p['y']))
  x=min(p['x'],b['x']);y=min(p['y'],b['y']);w=max(p['x']+p['width'],b['x']+b['width'])-x;h=max(p['y']+p['height'],b['y']+b['height'])-y
  if w+60<=e['width'] and h+60<=e['height']:
   e['left']=max(0,min(m['width']-e['width'],int(math.floor(x+w/2-e['width']/2+.5))))
   e['top']=max(0,min(m['height']-e['height'],int(math.floor(y+h/2-e['height']/2+.5))))
   with Image.open(d/'whole-book/tree.png') as image:image.crop((e['left'],e['top'],e['left']+e['width'],e['top']+e['height'])).save(d/'map/ending.png')
 (d/'map/previews.json').write_bytes((json.dumps(pre,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
