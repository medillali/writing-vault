import sys,json,difflib
sys.stdout.reconfigure(encoding='utf-8')
from save_focus_manual import P,A,B,F,ROOT,read,write,sha
old=read(P/'input-receipt.json')['formal_input_sha256'];d=[]
for name,expected in old.items():
 p=ROOT/name;actual=sha(p)
 if actual!=expected:d.append(dict(path=name,expected=expected,actual=actual))
p=F/'vol06-handoff.md';s=B/'vol06/handoff.md';print('MISMATCH',json.dumps(d,ensure_ascii=False));print('STAGE',sha(s),'FORMAL',sha(p));print('\n'.join(difflib.unified_diff(s.read_text(encoding='utf-8').splitlines(),p.read_text(encoding='utf-8').splitlines(),fromfile='stage-vol06-handoff',tofile='formal-vol06-handoff',n=1)))
write(P/'focus-input-metadata-investigation.json',{'status':'read-only-current-file-verification','mismatches':d,'stage_handoff_sha256':sha(s),'current_formal_handoff_sha256':sha(p),'principle':'原input-receipt保持历史；待primary核定仅研究组顶层formal_input_sha256更新，finding与其evidence对象不变。'})
