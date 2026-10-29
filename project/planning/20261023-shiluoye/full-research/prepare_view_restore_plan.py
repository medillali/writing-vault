"""备份前保存排除在标准备份外的派生图重建计划，不存原文。"""
from pathlib import Path
import argparse,hashlib,json,re,sys

B=Path(__file__).resolve().parent;ROOT=B.parents[2]
sys.path.insert(0,str(ROOT/'distill-novels/scripts'))
from fictionlib.graph import validate_graph,render_graph
from fictionlib.storage import atomic_write,json_text,safe_path

def prepare(vault):
    vault=Path(vault).resolve();base=vault/'library/reports/collection/qa/view-snapshots'
    entries=[];snapshots=set()
    for p in sorted((vault/'library/views/plots').rglob('index.html')):
        match=re.search(r'<script type="application/json" id="graph-data">(.*?)</script>',p.read_text(encoding='utf-8'),re.S)
        assert match,('缺少图数据',str(p))
        graph=json.loads(match[1]);validate_graph(graph)
        encoded=json_text(graph);key=hashlib.sha256(encoded.encode('utf-8')).hexdigest()
        snapshot=base/(key+'.json');atomic_write(snapshot,encoded);snapshots.add(key)
        entries.append({'directory':p.parent.relative_to(vault).as_posix(),
            'graph':snapshot.relative_to(vault).as_posix(),'sha256':key})
    result={'schema_version':1,'status':'derived-plot-regeneration-plan','entries':entries,
        'unique_snapshots':len(snapshots),'limits':'仅派生阅读图；不变更正典卡片、历史、源文或已冻结报告。'}
    atomic_write(vault/'library/reports/collection/qa/view-restore-plan.json',json_text(result))
    return {'views':len(entries),'unique_snapshots':len(snapshots)}

def regenerate(vault):
    vault=Path(vault).resolve();plan=json.loads((vault/'library/reports/collection/qa/view-restore-plan.json').read_text(encoding='utf-8'))
    assert plan['schema_version']==1
    for e in plan['entries']:
        assert e['directory'].startswith('library/views/plots/')
        assert e['graph'].startswith('library/reports/collection/qa/view-snapshots/')
        source=safe_path(vault,e['graph']);assert hashlib.sha256(source.read_bytes()).hexdigest()==e['sha256']
        graph=json.loads(source.read_text(encoding='utf-8'));validate_graph(graph)
        render_graph(graph,safe_path(vault,e['directory']))
    return {'regenerated_plot_views':len(plan['entries'])}

if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('mode',choices=['prepare','regenerate'])
    p.add_argument('--vault',type=Path,default=ROOT/'writing-vault');args=p.parse_args()
    print(json.dumps((prepare if args.mode=='prepare' else regenerate)(args.vault),ensure_ascii=False))
