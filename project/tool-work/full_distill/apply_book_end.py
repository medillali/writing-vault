"""在全书审计完成后保存累计修订、综合报告及审查证据。"""
import copy
import json
from pathlib import Path
from persist import ROOT,HERE,SID,SOURCE,CH,ev,make_graph,volume_chapters
from fictionlib.vault import Vault
from fictionlib.graph import save_graph,render_graph
from fictionlib.storage import commit,locked,json_text

def main():
    v=Vault(ROOT/'writing-vault')
    folder=v.root/'library/reports/super-skeleton'
    reports=[json.loads((folder/f'vol{n:02d}.json').read_text(encoding='utf-8')) for n in range(1,19)]
    index=json.loads((folder/'asset-index.json').read_text(encoding='utf-8'))
    ids=set(index['characters'].values())
    audit=json.loads((HERE/'character-final-audit.json').read_text(encoding='utf-8'))
    assert audit['complete_as_of_volume']==18 and set(audit['checked_asset_ids'])==ids
    assert len(audit['checked_asset_ids'])==len(ids)
    checked=audit['checked_records']
    assert len(checked)==len(ids) and {r['asset_id'] for r in checked}==ids
    assert all(r['reviewed_at_book_end'] is True and r['review_note'] for r in checked)
    updates={item['asset_id']:item for item in audit['updates']}
    assert len(updates)==len(audit['updates']) and set(updates)<=ids
    allowed={'summary','goal','conflict','arc_change','relationships','knowledge_limits'}
    chapter_volume={cid:n for n in range(1,19) for cid in volume_chapters(n)}
    changed=[]
    for aid in sorted(ids):
        asset=v.get_asset(aid)
        before={key:copy.deepcopy(asset[key]) for key in ['user_notes','favorite','review_status']}
        change=updates.get(aid)
        if change:
            assert set(change.get('content_updates',{}))<=allowed
            assert change.get('reason') and change.get('evidence')
            for e in change['evidence']:
                c=CH[e['chapter_id']]
                assert c['start_line']<=e['start_line']<=e['end_line']<=c['end_line']
            asset['content'].update(change.get('content_updates',{}))
            removed=change.get('aliases_to_remove',[])
            assert isinstance(removed,list) and all(isinstance(a,str) and a for a in removed)
            if removed:
                asset['content']['aliases']=[a for a in asset['content'].get('aliases',[]) if a not in removed]
                for alias in removed:
                    if index['characters'].get(alias)==aid:del index['characters'][alias]
            notes=asset['content'].setdefault('identity_notes',[])
            for note in change.get('identity_notes',[]):
                if note not in notes:notes.append(note)
            asset['evidence']=list({json.dumps(e,sort_keys=True):e for e in asset['evidence']+ev(change['evidence'])}.values())
        last=max(chapter_volume[e['chapter_id']] for e in asset['evidence'] if e.get('source_id')==SID and e.get('chapter_id') in chapter_volume)
        asset['content']['coverage_note']=f'本书18集已完整阅读并完成累计人物审计；本卡最新引用证据位于第{last}集，未再交代的结局保留未知。分集历史记录当时信息，不代表最终状态。'
        saved=v.put_asset(asset,base_revision=asset['revision'],generated=True)
        assert {key:saved[key] for key in before}==before
        changed.append({'asset_id':aid,'state_corrected':bool(change),'last_evidence_volume':last})
    files={'library/reports/super-skeleton/asset-index.json':json_text(index)}
    for name in ['book-synthesis.json','book-synthesis.md','question-ledger.json','question-ledger.md','cross-input.json','cross-volume.json']:
        files['library/reports/super-skeleton/'+name]=(HERE/name).read_text(encoding='utf-8')
    for path in HERE.glob('*'):
        if path.is_file() and (path.name.startswith(('reader-','review-','character-','thread-final','cross-audit','early-reconciliation','question-ledger-')) and path.suffix in {'.md','.json'}):
            if path.name in {'reader-brief.md','thread-final-planning.md','thread-final-review.json','question-ledger-review.json'}:continue
            files['library/reports/super-skeleton/audit/'+path.name]=path.read_text(encoding='utf-8')
    with locked(v.root):commit(v.root,files)
    graph=make_graph(reports,index,v)
    path=v.root/'library/sources'/SID/'plot-graph.json'
    old=json.loads(path.read_text(encoding='utf-8'))
    graph=save_graph(v,'source',SID,graph,base_revision=old['revision'])
    render_graph(graph,v.root/'library/views/plots'/(SID+'-full-nine'))
    v.build_views()
    status=v.validate()
    result={'character_cards_audited':len(ids),'state_corrections':len(updates),'human_fields_preserved':True,'cards':changed,'validation':status}
    (HERE/'book-end-applied.json').write_text(json_text(result),encoding='utf-8')
    print(json_text({k:value for k,value in result.items() if k!='cards'}))

if __name__=='__main__':main()
