from revision import revise
from common import A
import json
cid='v01-local-chapter_unresolved_index-0210-02';r=next(r for r in json.loads((A/'adjudications-local-v01-batch021.json').read_text(encoding='utf-8')) if r['candidate_id']==cid)
revise(1,21,cid,'range-wording',{'rationale':r['rationale'].replace('后来216—232升级','后来221—232升级')},'交付前自核文字范围：219之后不能写后来216，改221；证据数组、状态及其他19对象不变。')
