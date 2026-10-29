import pathlib,json,sys,re,collections
sys.stdout.reconfigure(encoding='utf-8')
root=pathlib.Path(__file__).resolve().parents[2]
m=json.loads((root/'writing-vault/private-sources/normalized/manifest.json').read_text(encoding='utf-8'))
digits={'零':0,'〇':0,'一':1,'二':2,'两':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9}
units={'十':10,'百':100,'千':1000,'万':10000}
def number(t):
    if t.isdigit():return int(t)
    if all(ch in digits for ch in t):return int(''.join(str(digits[ch]) for ch in t))
    n=0;v=0
    for c in t:
        if c in digits:v=digits[c]
        elif c in units:n+=(v or 1)*units[c];v=0
        else:return None
    return n+v
audit=[]
for s in m['sources']:
    if '情终流水' in s['title']:continue
    body=[]; headings=[]
    for c in s['chapters']:
        mat=re.search(r'第([〇零一二两三四五六七八九十百千万0-9]+)章',c['title'])
        if mat:body.append({**c,'printed_number':number(mat[1])})
        else:headings.append(c)
    nums=[c['printed_number'] for c in body]
    counts=collections.Counter(nums)
    duplicate=[n for n,c in counts.items() if c>1]
    missing=sorted(set(range(1,max(nums)+1))-set(nums)) if nums else []
    a={'source_id':s['source_id'],'title':s['title'],'indexed_segments':len(s['chapters']),'numbered_chapter_entries':len(body),'other_segments':len(headings),'highest_printed_number':max(nums) if nums else None,'duplicate_printed_numbers':duplicate,'missing_printed_numbers':missing,'chapter_id_rule':'按出现顺序；不因重号去重','body_chapter_ids':[c['chapter_id'] for c in body],'nonbody_segments':headings}
    audit.append(a)
    print(json.dumps({k:v for k,v in a.items() if k not in ['body_chapter_ids','nonbody_segments']},ensure_ascii=False))
    if missing:
        print('jumps',[(body[i-1]['title'],c['title'],c['start_line']) for i,c in enumerate(body) if i and c['printed_number']>body[i-1]['printed_number']+1][:20])
    print('nonbody',[(c['chapter_id'],c['title']) for c in headings[:20]])
out=root/'writing-vault/library/reports/collection';out.mkdir(parents=True,exist_ok=True)
(out/'chapter-audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
