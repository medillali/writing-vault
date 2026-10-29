"""第二卷独立入库，累计检查点；来源总图保留两卷末状态快照。"""
import pathlib,sys,json,uuid,copy,functools,collections,shutil
sys.stdout.reconfigure(encoding='utf-8')
root=pathlib.Path(__file__).resolve().parents[2];sys.path.insert(0,str(root/'distill-novels/scripts'))
from fictionlib.vault import Vault
from fictionlib.graph import save_graph,render_graph,graph_path,validate_graph
from fictionlib.storage import atomic_write,json_text
vault=root/'writing-vault';work=root/'.planning/20261023-shiluoye/zongheng-tianxia-vol02';dest=vault/'library/reports/zongheng-tianxia'
def read(path):return json.loads(path.read_text(encoding='utf-8'))
src=read(root/'.planning/20261023-shiluoye/zongheng-tianxia/source.json');sid=src['source_id'];revision=src['revision']
analysis=read(work/'analysis.json');raw_cards=read(work/'cards.json');raw_cards=raw_cards['cards'] if isinstance(raw_cards,dict) else raw_cards
graph=read(work/'graph.json');read_ids=analysis['read_chapter_ids']
assert set(read_ids)=={f'ch-{i:04d}' for i in range(51,102)} and len(read_ids)==51
v=Vault(vault);v._source=functools.lru_cache(maxsize=None)(v._source)
origin={c['origin_key']:c.get('asset_id') or {'character':'chr','scene':'scn','pattern':'pat'}[c['asset_type']]+'-'+uuid.uuid5(uuid.NAMESPACE_URL,c['origin_key']).hex for c in raw_cards}
saved=[]
for card in sorted(raw_cards,key=lambda c:c['asset_type']=='pattern'):
    card=copy.deepcopy(card)
    for e in card['evidence']:assert e['source_id']==sid and e['revision']==revision and e['chapter_id'] in read_ids
    card['asset_id']=origin[card['origin_key']]
    refs=card['content'].pop('derived_from_origin_keys',[])
    if refs:card['derived_from']=[{'asset_id':origin[k],'revision':v.get_asset(origin[k])['revision']} for k in refs]
    path=vault/v._asset_path(card['asset_id']);old=read(path) if path.exists() else None
    a=v.put_asset(card,old['revision'] if old else None,generated=True)
    saved.append({k:a[k] for k in ['asset_id','revision','origin_key','asset_type','title']})
def replace(data,mapping):
    if isinstance(data,dict):return {k:replace(val,mapping) for k,val in data.items()}
    if isinstance(data,list):return [replace(val,mapping) for val in data]
    if isinstance(data,str) and data in mapping:return mapping[data]
    return data
graph=replace(graph,origin);graph['owner']={'kind':'source','id':sid}
for node in graph['nodes']:
    if 'character_origin_keys' in node:node['characters']=node.pop('character_origin_keys')
    if 'asset_origin_key' in node:node['asset_id']=node.pop('asset_origin_key')
graph['reference_note']='人物和场景引用已映射到正式卡片ID；仅覆盖本卷已读范围。'
validate_graph(graph,v)
for name in ['read-log.json','reading-notes.md']:
    shutil.copyfile(work/name,dest/('vol02-'+name))
formal_cards=[v.get_asset(a['asset_id']) for a in saved]
for key,kind in [('characters','character'),('scenes','scene'),('reusable_patterns','pattern')]:
    analysis[key]=[a for a in formal_cards if a['asset_type']==kind]
atomic_write(dest/'vol02-analysis.json',json_text(analysis));atomic_write(dest/'vol02-cards.json',json_text(formal_cards))
report=(work/'report.md').read_text(encoding='utf-8')
report=report.replace('《天下无双》未恢复阅读','《天下无双》《斩龙》依序待正式研究')
report=report.replace('尚未写正式库、提交或推送','已写入正式资料库，未提交或推送')
for old,new in [('analysis.json','vol02-analysis.json'),('cards.json','vol02-cards.json'),('graph.json','vol02-graph.json'),('read-log.json','vol02-read-log.json'),('reading-notes.md','vol02-reading-notes.md')]:
    report=report.replace('`'+old+'`','['+new+']('+new+')')
atomic_write(dest/'vol02.md',report)
atomic_write(dest/'vol02-asset-map.json',json_text(saved));atomic_write(dest/'vol02-graph.json',json_text(graph))
render_graph(graph,vault/'library/views/plots'/sid/'vol02')
first=read(dest/'vol01-graph.json')
combined={'title':'纵横天下｜已读前两卷的阶段结构','nodes':[{'id':'collected-story','title':'第1—100章：两卷阶段快照','kind':'story','claim_kind':'synthesis','parent_id':None,'summary':'每卷的线索状态以各自卷末为准；尚未完成全书或跨卷综合。'}],'edges':[],'threads':[],'coverage':[{'source_id':sid,'revision':revision,'chapter_ids':sorted(set(read_ids+first['coverage'][0]['chapter_ids'])),'complete':False}],'notes':'卷一、卷二并置保留阶段观察；不能把卷一未解项当成卷二末仍未解。后续综合须依据逐卷证据另建跨卷因果。'}
for number,snapshot in [(1,first),(2,graph)]:
    snap=copy.deepcopy(snapshot)
    # 只改标识符及其引用，避免同名节点污染 kind/status 等枚举字段。
    node_ids={n['id']:f'v{number}-'+n['id'] for n in snap['nodes']}
    edge_ids={e['id']:f'v{number}-'+e['id'] for e in snap['edges']}
    for node in snap['nodes']:
        node['id']=node_ids[node['id']]
        if node.get('parent_id') is not None:node['parent_id']=node_ids[node['parent_id']]
    for edge in snap['edges']:
        edge['id']=edge_ids[edge['id']];edge['from']=node_ids[edge['from']];edge['to']=node_ids[edge['to']]
    for thread in snap['threads']:
        thread['id']=f'v{number}-'+thread['id']
        thread['node_ids']=[node_ids[n] for n in thread['node_ids']]
        thread['edge_ids']=[edge_ids[e] for e in thread.get('edge_ids',[])]
    for node in snap['nodes']:
        if node.get('parent_id') is None:
            node.update(parent_id='collected-story',kind='volume',title=f'卷{number}末快照｜'+node['title'],narrative_order=number)
    for thread in snap['threads']:thread['title']=f'卷{number}末｜'+thread['title']
    for kind in ['nodes','edges','threads']:combined[kind].extend(snap[kind])
old=read(vault/graph_path('source',sid));saved_graph=save_graph(v,'source',sid,combined,old['revision'])
render_graph(saved_graph,vault/'library/views/plots'/sid/'collected')
checkpoint=v.get_checkpoint('run-deep-zongheng-tianxia-20261023')
complete=sorted(set(checkpoint['completed_chapters']+read_ids))
checkpoint.update(completed_chapters=complete,pending_chapters=[c['chapter_id'] for c in src['chapters'] if c['chapter_id'] not in complete],completed_volumes=[1,2],assets=sorted(set(checkpoint['assets']+[a['asset_id'] for a in saved])),notes='逐章全文读完前两卷第1—100章，分别完成九维研究；章前介绍未计已读。下一批卷三第101章ch-0102。全书及后两书仍待继续；所有研究为待用户审阅草稿。')
v.checkpoint(checkpoint)
first_assets=read(dest/'asset-map.json');all_assets=first_assets+saved
counts=collections.Counter(a['asset_type'] for a in saved)
cl=['# 前两卷研究卡片','','各卷是独立阶段观察；同名人物不是重复新增的独立人物。旧开篇卡仍保留，用户评价未预填。','']
for number,assets in [(1,first_assets),(2,saved)]:
    cl+=['## 卷'+str(number),'']
    for typ,label in [('character','人物'),('scene','场景'),('pattern','机制')]:
        cl+=['### '+label,'']
        for a in assets:
            if a['asset_type']==typ:cl+=['- ['+a['title']+'](../../views/'+a['asset_id']+'.md) · v'+str(a['revision'])]
        cl+=['']
atomic_write(dest/'cards.md','\n'.join(cl)+'\n')
lines=['# 《网游之纵横天下》按卷蒸馏','','**已完成前两卷第1—100章连续阅读与分卷九维研究；全书尚未完成。**','','下一起点：卷三第101章，`ch-0102`。先研究本书，再按创作顺序推进《网游之天下无双》《斩龙》。','','| 卷 | 正文范围 | 报告 | 阅读日志 | 图 |','|---|---|---|---|---|']
for number,span in [(1,'1—49'),(2,'50—100')]:
    slug=f'vol{number:02d}'
    lines += [f'| 卷{number} | 第{span}章 | [九维报告]({slug}.md) | [日志]({slug}-read-log.json) | [阶段图](../../views/plots/{sid}/{slug}/index.html) |']
lines += ['', '[研究卡片](cards.md) · [跨卷衔接核验](跨卷衔接核验.md) · [统一管理目录](../collection/README.md)', '', f'[前两卷结构总览](../../views/plots/{sid}/collected/index.html)将各卷末快照分支显示；卷一的未解状态不被误作卷二末状态。尚未编造全书因果和终局。', '', '来源事实、人物推测、研究解释与用户评价分层。研究均为草稿，原文疑点保留，不用后文静默覆盖早期观察。', '', f'来源ID：`{sid}`；修订：`{revision}`。', '', '本轮本地保存，没有提交或推送。']
atomic_write(dest/'README.md','\n'.join(lines)+'\n')
atomic_write(work/'import-result.json',json_text({'assets':saved,'counts':dict(counts),'graph_revision':saved_graph['revision'],'read_chapters':len(read_ids),'cumulative_read_chapters':len(complete)}))
print(json.dumps({'volume':2,'counts':dict(counts),'read_chapters':len(read_ids),'cumulative_read_chapters':len(complete),'graph_revision':saved_graph['revision']},ensure_ascii=False))
