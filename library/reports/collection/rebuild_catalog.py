"""由正式来源、卡片、检查点和阅读单元映射重建总目录，不修改研究主档。"""
import json,hashlib
from pathlib import Path

HERE=Path(__file__).resolve().parent
VAULT=HERE.parents[2]
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def write(p,text):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')
def esc(x):return str(x).replace('|','｜').replace('\n',' ')
def main():
    config=load(HERE/'catalog-config.json')
    sources={s['source_id']:s for s in (load(p) for p in (VAULT/'library/sources').glob('*.json'))}
    runs=[load(p) for p in (VAULT/'exchanges/runs').glob('*.json')]
    assets=[load(p) for kind in ['characters','scenes','patterns'] for p in (VAULT/'library'/kind).glob('*.json')]
    unit_map=load(HERE/'reading-units.json')
    audits={a['source_id']:a for a in load(HERE/'chapter-audit.json')}
    active=config['books'].get(config.get('active_source_id'))
    active_label=(active['author']+'《'+active['title']+'》') if active else '本轮全书研究已完成，等待用户审阅'
    records=[];lines=['# 小说研究总目录','',config['ordering_rule'],'','当前推进：**'+active_label+'**。完整正文索引已建立；实际阅读与研究深度见下表。','', '[管理规则与查询方法](管理规则.md) · [跨书机制入口](机制索引.md) · [章节质量核验](chapter-audit.json)','']
    for group in config['author_orders']:
        lines+=['## '+group['author'],'',group['note'],'']
        if group.get('evidence_url'):lines+=['创作顺序依据：['+group['evidence_type']+']('+group['evidence_url']+')。','']
        lines+=['| 作品 | 已读正文单元 / 总单元 | 当前深度 | 人物 / 场景 / 机制卡 | 下一起点 |','|---|---:|---|---:|---|']
        for sid in group['source_ids']:
            book=config['books'][sid];source=sources[sid]
            rev=next(r for r in source['revisions'] if r['revision']==source['revision'])
            active_runs=[r for r in runs if r['source_id']==sid and r['source_revision']==source['revision']]
            completed=set(c for r in active_runs for c in r.get('completed_chapters',[]))
            if sid in unit_map:
                if unit_map[sid]['source_revision']!=source['revision']:
                    raise ValueError('来源修订已变化，请先重建阅读单元映射：'+sid)
                index_fields=[[c.get(k) for k in ['chapter_id','title','start_line','end_line']] for c in rev['chapters']]
                fingerprint=hashlib.sha256(json.dumps(index_fields,ensure_ascii=False,separators=(',',':')).encode('utf-8')).hexdigest()
                if unit_map[sid].get('index_fingerprint')!=fingerprint:
                    raise ValueError('章节索引已变化，请先重建阅读单元映射：'+sid)
                body=[u for u in unit_map[sid]['units'] if u['kind'] in ['body','prologue']]
            else:
                body=[{'unit_id':c['chapter_id'],'segment_ids':[c['chapter_id']],'title':c['title']} for c in rev['chapters'] if c['title']!='章前内容' and not ('集 ' in c['title'] and len(c['title'])<40)]
            covered=[u for u in body if set(u['segment_ids']).issubset(completed)]
            pending=[u for u in body if not set(u['segment_ids']).issubset(completed)]
            matches=[a for a in assets if any(e['source_id']==sid for e in a.get('evidence',[]))]
            counts={kind:sum(a['asset_type']==kind for a in matches) for kind in ['character','scene','pattern']}
            status='待顺序研究' if not covered else '开篇研究；全书待继续'
            if book['task_state']=='legacy_imported':status='既有全文首轮迁入；九维深化未宣称'
            if book['task_state']=='existing_full_nine':status='既有全书九维研究；待用户审阅'
            if book['task_state']=='completed_full_nine':
                if pending:raise ValueError('完整蒸馏状态尚有未读正文：'+sid)
                status='全书九维与终态核验完成；待用户审阅'
            if book['task_state']=='active':status='按卷连续九维研究进行中'
            if book['task_state']=='active' and not pending:status='正文已读；全书研究验收中'
            next_title=pending[0]['title'] if pending else '已读范围复核 / 用户审阅'
            if book['task_state']=='active' and not pending:next_title='全书综合、人物弧与终态核验'
            record={**book,'source_id':sid,'source_revision':source['revision'],'indexed_segments':len(rev['chapters']),'body_reading_units':len(body),'completed_body_units':len(covered),'completed_segment_ids':sorted(completed),'next_reading_unit':pending[0] if pending else None,'counts':counts,'run_ids':[r['run_id'] for r in active_runs],'status':status,'user_review':'未代替用户确认'}
            records.append(record)
            link='books/'+book['slug']+'.md'
            lines.append(f"| [{book['title']}]({link}) | {len(covered)} / {len(body)} | {status} | {counts['character']} / {counts['scene']} / {counts['pattern']} | {esc(next_title)} |")
            page=['# 《'+book['title']+'》资料入口','',f"作者：{book['author']}。{book['note']}",'',f"来源ID：`{sid}`；修订：`{source['revision']}`。",'',f"正文阅读单元：{len(covered)} / {len(body)}。状态：{status}。",'',f'下一起点：{next_title}。','', '[返回总目录](../README.md) · [管理规则](../管理规则.md)','']
            if book.get('report'):page+=['[专题研究报告](../'+book['report']+')','']
            for extra in book.get('additional_reports',[]):page+=['['+extra['title']+'](../'+extra['path']+')','']
            if sid in audits:
                audit=audits[sid]
                page+=['## 输入与章号','',f"索引段{audit['indexed_segments']}；正文条目{audit['logical_numbered_entries']}；序章{audit['prologue_entries']}；卷标题{audit['volume_heading_entries']}；合章标题{audit['combined_heading_entries']}。",'', '重复原章号：'+(', '.join(map(str,audit['duplicate_numbers'])) or '无')+'。合章展开后的章号缺口：'+(', '.join(map(str,audit['missing_numbers_after_combined_ranges'])) or '无')+'。编号连续不自动证明文件内容完整或研究结论正确。','']
                for err in audit['false_heading_segments']:page+=['- 索引片段 `'+err['segment_id']+'` 并回阅读单元 `'+err['attached_to']+'`；保留原证据ID。']
            page+=['','## 检查点','']
            for r in active_runs:page+=['- ['+r['run_id']+'](../../../../exchanges/runs/'+r['run_id']+'.json)：'+r.get('notes','')]
            for kind,label in [('character','人物材料'),('scene','场景材料'),('pattern','可迁移机制')]:
                page+=['','## '+label,'']
                subset=sorted((a for a in matches if a['asset_type']==kind),key=lambda a:a['title'])
                if not subset:page+=['尚无正式入库材料。']
                for a in subset:
                    page+=['- ['+a['title'].replace('[','［').replace(']','］')+'](../../../views/'+a['asset_id']+'.md) · v'+str(a['revision'])+' · '+a.get('review_status','draft')+'：'+a['content']['summary'].replace('\n',' ')]
            write(HERE/link,'\n'.join(page)+'\n')
        lines+=['']
    lines+=['## 保存状态','', '研究主档、历史、检查点和本目录均保存本地。本批失落叶研究及统一目录未由本任务提交或推送；蜗牛双书任务另有它自己范围的同步记录。原文继续单独保留；没有自动写入Space或ChatGPT记忆。','', '章节计数使用实际阅读单元：合章一次完整阅读，重复章号分别保留，正文误识别片段与前章一同阅读。目录可用本文件夹的 `rebuild_catalog.py` 重建。']
    receipts=[f'[{label}]({name})' for name,label in [('机制索引.md','按写作问题找机制'),('写作机制比较.md','五书写作机制比较'),('本批验收.md','本批范围与验收'),('迁移审查.md','旧库迁移审查'),('backup-verification.json','备份及实际恢复回执')] if (HERE/name).exists()]
    if receipts:lines+=['',' · '.join(receipts)]
    write(HERE/'catalog.json',json.dumps({'schema_version':1,'ordering_rule':config['ordering_rule'],'active_source_id':config['active_source_id'],'books':records},ensure_ascii=False,indent=2)+'\n')
    write(HERE/'README.md','\n'.join(lines)+'\n')
    print(json.dumps({'books':len(records),'assets':len(assets),'active':config['active_source_id']},ensure_ascii=False))

if __name__=='__main__':main()
