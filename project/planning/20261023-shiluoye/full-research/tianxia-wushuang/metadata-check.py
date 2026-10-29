"""无双元数据准备：只读JSON登记/工具代码，不打开normalized正文。"""
import json,pathlib,collections,hashlib,sys,ast
sys.stdout.reconfigure(encoding='utf-8')
P=pathlib.Path(__file__).resolve().parent;ROOT=P.parents[3];WORK=P.parent
load=lambda p:json.loads(p.read_text(encoding='utf-8'))
save=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
S=load(P/'source.json');sid=S['source_id'];rev=S['revision']
R=load(ROOT/'writing-vault/library/sources'/f'{sid}.json');RR=next(x for x in R['revisions'] if x['revision']==R['revision'])
U=load(ROOT/'writing-vault/library/reports/collection/reading-units.json')[sid]
Q=load(ROOT/'writing-vault/exchanges/runs/run-queue-tianxia-wushuang-20261023.json')
assert S['slug']=='tianxia-wushuang' and sid=='src-d8926e2a35f04bcf8139cff0ea516bbd'
assert rev==R['revision']==U['source_revision']==Q['source_revision']
assert S['chapters']==RR['chapters']
assert len(S['chapters'])==1609
assert [c['chapter_id'] for c in S['chapters']]==[f'ch-{i:04d}' for i in range(1,1610)]
assert not Q['completed_chapters'] and len(Q['pending_chapters'])==1609
chapters={c['chapter_id']:c for c in S['chapters']}
unitkeys=('unit_id','segment_ids','title','kind','printed_numbers','start_line','end_line')
all_units=S['preface']+[u for v in S['volumes'] for u in v['units']]
assert [{k:u[k] for k in unitkeys} for u in all_units]==[{k:u[k] for k in unitkeys} for u in U['units']]
segments=[c['chapter_id'] for u in all_units for c in u['segments']]
assert segments==[c['chapter_id'] for c in S['chapters']]
assert len(segments)==len(set(segments))
for u in all_units:
 assert [c['chapter_id'] for c in u['segments']]==u['segment_ids']
 assert all(c==chapters[c['chapter_id']] for c in u['segments'])
 assert u['start_line']==u['segments'][0]['start_line'] and u['end_line']==u['segments'][-1]['end_line']
 assert all(a['end_line']+1==b['start_line'] for a,b in zip(u['segments'],u['segments'][1:]))
assert [v['volume'] for v in S['volumes']]==list(range(1,9))
assert [v['body_units'] for v in S['volumes']]==[90,135,376,185,265,234,210,104]
nums=[n for u in all_units if u['kind']=='body' for n in u['printed_numbers']]
assert nums==list(range(1,1600))
assert len(S['preface'])==1 and S['preface'][0]['segment_ids']==['ch-0001']
assert len(U['index_corrections'])==1
correction=U['index_corrections'][0]
assert correction['segment_id']=='ch-0399' and correction['attached_to']=='ch-0398'
split=next(u for u in all_units if len(u['segment_ids'])>1)
assert split['unit_id']=='ch-0398' and split['segment_ids']==['ch-0398','ch-0399']
# 只stat确认文件存在，不read_bytes/hash/read_text原文；现修订一致性来自元数据。
normalized=pathlib.Path(S['normalized_path']);assert normalized.is_file()
tools={}
for name in ['read_chapters.py','save_primary_notes.py','check_volume.py','import_volume.py']:
 path=WORK/name;text=path.read_text(encoding='utf-8');ast.parse(text)
 tools[name]={'syntax':'passed','sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
assert "'tianxia-wushuang':'网游之天下无双'" in (WORK/'check_volume.py').read_text(encoding='utf-8')
assert "'tianxia-wushuang':'天下无双'" in (WORK/'import_volume.py').read_text(encoding='utf-8')
volume_rows=[]
for v in S['volumes']:
 units=v['units'];body=[u for u in units if u['kind'] in ['body','prologue']]
 volume_rows.append({'volume':v['volume'],'title':units[0]['title'],'body_units':len(body),'units_including_header':len(units),'raw_segments':sum(len(u['segments']) for u in units),'first_segment':units[0]['segment_ids'][0],'last_segment':units[-1]['segment_ids'][-1],'first_body_segment':body[0]['segment_ids'][0],'printed_body_range':[body[0]['printed_numbers'][0],body[-1]['printed_numbers'][-1]],'line_range':[units[0]['start_line'],units[-1]['end_line']],'characters_from_existing_spec':v['characters']})
V=S['volumes'][2];assigned=[c['chapter_id'] for u in V['units'] for c in u['segments']]
assert len(assigned)==378 and V['body_units']==376
directory=P/'vol03';directory.mkdir(exist_ok=True)
assignment={'source_id':sid,'revision':rev,'volume':3,'reader':'/root/zongheng_vol03_full','metadata_only':True,'status':'prepared_unread','reading_authorized':False,'start_gate':'先由主代理确认纵横全书审计正式完成并明确启动本卷，再读正文；元数据准备不解除此门槛。','body_unit_count':376,'raw_body_segment_count':377,'raw_segments_including_header':378,'raw_range':['ch-0229','ch-0606'],'first_body_chapter_id':'ch-0230','printed_body_range':[226,601],'line_range':[21744,52260],'unit_ids':[u['unit_id'] for u in V['units']],'assigned_chapter_ids':assigned,'index_correction':correction,'split_unit':split,'rules':['ch-0398和ch-0399一阅读单元、两原证据片段，各需全文读并各记笔记','独立卷标题ch-0229也在check_volume精确覆盖中；不计入376正文','不把assigned/pending当read，不复制纵横人物/等级/因果为无双既知','未来每1—2片段检查END，每2—4片段持久化，截断必须补读']}
state={'source_id':sid,'revision':rev,'volume':3,'reader':'/root/zongheng_vol03_full','status':'prepared_unread','metadata_only':True,'reading_authorized':False,'read_chapter_ids':[],'completed_chapter_ids':[],'completed_count':0,'completed_body_units':0,'next_chapter_id':'ch-0229','first_body_chapter_id':'ch-0230','assigned_chapter_ids':assigned,'pending_chapter_ids':assigned,'pending_truncations':[],'complete_volume':False,'complete_book':False,'note':'仅元数据准备，正文0已读；待主代理明确启动。不把索引/目录计实际阅读全文。'}
log={'source_id':sid,'revision':rev,'volume':3,'status':'prepared_unread','metadata_only':True,'complete_volume':False,'complete_book':False,'reading_unit_count':376,'assigned_segment_count':378,'chapters':[],'method':'未开始全文阅读，当前只核元数据；启动后按原片段逐一记full_text_read与真实reader。','index_corrections':[correction],'review_status':'draft'}
for name,data in [('assignment.json',assignment),('reader-state.json',state),('read-log.json',log)]:
 path=directory/name
 if path.exists():
  old=load(path);assert old==data,f'已有不同状态不覆盖：{name}'
 else:save(path,data)
notes=directory/'chapter-notes.jsonl'
if notes.exists():assert not notes.read_text(encoding='utf-8').strip(),'已有阅读笔记不重置'
else:notes.write_text('',encoding='utf-8')
result={'status':'passed_metadata_only','source_id':sid,'revision':rev,'source_index_count':1609,'body_units':1599,'volume_headers':8,'front_matter_segments':1,'all_reading_units':len(all_units),'nonpreface_raw_segments':1608,'one_body_unit_has_two_segments':split['unit_id'],'printed_body_numbers_continuous':True,'volume_specs':volume_rows,'index_corrections':U['index_corrections'],'reading_units_index_fingerprint':U['index_fingerprint'],'registry_spec_units_queue_revision_match':True,'all_segments_exactly_once':True,'normalized_file_exists':True,'normalized_file_bytes_from_stat':normalized.stat().st_size,'normalized_content_opened':False,'normalized_hash_recomputed':False,'revision_validation_boundary':'只核spec/registry/reading-units/queue元数据同修订；没有本轮重读/重算正文hash。','tool_static_checks':tools,'actual_full_Vault_check_volume_run':False,'actual_import_volume_run':False,'body_read_count':0,'catalog_active_source_unchanged':'src-2a13958390274509b2af019f6b12d981','existing_queue_state':Q['state'],'vol03_prepared_files':['assignment.json','reader-state.json','read-log.json','chapter-notes.jsonl'],'required_shared_tool_code_changes':[],'recommendations':['不要运行prepare.py作本轮验证；它会打开三书正文并重写source.json','现read_chapters可按raw覆盖，但上层须按units列全segments，勿跳ch0399','save_primary_notes.py硬编码reader=primary，不能用于本子代理原样记读者；未来采用本卷专用保存器或加显式reader参数','front-matter ch0001须启动后另分责任并实际读/存supplementary-read-log，全8卷只覆盖1608不足全1609','不运行check_volume/import_volume直到真实阅读/产物/主审齐备；合章现schema兼容，勿伪造完成包来试','正式导卷三前须卷一二已导；作者顺序/active source切换由主代理在门槛满足后执行']}
save(P/'metadata-check.json',result)
print(json.dumps({k:result[k] for k in ['status','source_id','revision','source_index_count','body_units','volume_headers','all_reading_units','body_read_count','normalized_content_opened','required_shared_tool_code_changes']},ensure_ascii=False))
