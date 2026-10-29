from revision import revise
from common import A
import json
r=json.loads((A/'adjudications-local-v01-batch014.json').read_text(encoding='utf-8'))[14]
revise(1,14,r['candidate_id'],'salary-locator',{'rationale':r['rationale'].replace('146主仍期待','147主仍期待'),'later_chapters':[120,132,147,234,445,1353]},'L12934期待5万位于raw147而非146，只修章号/定位，其他语义不变。')
