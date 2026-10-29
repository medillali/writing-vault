from pathlib import Path
import sys,json,hashlib,subprocess,collections
sys.stdout.reconfigure(encoding='utf-8')
R=Path(__file__).resolve().parents[2];P=Path(__file__).parent;V=R/'.verify/two-books';O=V/'library/reports/two-books-full-20261025'
def load(p):return json.loads(p.read_text(encoding='utf-8'))
report={};S=load(P/'sources.json')
for k,s in S.items():
 norm=Path(s['normalized_path']);actual=hashlib.sha256(norm.read_bytes()).hexdigest();assert actual==s['revision']
 raw=list(Path('E:/chromedownload').glob('*贼胆*.txt' if k=='z' else '*网游之练级专家*.txt'));assert len(raw)==1
 report[k]={'source_id':s['source_id'],'revision':actual,'raw_original_exists':True,'raw_original_sha256':hashlib.sha256(raw[0].read_bytes()).hexdigest(),'normalized_characters':len(norm.read_text(encoding='utf-8')),'actual_units':len(s['units'])}
baseline=load(P/'baseline-dirty.json');L=R/'writing-vault';changed=[n for n,sha in baseline.items() if hashlib.sha256((L/n).read_bytes()).hexdigest()!=sha]
report['concurrent_changes']=changed
report['unrelated_modified_files_preserved']=len(baseline)
(P/'preflight-result.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,ensure_ascii=False))
