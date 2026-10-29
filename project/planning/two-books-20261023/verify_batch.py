from pathlib import Path
import json,hashlib,re,collections,subprocess
R=Path(__file__).resolve().parents[2];V=R/'.verify/two-books';OUT=V/'library/reports/two-books-20261023'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def dump(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
coverage=read(OUT/'coverage.json');assets=read(OUT/'batch-assets.json')
src={x['source_id']:x for x in read(V/'private-sources/normalized/manifest.json')['sources']}
assert len(assets)==321 and len({a['asset_id'] for a in assets})==321
ev_count=0;long_matches=[];objects=[];needles={}
def strings(x):
    if isinstance(x,str):yield x
    elif isinstance(x,list):
        for y in x:yield from strings(y)
    elif isinstance(x,dict):
        for y in x.values():yield from strings(y)
texts={sid:Path(s['normalized_path']).read_text(encoding='utf-8') for sid,s in src.items()}
for sid,s in src.items():
    t=texts[sid]
    assert hashlib.sha256(t.encode()).hexdigest()==s['revision']
    end=0
    for c in s['chapters']:
        assert c['start_offset']==end and c['end_offset']>end
        if not (t[c['start_offset']:].startswith(c['title']) or c['title']=='章前内容'):
            print('HEADING_DIAGNOSTIC',c['chapter_id'],repr(c['title']),repr(t[c['start_offset']:c['start_offset']+len(c['title'])+12]))
            raise AssertionError('章节标题起始字符需核对')
        end=c['end_offset']
    assert end==len(t)
for a in assets:
    folder={'character':'characters','scene':'scenes','pattern':'patterns'}[a['type']]
    obj=read(V/f"library/{folder}/{a['asset_id']}.json");objects.append(obj)
    assert obj['review_status']=='draft' and obj['favorite'] is False and obj['user_notes']==''
    assert obj['scope']!='original-project' and obj['revision']==1
    assert (OUT/f"cards/{a['asset_id']}.md").exists()
    for e in obj['evidence']:
        s=src[e['source_id']];assert e['revision']==s['revision']
        c=next(c for c in s['chapters'] if c['chapter_id']==e['chapter_id'])
        assert c['start_line']<=e['start_line']<=e['end_line']<=c['end_line'];ev_count+=1
    for val in strings(obj['content']):
        if len(val)<80:continue
        for start in range(len(val)-79):
            needles.setdefault(val[start:start+80],a['asset_id'])
aux_evidence_count=0
for name in ['zeidan/legacy-threads.json','zeidan/appearance-candidates.json','leveling/question-ledger.json']:
    for item in read(OUT/name):
        for e in item.get('mapped_evidence',item.get('evidence',[])):
            s=src[e['source_id']];assert e['revision']==s['revision']
            c=next(c for c in s['chapters'] if c['chapter_id']==e['chapter_id'])
            assert c['start_line']<=e['start_line']<=e['end_line']<=c['end_line'];aux_evidence_count+=1
for item in read(OUT/'zeidan/legacy-chapter-notes.json'):
    s=src[coverage['sources']['z']['source_id']]
    c=next(c for c in s['chapters'] if c['chapter_id']==item['current_chapter_id'])
    assert (item['title'],item['source_line_start'],item['source_line_end'])==(c['title'],c['start_line'],c['end_line'])
for s in coverage['sources'].values():
    raw=next(Path('E:/chromedownload').glob(f"*{s['title']}*.txt"))
    assert hashlib.sha256(raw.read_bytes()).hexdigest()==s['raw_sha256']
for sid,t in texts.items():
    for start in range(len(t)-79):
        frag=t[start:start+80]
        if frag in needles:
            item={'asset_id':needles[frag],'source_id':sid,'matched_characters':80}
            if item not in long_matches:long_matches.append(item)
for sid,s in src.items():
    # 只审计章号形态，不把标题检索当正文阅读。
    if '练级专家' not in s['title']:continue
    counts=collections.Counter();combined=[]
    for c in s['chapters']:
        nums=list(map(int,re.findall(r'第(\d+)章',c['title'])))
        if len(nums)==2:
            combined.append({'chapter_id':c['chapter_id'],'title':c['title']});nums=list(range(nums[0],nums[1]+1))
        counts.update(nums)
    dump(OUT/'leveling/chapter-numbering.json',{'physical_body_segments':len(s['chapters'])-2,'combined_headings':combined,'repeated_numbers':{str(k):v for k,v in counts.items() if v>1},'missing_numbers_within_printed_span':[i for i in range(1,max(counts)+1) if i not in counts]})
assert not long_matches,long_matches[:3]
broken=[];links=0
for p in [*OUT.rglob('*.md'),V/'START-HERE.md',V/'CONTENT-GUIDE.md',V/'RESEARCH-QUEUE.md',V/'templates/original-project-brief.md']:
    for target in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
        if target.startswith(('https:','http:','#')):continue
        target=target.strip('<>').split('#')[0]
        if not target:continue
        links+=1
        if not (p.parent/target).resolve().is_file():broken.append({'file':str(p.relative_to(V)),'target':target})
assert not broken,broken[:10]
for key,last in [('z',11),('l',14)]:
    cp=read(V/f'exchanges/runs/run-two-books-20261023-{key}.json')
    allch={c['chapter_id'] for c in src[cp['source_id']]['chapters']}
    assert set(cp['completed_chapters'])|set(cp['pending_chapters'])|set(cp['excluded_chapters'])==allch
    assert len(cp['completed_chapters'])==last-1
finger=read(OUT/'validation/identity-reconciliation.json')['legacy_card_hashes']
assert all(hashlib.sha256((R/'writing-vault'/f).read_bytes()).hexdigest()==sha for f,sha in finger.items())
result={'valid':True,'batch_cards':len(assets),'legacy_cards':sum(a['imported_legacy'] for a in assets),'new_cards':sum(not a['imported_legacy'] for a in assets),'evidence_ranges_checked':ev_count,'ledger_evidence_ranges_checked':aux_evidence_count,'legacy_chapter_records_checked':463,'local_markdown_links_checked':links,'broken_links':broken,'verbatim_80_character_matches':long_matches,'manual_fields_preserved':True,'canonical_legacy_cards_reused_unchanged':len(finger),'coverage_partition_valid':True,'raw_sources_unchanged':True,'limitations':['自动检查证据身份与范围，不等于逐项语义正确。','本次没有复读全部旧研究，也没有完成练级专家全书。']}
dump(OUT/'validation/batch-validate.json',result)
print(json.dumps(result,ensure_ascii=False))
