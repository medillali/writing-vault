from common import A,P,dump,sha
import json
hits=[];inputs=[]
for p in sorted(A.glob('adjudications-history-*.json')):
 inputs.append({'path':str(p),'sha256':sha(p)})
 raw=json.loads(p.read_text(encoding='utf-8'));rows=raw if isinstance(raw,list) else raw.get('adjudications',raw.get('items',[]))
 for r in rows:
  t=json.dumps(r,ensure_ascii=False)
  if ('20万' in t or '二十万' in t) and any(x in t for x in ['御林','军团','军批','统兵']):hits.append({'file':p.name,'record':r})
dump(P/'cap-historical-adjudications-scan.json',{'purpose':'仅定位/派生复核，root历史文件未改；检索不是原文阅读','inputs':inputs,'hits':hits})
for x in hits:print(json.dumps(x,ensure_ascii=False))
