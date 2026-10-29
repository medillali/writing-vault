"""本专项的只读输入切片与独立记录辅助，不自动作语义裁定。"""
import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

HERE = Path(__file__).resolve().parent
POOL = HERE.parent / 'local-question-pool.json'
ROOT = HERE.parents[6]
BOOK = HERE.parents[2]
FORMAL = ROOT / 'writing-vault/library/reports/tianxia-wushuang'

def load_pool():
    data = json.loads(POOL.read_text(encoding='utf-8-sig'))
    if isinstance(data, list):
        return data
    for key in ('candidates', 'items', 'questions'):
        if key in data:
            return data[key]
    raise ValueError(list(data))

def main():
    p = argparse.ArgumentParser()
    p.add_argument('action')
    p.add_argument('args', nargs='*')
    a = p.parse_args()
    if a.action == 'meta':
        rows = load_pool()
        freeze = json.loads((HERE.parent/'candidate-id-freeze.json').read_text(encoding='utf-8-sig'))
        selected = [r for r in rows if int(r['volume']) <= 4]
        print(json.dumps({'pool_sha256':hashlib.sha256(POOL.read_bytes()).hexdigest(), 'count':len(rows), 'assigned':len(selected), 'by_volume':dict(Counter(r['volume'] for r in selected)), 'candidate_keys':list(selected[0]), 'first':selected[0], 'local_identity_hash':freeze['local']['candidate_identity_sha256'], 'formal_files':[{ 'name':q.name,'lines':len(q.read_text(encoding='utf-8-sig').splitlines()),'bytes':q.stat().st_size} for q in FORMAL.glob('vol0[123]*') if q.suffix in ('.md','.json')]}, ensure_ascii=False, indent=2))
    elif a.action == 'snapshot':
        rows = [r for r in load_pool() if int(r['volume'])<=4]
        if len(rows)!=923:
            raise ValueError(len(rows))
        output = HERE/'assigned-candidates.json'
        if output.exists():
            raise FileExistsError(output)
        output.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        log = []
        for v in range(1,4):
            for name in (f'vol{v:02d}.md',f'vol{v:02d}-handoff.md'):
                f = FORMAL/name
                log.append({'path':str(f.relative_to(ROOT)).replace('\\','/'),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'access':'complete_derived_interface_read','original_reader':'primary' if v<3 else '/root/zongheng_vol03_full','personal_original_reread':False,'truncation_repaired':'report L85—130 reread' if v==3 and name.endswith('.md') and 'handoff' not in name else None})
        (HERE/'input-read-log.json').write_text(json.dumps({'assigned_count':923,'pool_sha256_at_assignment':hashlib.sha256(POOL.read_bytes()).hexdigest(),'local_identity_hash':'de58286c9cba34cdeee288a55c261c98d55aaed83eeac0f011436263aa132b56','interfaces':log,'candidate_record_reads':[{'volume':1,'offset':1,'count':27,'format':'exact complete original prose/observation/detail, evidence metadata deduplicated, all atomic titles preserved','truncated_attempt_repaired':True}],'attribution':'本审阅者原亲读卷四和卷六前175片；本次卷一至三接口为派生材料阅读，不声称原文重读。'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(json.dumps({'snapshot_count':len(rows),'snapshot_sha256':hashlib.sha256(output.read_bytes()).hexdigest()},ensure_ascii=False))
    elif a.action == 'mark':
        volume,start,count = map(int,a.args)
        f = HERE/'input-read-log.json'
        log = json.loads(f.read_text(encoding='utf-8'))
        log['candidate_record_reads'].append({'volume':volume,'offset':start,'count':count,'format':'exact complete original prose/observation/detail with atomic titles, repeated evidence metadata deduplicated','truncated_pending':False})
        f.write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print('marked')
    elif a.action == 'marknotes':
        wanted = {f'ch-{int(c):04d}' for c in a.args}
        f = HERE/'input-read-log.json'
        log = json.loads(f.read_text(encoding='utf-8'))
        stored = {r['chapter_id']:r for r in log.get('complete_derived_notes_read',[])}
        for v in range(1,9):
            nf = BOOK/f'vol{v:02d}'/'chapter-notes.jsonl'
            if nf.exists():
                for line in nf.read_text(encoding='utf-8-sig').splitlines():
                    n = json.loads(line)
                    if n.get('chapter_id') in wanted:
                        stored[n['chapter_id']]={'chapter_id':n['chapter_id'],'path':str(nf.relative_to(ROOT)).replace('\\','/'),'record_sha256':hashlib.sha256(line.encode('utf-8')).hexdigest(),'original_reader':n.get('reader'),'access':'complete_derived_note_read_not_original_text_reread'}
        log['complete_derived_notes_read']=list(sorted(stored.values(),key=lambda x:x['chapter_id']))
        for v in (5,7,8):
            ip = FORMAL/f'vol{v:02d}-handoff.md'
            if not any(r['path']==str(ip.relative_to(ROOT)).replace('\\','/') for r in log['interfaces']):
                log['interfaces'].append({'path':str(ip.relative_to(ROOT)).replace('\\','/'),'sha256':hashlib.sha256(ip.read_bytes()).hexdigest(),'access':'complete_derived_interface_read','personal_original_reread':False})
        f.write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(json.dumps({'complete_derived_notes_logged':len(stored)},ensure_ascii=False))
    elif a.action == 'file':
        target = Path(a.args[0])
        start = int(a.args[1]) if len(a.args)>1 else 1
        end = int(a.args[2]) if len(a.args)>2 else 10**9
        lines = target.read_text(encoding='utf-8-sig').splitlines()
        print(f'BEGIN FILE {target} L{start}—{min(end,len(lines))} TOTAL {len(lines)}')
        for i in range(start-1,min(end,len(lines))):
            print(f'L{i+1}: {lines[i]}')
        print('END FILE')
    elif a.action == 'finalize':
        decisions_path = HERE / a.args[0]
        decisions = json.loads(decisions_path.read_text(encoding='utf-8-sig'))
        assigned = {r['candidate_id']:r for r in json.loads((HERE/'assigned-candidates.json').read_text(encoding='utf-8-sig'))}
        output = []
        for decision in decisions:
            if isinstance(decision,list):
                decision = dict(zip(('candidate_id','status','audit_domain','rationale','later_chapters','evidence_basis'),decision))
            original = assigned[decision['candidate_id']]
            if decision['status'] not in ('answered','partial','unrecovered','unknown'):
                raise ValueError(decision)
            if not decision['rationale'].strip() or not decision['audit_domain']:
                raise ValueError(decision)
            row = {k:v for k,v in original.items() if k!='terminal_assessment'}
            row.update(decision)
            row['later_evidence'] = decision.get('later_evidence',[])
            existing = {e['chapter_id'] for e in row['later_evidence']}
            for chapter in row['later_chapters']:
                cid = f'ch-{chapter:04d}'
                if cid in existing:
                    continue
                evidence = next((e for e in original['original_evidence'] if e['chapter_id']==cid),None)
                if evidence is not None:
                    row['later_evidence'].append(evidence)
                    existing.add(cid)
                    continue
                if not decision.get('evidence_basis'):
                    raise ValueError(f'后证{cid}须显式提供已读派生定位：{decision["candidate_id"]}')
                found = None
                for v in range(1,9):
                    nf = BOOK/f'vol{v:02d}'/'chapter-notes.jsonl'
                    if nf.exists():
                        for line in nf.read_text(encoding='utf-8-sig').splitlines():
                            note = json.loads(line)
                            if note.get('chapter_id') == cid:
                                found = note
                                break
                    if found is not None:
                        break
                if found is None:
                    raise ValueError('缺章节定位'+cid)
                citation_path = str(nf.relative_to(ROOT)).replace('\\','/') if decision['evidence_basis'].endswith('chapter-notes.jsonl') else decision['evidence_basis']
                row['later_evidence'].append({'source_id':'src-d8926e2a35f04bcf8139cff0ea516bbd','revision':'d819f7d0ecf5a2004a0a434e987569bbe25015422d45e16676af913292346857','chapter_id':cid,'start_line':found['start_line'],'end_line':found['end_line'],'claim_kind':'fact','access_level':'derived-volume-research','research_path':citation_path,'locator_basis':'existing chapter notes metadata; no additional original-text-reading claim'})
                existing.add(cid)
            row['reviewer'] = '/root/zongheng_vol05_full'
            row['review_status'] = 'draft_for_primary_review'
            output.append(row)
        if len({r['candidate_id'] for r in output})!=len(output):
            raise ValueError('重复ID')
        basename = decisions_path.stem.replace('decisions','adjudications-local')
        jf, mf = HERE/(basename+'.json'), HERE/(basename+'.md')
        jf.write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        md = ['# 无双本地候选终点评定：'+decisions_path.stem,'','本文件为独立待主审裁定；保留原记录，非池主档。chapter号均为raw。其他卷派生输入不冒称原文复读。','']
        for row in output:
            md.extend(['## '+row['candidate_id'],'','- 原子项：'+row['title'],'- 完整原记录：'+json.dumps(row['original_record'],ensure_ascii=False),'- 终点：'+row['status']+'；领域：'+row['audit_domain'],'- 理由：'+row['rationale'],'- 后证：'+(', '.join(f'{c:04d}' for c in row['later_chapters']) or '无新增回收证；原始证据保留在JSON，未知不等作者遗忘。'),''])
        mf.write_text('\n'.join(md)+'\n',encoding='utf-8')
        print(json.dumps({'count':len(output),'statuses':dict(Counter(r['status'] for r in output)),'outputs':{jf.name:hashlib.sha256(jf.read_bytes()).hexdigest(),mf.name:hashlib.sha256(mf.read_bytes()).hexdigest()}},ensure_ascii=False))
    elif a.action == 'candidates':
        volume, start, count = map(int, a.args)
        rows = [r for r in load_pool() if int(r['volume'])==volume]
        picked = rows[start-1:start-1+count]
        print(f'BEGIN CANDIDATES volume={volume} offset={start} count={len(picked)} total={len(rows)}')
        for r in picked:
            print(json.dumps(r,ensure_ascii=False))
        print('END CANDIDATES')
    elif a.action == 'records':
        volume, start, count = map(int, a.args)
        rows = [r for r in load_pool() if int(r['volume'])==volume]
        picked = rows[start-1:start-1+count]
        print(f'BEGIN RECORDS volume={volume} offset={start} count={len(picked)} total={len(rows)}')
        seen = set()
        for r in picked:
            key = (r['original_field'],r['original_index'])
            if key not in seen:
                record = r['original_record']
                prose = {k:v for k,v in record.items() if k!='evidence'} if isinstance(record,dict) else record
                evidence = [{k:e[k] for k in ('chapter_id','start_line','end_line','claim_kind') if k in e} for e in r['original_evidence']]
                print(json.dumps({'original_field':key[0],'original_index':key[1],'complete_original_record_except_repeated_evidence_metadata':prose,'evidence_locators':evidence},ensure_ascii=False))
                seen.add(key)
            print(json.dumps({'candidate_id':r['candidate_id'],'atomic_index':r['atomic_index'],'exact_atomic_title':r['title']},ensure_ascii=False))
        print('END RECORDS')
    elif a.action == 'notes':
        wanted = {f'ch-{int(c):04d}' for c in a.args}
        for v in range(1,9):
            f = BOOK / f'vol{v:02d}' / 'chapter-notes.jsonl'
            if f.exists():
                for line in f.read_text(encoding='utf-8-sig').splitlines():
                    row = json.loads(line)
                    if row.get('chapter_id') in wanted:
                        print(json.dumps({'volume':v,'record':row},ensure_ascii=False))
    else:
        raise ValueError(a.action)

if __name__=='__main__':
    main()
