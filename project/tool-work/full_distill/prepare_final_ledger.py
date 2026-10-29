"""为终点人工复核排列全部原问；绝不自动升级阶段结论。"""
import copy
import json
from persist import HERE,SID,SOURCE,json_text

reports=[json.loads((HERE/f'vol{n:02d}.json').read_text(encoding='utf-8')) for n in range(1,19)]
target=HERE/'question-ledger-review.json'
assert not target.exists(), '不要覆写已有终点审计进度'
seeds={}
for name in ['question-ledger-01-07.json','question-ledger-08-12.json']:
    if (HERE/name).exists():
        for item in json.loads((HERE/name).read_text(encoding='utf-8'))['entries']:
            seeds[(item['origin_volume'],item['source_question_index'])]=item
entries=[]
for report in reports:
    for i,q in enumerate(report['questions'],1):
        n=report['volume']
        entry=copy.deepcopy(seeds.get((n,i),{}))
        entry['seed_review_scope']=entry.get('latest_volume',0)
        entry.update(id=f'q-v{n:02d}-{i:02d}',origin_volume=n,origin_volumes=[n],source_question_index=i,
                     question=q['question'],origin_evidence=q['evidence'],reviewed_at_book_end=False)
        entry.setdefault('status','pending')
        entry.setdefault('answer','')
        entry.setdefault('answer_evidence',[])
        entry.setdefault('revisit_focus',q.get('reason',''))
        entries.append(entry)
result={'schema_version':1,'source_id':SID,'revision':SOURCE['revision'],
        'completion':'pending_book_end_review','coverage':{'volumes':list(range(1,19))},
        'entries':entries,'pending_questions':[e['id'] for e in entries],
        'revision_sources':[{'volume':r['volume'],'revisions':r['revisions_to_earlier']} for r in reports],
        'revision_reviews':[{'origin_volume':r['volume'],'source_revision_index':i,'original_revision':copy.deepcopy(revision),
                             'review':'','evidence':[],'reviewed_at_book_end':False}
                            for r in reports for i,revision in enumerate(r['revisions_to_earlier'],1)],
        'policy':'原问题逐项保留；阶段答案只是复核种子，不代表已读终点后文。'}
target.write_text(json_text(result),encoding='utf-8')
print(json_text({'questions':len(entries),'reviewed_at_book_end':0,'file':str(target)}))
