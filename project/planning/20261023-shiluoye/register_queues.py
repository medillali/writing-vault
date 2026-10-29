import json,pathlib,sys,copy
sys.stdout.reconfigure(encoding='utf-8')
root=pathlib.Path(__file__).resolve().parents[2];sys.path.insert(0,str(root/'distill-novels/scripts'))
from fictionlib.vault import Vault
v=Vault(root/'writing-vault');sources=v.sources();byid={s['source_id']:s for s in sources};v._source=lambda sid:copy.deepcopy(byid[sid])
config=json.loads((root/'writing-vault/library/reports/collection/catalog-config.json').read_text(encoding='utf-8'))
for sid,book in config['books'].items():
    if book['task_state'] not in ['queued_after_zongheng','queued_after_wushuang','registered']:continue
    src=byid[sid];rev=next(r for r in src['revisions'] if r['revision']==src['revision'])
    run='run-queue-'+book['slug']+'-20261023'
    data={'run_id':run,'source_id':sid,'source_revision':src['revision'],'completed_chapters':[],'pending_chapters':[c['chapter_id'] for c in rev['chapters']],'dimensions':['worldbuilding','characters','plot','style','narrative','dialogue','pacing','themes','continuity'],'notes':book['note']+' 已索引不代表完成阅读。','state':book['task_state']}
    v.checkpoint(data);print(run,len(data['pending_chapters']))
audit=json.loads((root/'.planning/20261023-shiluoye/source-audit.json').read_text(encoding='utf-8'))
safe=[{k:val for k,val in a.items() if k not in ['input_path','numeric_chapters','duplicate_numbers','missing_numbers']} for a in audit]
for src,dst in zip(audit,safe):dst['input_filename']=pathlib.Path(src['input_path']).name
(root/'writing-vault/library/reports/collection/input-audit.json').write_text(json.dumps(safe,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
