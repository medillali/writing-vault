from pathlib import Path
import json,sys,hashlib
P=Path(__file__).parent;books=json.loads((P/'sources.json').read_text(encoding='utf-8'))
key=sys.argv[1];start=int(sys.argv[2]);end=int(sys.argv[3]);worker=sys.argv[4] if len(sys.argv)>4 else 'root'
b=books[key];assert 1<=start<=end<=len(b['units'])
body=Path(b['normalized_path']).read_text(encoding='utf-8');lines=body.splitlines()
chunks=[]
for ordinal in range(start,end+1):
 u=b['units'][ordinal-1];chunk='\n'.join(lines[u['start_line']-1:u['end_line']])
 chunks.append(f"\n=== unit {ordinal} | {u['unit_id']} | {u['title']} | L{u['start_line']}-{u['end_line']} ===\n"+'\n'.join(f'L{i}: {line}' for i,line in enumerate(lines[u['start_line']-1:u['end_line']],u['start_line'])))
output='\n'.join(chunks)
assert len(output)<125000,'单次输出过大，请缩小范围，禁止截断正文冒充阅读。'
receipt={'worker':worker,'source_id':b['source_id'],'revision':b['revision'],'start_unit':start,'end_unit':end,'units':[u['unit_id'] for u in b['units'][start-1:end]],'retrieved_characters':len(output),'retrieval_sha256':hashlib.sha256(output.encode()).hexdigest(),'status':'retrieved-for-model-reading'}
log=P/f'retrieval-{worker}.jsonl'
with log.open('a',encoding='utf-8') as f:f.write(json.dumps(receipt,ensure_ascii=False)+'\n')
sys.stdout.reconfigure(encoding='utf-8');print(output)
