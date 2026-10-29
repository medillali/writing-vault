"""只读筛查照顾母亲/选校主体，按逻辑字符串输出，避免JSONL整行截断。"""
from pathlib import Path
import hashlib,json,sys
sys.stdout.reconfigure(encoding='utf-8')
HERE=Path(__file__).resolve().parent
WS=next(p for p in HERE.parents if (p/'writing-vault').is_dir())
BOOK=HERE.parents[2]
FORMAL=WS/'writing-vault/library/reports/tianxia-wushuang'
terms={'mother':['母亲','妈妈','林母','母病'],
       'care':['照顾','照护','照料','护理','看护','陪护'],
       'school':['清华','北大','苏州大学','苏大','离家近']}
def pred(s):
    return any(t in s for t in terms['school']) or (any(t in s for t in terms['mother']) and any(t in s for t in terms['care']))
def visit(v,p=''):
    if isinstance(v,str): return [(p,v)] if pred(v) else []
    if isinstance(v,list): return [r for i,x in enumerate(v) for r in visit(x,p+'/'+str(i))]
    if isinstance(v,dict): return [r for k,x in v.items() for r in visit(x,p+'/'+k)]
    return []
files=set()
for base in [BOOK,FORMAL]:
    files.update(p for p in base.rglob('*') if p.is_file() and p.suffix.lower() in ['.json','.jsonl','.md','.py']
                 and '__pycache__' not in p.parts and not p.name.startswith(('note-1117-','scan_note_1117_','build_note_1117_')))
files.add(WS/'writing-vault/library/characters/chr-bcb0eab749ce507599d2144bd0c27e3c.json')
hits=[]
for f in sorted(files):
    raw=f.read_text(encoding='utf-8-sig')
    if not pred(raw): continue
    if f.suffix=='.json':
        try: matches=visit(json.loads(raw))
        except json.JSONDecodeError: matches=[(f'line:{i}',s) for i,s in enumerate(raw.splitlines(),1) if pred(s)]
    elif f.suffix=='.jsonl':
        matches=[]
        for i,s in enumerate(raw.splitlines(),1):
            try: obj=json.loads(s)
            except json.JSONDecodeError: continue
            for pointer,text in visit(obj): matches.append((f'line:{i}'+pointer,text))
    else:
        matches=[(f'line:{i}',s) for i,s in enumerate(raw.splitlines(),1) if pred(s)]
    if matches:
        hits.append(dict(path=f.relative_to(WS).as_posix(),sha256=hashlib.sha256(f.read_bytes()).hexdigest(),
                         matches=[dict(pointer=p,text=s) for p,s in matches]))
summary={'files_scanned':len(files),'files_with_semantic_string_hits':len(hits),
         'string_hits':sum(len(h['matches']) for h in hits)}
if '--save' in sys.argv:
    bad='陆说当年选苏州大学为了每日照顾母亲'
    affected=[dict(path=h['path'],sha256=h['sha256'],matches=[m for m in h['matches'] if bad in m['text']])
              for h in hits if any(bad in m['text'] for m in h['matches'])]
    adjudications=[r for p in sorted(HERE.glob('adjudications-local-v06-part*.json'))
                  for r in json.loads(p.read_text(encoding='utf-8-sig'))]
    assert len(adjudications)==657
    adjudication_hits=[dict(candidate_id=r['candidate_id'],matches=visit(r)) for r in adjudications if visit(r)]
    result=dict(status='complete_targeted_semantic_string_impact_scan',summary=summary,terms=terms,
                affected_logical_fact_count=1,affected_physical_file_count=len(affected),affected=affected,
                owned_657_count_checked=657,owned_657_matching_candidate_count=len(adjudication_hits),
                owned_657_matches=adjudication_hits,matches=hits,
                boundary='检索定位后完整核对命中逻辑字符串，不冒称重读2172份全文或其全部原章；当前明确错误为1117第一事实句的四个物理副本。旧原件不改。')
    (HERE/'note-1117-impact-scan.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({**summary,'affected_file_count':len(affected),'owned_657_matches':len(adjudication_hits)},ensure_ascii=False))
else:
    print('BEGIN MOTHER/SCHOOL SEMANTIC STRING SCAN')
    for h in hits: print(json.dumps(h,ensure_ascii=False))
    print(json.dumps(summary,ensure_ascii=False))
    print('END MOTHER/SCHOOL SEMANTIC STRING SCAN')
