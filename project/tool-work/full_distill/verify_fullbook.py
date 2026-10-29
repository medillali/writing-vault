"""全书完成后的覆盖、人工资料保护及无原文恢复验收。"""
import json
from pathlib import Path
import subprocess
import sys
from persist import ROOT,HERE,SID,CH,DIMS,check_report
from fictionlib.vault import Vault
from fictionlib.exchange import backup,restore
from fictionlib.graph import render_graph
from verify_preservation import verify

def run():
    from verify_cross_retention import verify as verify_cross
    cross_retention=verify_cross()
    vault=Vault(ROOT/'writing-vault')
    folder=vault.root/'library/reports/super-skeleton'
    reports=[json.loads((folder/f'vol{n:02d}.json').read_text(encoding='utf-8')) for n in range(1,19)]
    for report in reports:check_report(report)
    identities=json.loads((folder/'asset-index.json').read_text(encoding='utf-8'))['characters']
    for group in [['龙焰','龙焰（不死巨龙）'],['雷奥','雷奥形死息傀儡'],['拉西萝茜','克丽丝','降临战斗天使'],['泰特尼斯','斯图帝勒']]:
        assert len({identities[name] for name in group})==len(group),group
    assert identities['里维里斯特']==identities['森林巨树']
    assert not set(['魅影舞者','亡灵圣者','黑武士侯爵','自称冥月女神','雷神之主'])&set(identities)
    assert '大巫' not in identities
    assert identities['霍夫曼']!=identities['切里莫·亚力莫菲']
    assert '大巫' not in vault.get_asset(identities['霍夫曼'])['content']['aliases']
    covered=[c for report in reports for c in report['chapter_ids']]
    assert covered==list(CH) and len(set(covered))==202
    checkpoint=vault.get_checkpoint('run-deep-super-skeleton-20261022')
    assert checkpoint['completed_chapters']==covered and not checkpoint['pending_chapters']
    assert checkpoint['completed_volumes']==list(range(1,19))
    graph=json.loads((vault.root/'library/sources'/SID/'plot-graph.json').read_text(encoding='utf-8'))
    assert graph['coverage'][0]['complete'] is True
    thread_audit=json.loads((folder/'audit/thread-final-audit.json').read_text(encoding='utf-8'))
    assert thread_audit['complete_as_of_volume']==18 and all(t['reviewed_at_book_end'] is True for t in thread_audit['entries'])
    final_threads={t['tracking_key']:t for t in graph['threads'] if t.get('tracking_key')}
    for item in thread_audit['entries']:
        assert item['key'] in final_threads,item['key']
        assert final_threads[item['key']]['status']==item['final']['status'],item['key']
    synthesis=json.loads((folder/'book-synthesis.json').read_text(encoding='utf-8'))
    from persist import SOURCE
    assert synthesis['source_id']==SID and synthesis['revision']==SOURCE['revision']
    assert set(synthesis['dimensions'])==set(DIMS)
    assert all(len(synthesis['dimensions'][d])>=3 for d in DIMS)
    chapter_volume={cid:r['volume'] for r in reports for cid in r['chapter_ids']}
    assert synthesis['coverage']['volumes']==list(range(1,19))
    assert synthesis['coverage']['index_segments']==len(covered)
    assert synthesis['coverage']['full_read_blocks']==sum(len(r['read_parts']) for r in reports)
    for dimension in synthesis['dimensions'].values():
        for item in dimension:
            assert all(item.get(k) for k in ['claim','mechanism','application','limitation','evidence'])
            assert item.get('claim_kind') in {'fact','inference','synthesis'}
            assert len({chapter_volume[e['chapter_id']] for e in item['evidence']})>=2
            for e in item['evidence']:
                c=CH[e['chapter_id']]
                assert c['start_line']<=e['start_line']<=e['end_line']<=c['end_line']
    ledger=json.loads((folder/'question-ledger.json').read_text(encoding='utf-8'))
    assert ledger['completion']=='complete_as_of_volume_18' and not ledger['pending_questions']
    expected={(r['volume'],i):q for r in reports for i,q in enumerate(r['questions'],1)}
    actual={(e['origin_volume'],e['source_question_index']):e for e in ledger['entries']}
    assert len(actual)==len(ledger['entries']) and set(actual)==set(expected)
    for key,q in expected.items():
        item=actual[key]
        assert item['question']==q['question'] and item['origin_evidence']==q['evidence']
        assert item['status'] in {'answered','partial','open','text-uncertain'}
        assert item.get('answer') and item.get('reviewed_at_book_end') is True
        for e in item['origin_evidence']+item.get('answer_evidence',[]):
            c=CH[e['chapter_id']]
            assert c['start_line']<=e['start_line']<=e['end_line']<=c['end_line']
    expected_revisions={(r['volume'],i):revision for r in reports for i,revision in enumerate(r['revisions_to_earlier'],1)}
    actual_revisions={(r['origin_volume'],r['source_revision_index']):r for r in ledger['revision_reviews']}
    assert set(actual_revisions)==set(expected_revisions) and len(actual_revisions)==len(ledger['revision_reviews'])
    for key,revision in expected_revisions.items():
        actual=actual_revisions[key]
        assert actual['original_revision']==revision and actual['reviewed_at_book_end'] is True
        assert actual['review'] and actual['evidence']
        for e in actual['evidence']:
            c=CH[e['chapter_id']]
            assert c['start_line']<=e['start_line']<=e['end_line']<=c['end_line']
    protected=verify()
    original_assets={a['asset_id']:a for a in vault.search()}
    archive=ROOT/'backups/super-skeleton-full-nine-20261022-final.zip'
    destination=ROOT/'.verify/d18-final'
    assert not archive.exists() and not destination.exists(), '验收备份与恢复目标须为新路径'
    saved=backup(vault,archive)
    restored=restore(archive,destination)
    assert not (destination/'private-sources').exists()
    assert not (destination/'.git').exists()
    copy=Vault(destination)
    assert {a['asset_id']:a for a in copy.search()}==original_assets
    assert (destination/'library/sources'/SID/'plot-graph.json').read_bytes()==(vault.root/'library/sources'/SID/'plot-graph.json').read_bytes()
    generator=destination/'library/reports/super-skeleton/rebuild_review.py'
    result=subprocess.run([sys.executable,'-X','utf8',str(generator)],cwd=destination,capture_output=True,text=True,encoding='utf-8')
    assert result.returncode==0,result.stderr
    page='library/views/超级骷髅兵全书审查.html'
    assert (destination/page).read_bytes()==(vault.root/page).read_bytes(), '恢复后的独立生成页面不一致'
    render_graph(graph,destination/'library/views/plots'/(SID+'-full-nine'))
    copy.build_views()
    result={'volumes':18,'indexed_segments':len(covered),'nine_dimension_items':sum(len(x) for r in reports for x in r['dimensions'].values()),'questions_reviewed_at_book_end':len(expected),'revisions_reviewed_at_book_end':len(actual_revisions),
            'assets':len(original_assets),'graph_nodes':len(graph['nodes']),'graph_edges':len(graph['edges']),'threads_audited':len(thread_audit['entries']),
            'protected':protected,'cross_relation_retention':cross_retention,'backup':saved,'restore':restored,'rebuild_without_original':True,'identical_review_html':True}
    (HERE/'fullbook-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':run()
