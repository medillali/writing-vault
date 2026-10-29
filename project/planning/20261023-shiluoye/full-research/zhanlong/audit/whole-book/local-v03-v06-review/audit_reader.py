"""只读审计输入与固定凭据；不判题、不改主池或正式库。"""
from pathlib import Path
import collections
import re
import datetime
import hashlib
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent
AUDIT=H.parent
BOOK=AUDIT.parents[1]
ROOT=BOOK.parents[3]
FORMAL=ROOT/'writing-vault/library/reports/zhanlong'

def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def out(value):print(json.dumps(value,ensure_ascii=False,indent=2))
pool=read(AUDIT/'local-question-pool.json')
rows=pool['candidates']
cmd=sys.argv[1]
if cmd=='init':
    assert pool['pending_inputs']==[]
    historical=read(AUDIT/'historical-question-pool.json')
    assert historical['pending_inputs']==[]
    targets={str(v):[r['candidate_id'] for r in rows if r['volume']==v] for v in [3,6]}
    files=[AUDIT/'local-question-pool.json',AUDIT/'historical-question-pool.json',AUDIT/'WORKFLOW.md',BOOK/'source.json',BOOK/'primary-focused-rereads.json']
    files+=sorted((BOOK/'primary-ending-reread').glob('*'))
    for v in range(1,7):
        files += [FORMAL/f'vol{v:02d}-{kind}' for kind in ['analysis.json','cards.json','graph.json','report.md','handoff.md','chapter-notes.jsonl'] if (FORMAL/f'vol{v:02d}-{kind}').exists()]
    files += sorted(FORMAL.glob('*corrections*.json'))
    receipt=dict(status='inputs_frozen_for_independent_adjudication',actual_reviewer='zongheng_vol05_full',
                 fixed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                 reading_attribution='本人实际全文：卷3 prefix raw505—653、卷6 raw1180—1386；卷3尾为primary原文实读，其他卷为其原读者。全书终评按正式派生材料与注明的定向原文复核，不宣个人重读全书。',
                 local_pool_count=len(rows),historical_pool_count=len(historical['candidates']),
                 assigned_volumes=[3,6],assigned_candidate_ids=targets,
                 assigned_counts={v:len(ids) for v,ids in targets.items()},
                 input_sha256={p.relative_to(ROOT).as_posix():sha(p) for p in files if p.is_file()},
                 prohibited='不改主池、正式库、冻结分卷、root签收或发布文件；本目录只保存独立研究与输入凭据。')
    target=H/'input-manifest.json'
    assert not target.exists()
    target.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    out(dict(counts=receipt['assigned_counts'],all_local=len(rows),historical=len(historical['candidates']),
             inputs=len(receipt['input_sha256']),manifest_sha256=sha(target),pool_sha256=sha(AUDIT/'local-question-pool.json')))
elif cmd=='show':
    volume,lo,hi=map(int,sys.argv[2:5]);selected=[r for r in rows if r['volume']==volume]
    for n,row in enumerate(selected[lo-1:hi],lo):
        print(f'BEGIN candidate {volume}:{n} {row["candidate_id"]}')
        out(row)
        print(f'END candidate {volume}:{n} {row["candidate_id"]}')
elif cmd=='notes':
    volume,lo,hi=map(int,sys.argv[2:5])
    notes=[json.loads(line) for line in (FORMAL/f'vol{volume:02d}-chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if line.strip()]
    for row in notes:
        n=int(row['chapter_id'].split('-')[-1])
        if lo<=n<=hi:
            print(f'BEGIN notes {row["chapter_id"]}')
            out(row)
            print(f'END notes {row["chapter_id"]}')
elif cmd=='file':
    rel=sys.argv[2];lo=int(sys.argv[3]);hi=int(sys.argv[4]);lines=(ROOT/rel).read_text(encoding='utf-8').splitlines()
    print(f'BEGIN {rel} lines {lo}-{min(hi,len(lines))}/{len(lines)}')
    for n,line in enumerate(lines[lo-1:hi],lo):print(f'{n}: {line}')
    print(f'END {rel}')
elif cmd=='locate':
    source=read(BOOK/'source.json')
    for n in map(int,sys.argv[2:]):
        out(dict(line=n,chapter=next(c for c in source['chapters'] if c['start_line']<=n<=c['end_line'])))
elif cmd=='compact':
    volume,lo,hi=map(int,sys.argv[2:5]);selected=[r for r in rows if r['volume']==volume]
    seen=set()
    for n,row in enumerate(selected[lo-1:hi],lo):
        record_key=(row['original_path'],row['original_field'],row['original_index'])
        print(f'BEGIN candidate {volume}:{n} {row["candidate_id"]}')
        if record_key not in seen:
            out(dict(original_path=row['original_path'],original_field=row['original_field'],original_index=row['original_index'],
                     original_record=row['original_record'],original_evidence=row['original_evidence']))
            seen.add(record_key)
        else:print('原记录/证据与本输出此前同original_index完整记录逐值相同。')
        out(dict(candidate_id=row['candidate_id'],atomic_index=row['atomic_index'],title=row['title']))
        print(f'END candidate {volume}:{n} {row["candidate_id"]}')
elif cmd=='search-notes':
    keyword=sys.argv[2];lo=int(sys.argv[3]) if len(sys.argv)>3 else 1;hi=int(sys.argv[4]) if len(sys.argv)>4 else 6
    for volume in range(lo,hi+1):
        notes=[json.loads(line) for line in (FORMAL/f'vol{volume:02d}-chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if line.strip()]
        for row in notes:
            if keyword in json.dumps(row,ensure_ascii=False):
                print(f'BEGIN matching notes volume={volume} {row["chapter_id"]}')
                out(row)
                print(f'END matching notes volume={volume} {row["chapter_id"]}')
elif cmd=='selected-notes':
    volume=int(sys.argv[2]);wanted=set(map(int,sys.argv[3:]))
    notes=[json.loads(line) for line in (FORMAL/f'vol{volume:02d}-chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if line.strip()]
    for row in notes:
        if int(row['chapter_id'][3:]) in wanted:
            print(f'BEGIN notes {row["chapter_id"]}')
            out(row)
            print(f'END notes {row["chapter_id"]}')
elif cmd=='note-locations':
    keyword=sys.argv[2]
    for volume in range(1,7):
        for line in (FORMAL/f'vol{volume:02d}-chapter-notes.jsonl').read_text(encoding='utf-8').splitlines():
            row=json.loads(line)
            if keyword in json.dumps(row,ensure_ascii=False):
                out(dict(volume=volume,chapter_id=row['chapter_id'],title=row.get('title'),start_line=row['start_line'],end_line=row['end_line']))
elif cmd=='source-range':
    lo,hi=map(int,sys.argv[2:4]);source=read(BOOK/'source.json')
    text=Path(source['normalized_path']).read_text(encoding='utf-8').splitlines()
    print(f'BEGIN targeted-source-range L{lo}—L{hi} (不是整章重读声明)')
    for n,line in enumerate(text[lo-1:hi],lo):print(f'L{n}: {line}')
    print(f'END targeted-source-range L{hi}')
elif cmd=='source-matches':
    terms=sys.argv[2:];source=read(BOOK/'source.json')
    for n,line in enumerate(Path(source['normalized_path']).read_text(encoding='utf-8').splitlines(),1):
        if all(term in line for term in terms):print(f'L{n}: {line}')
elif cmd=='batch-item':
    file=sys.argv[2];suffix=sys.argv[3]
    out(next(r for r in read(AUDIT/file) if r['candidate_id'].endswith(suffix)))
elif cmd=='scan-shield-wording':
    def walk(value,path=()):
        if isinstance(value,dict):
            for k,v in value.items():yield from walk(v,path+(k,))
        elif isinstance(value,list):
            for i,v in enumerate(value):yield from walk(v,path+(i,))
        elif isinstance(value,str) and (re.search(r'(10h|10小时|十小时).{0,20}(后|才)',value) or ('公告' in value and '狮' in value)):
            yield dict(path=list(path),value=value)
    for file in sorted(FORMAL.glob('vol03-*')):
        if file.suffix=='.json':
            hits=list(walk(read(file)))
            if hits:out(dict(file=file.relative_to(ROOT).as_posix(),sha256=sha(file),hits=hits))
        elif file.suffix=='.jsonl':
            for i,line in enumerate(file.read_text(encoding='utf-8').splitlines()):
                row=json.loads(line);hits=list(walk(row))
                if hits:out(dict(file=file.relative_to(ROOT).as_posix(),sha256=sha(file),jsonl_index=i,chapter_id=row.get('chapter_id'),reader=row.get('reader'),hits=hits))
        elif file.suffix=='.md':
            for i,line in enumerate(file.read_text(encoding='utf-8').splitlines(),1):
                if re.search(r'(10h|10小时|十小时).{0,20}(后|才)',line) or ('公告' in line and '狮' in line):out(dict(file=file.relative_to(ROOT).as_posix(),line=i,value=line))
elif cmd=='scan-bailining-context':
    def walk(value,path=()):
        if isinstance(value,dict):
            for k,v in value.items():yield from walk(v,path+(k,))
        elif isinstance(value,list):
            for i,v in enumerate(value):yield from walk(v,path+(i,))
        elif isinstance(value,str) and '百里宁' in value:yield dict(path=list(path),value=value)
    files=list((BOOK/'vol06').glob('*'))+list(FORMAL.glob('vol06-*'))+list((ROOT/'writing-vault/library/characters').glob('*.json'))
    for f in files:
        if not f.is_file():continue
        if f.suffix=='.json':
            try:hits=list(walk(read(f)))
            except Exception:continue
            if hits:out(dict(file=f.relative_to(ROOT).as_posix(),sha256=sha(f),hits=hits))
        elif f.suffix=='.jsonl':
            hits=[]
            for i,line in enumerate(f.read_text(encoding='utf-8').splitlines()):
                if not line.strip():continue
                row=json.loads(line)
                for h in walk(row):hits.append(dict(jsonl_index=i,chapter_id=row.get('chapter_id'),reader=row.get('reader'),**h))
            if hits:out(dict(file=f.relative_to(ROOT).as_posix(),sha256=sha(f),hits=hits))
        elif f.suffix=='.md':
            hits=[dict(line=i,value=l) for i,l in enumerate(f.read_text(encoding='utf-8').splitlines(),1) if '百里宁' in l]
            if hits:out(dict(file=f.relative_to(ROOT).as_posix(),sha256=sha(f),hits=hits))
else:raise ValueError(cmd)
