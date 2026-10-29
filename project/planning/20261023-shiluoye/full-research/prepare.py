"""只准备真实来源的研究范围和读章入口，不登记已读。"""
import pathlib,json,hashlib,re,sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT=pathlib.Path(__file__).resolve().parents[3];WORK=pathlib.Path(__file__).resolve().parent;VAULT=ROOT/'writing-vault'
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
manifest=load(VAULT/'private-sources/normalized/manifest.json')
entries=manifest.get('sources',manifest) if isinstance(manifest,dict) else manifest
units=load(VAULT/'library/reports/collection/reading-units.json')
selected=[('zongheng-tianxia','src-2a13958390274509b2af019f6b12d981'),('tianxia-wushuang','src-d8926e2a35f04bcf8139cff0ea516bbd'),('zhanlong','src-20f2d16e3d1b472fa4b230ab0e1770c9')]
summary=[]
for slug,sid in selected:
    source=load(VAULT/'library/sources'/f'{sid}.json');rev=next(r for r in source['revisions'] if r['revision']==source['revision'])
    raw=next(s for s in entries if s['source_id']==sid)
    normalized=pathlib.Path(raw['normalized_path'])
    if not normalized.is_absolute():normalized=VAULT/'private-sources/normalized'/normalized
    assert normalized.is_file(),normalized
    assert hashlib.sha256(normalized.read_bytes()).hexdigest()==source['revision']
    text_lines=normalized.read_text(encoding='utf-8').splitlines(keepends=True)
    chapters={c['chapter_id']:c for c in rev['chapters']}
    volume=0;volumes={};preface=[]
    for unit in units[sid]['units']:
        match=re.match(r'^卷([一二三四五六七八九十]+)',unit['title'])
        if match:
            number={'一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9,'十':10}.get(match.group(1))
            assert number is not None,unit['title']
            volume=number
        record={**unit,'segments':[chapters[c] for c in unit['segment_ids']]}
        if not volume:preface.append(record);continue
        volumes.setdefault(volume,[]).append(record)
    directory=WORK/slug
    data={'slug':slug,'source_id':sid,'revision':source['revision'],'title':source['title'],'normalized_path':str(normalized),'chapters':rev['chapters'],'preface':preface,'volumes':[{'volume':number,'units':items,'body_units':sum(u['kind'] in ['body','prologue'] for u in items),'characters':sum(len(''.join(text_lines[chapters[c]['start_line']-1:chapters[c]['end_line']])) for u in items for c in u['segment_ids'])} for number,items in sorted(volumes.items())]}
    save(directory/'source.json',data)
    summary.append({'book':source['title'],'source_id':sid,'volumes':[{'volume':v['volume'],'body_units':v['body_units'],'characters':v['characters'],'first':v['units'][0]['title'],'last':v['units'][-1]['title']} for v in data['volumes']],'preface_segments':sum(len(u['segment_ids']) for u in preface)})
save(WORK/'source-plan.json',summary)
print(json.dumps(summary,ensure_ascii=False))
