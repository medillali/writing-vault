from save_manual_batch import P,F,read,write,sha
import json,copy
file=P/'adjudications-local-v02-batch010.json';rows=read(file);cid='v02-local-chapter_unresolved_index-0085-01'
before=next(x for x in rows if x['candidate_id']==cid);after=copy.deepcopy(before)
after.update(status='answered',rationale='350主收寒铁剑后许补偿，416约送龙吻时亲自联系“你连寒铁剑都送我了”，明确回馈关系；418龙吻实交林且林坚持转20万元，419已80级实穿。补偿承诺已有具体礼物与收用后证，不再以没有逐字偿清账单留作全未知；这是半赠半卖的亲密互赠，不写全白送、等价现金债已结清，也不把交剑附会为性同意。')
for k in [416,418,419]:
    if k in after['later_chapters']:continue
    f=F/'vol02-chapter-notes.jsonl';n=next(json.loads(l) for l in f.read_text(encoding='utf-8').splitlines() if l.strip() and json.loads(l)['chapter_id']==f'ch-{k:04d}')
    after['later_chapters'].append(k);after['later_evidence'].append(dict(source_id=n['source_id'],revision=n['revision'],chapter_id=n['chapter_id'],start_line=n['start_line'],end_line=n['end_line'],claim_kind='fact',evidence_access='正式完整四栏派生；416另本轮BEGIN-END定向原文复读',material_path='writing-vault/library/reports/zhanlong/vol02-chapter-notes.jsonl',material_sha256=sha(f),source_reader=n['reader']))
out=P/'hantie-gift-compensation-proposal.json';assert not out.exists();write(out,dict(status='proposal-pending-primary-review-not-applied',reason='本轮完整读416原文，L34751—34753主明确把所送礼与林先送寒铁剑联系；补已有特定回馈而非靠泛互赠倒证。',changes=[dict(path=file.name,candidate_id=cid,input_sha256=sha(file),before=before,after=after,scope='仅此条status/rationale及新增416/418/419证据，其余19逐值不动')]))
print(sha(out))
