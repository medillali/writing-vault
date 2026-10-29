"""只冻结候选ID/来源位置，不把未审终点占位称完成。"""
import json,pathlib,hashlib,sys,collections
sys.stdout.reconfigure(encoding='utf-8');H=pathlib.Path(__file__).resolve().parent
read=lambda p:json.loads(p.read_text(encoding='utf-8'));result={}
for pool,filename in [('historical','historical-question-pool.json'),('local','local-question-pool.json')]:
 d=read(H/filename);rows=d['candidates'];keys=[dict(candidate_id=x['candidate_id'],volume=x['volume'],original_path=x['original_path'],original_field=x.get('original_field',x.get('entry_type')),original_index=x['original_index'],atomic_index=x.get('atomic_index')) for x in rows]
 result[pool]=dict(path=filename,count=len(rows),by_volume={str(v):sum(x['volume']==v for x in rows) for v in range(1,9)},candidate_identity_sha256=hashlib.sha256(json.dumps(keys,ensure_ascii=False,sort_keys=True).encode('utf-8')).hexdigest(),ids=[x['candidate_id'] for x in rows])
result['note']='候选ID及原记录位置已稳定；分工只写各自adjudications文件，主池只由本代理合并。不是终点判定全部完成。'
result['already_adjudicated_history_1_to_4']=[x['candidate_id'] for x in read(H/'historical-question-pool.json')['candidates'] if x['volume']<=4 and x['terminal_assessment']['review_progress']=='reviewed-draft']
(H/'candidate-id-freeze.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:{kk:vv for kk,vv in val.items() if kk!='ids'} if isinstance(val,dict) else val for k,val in result.items()},ensure_ascii=False))
