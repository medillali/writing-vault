"""对齐并行双书任务的新进度，只更新本任务的派生目录。"""
import pathlib,json,sys,collections
sys.stdout.reconfigure(encoding='utf-8')
root=pathlib.Path(__file__).resolve().parents[2];v=root/'writing-vault';d=v/'library/reports/collection'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
config=read(d/'catalog-config.json')
leveling=config['books']['src-359a2bd5a60747038b12a7ba483a5f80']
leveling.update(task_state='opening_only',report='../two-books-20261023/leveling/analysis.md',note='并行双书任务已完成序章和第1—12章研究；下一原第13章。索引已由该任务纠正正文误分章，当前388段；全书仍待继续。')
zeidan=config['books']['src-2d8a13f33737429da512e5cc9e839712']
zeidan['additional_reports']=[{'title':'本次前10章回读与双书研究','path':'../two-books-20261023/README.md'}]
zeidan['note']='旧库463章逐章研究已核验迁入；并行双书任务另完成前10章回读与新卡。旧首轮与新研究分开保留，不等于本轮全书重读或全书九维深化。'
(d/'catalog-config.json').write_text(json.dumps(config,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
cards=[]
for folder in ['characters','scenes','patterns']:
    for p in (v/'library'/folder).glob('*.json'):
        a=read(p)
        if a['asset_id'].startswith(('chr-twobooks-','scn-twobooks-','pat-twobooks-')):cards.append(a)
print(json.dumps({'concurrent_cards':len(cards),'author_tagged':sum('作者:发飙的蜗牛' in a['tags'] for a in cards),'sample_tags':[a['tags'] for a in cards[:3]]},ensure_ascii=False))
