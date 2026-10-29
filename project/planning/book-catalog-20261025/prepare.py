from pathlib import Path
import json,subprocess,hashlib
R=Path(__file__).resolve().parents[2];V=R/'writing-vault';P=Path(__file__).parent
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def dump(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def git(*args):return subprocess.run(['git','-c',f'safe.directory={V.as_posix()}','-C',str(V),*args],capture_output=True,check=True).stdout.decode('utf-8')
assert not (V/'书库').exists(),'已有书库入口，先审查后续接'
tracked=set(git('ls-files','-z').split('\0'))-{''};dirty=set(git('diff','--name-only','-z').split('\0'))-{''}
dump(P/'baseline.json',{'head':git('rev-parse','HEAD').strip(),'tracked_modified':{n:hashlib.sha256((V/n).read_bytes()).hexdigest() for n in dirty},'readme_before':(V/'README.md').read_text(encoding='utf-8')})
config=load(V/'library/reports/collection/catalog-config.json');records=[]
runs=[(f,load(f)) for f in (V/'exchanges/runs').glob('*.json') if f.relative_to(V).as_posix() in tracked]
for group in config['author_orders']:
 for order,sid in enumerate(group['source_ids'],1):
  b=config['books'][sid];source=load(V/f'library/sources/{sid}.json');checkpoint=[(f,x) for f,x in runs if x['source_id']==sid]
  row={'source_id':sid,'source_revision':source['revision'],'title':b['title'],'directory':b['title'],'author':b['author'],'author_order':order,'genres':['玄幻'] if b['author']=='情终流水' else ['网游'],'tags':['西方奇幻','不死生物'] if b['author']=='情终流水' else ['虚拟现实'],'published_links':[],'source_record_published':f'library/sources/{sid}.json' in tracked}
  if sid in ['src-2d8a13f33737429da512e5cc9e839712','src-359a2bd5a60747038b12a7ba483a5f80']:
   k='zeidan' if b['title']=='贼胆' else 'leveling';base=f'library/reports/two-books-full-20261025/{k}';cov=load(V/base/'coverage.json')
   row.update(research_status='full',coverage_label=f'全书{cov["actual_reading_units"]}个实际单元，{cov["stages"]}个九维阶段；待用户审阅',report=base+'/README.md',map={'overview':base+'/plot/README.md','html':base+'/plot/map/index.html','reader':base+'/plot/relations/index.html','png':base+'/plot/whole-book/tree.png','svg':base+'/plot/whole-book/tree.svg','preview':base+'/plot/whole-book/tree-preview.png','graph':base+'/plot/graph.json','events':cov['cards']['scene'],'stages':cov['stages'],'relations':cov['graph_relations'],'unit_count':cov['actual_reading_units']})
  elif b['title']=='超级骷髅兵':
   base='library/reports/super-skeleton';m=load(V/base/'reading/plot/whole-book/manifest.json')
   row.update(research_status='full',coverage_label='全书183个正文/序章，18集九维；待用户审阅',report=base+'/README.md',map={'overview':base+'/reading/plot/map.md','html':base+'/reading/plot/reader/index.html','png':base+'/reading/plot/whole-book/tree.png','svg':base+'/reading/plot/whole-book/tree.svg','preview':base+'/reading/plot/whole-book/tree-preview.png','events':len(m['events']),'relations':len(m['edges']),'stages':18,'unit_count':183})
  else:
   done=set(c for _,x in checkpoint for c in x.get('completed_chapters',[]));row.update(research_status='partial' if done else 'queued',coverage_label=f'Git已发布开篇{len(done)}章；全书未完成' if done else '已建书目，Git尚无正式逐章研究')
   if b['author']=='失落叶':row['local_progress_note']='本地另有顺序研究任务正在推进，活动检查点以exchanges/runs为准；本目录不把尚未提交的续读稿混入本批发布。'
  if row['source_record_published']:row['published_links'].append({'label':'来源登记与修订','path':f'library/sources/{sid}.json'})
  for f,x in checkpoint:
   if row['research_status']=='full' and 'full-two-books' not in x['run_id'] and 'deep-super-skeleton' not in x['run_id']:continue
   row['published_links'].append({'label':'正式检查点 '+x['run_id'],'path':f.relative_to(V).as_posix()})
  records.append(row)
dump(V/'书库/catalog.json',{'schema_version':1,'scope':'已登记作品的阅读导航；研究覆盖仅指Git已发布检查点。书目建档不代表全书已读。','classification_rule':'类型为本资料库的研究分类，不冒称平台官方分类；玄幻粗类下用西方奇幻标签细分。类型允许多选，可扩展都市、仙侠、科幻等。','identity_rule':'source_id为来源身份；同名作品另设唯一directory，不按书名合并来源。','books':records})
print('书目元数据已保存：',len(records))
