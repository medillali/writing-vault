import pathlib,json,sys,re
from urllib.parse import unquote
sys.stdout.reconfigure(encoding='utf-8')
root=pathlib.Path(__file__).resolve().parents[2];vault=root/'writing-vault'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
sid='src-2a13958390274509b2af019f6b12d981'
catalog=read(vault/'library/reports/collection/catalog.json')
book=next(b for b in catalog['books'] if b['source_id']==sid)
assert book['completed_body_units']==100 and book['body_reading_units']==1180
assert book['next_reading_unit']['segment_ids'][0]=='ch-0102'
assert book['counts']=={'character':22,'scene':31,'pattern':14}
graph=read(vault/'library/sources'/sid/'plot-graph.json')
assert graph['revision']==3 and len(graph['coverage'][0]['chapter_ids'])==100 and not graph['coverage'][0]['complete']
for volume in [1,2]:
    old=read(vault/f'library/reports/zongheng-tianxia/vol{volume:02d}-graph.json')
    for kind in ['nodes','edges','threads']:
        combined={x['id']:x for x in graph[kind]}
        for record in old[kind]:
            final=combined[f'v{volume}-'+record['id']]
            for field in ['claim_kind','evidence','knowledge','status','summary','resolution_note']:
                assert record.get(field)==final.get(field),(kind,record['id'],field)
backup=read(vault/'library/reports/collection/backup-verification.json')
assert backup['restore']['valid'] and backup['restore']['assets']==626 and backup['all_manifest_hashes_verified']
assert pathlib.Path(backup['backup']['path']).is_file()
links=0
for folder in ['collection','zeidan','zongheng-tianxia']:
    for p in (vault/'library/reports'/folder).rglob('*.md'):
        for target in re.findall(r'\]\(([^\n)]+)\)',p.read_text(encoding='utf-8')):
            target=unquote(target.strip('<>').split('#',1)[0])
            if not target or re.match(r'^[a-z]+://',target):continue
            assert (p.parent/target).resolve().is_file(),(p,target)
            links+=1
print(json.dumps({'catalog_books':len(catalog['books']),'zongheng_completed':100,'zongheng_next':'第101章 ch-0102','current_cards':626,'merged_graph_stage_claims_preserved':True,'final_links_checked':links,'broken_links':0,'restored_files':backup['restore']['verified_files'],'backup_verified':True},ensure_ascii=False))
