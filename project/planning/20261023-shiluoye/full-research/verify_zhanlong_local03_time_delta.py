from check_volume import WORK,read
import hashlib,json,sys
sys.stdout.reconfigure(encoding='utf-8')
P=WORK/'zhanlong/audit/whole-book';old=P/'local-v03-v06-review/corrections/batch001-time/before.json';new=P/'adjudications-local-v03-batch001.json'
assert hashlib.sha256(old.read_bytes()).hexdigest()=='b88b41c4bec4685328a52e30cdeda2b28536ec7b3bedbd4cb583e366c1e1d7eb'
a,z=read(old),read(new);assert len(a)==len(z)==20
diff=[(x,y) for x,y in zip(a,z) if x!=y];assert len(diff)==1
x,y=diff[0];assert x['candidate_id']==y['candidate_id']=='v03-local-unresolved_and_anomalies-0001-01'
assert {k:v for k,v in x.items() if k!='rationale'}=={k:v for k,v in y.items() if k!='rationale'}
print(json.dumps({'candidate_id':y['candidate_id'],'before':x['rationale'],'after':y['rationale'],'other_values_exactly_unchanged':True,'new_sha256':hashlib.sha256(new.read_bytes()).hexdigest()},ensure_ascii=False))
