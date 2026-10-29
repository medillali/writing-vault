"""实际定向核833系统后，精准补正确末刀与证据章；未签稿留before。"""
from pathlib import Path
import json,copy
B=Path(__file__).parent/'zhanlong';P=B/'audit/whole-book'
def read(q):return json.loads(q.read_text(encoding='utf-8'))
p=P/'adjudications-history-v02-batch001.json';rows=read(p);r=next(x for x in rows if x['candidate_id']=='v02-question-v02-q-north');before=copy.deepcopy(r)
r['rationale']='罗林早救父、受兵符军田是真实行动；后来叛变杀父/害霜并列异魔君王，588寒荒败。832霜破退路，833系统明确问剑完成击杀、炎龙伤将随后斩尸头，不能写主或御林独杀。410噬灵全焚与416再列军中仍有口径断层，429普通80%恢复不能精确指定该军种复原机制或人数。'
r['later_chapters']=[410,415,416,429,580,585,588,832,833]
s=read(B/'source.json');cs={int(c['chapter_id'][3:]):c for c in s['chapters']}
r['later_evidence']=[{k:s[k] for k in ['source_id','revision']}|{k:cs[n][k] for k in ['chapter_id','start_line','end_line']}|{'claim_kind':'inference'} for n in r['later_chapters']]
dest=P/'history-v02-pre-sign';dest.mkdir(exist_ok=True);assert not (dest/p.name).exists();(dest/p.name).write_bytes(p.read_bytes())
p.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(P/'history-v02-pre-sign-corrections.json').write_text(json.dumps({'reviewer':'primary','basis':'root实际定向读830—833罗林原文命中，833 L63814系统问剑末刀，非主。','changes':[{'file':p.name,'candidate_id':r['candidate_id'],'before':before,'after':r}]},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
