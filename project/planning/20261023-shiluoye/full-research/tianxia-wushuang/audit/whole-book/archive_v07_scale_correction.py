import pathlib,hashlib,json,sys
sys.stdout.reconfigure(encoding='utf-8');H=pathlib.Path(__file__).resolve().parent
p=H/'adjudications-local-v07-anomalies.json';old=p.read_bytes();out=H/'reviewed-batches/adjudications-local-v07-before-scale-correction.json'
assert not out.exists();out.write_bytes(old)
print(hashlib.sha256(old).hexdigest())
