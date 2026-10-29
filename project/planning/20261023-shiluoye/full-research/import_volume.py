"""串行保存已审查分卷；研究主档通过现有资料库API写入。"""
import pathlib,json,sys,copy,functools,collections,hashlib
from check_volume import load_and_check,read,ROOT,WORK
sys.path.insert(0,str(ROOT/'distill-novels/scripts'))
from fictionlib.vault import Vault
from fictionlib.graph import save_graph,graph_path,render_graph
from fictionlib.storage import atomic_write,json_text
from import_card_adapter import adapt_card
sys.stdout.reconfigure(encoding='utf-8')
book=sys.argv[1];number=int(sys.argv[2]);assert '--reviewed' in sys.argv,'须先完成主代理文学审查，再加--reviewed入库'
source,spec,directory,analysis,cards,graph,mapping,preflight=load_and_check(book,number)
review_path=WORK/book/f'review-vol{number:02d}.json'
assert review_path.exists(),'须先保存主代理文学审查记录'
primary_review=read(review_path)
assert primary_review.get('status')=='reviewed_for_library_import' and primary_review.get('reviewer')=='primary'
for name,digest in primary_review.get('input_sha256',{}).items():
    assert pathlib.Path(name).name==name
    assert hashlib.sha256((directory/name).read_bytes()).hexdigest()==digest,f'已审输入发生改变，须重新审阅：{name}'
sid=source['source_id'];rev=source['revision'];vault=ROOT/'writing-vault';dest=vault/'library/reports'/book
atomic_write(dest/'audit'/f'review-vol{number:02d}.json',json_text(primary_review))
for previous in range(1,number):assert (dest/f'vol{previous:02d}-graph.json').exists(),f'前卷{previous}尚未入库'
cards=[adapt_card(card) for card in cards]
v=Vault(vault);v._source=functools.lru_cache(maxsize=None)(v._source)
saved=[]
for raw in sorted(cards,key=lambda c:c['asset_type']=='pattern'):
    card=copy.deepcopy(raw);card['asset_id']=mapping[card['origin_key']]
    origins=card['content'].pop('derived_from_origin_keys',[])
    if origins:card['derived_from']=[{'asset_id':mapping[k],'revision':v.get_asset(mapping[k])['revision']} for k in origins]
    path=vault/v._asset_path(card['asset_id']);old=read(path) if path.exists() else None
    record=v.put_asset(card,old['revision'] if old else None,generated=True)
    saved.append({key:record[key] for key in ['asset_id','origin_key','revision','asset_type','title']})
slug=f'vol{number:02d}'
analysis['imported_assets']=saved
atomic_write(dest/f'{slug}-analysis.json',json_text(analysis))
atomic_write(dest/f'{slug}-cards.json',json_text([v.get_asset(r['asset_id']) for r in saved]))
atomic_write(dest/f'{slug}-asset-map.json',json_text(saved))
atomic_write(dest/f'{slug}-graph.json',json_text(graph))
copied=['read-log.json','chapter-notes.jsonl','handoff.md','reader-state.json','validation.json']
copied += [name for name in ['reading-attribution.json','primary-corrections.json','merge-receipt.json','reader-merge-validation.json','freeze-manifest.json','primary-review-delta.json','delivery-freeze.json','PREFIX-HANDOFF.md','tail-derived-reading-receipt.json','priority-corrections-delta.json','primary-delta-20261026.json'] if (directory/name).is_file()]
copied += [name for name in ['prefix-validation.json','prefix-chapter-notes.jsonl','prefix-reader-state.json','prefix-read-log.json','priority-corrections.md','prefix-handoff.md','note-corrections.json','primary-prefix-derived-reading-progress.json'] if (directory/name).is_file()]
copied += [name for name in ['chapter-unresolved-index.json','prefreeze-reference-corrections.json','prefreeze-reference-corrections-2.json'] if (directory/name).is_file()]
copied += [name for name in ['primary-review-proposal.json','primary-review-proposal.md','scene-transfer-proposals.json','scene-transfer-proposals.md','primary-review-applied-delta.json','primary-review-applied-delta.md'] if (directory/name).is_file()]
copied += [name for name in ['self-review-receipt.json','self-audit.json','freeze-receipt.json','primary-review-merged-delta.json','primary-review-supplement-delta.json'] if (directory/name).is_file()]
link_targets=list(dict.fromkeys(['analysis.json','cards.json','graph.json','read-log.json','chapter-notes.jsonl','handoff.md','reader-state.json','validation.json']+copied))
def relocate_markdown(text):
    # 只改本卷包内已复制文件的链接；冻结原稿不动，正式阅读页可在恢复目录使用。
    for prefix in [directory.as_posix()+'/',str(directory)+'\\','']:
        text=text.replace('('+prefix+'report.md)', '('+slug+'.md)')
    for target in link_targets:
        for prefix in [directory.as_posix()+'/',str(directory)+'\\','']:
            text=text.replace('('+prefix+target+')','('+slug+'-'+target+')')
    return text
for name in copied:
    copied_text=(directory/name).read_text(encoding='utf-8')
    if name.endswith('.md'):
        copied_text=relocate_markdown(copied_text)
    atomic_write(dest/f'{slug}-{name}',copied_text)
report=(directory/'report.md').read_text(encoding='utf-8')
report=relocate_markdown(report)
for name in link_targets:
    report=report.replace('('+name+')','('+slug+'-'+name+')').replace('`'+name+'`','['+slug+'-'+name+']('+slug+'-'+name+')')
report+='\n\n## 正式保存记录\n\n本卷研究已通过现有资料库接口保存；仍为待用户审阅草稿。\n\n[分卷入口](README.md) · [阶段图](../../views/plots/'+sid+'/'+slug+'/index.html) · [正式卡片主档]('+slug+'-cards.json)\n'
atomic_write(dest/f'{slug}.md',report);render_graph(graph,vault/'library/views/plots'/sid/slug)
snapshots=[]
for volume in range(1,len(source['volumes'])+1):
    path=dest/f'vol{volume:02d}-graph.json'
    if path.exists():snapshots.append((volume,read(path)))
covered={cid for _,g in snapshots for row in g['coverage'] for cid in row['chapter_ids']}
supplement=WORK/book/'supplementary-read-log.json'
if supplement.exists():
    extra=read(supplement);assert extra['source_id']==sid and extra['revision']==rev
    covered.update(row['chapter_id'] for row in extra['chapters'] if row['full_text_read'])
    atomic_write(dest/'supplementary-read-log.json',json_text(extra))
all_ids={c['chapter_id'] for c in source['chapters']};assert covered.issubset(all_ids)
complete=covered==all_ids
combined={'title':{'zongheng-tianxia':'纵横天下','tianxia-wushuang':'天下无双','zhanlong':'斩龙'}[book]+'｜分卷阶段结构','owner':{'kind':'source','id':sid},'nodes':[{'id':'collected-story','title':'全书分卷快照' if complete else '已读分卷快照','kind':'story','parent_id':None,'claim_kind':'synthesis','summary':'每卷保留各自卷末观察；跨卷因果和终点结论以全书审计为准。'}],'edges':[],'threads':[],'coverage':[{'source_id':sid,'revision':rev,'chapter_ids':sorted(covered),'complete':complete}],'notes':'各卷并列保留阶段状态；后卷不得静默改写前卷事实。同主题不自动产生跨卷因果。'}
for volume,snapshot in snapshots:
    data=copy.deepcopy(snapshot);nodes={n['id']:f'v{volume}-'+n['id'] for n in data['nodes']};edges={e['id']:f'v{volume}-'+e['id'] for e in data['edges']}
    for node in data['nodes']:
        node['id']=nodes[node['id']]
        if node.get('parent_id') is None:node.update(parent_id='collected-story',kind='volume',title=f'卷{volume}末｜'+node['title'],narrative_order=volume)
        else:node['parent_id']=nodes[node['parent_id']]
    for edge in data['edges']:edge.update(id=edges[edge['id']],**{'from':nodes[edge['from']],'to':nodes[edge['to']]})
    for thread in data['threads']:
        thread['id']=f'v{volume}-'+thread['id'];thread['title']=f'卷{volume}末｜'+thread['title']
        thread['node_ids']=[nodes[x] for x in thread['node_ids']];thread['edge_ids']=[edges[x] for x in thread.get('edge_ids',[])]
    for kind in ['nodes','edges','threads']:combined[kind].extend(data[kind])
path=vault/graph_path('source',sid);old=read(path) if path.exists() else None
merged=save_graph(v,'source',sid,combined,old['revision'] if old else None)
render_graph(merged,vault/'library/views/plots'/sid/'collected')
run_id='run-deep-zongheng-tianxia-20261023' if book=='zongheng-tianxia' else f'run-deep-{book}-20261025'
path=vault/'exchanges/runs'/f'{run_id}.json';checkpoint=read(path) if path.exists() else {'run_id':run_id,'source_id':sid,'source_revision':rev,'assets':[]}
checkpoint.update(completed_chapters=sorted(covered),pending_chapters=[c['chapter_id'] for c in source['chapters'] if c['chapter_id'] not in covered],completed_volumes=[n for n,_ in snapshots],assets=sorted(set(checkpoint.get('assets',[])+[a['asset_id'] for a in saved])),dimensions=['worldbuilding','characters','plot','style','narrative','dialogue','pacing','themes','continuity'],notes=f'已正式保存卷{",".join(str(n) for n,_ in snapshots)}全文阅读及九维研究；全书源片段覆盖{len(covered)}/{len(all_ids)}。全书综合/终点审计以独立报告为准，研究尚待用户审阅。')
v.checkpoint(checkpoint)
body=[u for vol in source['volumes'] for u in vol['units'] if u['kind'] in ['body','prologue']]
completed_body=sum(set(u['segment_ids']).issubset(covered) for u in body)
next_unit=next((u for u in body if not set(u['segment_ids']).issubset(covered)),None)
lines=['# 《'+{'zongheng-tianxia':'网游之纵横天下','tianxia-wushuang':'网游之天下无双','zhanlong':'斩龙'}[book]+'》全量蒸馏','','按用户要求采用《超级骷髅兵》的逐卷九维与全书审计流程。当前正文已读及正式研究：'+f'{completed_body}/{len(body)}个阅读单元；{len(snapshots)}/{len(source["volumes"])}卷。','',('下一起点：'+next_unit['title']) if next_unit else '全部正文已读；全书综合、人物弧与伏笔终点审计需另查验收记录。','', '| 卷 | 阅读单元 | 报告 | 实读日志 | 阶段图 |','|---|---:|---|---|---|']
for vol in source['volumes']:
    n=vol['volume'];prefix=f'vol{n:02d}';ready=any(done==n for done,_ in snapshots)
    lines.append(f'| 卷{n} | {vol["body_units"]} | '+(f'[九维报告]({prefix}.md) | [日志]({prefix}-read-log.json) | [阶段图](../../views/plots/{sid}/{prefix}/index.html) |' if ready else '待正式入库 | 待完成 | 待完成 |'))
lines+=['', '[人物/场景/机制中文阅读](reading/README.md) · [分卷结构总览](../../views/plots/'+sid+'/collected/index.html) · [统一资料目录](../collection/README.md)','', '原文事实、人物推测、研究解释与用户评价分层管理。各卷末的未解状态不会被后文静默覆盖；旧笔记和用户审美不被重置。','', '本轮已在本地保存。Git远程、备份恢复和整书验收均以实际记录为准。']
atomic_write(dest/'README.md','\n'.join(lines)+'\n')
import runpy
reading=runpy.run_path(str(vault/'library/reports/collection/rebuild_book_reading.py'))['build'](book)
result={**preflight,'formal_assets':saved,'completed_body_units':completed_body,'complete_source_coverage':complete,'graph_revision':merged['revision'],'next_unit':next_unit,'reading':reading}
atomic_write(directory/'import-result.json',json_text(result))
print(json.dumps({k:v for k,v in result.items() if k not in ['formal_assets','next_unit']},ensure_ascii=False))
