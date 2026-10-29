"""本卷读者保存器；只保存模型实际读完的观察，绝不打开小说正文。"""
import argparse,hashlib,json,os,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
HERE=Path(__file__).resolve().parent
load=lambda p:json.loads(p.read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def context():
 assignment=load(HERE/'assignment.json');state=load(HERE/'reader-state.json')
 source_path=HERE.parent/'source.json';source=load(source_path)
 assert source['slug']=='tianxia-wushuang'
 assert source['source_id']==assignment['source_id']==state['source_id']
 assert source['revision']==assignment['revision']==state['revision']
 assert sha(source_path)==assignment['source_spec_sha256'],'source metadata changed; do not continue from stale boundaries'
 assert assignment['reader']==state['reader']=='/root/zongheng_vol04_full'
 volume=assignment['volume'];assert state['volume']==volume and HERE.name==f'vol{volume:02}'
 spec=next(v for v in source['volumes'] if v['volume']==volume)
 expected=[c['chapter_id'] for u in spec['units'] for c in u['segments']]
 assert expected==assignment['assigned_chapter_ids']==state['assigned_chapter_ids']
 units=load(HERE.parents[4]/'writing-vault/library/reports/collection/reading-units.json')[source['source_id']]
 assert units['source_revision']==source['revision']
 assert units['index_fingerprint']==assignment['reading_units_index_fingerprint']
 cmeta={c['chapter_id']:c for c in source['chapters']}
 unit_for={c['chapter_id']:u for u in spec['units'] for c in u['segments']}
 records=[json.loads(line) for line in (HERE/'chapter-notes.jsonl').read_text(encoding='utf-8').splitlines() if line.strip()]
 ids=[n['chapter_id'] for n in records]
 assert ids==expected[:len(ids)],'notes must be a unique contiguous assigned prefix'
 for n in records:
  c=cmeta[n['chapter_id']]
  assert n['source_id']==source['source_id'] and n['revision']==source['revision']
  assert n['reader']==assignment['reader'] and n['full_text_read'] is True
  assert n['start_line']==c['start_line'] and n['end_line']==c['end_line']
 assert ids==state['completed_chapter_ids']==state['read_chapter_ids']
 return assignment,state,source,spec,expected,cmeta,unit_for,records

def atomic_write(path,text):
 assert path.parent.resolve()==HERE,'write must stay inside this volume directory'
 temp=path.with_name(path.name+'.saving')
 assert not temp.exists(),'previous interrupted write requires inspection'
 temp.write_text(text,encoding='utf-8');os.replace(temp,path)

def save_batch(path):
 assignment,state,source,spec,expected,cmeta,unit_for,records=context()
 assert assignment['reading_authorized'] is True and state['reading_authorized'] is True,'NOT_STARTED: explicit primary start authorization is required'
 assert assignment['metadata_only'] is False and state['metadata_only'] is False
 assert state.get('start_authorization_reference'),'start message reference required'
 assert not state.get('pending_truncations') and not state.get('unresolved_truncations'),'finish the pending truncated text before marking any full read'
 path=path.resolve();assert path.parent==HERE,'batch must be persisted in this volume directory'
 batch=load(path)
 assert batch['source_id']==source['source_id'] and batch['revision']==source['revision']
 assert batch['volume']==assignment['volume'] and batch['reader']==assignment['reader']
 observations=batch['observations'];assert isinstance(observations,list) and 1<=len(observations)<=4
 new=[];start=len(records)
 for offset,observation in enumerate(observations):
  o=dict(observation);cid=o['chapter_id']
  assert start+offset<len(expected) and cid==expected[start+offset],'must save the next consecutive assigned segments'
  c=cmeta[cid];u=unit_for[cid]
  assert o.pop('model_full_text_read',None) is True
  assert o.pop('begin_marker_seen',None) is True and o.pop('end_marker_seen',None) is True
  assert o.pop('end_marker',None)==f"END {cid} L{c['end_line']}"
  assert o.pop('unresolved_truncation',None) is False
  for field in ['facts','inferences','state_changes','unresolved']:
   assert field in o and isinstance(o[field],list),f'missing reader observation list: {field}'
  assert o['facts'],'a read segment must have an actual observation, including a header when applicable'
  forbidden={'source_id','revision','reader','volume','title','start_line','end_line','full_text_read','unit_id','unit_kind'}&set(o)
  assert not forbidden,f'protected metadata must not be supplied by observations: {forbidden}'
  new.append(dict(**o,source_id=source['source_id'],revision=source['revision'],reader=assignment['reader'],volume=assignment['volume'],title=c['title'],start_line=c['start_line'],end_line=c['end_line'],full_text_read=True,unit_id=u['unit_id'],unit_kind=u['kind']))
 records+=new;done={n['chapter_id'] for n in records}
 body=[u for u in spec['units'] if u['kind'] in ['body','prologue']]
 headers=[u for u in spec['units'] if u['kind'] not in ['body','prologue']]
 completed_bodies=sum(set(u['segment_ids'])<=done for u in body)
 completed_headers=sum(set(u['segment_ids'])<=done for u in headers)
 state.update(status='read_complete_pending_research' if len(done)==len(expected) else 'reading',metadata_only=False,read_chapter_ids=[x for x in expected if x in done],completed_chapter_ids=[x for x in expected if x in done],completed_count=len(done),completed_body_units=completed_bodies,body_units_completed=completed_bodies,raw_segments_completed=len(done),volume_headers_completed=completed_headers,next_chapter_id=next((x for x in expected if x not in done),None),pending_chapter_ids=[x for x in expected if x not in done],pending_truncations=[],unresolved_truncations=[],complete_volume=len(done)==len(expected),complete_book=False,note='只计本读者实际全文读完的原片段；研究交付与主审另记，前后卷和同名人物事实不倒灌。')
 log=dict(source_id=source['source_id'],revision=source['revision'],volume=assignment['volume'],reader=assignment['reader'],status=state['status'],metadata_only=False,complete_volume=state['complete_volume'],complete_book=False,reading_unit_count=assignment['body_unit_count'],assigned_segment_count=len(expected),body_units_completed=completed_bodies,raw_segments_completed=len(done),volume_headers_completed=completed_headers,chapters=[{k:n[k] for k in ['chapter_id','start_line','end_line','full_text_read','reader']} for n in records],method='由模型按全文BEGIN/END实际阅读后提供2—4片段观察；本脚本只保存元数据/笔记，不读取normalized正文。',review_status='draft')
 # 所有观察检查完后才写；先笔记再日志/状态，若写入被中断则保留文件供人工对账，不自动重置。
 atomic_write(HERE/'chapter-notes.jsonl',''.join(json.dumps(n,ensure_ascii=False)+'\n' for n in records))
 atomic_write(HERE/'read-log.json',json.dumps(log,ensure_ascii=False,indent=2)+'\n')
 atomic_write(HERE/'reader-state.json',json.dumps(state,ensure_ascii=False,indent=2)+'\n')
 return dict(status=state['status'],volume=assignment['volume'],body_units_completed=completed_bodies,raw_segments_completed=len(done),volume_headers_completed=completed_headers,next_chapter_id=state['next_chapter_id'])

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');parser.add_argument('--batch',type=Path);args=parser.parse_args()
 assert args.check != (args.batch is not None),'choose --check or --batch'
 if args.check:
  assignment,state,source,spec,expected,cmeta,unit_for,records=context()
  print(json.dumps(dict(status='metadata-and-saver-check-passed',volume=assignment['volume'],reading_authorized=state['reading_authorized'],body_units_completed=state['completed_body_units'],raw_segments_completed=len(records),expected_raw_segments=len(expected),next_chapter_id=state['next_chapter_id'],normalized_content_opened=False),ensure_ascii=False))
 else:print(json.dumps(save_batch(args.batch),ensure_ascii=False))
if __name__=='__main__':main()
