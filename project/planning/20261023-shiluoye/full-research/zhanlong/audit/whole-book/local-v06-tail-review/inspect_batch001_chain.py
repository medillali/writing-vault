from save_tail_manual import Q,read,write,sha
import hashlib,json
p=Q/'adjudications-local-v06-tail-batch001.json';snap=Q/'batch001-before-primary-precision.json';d=read(Q/'batch001-primary-precision-delta.json');s=read(Q/'batch001-pre-delivery-selfcheck-delta.json')
b=read(snap);a=read(p)
print('snapshot_sha',sha(snap),'current_sha',sha(p),'delta_before',d['batch_before_sha256'])
print('snapshot8',b[8]['rationale']);print('selfcheckafter8',s['after']['rationale'])
print('snapshot15',b[15]['rationale'])
# 首次可审SHA来自selfcheck脚本打印的文件。重建同一明确对象以核序列化路径。
z=json.loads(json.dumps(b,ensure_ascii=False));z[8]=s['after'];serialized=(json.dumps(z,ensure_ascii=False,indent=2)+'\n').encode()
print('rebuild_from_selfcheck',hashlib.sha256(serialized).hexdigest())
for i in range(20):
 if b[i]!=z[i]:print('DIFF_SNAPSHOT_SELF',i,[k for k in b[i] if b[i][k]!=z[i][k]])
raw=snap.read_bytes();lf=raw.replace(b'\r\n',b'\n');crlf=lf.replace(b'\n',b'\r\n')
print('lfsha',hashlib.sha256(lf).hexdigest(),'crlfsha',hashlib.sha256(crlf).hexdigest(),'CRLF',raw.count(b'\r\n'))
