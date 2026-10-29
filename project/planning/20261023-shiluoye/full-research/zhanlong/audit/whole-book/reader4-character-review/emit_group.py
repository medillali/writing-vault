import sys,json,hashlib
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
D=Path(__file__).resolve().parent;A=D.parent;ROOT=D.parents[6];F=ROOT/'writing-vault/library/reports/zhanlong'
def rd(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def wr(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
receipt=rd(D/'input-receipt.json');assignment=receipt['assignment'];source=rd(A.parents[1]/'source.json')
notes={};note_paths={}
for v in range(1,7):
 p=F/f'vol{v:02}-chapter-notes.jsonl'
 for s in p.read_text(encoding='utf-8-sig').splitlines():
  x=json.loads(s);notes[x['chapter_id']]=x;note_paths[x['chapter_id']]=p
data=rd(D/sys.argv[1]);num=data['group'];dest=A/f'reader4-character-arcs-part{num:02}.json';assert not dest.exists(),'frozen output exists; use explicit delta'
pins=dict(receipt['formal_input_sha256']);rows=[];excerpts=[]
for d in data['rows']:
 i=d['assignment'];e=assignment[i-1];refs=[]
 for m in e['stage_cards']:
  p=F/f"vol{m['volume']:02}-cards.json";c=rd(p)[m['index']-1];assert c['origin_key']==m['origin_key']
  for ref in c['evidence']:
   x=dict(ref);x.update(access_level='derived-formal-character-and-state-interface',research_path=p.relative_to(ROOT).as_posix(),research_sha256=sha(p));x['original_reader']=notes.get(x['chapter_id'],{}).get('reader','source-card-attribution-not-expanded');refs.append(x)
 for ch in d.get('notes',[]):
  cid=f'ch-{ch:04}';n=notes[cid];p=note_paths[cid];pins[p.relative_to(ROOT).as_posix()]=sha(p)
  refs.append(dict(source_id=source['source_id'],revision=source['revision'],chapter_id=cid,start_line=n['start_line'],end_line=n['end_line'],claim_kind='fact',access_level='derived-formal-four-column-note',research_path=p.relative_to(ROOT).as_posix(),research_sha256=sha(p),original_reader=n['reader']))
 for ch,a,b in d.get('limited_ranges',[]):
  bounds=next(c for c in source['chapters'] if c['chapter_id']==f'ch-{ch:04}');assert bounds['start_line']<=a<=b<=bounds['end_line'],(i,ch,a,b,bounds)
  excerpts.append({'chapter_id':f'ch-{ch:04}','start_line':a,'end_line':b,'actual_reader':'/root/zongheng_vol04_full','access_scope':'targeted-limited-source-excerpt-not-full-chapter','additional_unique_chapters':0})
  refs.append(dict(source_id=source['source_id'],revision=source['revision'],chapter_id=f'ch-{ch:04}',start_line=a,end_line=b,claim_kind='fact',access_level='targeted-limited-source-excerpt-not-full-chapter',research_path=(D/f'part{num:02}-access-receipt.json').relative_to(ROOT).as_posix(),original_reader=notes[f'ch-{ch:04}']['reader']))
 for item in d.get('priority_sources',[]):
  p=ROOT/item['path'];pins[item['path']]=sha(p)
  for ch,a,b in item['refs']:
   refs.append(dict(source_id=source['source_id'],revision=source['revision'],chapter_id=f'ch-{ch:04}',start_line=a,end_line=b,claim_kind='fact',access_level=item.get('access_level','derived-primary-approved-priority-overlay'),research_path=item['path'],research_sha256=sha(p),original_reader=notes[f'ch-{ch:04}']['reader'],current_verifier='primary'))
 row={'audit_id':f'character-arc-r4-{i:03}','name':d.get('name',e['name']),**{k:d[k] for k in ['initial_comparison_stage','key_decisions','costs','terminal_state','evidence_boundaries']},'review_status':'draft','terminal_certainty':d.get('terminal_certainty','last_explicit_evidence_with_labelled_unknowns'),'stage_card_mapping':e['stage_cards'],'evidence':refs,'actual_reviewer':'/root/zongheng_vol04_full','reading_attribution':'本人原始全文为卷二raw252—404及卷五raw969—1179；卷二405—504为primary原读后本人完整派生接读。其余卷本次按正式卡/阶段状态/交接及列明逐章派生或限定原文范围接读；不冒称个人重新全文全书。证据original_reader保持首读者，限定复核不增加唯一覆盖。'}
 rows.append(row)
access={'source_id':source['source_id'],'revision':source['revision'],'status':'actual-derived-reading-and-limited-source-check-receipt','group':num,'actual_reviewer':'/root/zongheng_vol04_full','entities':[x['audit_id'] for x in rows],'cards_and_stage_states_complete':[assignment[d['assignment']-1] for d in data['rows']],'handoffs_read_complete':[f'vol{v:02}-handoff.md' for v in range(1,7)],'formal_note_rows_complete':sorted(set(ch for d in data['rows'] for ch in d.get('notes',[]))),'limited_source_ranges':excerpts,'targeted_full_indexed_chapters_actual_begin_end':data.get('direct_full_chapters',[]),'boundary':'仅记录实际材料访问；卡片引用不等本次逐章全文。'}
wr(D/f'part{num:02}-access-receipt.json',access);access_sha=sha(D/f'part{num:02}-access-receipt.json')
for row in rows:
 for ref in row['evidence']:
  if ref.get('research_path','').endswith(f'part{num:02}-access-receipt.json'):ref['research_sha256']=access_sha
pins[(D/f'part{num:02}-access-receipt.json').relative_to(ROOT).as_posix()]=access_sha
support={k:v for k,v in pins.items() if not k.startswith('writing-vault/')};pins={k:v for k,v in pins.items() if k.startswith('writing-vault/')}
wrapper={'status':'stable_group_draft_pending_primary_review','source_id':source['source_id'],'revision':source['revision'],'group_number':num,'actual_reviewer':'/root/zongheng_vol04_full','formal_input_sha256':pins,'additional_support_sha256':support,'characters':rows}
wr(dest,wrapper)
md=['# 《斩龙》reader4人物全弧第%d组（待主审）'%num,'','仅派生接读与列明限定原文核对，未宣个人全书原文重读。','']
for r in rows:
 md.extend(['## '+r['audit_id']+' '+r['name'],''])
 for k,label in [('initial_comparison_stage','起点'),('key_decisions','选择'),('costs','代价'),('terminal_state','终态'),('evidence_boundaries','边界')]:md.extend([label+'：'+r[k],''])
 md.extend(['阶段卡：'+'；'.join(f"v{m['volume']}:{m['title']} ({m['asset_id']})" for m in r['stage_card_mapping']) or '阶段卡：补核实体，未凭空制造旧卡。','证据：'+'；'.join(f"{z['chapter_id']} L{z['start_line']}—{z['end_line']}" for z in r['evidence']),''])
dest.with_suffix('.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
print(json.dumps({'json':dest.name,'sha256':sha(dest),'md_sha256':sha(dest.with_suffix('.md')),'characters':len(rows),'evidence_count':sum(len(x['evidence']) for x in rows)},ensure_ascii=False))
