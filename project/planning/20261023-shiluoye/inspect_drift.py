import pathlib,json,collections,sys
sys.stdout.reconfigure(encoding='utf-8')
root=pathlib.Path(__file__).resolve().parents[2];v=root/'writing-vault'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
units=read(v/'library/reports/collection/reading-units.json')
for p in (v/'library/sources').glob('*.json'):
    s=read(p);r=next(x for x in s['revisions'] if x['revision']==s['revision']);mapped=units.get(s['source_id'],{});actual=[c for u in mapped.get('units',[]) for c in u['segment_ids']];expected=[c['chapter_id'] for c in r['chapters']]
    print('SOURCE',s['source_id'],s.get('title'),s['revision'],len(r['chapters']),len(actual),'map_revision',mapped.get('source_revision'),'extra',sorted(set(actual)-set(expected))[:10],'missing',sorted(set(expected)-set(actual))[:10])
groups=collections.Counter()
for folder in ['characters','scenes','patterns']:
    for p in (v/'library'/folder).glob('*.json'):
        a=read(p);groups['/'.join(a.get('origin_key','').split('/')[:2])]+=1
print('ASSETGROUPS',json.dumps(dict(groups),ensure_ascii=False))
for p in (v/'library').rglob('*.json'):
    if 'graph' in p.name:
        g=read(p)
        if 'nodes' in g:print('GRAPH',p.relative_to(v),g.get('owner'),g.get('updated_at'))
for p in (v/'exchanges/runs').glob('*.json'):
    r=read(p);s=read(v/'library/sources'/(r['source_id']+'.json'));revision=next(x for x in s['revisions'] if x['revision']==r['source_revision']);missing=[c for c in revision['chapters'] if c['chapter_id'] not in set(r['completed_chapters']+r['pending_chapters'])]
    print('RUN',r['run_id'],len(r['completed_chapters']),'missing',[(c['chapter_id'],c['title']) for c in missing[:10]],'missing_count',len(missing))
