from revision import revise
from common import A
import json
cid='v01-local-chapter_unresolved_index-0238-01';r=next(r for r in json.loads((A/'adjudications-local-v01-batch024.json').read_text(encoding='utf-8')) if r['candidate_id']==cid)
revise(1,24,cid,'reinforcement-typo',{'rationale':r['rationale'].replace('951余援红草','950余援红草')},'交付前自核950余误写951余，仅改此数，状态/后证/其余6不变。')
