from save_tail_manual import Q,read,write,sha
import hashlib
p=Q/'batch001-before-primary-precision.json';raw=p.read_bytes();lf=raw.replace(b'\r\n',b'\n')
assert sha(p)=='c0f890475026d2b4935c31f3a0722de98745dd19c84639b13dee7b1f2cade87e'
assert hashlib.sha256(lf).hexdigest()=='6f9d27c215f945eb7c97c12d919a8cd0867724941d62a381c485a9ed14b187b9'
write(Q/'batch001-hash-newline-explanation.json',dict(status='verified-byte-level',actual_before_snapshot=p.name,actual_before_file_sha256=sha(p),delta_reported_before_sha256=hashlib.sha256(lf).hexdigest(),reason='保存器Path.write_text在Windows产生CRLF；delta代码对内存JSON的UTF-8/LF字节直接hash，故误把LF序列化指纹标成batch_before_sha256。不是中间文学字段漂移。',proof=dict(lf_normalization_only_equal=True,crlf_count=raw.count(b'\r\n'),json_values_equal=True,first_delivered_rationale_already_contains_1265_restriction=True),current_batch_sha256=sha(Q/'adjudications-local-v06-tail-batch001.json'),correction='真正before文件SHA以actual_before_file_sha256为准，保原delta误标值作为历史；不改当前20对象。'))
print(sha(Q/'batch001-hash-newline-explanation.json'))
