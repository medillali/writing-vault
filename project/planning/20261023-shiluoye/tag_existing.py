import pathlib,sys,json,copy
sys.stdout.reconfigure(encoding='utf-8')
root=pathlib.Path(__file__).resolve().parents[2];sys.path.insert(0,str(root/'distill-novels/scripts'))
from fictionlib.vault import Vault
v=Vault(root/'writing-vault');sources=v.sources();lookup={s['source_id']:s for s in sources};v._source=lambda sid:copy.deepcopy(lookup[sid])
targets={'src-7e18e3668cd940a7b76e7a7e76f4e292':('发飙的蜗牛','重生之贼行天下'),'src-2a13958390274509b2af019f6b12d981':('失落叶','网游之纵横天下')}
results=[]
for asset in v._assets():
    ids={e['source_id'] for e in asset.get('evidence',[])}
    if len(ids)==1 and next(iter(ids)) in targets:
        author,title=targets[next(iter(ids))];updated=copy.deepcopy(asset)
        updated['tags']=list(dict.fromkeys(asset['tags']+['作者:'+author,'作品:'+title]))
        result=v.put_asset(updated,asset['revision'],generated=True)
        assert all(result[k]==asset[k] for k in ['favorite','user_notes','review_status'])
        results.append({'asset_id':result['asset_id'],'before':asset['revision'],'after':result['revision'],'user_fields_preserved':True})
        print(result['asset_id'],result['title'],json.dumps(result['content'],ensure_ascii=False))
out=root/'.planning/20261023-shiluoye/tag-update-audit.json';out.write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
