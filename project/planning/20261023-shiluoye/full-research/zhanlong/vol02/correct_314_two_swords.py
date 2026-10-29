"""记录受控文学主审纠正前后，不静改实际逐章阅读笔记。"""
import pathlib,json,hashlib,sys,shutil,datetime
sys.stdout.reconfigure(encoding='utf-8');P=pathlib.Path(__file__).parent
C=P/'review-corrections';B=C/'raw0314-two-swords-before';B.mkdir(parents=True,exist_ok=True)
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
names=['analysis.json','cards.json','graph.json','read-log.json','reader-state.json','chapter-notes.jsonl','report.md','handoff.md','freeze-manifest.json','validation.json','research_dimensions.py','research_graph.py']
if sys.argv[1]=='before':
 for n in names:
  assert not (B/n).exists(),n
  shutil.copyfile(P/n,B/n)
 save(B/'snapshot.json',{'reason':'primary要求纠正314两剑误合/continuity05文学内容/characters03措辞','sha256':{n:h(B/n) for n in names}})
 print('before snapshot saved')
else:
 before=read(B/'analysis.json');after=read(P/'analysis.json')
 x=json.loads(json.dumps(before));x['dimensions']['characters'][2]=after['dimensions']['characters'][2];x['dimensions']['continuity'][4]=after['dimensions']['continuity'][4];x['open_questions']=[q for q in x['open_questions'] if q['id']!='v02-q-zhanhua']
 for suffix,field,a,b in [('leizi','stage_change','不使用卷五现实回顾反填本卷具体死因','不以后卷信息反填本卷现实生死'),('yelai','relationships','不借卷五NPC夏禹职倒灌','不将其他实体的职务套给叶来')]:
  row=next(r for r in x['major_character_states'] if r['origin_key'].endswith('/character/'+suffix));row[field]=row[field].replace(a,b)
 assert x==after,'新增两处人物通用边界外分析变化'
 bc=read(B/'cards.json');ac=read(P/'cards.json');cc=json.loads(json.dumps(bc));ci=next(i for i,c in enumerate(cc) if c['origin_key'].endswith('/scene/unseal'));cc[ci]['content']['obstacle']=cc[ci]['content']['obstacle'].replace('姐妹目的不同','双方目的不同')
 for suffix,field,a,b in [('leizi','stage_change','不使用卷五现实回顾反填本卷具体死因','不以后卷信息反填本卷现实生死'),('yelai','relationship_direction','不借卷五NPC夏禹职倒灌','不将其他实体的职务套给叶来')]:
  row=next(r for r in cc if r['origin_key'].endswith('/character/'+suffix));row['content'][field]=row['content'][field].replace(a,b)
 assert cc==ac,'已要求三处卡词外发生变化'
 assert h(B/'graph.json')==h(P/'graph.json')
 assert h(B/'chapter-notes.jsonl')==h(P/'chapter-notes.jsonl') and h(B/'read-log.json')==h(P/'read-log.json')
 deltas=[{'path':'dimensions.characters[2].limits_and_counterevidence','before':before['dimensions']['characters'][2]['limits_and_counterevidence'],'after':after['dimensions']['characters'][2]['limits_and_counterevidence']},{'path':'dimensions.continuity[4]','before':before['dimensions']['continuity'][4],'after':after['dimensions']['continuity'][4]},{'path':'open_questions/v02-q-zhanhua','before':next(q for q in before['open_questions'] if q['id']=='v02-q-zhanhua'),'after':None,'reason':'研究者误合两剑造成假物链，撤回；不删除原逐章笔记。'}]
 deltas.append({'path':'cards.scene/unseal.content.obstacle','before':bc[ci]['content']['obstacle'],'after':ac[ci]['content']['obstacle'],'reason':'primary追加要求：双方是主队与池妹，不是姐妹。'})
 for suffix,field in [('leizi','stage_change'),('yelai','relationship_direction')]:
  b=next(c for c in bc if c['origin_key'].endswith('/character/'+suffix));a=next(c for c in ac if c['origin_key'].endswith('/character/'+suffix));deltas.append({'path':'cards.character/'+suffix+'.content.'+field,'before':b['content'][field],'after':a['content'][field],'major_character_states_synchronized':True})
 save(C/'raw0314-two-swords-delta.json',{'status':'applied-draft-primary-requested-correction','reader':'/root/zongheng_vol04_full','reread':'raw0314 BEGIN L26847—END L26930实际全文复核；必要回读不新增覆盖数','changes':deltas,'unchanged':['graph.json','chapter-notes.jsonl','read-log.json'],'analysis_other_values_equal':True,'cards_other_values_equal':True,'before_sha256':{n:h(B/n) for n in names},'after_sha256':{n:h(P/n) for n in ['analysis.json','cards.json','graph.json','chapter-notes.jsonl','read-log.json','report.md','handoff.md']},'supporting_overlay':'../priority-corrections-delta.json'})
 print(json.dumps({'delta_sha256':h(C/'raw0314-two-swords-delta.json'),'analysis_sha256':h(P/'analysis.json')},ensure_ascii=False))
