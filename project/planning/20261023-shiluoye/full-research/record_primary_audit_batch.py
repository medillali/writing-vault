"""仅在主代理实际逐项读完指定稳定组后调用；记录部分主审，不宣整书完成。"""
from pathlib import Path
import hashlib,json,sys
B=Path(__file__).parent;D=B/sys.argv[1];A=D/'audit/whole-book';p=D/'primary-audit-review-progress.json'
data=json.loads(p.read_text(encoding='utf-8')) if p.exists() else dict(reviewer='primary',status='partial-semantic-review-in-progress',user_approval=False,batches=[])
names=sys.argv[2:]
for name in names:
 q=A/name;rows=json.loads(q.read_text(encoding='utf-8'))
 assert isinstance(rows,list) and all(x.get('candidate_id') and x.get('status') in ['answered','partial','unrecovered','unknown'] and x.get('rationale') for x in rows)
 entry=dict(path=name,sha256=hashlib.sha256(q.read_bytes()).hexdigest(),candidate_ids=[x['candidate_id'] for x in rows],count=len(rows),scope='已逐项读取终点判断、理由与后证章，不冒称由本检查产生正文阅读')
 data['batches']=[x for x in data['batches'] if x['path']!=name]+[entry]
data['distinct_reviewed_candidate_ids']=sorted({k for x in data['batches'] for k in x['candidate_ids']})
data['distinct_reviewed_candidates']=len(data['distinct_reviewed_candidate_ids'])
data['limits']='尚非整书签收；待全部人物弧、重点与两池终点判断逐项主审后，冻结清单另签。'
p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'partial_primary_reviewed_candidates':data['distinct_reviewed_candidates'],'batches':len(data['batches'])}))
