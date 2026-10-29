from check_volume import WORK,read
import copy,hashlib,json,sys
sys.stdout.reconfigure(encoding='utf-8')
p=WORK/'zhanlong/vol04/continuity-proposal';old=read(p/'before-after.v1.json');new=read(p/'before-after.json')
assert hashlib.sha256((p/'before-after.json').read_bytes()).hexdigest()=='1cb9ad3e1dc0c11616667fcbd1d78db314857fb58ff658c6d3d736d7fda5bee7'
expected=copy.deepcopy(old);added=[]
for field,kind in [('evidence','fact'),('interpretation_evidence','inference')]:
 arr=new['changes'][2]['after'][field]
 assert arr[:-2]==old['changes'][2]['after'][field]
 for ref,chapter,start,end in zip(arr[-2:],['ch-0946','ch-0956'],[70737,71391],[70805,71462]):
  assert ref==dict(source_id='src-20f2d16e3d1b472fa4b230ab0e1770c9',revision='61ab0b114c76446fda554abfafdac8c432cd88afaba7c2541f4473a3902134e3',chapter_id=chapter,start_line=start,end_line=end,claim_kind=kind)
  added.append(ref)
 expected['changes'][2]['after'][field]=arr
assert expected==new
print(json.dumps({'all_other_values_exactly_unchanged':True,'added_evidence':added},ensure_ascii=False))
