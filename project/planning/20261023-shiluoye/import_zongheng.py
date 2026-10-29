import pathlib,sys,json,uuid,copy,functools,collections,shutil
sys.stdout.reconfigure(encoding='utf-8')
root=pathlib.Path(__file__).resolve().parents[2];sys.path.insert(0,str(root/'distill-novels/scripts'))
from fictionlib.vault import Vault
from fictionlib.graph import save_graph,render_graph,graph_path
from fictionlib.storage import atomic_write,json_text
work=root/'.planning/20261023-shiluoye/zongheng-tianxia';vault=root/'writing-vault'
src=json.loads((work/'source.json').read_text(encoding='utf-8'));sid=src['source_id'];revision=src['revision']
analysis=json.loads((work/'analysis.json').read_text(encoding='utf-8'))
raw_cards=json.loads((work/'cards.json').read_text(encoding='utf-8'))
if isinstance(raw_cards,dict):raw_cards=raw_cards['cards']
graph=json.loads((work/'graph.json').read_text(encoding='utf-8'))
log=json.loads((work/'read-log.json').read_text(encoding='utf-8'))
read_ids=analysis['read_chapter_ids']
assert set(read_ids)=={f'ch-{i:04d}' for i in range(2,51)},read_ids
assert all(c['source_id']==sid and c['revision']==revision for c in graph['coverage'])
assert not any(c['complete'] for c in graph['coverage'])
v=Vault(vault);v._source=functools.lru_cache(maxsize=None)(v._source)
origin_map={}
for card in raw_cards:
    prefix={'character':'chr','scene':'scn','pattern':'pat'}[card['asset_type']]
    origin_map[card['origin_key']]=card.get('asset_id') or prefix+'-'+uuid.uuid5(uuid.NAMESPACE_URL,card['origin_key']).hex
saved=[]
for card in sorted(raw_cards,key=lambda c:c['asset_type']=='pattern'):
    card=copy.deepcopy(card)
    for e in card['evidence']:
        assert e['source_id']==sid and e['revision']==revision and e['chapter_id'] in read_ids,e
    card['asset_id']=origin_map[card['origin_key']]
    refs=card['content'].pop('derived_from_origin_keys',[])
    if refs:card['derived_from']=[{'asset_id':origin_map[k],'revision':v.get_asset(origin_map[k])['revision']} for k in refs]
    path=vault/v._asset_path(card['asset_id']);previous=json.loads(path.read_text(encoding='utf-8')) if path.exists() else None
    asset=v.put_asset(card,previous['revision'] if previous else None,generated=True)
    saved.append({'asset_id':asset['asset_id'],'revision':asset['revision'],'origin_key':asset['origin_key'],'asset_type':asset['asset_type'],'title':asset['title']})
def replace_refs(x):
    if isinstance(x,dict):return {k:replace_refs(val) for k,val in x.items()}
    if isinstance(x,list):return [replace_refs(val) for val in x]
    if isinstance(x,str) and x in origin_map:return origin_map[x]
    return x
graph=replace_refs(graph)
path=vault/graph_path('source',sid);previous=json.loads(path.read_text(encoding='utf-8')) if path.exists() else None
saved_graph=save_graph(v,'source',sid,graph,previous['revision'] if previous else None)
dest=vault/'library/reports/zongheng-tianxia';dest.mkdir(parents=True,exist_ok=True)
for name in ['read-log.json','reading-notes.md']:
    shutil.copyfile(work/name,dest/('vol01-'+name))
formal_cards=[v.get_asset(a['asset_id']) for a in saved]
for key,kind in [('characters','character'),('scenes','scene'),('reusable_patterns','pattern')]:
    analysis[key]=[a for a in formal_cards if a['asset_type']==kind]
atomic_write(dest/'vol01-analysis.json',json_text(analysis))
atomic_write(dest/'vol01-cards.json',json_text(formal_cards))
report=(work/'report.md').read_text(encoding='utf-8')
for old,new in [('analysis.json','vol01-analysis.json'),('cards.json','vol01-cards.json'),('graph.json','vol01-graph.json'),('read-log.json','vol01-read-log.json'),('reading-notes.md','vol01-reading-notes.md')]:
    report=report.replace('`'+old+'`','['+new+']('+new+')')
report=report.replace('机制的 `derived_from_origin_keys` 指向具体场景卡，正式入库时由主代理转换为资产版本引用。','机制由具体场景卡派生，正式卡片的 `derived_from` 已固定资产版本。')
report=report.replace('本子任务只写分配的规划目录，没有修改正式资料库、提交或推送。','本卷材料经入库前复核后保存至正式资料库；没有提交或推送。')
atomic_write(dest/'vol01.md',report)
atomic_write(dest/'asset-map.json',json_text(saved))
atomic_write(dest/'vol01-graph.json',json_text(saved_graph))
graph_result=render_graph(saved_graph,vault/'library/views/plots'/sid/'vol01')
checkpoint={'run_id':'run-deep-zongheng-tianxia-20261023','source_id':sid,'source_revision':revision,'completed_chapters':sorted(read_ids),'pending_chapters':[c['chapter_id'] for c in src['chapters'] if c['chapter_id'] not in read_ids],'dimensions':['worldbuilding','characters','plot','style','narrative','dialogue','pacing','themes','continuity'],'completed_volumes':[1],'assets':[x['asset_id'] for x in saved],'notes':'逐章完整阅读卷一第1—49章；章前介绍未计已读。下一批卷二第50章ch-0051。仅卷一九维研究完成，整书与后两书仍待继续，研究草稿待用户审阅。'}
v.checkpoint(checkpoint)
counts=collections.Counter(x['asset_type'] for x in saved)
lines=['# 《网游之纵横天下》按卷蒸馏','', '**当前完成：卷一《卷土重来》第1—49章连续阅读与九维研究。全书尚未完成。**','', '下一批：卷二《龙吟天下》第50章《守墓人之戒》，chapter_id为`ch-0051`。依用户要求，先研究本书，再推进《网游之天下无双》《斩龙》。','', '- [卷一九维研究报告](vol01.md)','- [逐章阅读日志](vol01-read-log.json)','- [卷一结构化分析](vol01-analysis.json)',f'- [卷一主线与暗线图](../../views/plots/{sid}/vol01/index.html)','- [卡片目录](cards.md) · [统一管理目录](../collection/README.md)','',f"本批新增人物材料{counts['character']}、场景{counts['scene']}、机制{counts['pattern']}。既有前5章卡片保留，属于早期观察版本，未静默合并人物或覆盖用户评价。",'', '所有事实与推断带来源和章节证据。图覆盖只限第一卷；先前开篇图保留在版本历史中。解读是供审查的草稿，来源内部人名、数值疑点另列，不替原文做无证据修正。','',f'来源ID：`{sid}`；修订：`{revision}`。','', '本轮本地保存；没有执行远程推送。']
atomic_write(dest/'README.md','\n'.join(lines)+'\n')
cl=['# 卷一研究卡片','', '从来源事实进入场景机制，再结合自己的目标选择；用户评价未预填。','']
for typ,title in [('character','人物'),('scene','场景'),('pattern','机制')]:
    cl+=['## '+title,'']
    for a in saved:
        if a['asset_type']==typ:cl+=['- ['+a['title']+'](../../views/'+a['asset_id']+'.md) · v'+str(a['revision'])]
    cl+=['']
atomic_write(dest/'cards.md','\n'.join(cl)+'\n')
atomic_write(work/'import-result.json',json_text({'assets':saved,'counts':dict(counts),'graph_revision':saved_graph['revision'],'render':graph_result,'read_chapters':len(read_ids)}))
print(json.dumps({'counts':dict(counts),'graph_revision':saved_graph['revision'],'read_chapters':len(read_ids)},ensure_ascii=False))
