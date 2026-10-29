"""本代理卷五/七隔离准备；只读JSON元数据，不打开normalized原文。"""
import ast,hashlib,json,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
HERE=Path(__file__).resolve().parent;BOOK=HERE.parent;ROOT=HERE.parents[4]
load=lambda p:json.loads(p.read_text(encoding='utf-8'))
save=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
S=load(BOOK/'source.json');SID='src-d8926e2a35f04bcf8139cff0ea516bbd';REV='d819f7d0ecf5a2004a0a434e987569bbe25015422d45e16676af913292346857'
assert S['slug']=='tianxia-wushuang' and S['source_id']==SID and S['revision']==REV
U=load(ROOT/'writing-vault/library/reports/collection/reading-units.json')[SID]
assert U['source_revision']==REV
REG=load(ROOT/'writing-vault/library/sources'/f'{SID}.json');assert REG['revision']==REV
RR=next(x for x in REG['revisions'] if x['revision']==REV);assert S['chapters']==RR['chapters']
fields=['unit_id','segment_ids','title','kind','printed_numbers','start_line','end_line']
units=S['preface']+[u for v in S['volumes'] for u in v['units']]
assert [{k:u[k] for k in fields} for u in units]==[{k:u[k] for k in fields} for u in U['units']]
spec_hash=hashlib.sha256((BOOK/'source.json').read_bytes()).hexdigest()
script=(HERE/'save_notes.py').read_text(encoding='utf-8');ast.parse(script)
expected_ranges={5:(265,266,'ch-0793','ch-1058',787,1051),7:(210,211,'ch-1294','ch-1504',1286,1495)}
prepared=[]
for v in [5,7]:
 d=BOOK/f'vol{v:02}';d.mkdir(exist_ok=True)
 spec=next(x for x in S['volumes'] if x['volume']==v);us=spec['units'];body=[u for u in us if u['kind'] in ['body','prologue']]
 assigned=[c['chapter_id'] for u in us for c in u['segments']]
 target=expected_ranges[v];assert (len(body),len(assigned),assigned[0],assigned[-1],body[0]['printed_numbers'][0],body[-1]['printed_numbers'][-1])==target
 assert len(assigned)==len(set(assigned));assert all(len(u['segments'])==1 for u in us)
 assert all(a['end_line']+1==b['start_line'] for a,b in zip([c for u in us for c in u['segments']],[c for u in us for c in u['segments']][1:]))
 assignment=dict(source_id=SID,revision=REV,volume=v,reader='/root/zongheng_vol04_full',metadata_only=True,status='prepared_unread',reading_authorized=False,source_spec_sha256=spec_hash,reading_units_index_fingerprint=U['index_fingerprint'],start_gate='等主代理明确启动本书正文；卷五完成交付后继续卷七，元数据准备不解除启动门槛。',body_unit_count=len(body),raw_body_segment_count=sum(len(u['segments']) for u in body),raw_segments_including_header=len(assigned),raw_range=[assigned[0],assigned[-1]],first_body_chapter_id=body[0]['segment_ids'][0],printed_body_range=[body[0]['printed_numbers'][0],body[-1]['printed_numbers'][-1]],line_range=[us[0]['start_line'],us[-1]['end_line']],unit_ids=[u['unit_id'] for u in us],assigned_chapter_ids=assigned,index_corrections=[x for x in U['index_corrections'] if x['segment_id'] in assigned],rules=['只计真实全文阅读；当前正文、标题、片段已读均0','独立卷标题也须实际读并列入精确coverage，不计正文章','按unit全部segments完成计正文；不用raw减偏移猜印刷章号','每2—4实际读片段持久化；截断必须补读，不提前记full_text_read','不读后卷结果倒填本卷；其他书同名人物不自动合并','不写正式库/Git/其他代理目录'])
 state=dict(source_id=SID,revision=REV,volume=v,reader='/root/zongheng_vol04_full',status='prepared_unread',metadata_only=True,reading_authorized=False,read_chapter_ids=[],completed_chapter_ids=[],completed_count=0,completed_body_units=0,body_units_completed=0,raw_segments_completed=0,volume_headers_completed=0,next_chapter_id=assigned[0],first_body_chapter_id=body[0]['segment_ids'][0],assigned_chapter_ids=assigned,pending_chapter_ids=assigned,pending_truncations=[],unresolved_truncations=[],complete_volume=False,complete_book=False,note='只准备元数据和保存器，正文/标题0已读；等待主代理明确启动。')
 log=dict(source_id=SID,revision=REV,volume=v,reader='/root/zongheng_vol04_full',status='prepared_unread',metadata_only=True,complete_volume=False,complete_book=False,reading_unit_count=len(body),assigned_segment_count=len(assigned),body_units_completed=0,raw_segments_completed=0,volume_headers_completed=0,chapters=[],method='当前未开始全文阅读；不把assigned/pending或目录元数据计已读。',review_status='draft')
 for name,data in [('assignment.json',assignment),('reader-state.json',state),('read-log.json',log)]:
  p=d/name
  if p.exists():assert load(p)==data,f'existing state differs; do not reset {p}'
  else:save(p,data)
 notes=d/'chapter-notes.jsonl'
 if notes.exists():assert notes.stat().st_size==0,'existing notes must not be reset'
 else:notes.write_text('',encoding='utf-8')
 saver=d/'save_notes.py'
 if saver.exists():assert saver.read_text(encoding='utf-8')==script
 else:saver.write_text(script,encoding='utf-8')
 row=dict(volume=v,status='prepared_unread',body_units=len(body),raw_segments_including_header=len(assigned),raw_range=assignment['raw_range'],first_body_chapter_id=assignment['first_body_chapter_id'],printed_body_range=assignment['printed_body_range'],line_range=assignment['line_range'],reading_authorized=False,body_read_count=0,raw_segment_read_count=0,normalized_content_opened=False,source_id=SID,revision=REV,source_spec_sha256=spec_hash,reading_units_index_fingerprint=U['index_fingerprint'],saver_syntax='passed',saver_sha256=hashlib.sha256(saver.read_bytes()).hexdigest(),shared_helpers_modified=False,Vault_or_import_run=False)
 save(d/'prepared-check.json',row)
 handoff=['# 本卷元数据准备交接','',f"卷{v}；{len(body)}正文，含卷标题{len(assigned)}原片段；范围`{assigned[0]}—{assigned[-1]}`，印刷正文{assignment['printed_body_range'][0]}—{assignment['printed_body_range'][1]}。",'', '**状态：prepared_unread，正文、标题和原片段实际已读均0。** 没有打开normalized或调用读章器。','', '来源与阅读单元映射已按正式登记核对；`assignment.json`固定全部指定ID，`reader-state.json`、`read-log.json`空账，`chapter-notes.jsonl`为空。','', '保存器`save_notes.py --check`只核元数据/已有账；`--batch`默认因reading_authorized=false拒绝保存。以后主代理明确启动后，在assignment和state同时解除metadata_only并记start_authorization_reference，再按全文实际提供观察。不要为测试伪造已读记录。','', '批次JSON顶层需source_id/revision/volume/reader/observations；每条提供chapter_id、facts/inferences/state_changes/unresolved数组，model_full_text_read=true、begin_marker_seen=true、end_marker_seen=true、end_marker精确匹配、unresolved_truncation=false。保存器拒重复、越卷、错修订和不连续输入；本身不读取正文。','', '续读先读本卷state与前卷handoff；未读前史明确标派生/未知，不能把纵横或其他书同名人物命运倒灌。本代理顺序卷五→卷七，单卷交付八类产物后再换卷，不写正式库。','', '当前只完成隔离准备，不运行check_volume/import_volume、不伪造研究包；启动后仍须实际读全卷标题和正文全部片段才满足覆盖。','']
 (d/'preparation-handoff.md').write_text('\n'.join(handoff),encoding='utf-8');prepared.append(row)
print(json.dumps(dict(status='prepared_metadata_only',volumes=prepared,normalized_content_opened=False,shared_helpers_modified=False),ensure_ascii=False))
