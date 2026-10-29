"""装配已经人工逐项撰写的裁定，保原候选并校验来源；不生成终点评语。"""
from pathlib import Path
import collections, datetime, hashlib, json, sys
sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;A=H.parent;BOOK=A.parents[1];ROOT=BOOK.parents[3]
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
volume,batch=map(int,sys.argv[1:3]);stem=f'adjudications-local-v{volume:02d}-batch{batch:03d}'
manifest=read(H/'input-manifest.json');pool=A/'local-question-pool.json'
assert sha(pool)==manifest['input_sha256'][pool.relative_to(ROOT).as_posix()]
rows={r['candidate_id']:r for r in read(pool)['candidates']}
source=read(BOOK/'source.json');chapters={int(c['chapter_id'][3:]):c for c in source['chapters']}
authored=read(H/f'authored-v{volume:02d}-batch{batch:03d}.json')
assert 1<=len(authored)<=20
assert len({r['candidate_id'] for r in authored})==len(authored)
assert not (A/f'{stem}.json').exists()
previous=[]
for p in sorted(A.glob(f'adjudications-local-v{volume:02d}-batch*.json')):previous += read(p)
assigned=manifest['assigned_candidate_ids'][str(volume)]
assert [r['candidate_id'] for r in authored]==assigned[len(previous):len(previous)+len(authored)]
now=datetime.datetime.now(datetime.timezone.utc).isoformat();output=[]
for decision in authored:
    row=rows[decision['candidate_id']]
    assert row['volume']==volume
    assert decision['status'] in ['answered','partial','unrecovered','unknown']
    assert len(decision['rationale'])>=35 and decision['audit_domain']
    refs=[]
    for spec in decision['refs']:
        n,start,end,*kind=spec;c=chapters[n]
        assert c['start_line']<=start<=end<=c['end_line'],(row['candidate_id'],spec,c)
        refs.append(dict(source_id=source['source_id'],revision=source['revision'],chapter_id=c['chapter_id'],start_line=start,end_line=end,claim_kind=kind[0] if kind else 'fact'))
    item={k:v for k,v in row.items() if k!='terminal_assessment'}
    item.update(status=decision['status'],audit_domain=decision['audit_domain'],rationale=decision['rationale'],
                later_chapters=list(dict.fromkeys(spec[0] for spec in decision['refs'])),later_evidence=refs,
                actual_reviewer='zongheng_vol05_full',reviewed_at=now,
                reading_attribution=decision.get('reading_attribution','原文初读归属：本裁定者卷3前149片与卷6；primary卷3尾100片，其他卷按原reader。当前终评列证按本人原实读、实际派生接读或source-checks列明的定向原文复核使用，不冒领他人全文。'),
                source_candidate_pool_sha256=sha(pool),review_status='draft_pending_primary_semantic_review')
    output.append(item)
dump(A/f'{stem}.json',output)
md=[f'# 卷{volume}本地候选终评第{batch:03d}批','',f'人工终评{len(output)}项，待primary逐项主审；不改原池/冻结卷。原题与原记录完整保存在同名JSON。','']
for r in output:
    md += ['## '+r['candidate_id'],'','原子题：'+r['title'],'','终点：'+r['status']+' / '+r['audit_domain'],'',r['rationale'],'',
           '证据：'+'；'.join(f"raw{int(e['chapter_id'][3:])} L{e['start_line']}—{e['end_line']} ({e['claim_kind']})" for e in r['later_evidence']),'']
(A/f'{stem}.md').write_text('\n'.join(md),encoding='utf-8')
all_rows=previous+output
state_path=H/'review-state.json'
state=read(state_path) if state_path.exists() else dict(actual_reviewer='zongheng_vol05_full',input_manifest_sha256=sha(H/'input-manifest.json'),volumes={})
state['volumes'][str(volume)]=dict(assigned=len(assigned),drafted=len(all_rows),next_candidate_index=len(all_rows)+1 if len(all_rows)<len(assigned) else None,
    drafted_ids=[r['candidate_id'] for r in all_rows],batches=batch,status='in_progress' if len(all_rows)<len(assigned) else 'local_adjudication_drafts_complete_pending_primary')
state['updated_at']=now;dump(state_path,state)
receipt=dict(batch=f'{stem}.json',sha256=sha(A/f'{stem}.json'),count=len(output),counts=dict(collections.Counter(r['status'] for r in output)),
             original_records_preserved=True,source_bounds_checked=True,source_candidate_pool_unchanged=True,actual_reviewer='zongheng_vol05_full')
dump(H/f'{stem}-validation.json',receipt)
print(json.dumps(receipt,ensure_ascii=False))
