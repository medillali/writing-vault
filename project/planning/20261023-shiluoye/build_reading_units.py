import pathlib,json,re,sys,collections,hashlib
sys.stdout.reconfigure(encoding='utf-8')
root=pathlib.Path(__file__).resolve().parents[2]
m=json.loads((root/'writing-vault/private-sources/normalized/manifest.json').read_text(encoding='utf-8'))
digits={c:i for i,c in enumerate('零一二三四五六七八九')};digits.update({'〇':0,'两':2})
units={'十':10,'百':100,'千':1000,'万':10000}
def num(t):
    if t.isdigit():return int(t)
    if all(c in digits for c in t):return int(''.join(str(digits[c]) for c in t))
    result=n=0
    for c in t:
        if c in digits:n=digits[c]
        elif c in units:result+=(n or 1)*units[c];n=0
    return result+n
out=root/'writing-vault/library/reports/collection'; out.mkdir(parents=True,exist_ok=True)
all_units={}; audits=[]
for s in m['sources']:
    reading=[];false=[]
    for c in s['chapters']:
        t=c['title']; heading=t[t.find('第'):] if '第' in t else t
        mat=re.match(r'^第([〇零一二两三四五六七八九十百千万0-9]+)章(?:\s*[-—~～]\s*第([〇零一二两三四五六七八九十百千万0-9]+)章)?',heading)
        matches=[x for x in mat.groups() if x] if mat else []
        typ='body' if matches else ('front-matter' if t=='章前内容' else 'volume' if re.fullmatch(r'(?:第[一二三四五六七八九十]+[卷集]|卷[一二三四五六七八九十]+)\s+.{1,40}',t) else 'prologue' if t.startswith('序章') else 'continuation')
        if typ=='continuation':
            assert reading and reading[-1]['kind'] in ['body','prologue'],(s['title'],c)
            reading[-1]['segment_ids'].append(c['chapter_id']);reading[-1]['end_line']=c['end_line']
            false.append({'segment_id':c['chapter_id'],'attached_to':reading[-1]['unit_id'],'reason':'正文句以第一节课或回合开头，被通用解析器误当标题；通过阅读单元映射连接回上一个正文段，不更改已登记的原证据ID。','title':t})
        else:
            numbers=[num(x) for x in matches]
            if len(numbers)>1:
                assert len(numbers)==2 and numbers[1]>=numbers[0],(s['title'],t,numbers)
                numbers=list(range(numbers[0],numbers[1]+1))
            reading.append({'unit_id':c['chapter_id'],'segment_ids':[c['chapter_id']],'title':t,'kind':typ,'printed_numbers':numbers,'start_line':c['start_line'],'end_line':c['end_line']})
    index_fields=[[c.get(k) for k in ['chapter_id','title','start_line','end_line']] for c in s['chapters']]
    index_fingerprint=hashlib.sha256(json.dumps(index_fields,ensure_ascii=False,separators=(',',':')).encode('utf-8')).hexdigest()
    all_units[s['source_id']]={'source_revision':s['revision'],'index_fingerprint':index_fingerprint,'units':reading,'index_corrections':false}
    numbers=[n for u in reading for n in u['printed_numbers']];cnt=collections.Counter(numbers)
    audit={'source_id':s['source_id'],'title':s['title'],'indexed_segments':len(s['chapters']),'logical_numbered_entries':sum(u['kind']=='body' for u in reading),'prologue_entries':sum(u['kind']=='prologue' for u in reading),'front_matter_entries':sum(u['kind']=='front-matter' for u in reading),'volume_heading_entries':sum(u['kind']=='volume' for u in reading),'combined_heading_entries':sum(len(u['printed_numbers'])>1 for u in reading),'highest_printed_number':max(numbers),'duplicate_numbers':[n for n,c in cnt.items() if c>1],'missing_numbers_after_combined_ranges':sorted(set(range(1,max(numbers)+1))-set(numbers)),'false_heading_segments':false,'numbering_is_not_semantic_reading':True}
    audits.append(audit);print(json.dumps({k:v for k,v in audit.items() if k not in ['false_heading_segments']},ensure_ascii=False))
(out/'reading-units.json').write_text(json.dumps(all_units,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(out/'chapter-audit.json').write_text(json.dumps(audits,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('ZONGHENG VOLUMES')
s=next(s for s in m['sources'] if '纵横天下' in s['title']);last=None
for c in s['chapters']:
    vol=c['title'].split(' 第')[0] if c['title'].startswith('卷') else None
    if vol and vol!=last:print(c['chapter_id'],c['title']);last=vol
