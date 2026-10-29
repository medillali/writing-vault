import copy,hashlib,json
from audit_evidence import H
p=H/'adjudications-local-v07-part02.json';raw=p.read_bytes();d=json.loads(raw);a=next(x for x in d if x['candidate_id']=='v07-local-local_historical_questions-045-01');b=copy.deepcopy(a)
b['rationale']='父承小时被撞/赔四万，与梦中救主及犹豫反应部分呼应，但未完整口述事故因主，不能将梦全部细节作客观重演。母则214—215已明确亡八年、陆何实际扫母墓，死因未给；不写成仅离开而存死未知，也不由陆错过临终的自责证明电竞致死。'
b['later_chapters']=sorted(set(a['later_chapters']+[214,215]))
o=dict(status='proposal_pending_primary_approval_do_not_merge_yet',candidate_id=a['candidate_id'],signed_batch_sha256=hashlib.sha256(raw).hexdigest(),before=a,after=b,unchanged_other_items=59,reason='无双母已亡与前书母离家限制串用；只提独立delta，当前已签batch尚未修改。',source_match='完整读取primary无双214/215/216四栏；214祭日，215母16岁时亡/现24八年、陆何扫墓，死因未知。')
(H/'local07-part02-mother-correction-proposal.json').write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(o['signed_batch_sha256'])
