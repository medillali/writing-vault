"""保存primary已经实际阅读全文后手写的笔记；仅附元数据，不读取正文或生成结论。"""
from pathlib import Path
import datetime, json, sys
sys.stdout.reconfigure(encoding='utf-8')
B=Path(__file__).resolve().parent
source=json.loads((B/'source.json').read_text(encoding='utf-8'))
v=int(sys.argv[1]);ranges={1:(152,251),2:(405,504),3:(654,753)}
start,end=ranges[v];dest=B/f'primary-vol{v:02d}-tail';dest.mkdir(parents=True,exist_ok=True)
batchpath=Path(sys.argv[2]).resolve();assert batchpath.is_relative_to(dest.resolve())
batch=json.loads(batchpath.read_text(encoding='utf-8'))
assert isinstance(batch,list) and 1<=len(batch)<=4
index={c['chapter_id']:c for c in source['chapters']}
notepath=dest/'chapter-notes.jsonl'
old=[json.loads(s) for s in notepath.read_text(encoding='utf-8').splitlines() if s.strip()] if notepath.exists() else []
done={r['chapter_id'] for r in old};now=datetime.datetime.now(datetime.timezone.utc).isoformat()
for authored in batch:
    cid=authored['chapter_id'];n=int(cid[3:]);assert start<=n<=end and cid not in done
    assert authored['full_text_read'] is True,'必须由实际读者手动确认，不能元数据自动标读'
    assert all(k in authored and isinstance(authored[k],list) for k in ['facts','inferences','state_changes','unresolved'])
    assert authored['facts'],'不可用空事实表示读过'
    c=index[cid]
    row=dict(authored,source_id=source['source_id'],revision=source['revision'],title=c['title'],start_line=c['start_line'],end_line=c['end_line'],reader='primary',read_at=now,reading_scope='actual-complete-raw-segment-in-assigned-tail')
    old.append(row);done.add(cid)
old.sort(key=lambda r:int(r['chapter_id'][3:]))
numbers=[int(r['chapter_id'][3:]) for r in old]
assert numbers==list(range(start,max(numbers)+1)),'只能按实际连续阅读保存，不能跳过待补片'
def write(path,x):path.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
temp=notepath.with_suffix('.pending')
temp.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in old),encoding='utf-8');temp.replace(notepath)
pending=[f'ch-{n:04d}' for n in range(start,end+1) if f'ch-{n:04d}' not in done]
state=dict(source_id=source['source_id'],revision=source['revision'],reader='primary',assigned_volume=v,assigned_raw_range=[start,end],completed_chapter_ids=[r['chapter_id'] for r in old],pending_chapter_ids=pending,next_raw_index=int(pending[0][3:]) if pending else None,truncated_pending=[],assigned_range_complete=not pending,complete_volume=False,complete_book=False,method='read_chapters.py实际BEGIN-END全文；每2—4章手写四栏笔记后持久化，helper不读正文不生成语义。')
write(dest/'reader-state.json',state)
write(dest/'read-log.json',dict(source_id=source['source_id'],revision=source['revision'],reader='primary',assigned_raw_range=[start,end],chapters=[{k:r[k] for k in ['chapter_id','start_line','end_line','full_text_read','reader','read_at']} for r in old],complete_book=False,complete_volume=False,assigned_range_complete=not pending,truncated_pending=[],scope='仅本尾段原文全文，不冒称此前prefix亲读；合并整卷时保逐行reader。'))
print(json.dumps({'volume':v,'saved_batch':len(batch),'actual_tail_segments':len(old),'target_segments':end-start+1,'next_raw':state['next_raw_index'],'complete_volume':False},ensure_ascii=False))
