"""把经过阅读审查的单集研究稿写入既有库；不替代文学判断。"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys

ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).parent
sys.path.insert(0,str(ROOT/'distill-novels/scripts'))
from fictionlib.vault import Vault
from fictionlib.graph import save_graph,render_graph,graph_path
from fictionlib.storage import json_text,commit,locked

SID='src-9ff09c395734410b856f77c77a652834'
DIMS=['worldbuilding','characters','plot','style','narrative','dialogue','pacing','themes','continuity']
SOURCE=next(s for s in json.loads((ROOT/'writing-vault/private-sources/normalized/manifest.json').read_text(encoding='utf-8'))['sources'] if s['source_id']==SID)
CH={c['chapter_id']:c for c in SOURCE['chapters']}
HEADS=[c for c in SOURCE['chapters'] if re.match(r'^第.*集\s',c['title'])]

def volume_chapters(n):
    start=0 if n==1 else HEADS[n-1]['start_offset']
    end=HEADS[n]['start_offset'] if n<18 else SOURCE['characters']
    return [c['chapter_id'] for c in SOURCE['chapters'] if start<=c['start_offset']<end]

def ev(entries,kind='inference'):
    return [{'source_id':SID,'revision':SOURCE['revision'],**e,'claim_kind':e.get('claim_kind',kind)} for e in entries]

def check_report(report):
    n=report['volume']
    assert 1<=n<=18 and report['source_id']==SID and report['revision']==SOURCE['revision']
    expected=volume_chapters(n)
    assert report['chapter_ids']==expected,(n,'chapter coverage',report['chapter_ids'],expected)
    assert [x['chapter_id'] for x in report['chapter_notes']]==expected,(n,'chapter notes')
    assert set(report['dimensions'])==set(DIMS)
    assert all(len(report['dimensions'][d])>=3 for d in DIMS)
    for item in report['chapter_notes']:
        assert set(item['dimensions_checked'])==set(DIMS),(n,item['chapter_id'],'dimensions')
    def evidence_walk(obj):
        if isinstance(obj,dict):
            for key,value in obj.items():
                if key=='evidence':
                    assert isinstance(value,list) and value,(n,'empty evidence')
                    for e in value:
                        c=CH[e['chapter_id']]
                        assert e['chapter_id'] in expected,(n,'outside volume evidence',e)
                        assert c['start_line']<=e['start_line']<=e['end_line']<=c['end_line'],(n,'evidence boundary',e,c)
                else:evidence_walk(value)
        elif isinstance(obj,list):
            for value in obj:evidence_walk(value)
    evidence_walk(report)
    event_keys={e['key'] for e in report['events']}
    assert len(event_keys)==len(report['events'])
    known_names=set()
    for number in range(1,n+1):
        prior=report if number==n else json.loads((HERE/f'vol{number:02d}.json').read_text(encoding='utf-8'))
        for character in prior['characters']:
            known_names.update([character['name'],*character.get('aliases',[])])
    for event in report['events']:
        assert set(event.get('characters',[]))<=known_names,(n,'missing character record',event['key'],set(event.get('characters',[]))-known_names)
        assert all(k['observer']=='reader' or k['observer'] in known_names for k in event.get('knowledge',[])),(n,'missing observer record',event['key'])
    scene_keys={s['key'] for s in report['scenes']}
    assert len(scene_keys)==len(report['scenes'])
    for e in report['edges']:
        assert e['from'] in event_keys and e['to'] in event_keys
    for t in report['threads']:
        assert t['event_keys'] and set(t['event_keys'])<=event_keys
        for pair in t.get('edge_pairs',[]):
            assert len(pair)==2 and set(pair)<=set(t['event_keys']),(n,'thread endpoint outside members',t['key'],pair)
            assert any(e['from']==pair[0] and e['to']==pair[1] for e in report['edges']),(n,'missing thread edge',t['key'],pair)
    for p in report['patterns']:
        assert p['scene_keys'] and set(p['scene_keys'])<=scene_keys
    # 块号完整性与脚本相同，仅证明读者提交了全范围声明。
    lines=Path(SOURCE['normalized_path']).read_text(encoding='utf-8').splitlines(keepends=True)
    count=0;parts=1
    for line in lines[CH[expected[0]]['start_line']-1:CH[expected[-1]]['end_line']]:
        if count and count+len(line)>9000:parts+=1;count=0
        count+=len(line)
    assert report['read_parts']==list(range(1,parts+1)),(n,'read parts',parts)
    return {'volume':n,'chapters':len(expected),'read_parts':parts,'evidence_valid':True}

def key_id(prefix,value):
    return prefix+hashlib.sha256(value.encode('utf-8')).hexdigest()[:16]

def save_volume(vault,report):
    n=report['volume']
    validation=check_report(report)
    folder=vault.root/'library/reports/super-skeleton'
    existing_reports=[json.loads(p.read_text(encoding='utf-8')) for p in sorted(folder.glob('vol[0-9][0-9].json'))]
    assert sorted(r['volume'] for r in existing_reports)==list(range(1,len(existing_reports)+1))
    assert n in {len(existing_reports),len(existing_reports)+1} or n==1 and not existing_reports
    reports=[r for r in existing_reports if r['volume']!=n]+[report]
    reports.sort(key=lambda r:r['volume'])
    index_path=folder/'asset-index.json'
    index=json.loads(index_path.read_text(encoding='utf-8')) if index_path.exists() else {'characters':{},'scenes':{},'patterns':{}}
    assets=vault.search(source_id=SID)
    for a in assets:
        if a['asset_type']=='character' and '/opening-test-' in a.get('origin_key',''):
            index['characters'].setdefault(a['title'].split('：')[0],a['asset_id'])
    known_names=set(index['characters'])
    for raw in report['characters']:
        known_names.update([raw['name'],*raw.get('aliases',[])])
    for event in report['events']:
        assert set(event.get('characters',[]))<=known_names,(n,'unknown character before mutation',event['key'])
        assert all(k['observer']=='reader' or k['observer'] in known_names for k in event.get('knowledge',[])),(n,'unknown observer before mutation',event['key'])
    protected={a['asset_id']:{k:a[k] for k in ['user_notes','favorite','review_status']} for a in vault.search()}
    saved=[]
    for raw in report['characters']:
        name=raw['name']
        matches={index['characters'][alias] for alias in [name,*raw.get('aliases',[])] if alias in index['characters']}
        assert len(matches)<=1,('ambiguous character identity',name,matches)
        old=vault.get_asset(next(iter(matches))) if matches else None
        prior=copy.deepcopy(old['content']) if old else {}
        content={}
        if prior.get('identity_notes'):content['identity_notes']=copy.deepcopy(prior['identity_notes'])
        if old:
            opening=prior.get('opening_observations',prior if 'volume_history' not in prior else None)
            if opening:content['opening_observations']=opening
        history=[h for h in prior.get('volume_history',[]) if h['volume']!=n]
        history.append({'volume':n,**copy.deepcopy(raw)})
        content.update({k:copy.deepcopy(v) for k,v in raw.items() if k not in ['evidence','name','aliases']})
        content.update(name=name,aliases=sorted(set(prior.get('aliases',[])+raw.get('aliases',[]))),volume_history=history,
                       coverage_note=f'九维深化已覆盖第1至{n}集；变化记录以各集证据为准。')
        evidence=ev(raw['evidence'])
        if old:
            evidence=list({json.dumps(e,sort_keys=True):e for e in old['evidence']+evidence}.values())
        data={'asset_type':'character','scope':'source-analysis','title':f'{name}：分集人物研究',
              'origin_key':old['origin_key'] if old else SID+'/full-nine/character/'+name,
              'content':content,'evidence':evidence,'tags':sorted(set((old['tags'] if old else [])+['全书九维',f'第{n:02d}集']))}
        if old:data['asset_id']=old['asset_id']
        record=vault.put_asset(data,base_revision=old['revision'] if old else None,generated=True)
        for alias in [name,*raw.get('aliases',[])]:index['characters'][alias]=record['asset_id']
        saved.append(record['asset_id'])
    for kind,collection in [('scene','scenes'),('pattern','patterns')]:
        for raw in report[collection]:
            old=vault.get_asset(index[collection][raw['key']]) if raw['key'] in index[collection] else None
            content={k:copy.deepcopy(v) for k,v in raw.items() if k not in ['key','title','evidence','scene_keys']}
            content['volume']=n
            data={'asset_type':kind,'scope':'reusable-pattern' if kind=='pattern' else 'source-analysis',
                  'title':raw['title'],'origin_key':SID+'/full-nine/'+raw['key'],'content':content,
                  'tags':['全书九维',f'第{n:02d}集'],'evidence':ev(raw['evidence'],'synthesis' if kind=='pattern' else 'inference')}
            if kind=='pattern':
                data['derived_from']=[{'asset_id':index['scenes'][k],'revision':vault.get_asset(index['scenes'][k])['revision']} for k in raw['scene_keys']]
            if old:data['asset_id']=old['asset_id']
            record=vault.put_asset(data,base_revision=old['revision'] if old else None,generated=True)
            index[collection][raw['key']]=record['asset_id'];saved.append(record['asset_id'])
    graph=make_graph(reports,index,vault)
    current=json.loads((vault.root/graph_path('source',SID)).read_text(encoding='utf-8'))
    graph=save_graph(vault,'source',SID,graph,base_revision=current['revision'])
    render_graph(graph,vault.root/'library/views/plots'/(SID+'-full-nine'))
    completed=[c for r in reports for c in r['chapter_ids']]
    report_files={f'library/reports/super-skeleton/vol{n:02d}.json':json_text(report),
                  f'library/reports/super-skeleton/vol{n:02d}.md':(HERE/f'vol{n:02d}.md').read_text(encoding='utf-8'),
                  'library/reports/super-skeleton/asset-index.json':json_text(index)}
    if (HERE/'cross-volume.json').exists():
        report_files['library/reports/super-skeleton/cross-volume.json']=(HERE/'cross-volume.json').read_text(encoding='utf-8')
    if (HERE/f'review-{n:02d}.md').exists():
        report_files[f'library/reports/super-skeleton/audit/review-{n:02d}.md']=(HERE/f'review-{n:02d}.md').read_text(encoding='utf-8')
    with locked(vault.root):
        commit(vault.root,report_files)
    status=vault.validate()
    for a in vault.search():
        if a['asset_id'] in protected:
            assert {k:a[k] for k in protected[a['asset_id']]}==protected[a['asset_id']]
    checkpoint=vault.checkpoint({'run_id':'run-deep-super-skeleton-20261022','source_id':SID,'source_revision':SOURCE['revision'],
        'completed_chapters':completed,'pending_chapters':[c for c in CH if c not in completed],
        'dimensions':DIMS,'completed_volumes':list(range(1,len(reports)+1)),
        'notes':'本轮完整逐块阅读并九维检查；章前说明和集标题计入覆盖但不计作正文。每集研究草稿待用户审查。',
        'assets':sorted(set(index['characters'].values())|set(index['scenes'].values())|set(index['patterns'].values()))})
    vault.build_views()
    result={**validation,'status':status,'saved_asset_ids':saved,'graph':{'nodes':len(graph['nodes']),'edges':len(graph['edges']),'threads':len(graph['threads'])},
            'completed_volumes':len(reports),'completed_segments':len(completed),'human_fields_preserved':True}
    (HERE/f'persist-{n:02d}.json').write_text(json_text(result),encoding='utf-8')
    return result

def make_graph(reports,index,vault):
    nodes=[{'id':'story','kind':'story','parent_id':None,'title':'超级骷髅兵：九维深化剧情结构','claim_kind':'inference'}]
    edges=[];threads=[]
    for r in reports:
        n=r['volume'];parent=f'vol-{n:02d}'
        nodes.append({'id':parent,'kind':'volume','parent_id':'story','title':r['title'],'summary':r['overview'],'claim_kind':'inference','narrative_order':n*100})
        for i,event in enumerate(r['events']):
            names=event.get('characters',[])
            assert all(name in index['characters'] for name in names),(n,'missing event character',names)
            knowledge=[]
            for k in event.get('knowledge',[]):
                observer=k['observer']
                assert observer=='reader' or observer in index['characters'],(n,'missing knowledge observer',observer)
                knowledge.append({**k,'observer':observer if observer=='reader' else index['characters'][observer]})
            nodes.append({'id':event['key'],'parent_id':parent,'kind':'event','title':event['title'],'summary':event['summary'],
                          'characters':[index['characters'][x] for x in names],'knowledge':knowledge,'claim_kind':'fact',
                          'narrative_order':n*100+i+1,'evidence':ev(event['evidence'],'fact')})
        pairs={}
        for i,edge in enumerate(r['edges']):
            eid=f'v{n:02d}-edge-{i+1:02d}'
            edges.append({**edge,'id':eid,'evidence':ev(edge['evidence'],edge['claim_kind'])})
            pairs.setdefault((edge['from'],edge['to']),[]).append(eid)
        for i,t in enumerate(r['threads']):
            relations=[e for pair in t.get('edge_pairs',[]) for e in pairs.get(tuple(pair),[])]
            members=list(dict.fromkeys(t['event_keys']))
            assert all(e['from'] in members and e['to'] in members for e in edges if e['id'] in relations)
            threads.append({'id':f'v{n:02d}-thread-{i+1:02d}','title':f'第{n}集 · '+t['title'],'kind':t['kind'],'status':t['status'],
                            'node_ids':members,'edge_ids':relations,'resolution_note':t.get('resolution_note',''),'question':t.get('question',''),
                            'tracking_key':t['key']})
    cross=HERE/'cross-volume.json'
    if cross.exists():
        data=json.loads(cross.read_text(encoding='utf-8'))
        node_ids={n['id'] for n in nodes}
        for edge in data.get('edges',[]):
            if edge['from'] in node_ids and edge['to'] in node_ids:edges.append({**edge,'evidence':ev(edge['evidence'],edge['claim_kind'])})
        edge_ids={e['id'] for e in edges}
        for thread in data.get('threads',[]):
            if set(thread['node_ids'])<=node_ids and set(thread['edge_ids'])<=edge_ids:threads.append(thread)
    covered=[ch for r in reports for ch in r['chapter_ids']]
    return {'title':f'超级骷髅兵 · 九维深化第1—{len(reports)}集','nodes':nodes,'edges':edges,'threads':threads,
            'coverage':[{'source_id':SID,'revision':SOURCE['revision'],'chapter_ids':covered,'complete':set(covered)==set(CH)}]}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('volume',type=int);p.add_argument('--check-only',action='store_true');p.add_argument('--vault',type=Path,default=ROOT/'writing-vault')
    a=p.parse_args();report=json.loads((HERE/f'vol{a.volume:02d}.json').read_text(encoding='utf-8'))
    print(json_text(check_report(report) if a.check_only else save_volume(Vault(a.vault),report)))
