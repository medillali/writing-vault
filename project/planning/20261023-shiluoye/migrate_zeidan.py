"""一次性迁移既有研究；通过现有 Vault 保存卡片及检查点。"""
import pathlib,sys,json,hashlib,copy,collections
sys.stdout.reconfigure(encoding='utf-8')
root=pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0,str(root/'distill-novels/scripts'))
from fictionlib.vault import Vault
from fictionlib.storage import atomic_write,json_text
vault=root/'writing-vault'; work=root/'.planning/20261023-shiluoye/zeidan'
old=root.parent/'Chinese Novel/books/zeidan/distillation'
s=json.loads((work/'source.json').read_text(encoding='utf-8'))
mapping=json.loads((work/'chapter-map.json').read_text(encoding='utf-8'))
byseq={x['legacy_sequence']:x for x in mapping}
v=Vault(vault)
# 此批不再改变来源；缓存来源目录减少每条证据重复读取八本章节清单，验证规则保持不变。
sources=v.sources(); source_lookup={name:src for src in sources for name in [src['source_id'],*src.get('aliases',[])]}
v._source=lambda sid:copy.deepcopy(source_lookup[sid])
report=vault/'library/reports/zeidan';report.mkdir(parents=True,exist_ok=True)
legacy=report/'legacy';legacy.mkdir(exist_ok=True)
provenance=[]
for name in ['coverage.json','validation.json','entities.json','entity-groups.json','scenes.json','threads.json','chapter-notes.jsonl','review-statistics.json','artifact-check.json']:
    data=(old/name).read_bytes(); target=legacy/name
    if target.exists() and target.read_bytes()!=data:raise ValueError('迁移副本冲突: '+str(target))
    target.write_bytes(data)
    provenance.append({'legacy_file':name,'sha256':hashlib.sha256(data).hexdigest(),'size':len(data)})

def evidence(record):
    output=[]
    kinds=['fact'] if record.get('facts') else ['inference']
    if record.get('inferences') and 'inference' not in kinds:kinds.append('inference')
    for e in record['evidence']:
        c=byseq[e['sequence']]
        assert c['start_line']<=e['line_start']<=e['line_end']<=c['end_line'],(record['record_id'],e,c)
        for kind in kinds:output.append({'source_id':s['source_id'],'revision':s['revision'],'chapter_id':c['chapter_id'],'start_line':e['line_start'],'end_line':e['line_end'],'claim_kind':kind})
    return output

saved=[]; candidates=[]
for filename,kind,prefix in [('entities.json','character','chr'),('scenes.json','scene','scn')]:
    records=json.loads((old/filename).read_text(encoding='utf-8'))
    for record in records:
        if kind=='character' and record['maintenance_depth'].startswith('待补'):
            candidates.append({**record,'mapped_evidence':evidence(record)});continue
        aid=prefix+'-zeidan-legacy-'+record['record_id'].lower()
        content={k:copy.deepcopy(val) for k,val in record.items() if k not in ['evidence','user_feedback']}
        content['summary']='；'.join(record.get('facts',[])[:2]) or '；'.join(record.get('inferences',[])[:2])
        content['provenance_note']='迁入旧库首轮研究，保留分段记录和事实/推断边界；本次不是重新全文阅读。'
        content['user_feedback']=record.get('user_feedback')
        content['legacy_record_ref']='library/reports/zeidan/legacy/'+filename+'#'+record['record_id']
        card={'asset_id':aid,'asset_type':kind,'scope':'source-analysis','title':'贼胆｜'+record['name']+'｜'+record['record_id'],'origin_key':s['source_id']+'/legacy/'+record['record_id'],'tags':['作者:发飙的蜗牛','作品:贼胆','既有研究迁入',record['worker_part']],'content':content,'evidence':evidence(record),'review_status':'draft','user_notes':'','favorite':False}
        path=vault/v._asset_path(aid); previous=json.loads(path.read_text(encoding='utf-8')) if path.exists() else None
        result=v.put_asset(card,previous['revision'] if previous else None,generated=True)
        saved.append({'asset_id':result['asset_id'],'revision':result['revision'],'legacy_record_id':record['record_id'],'asset_type':kind,'name':record['name']})
        if len(saved)%25==0:print('saved',len(saved),flush=True)
threads=json.loads((old/'threads.json').read_text(encoding='utf-8'))
mapped_threads=[{**r,'mapped_evidence':evidence(r)} for r in threads]
atomic_write(report/'threads.json',json_text({'source_id':s['source_id'],'source_revision':s['revision'],'records':mapped_threads,'boundary':'保留原阶段状态，不用末段信息静默覆盖早期记录；本次未重构新的因果图。'}))
atomic_write(report/'appearance-candidates.json',json_text(candidates))
atomic_write(report/'chapter-map.json',json_text(mapping))
atomic_write(report/'asset-map.json',json_text(saved))
atomic_write(report/'migration-audit.json',json_text({'source_id':s['source_id'],'source_revision':s['revision'],'mapped_chapters':len(mapping),'characters':sum(x['asset_type']=='character' for x in saved),'scenes':sum(x['asset_type']=='scene' for x in saved),'candidates':len(candidates),'threads':len(threads),'legacy_artifacts':provenance,'all_evidence_bounds_validated':True,'new_full_read_claim':False,'user_review_status':'pending'}))
completed=[c['chapter_id'] for c in mapping]
cp={'run_id':'run-legacy-zeidan-20261023','source_id':s['source_id'],'source_revision':s['revision'],'completed_chapters':completed,'pending_chapters':[c['chapter_id'] for c in s['chapters'] if c['chapter_id'] not in completed],'dimensions':['characters','plot'],'coverage_method':'imported_verified_legacy_reading_records','notes':'已迁入旧库463章逐章全文阅读记录。正文全覆盖；章前介绍未计入已读。旧研究主要人物/剧情/场景，不能升级成全书九维深化或本轮重新阅读。用户审阅待定。','assets':[x['asset_id'] for x in saved]}
v.checkpoint(cp)
lines=['# 《贼胆》既有研究迁入','', '旧工作区的463章逐章研究已接入同一来源身份和可检索卡库。本次核验来源哈希、章节映射及证据范围，保留旧研究内容；没有重新声称通读全书。','',f"人物材料183份、场景109份、剧情线69条；60条出场候选单列。人物材料包含同一人物的不同阶段记录，不能把183份材料称为183个去重人物。",'', '## 阅读入口','', '- [卡片索引](cards.md) · [剧情线台账](threads.md) · [出场候选](appearance-candidates.json)','- [逐章研究](legacy/chapter-notes.jsonl) · [旧覆盖记录](legacy/coverage.json) · [本次迁移核验](migration-audit.json)','', '事实、研究解释、用户评价分别保存；用户评价保持原值。旧研究没有统一的九维逐章验收，本次不会为未做过的维度补上完成标记。','', '## 来源与恢复','',f"来源：`{s['source_id']}`。修订：`{s['revision']}`。",'', '原文留在private-sources；[章节映射](chapter-map.json)连接旧顺序号与新chapter_id，保留重复章号。复制旧JSON的SHA-256保存在迁移核验内。主档可在同一库查询，旧目录未删除。']
atomic_write(report/'README.md','\n'.join(lines)+'\n')
cardlines=['# 《贼胆》人物与场景索引','', '同名不同阶段分别保留，编号是研究记录，不是去重人物。','']
for x in saved:cardlines.append(f"- [{x['name']} · {x['legacy_record_id']}](../../views/{x['asset_id']}.md) · {x['asset_type']} · v{x['revision']}")
atomic_write(report/'cards.md','\n'.join(cardlines)+'\n')
threadlines=['# 《贼胆》剧情线台账','', '以下是既有研究分段观察；“A末”等状态不是全书终点状态。事实、解释和阶段状态保持原始区分。','']
for r in mapped_threads:
    threadlines.extend(['## '+r['record_id']+' '+r['name'],'','阶段：'+r['worker_part']+'；原状态：'+str(r.get('status',r.get('status_at_420','未单列'))),'','事实：',''])
    threadlines.extend('- '+x for x in r.get('facts',[]))
    if r.get('inferences'):threadlines.extend(['','解释：','',*['- '+x for x in r['inferences']]])
    threadlines.extend(['','依据：'+'；'.join(e['chapter_id']+' L'+str(e['start_line'])+'—'+str(e['end_line']) for e in r['mapped_evidence'] if e['claim_kind']=='fact'),''])
atomic_write(report/'threads.md','\n'.join(threadlines)+'\n')
print(json.dumps({'saved_cards':len(saved),'candidate_count':len(candidates),'thread_count':len(threads),'mapped_chapters':len(mapping)},ensure_ascii=False),flush=True)
