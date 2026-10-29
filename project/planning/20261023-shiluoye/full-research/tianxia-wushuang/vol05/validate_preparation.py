"""只检隔离元数据和未启动保存门槛；不读取正文，不造观察批次。"""
import ast,hashlib,json,runpy,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
HERE=Path(__file__).resolve().parent;BOOK=HERE.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
results=[]
for volume in [5,7]:
 d=BOOK/f'vol{volume:02}'
 protected=['assignment.json','reader-state.json','read-log.json','chapter-notes.jsonl']
 before={f:sha(d/f) for f in protected}
 ast.parse((d/'save_notes.py').read_text(encoding='utf-8'))
 module=runpy.run_path(str(d/'save_notes.py'),run_name='prepared_saver_check')
 assignment,state,source,spec,expected,cmeta,unit_for,records=module['context']()
 assert not records and (d/'chapter-notes.jsonl').stat().st_size==0
 assert state['status']=='prepared_unread' and state['metadata_only'] is True and state['reading_authorized'] is False
 assert state['body_units_completed']==state['raw_segments_completed']==state['volume_headers_completed']==0
 assert not state['complete_volume'] and not state['complete_book']
 assert json.loads((d/'read-log.json').read_text(encoding='utf-8'))['chapters']==[]
 missing=d/'__no_reading_batch__.json';assert not missing.exists()
 try:module['save_batch'](missing)
 except AssertionError as error:
  assert 'NOT_STARTED' in str(error),str(error)
 else:raise AssertionError('unstarted saver accepted a batch')
 assert before=={f:sha(d/f) for f in protected},'gate test must not alter any reading ledger'
 assert not missing.exists()
 row=dict(status='passed_metadata_and_disabled_saver_gate',volume=volume,expected_body_units=assignment['body_unit_count'],expected_raw_segments=len(expected),first_segment=expected[0],last_segment=expected[-1],reading_authorized=False,actual_body_read_count=0,actual_raw_segment_read_count=0,unauthorized_save_rejected_before_batch_open=True,ledger_sha256_unchanged=True,normalized_content_opened=False,normalized_hash_recomputed=False,actual_check_volume_run=False,actual_Vault_or_import_run=False,syntax='passed',ledger_sha256=before,saver_sha256=sha(d/'save_notes.py'))
 (d/'preparation-validation.json').write_text(json.dumps(row,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');results.append(row)
print(json.dumps(dict(status='passed_metadata_only',volumes=results),ensure_ascii=False))
