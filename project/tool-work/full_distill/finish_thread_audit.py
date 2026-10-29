"""校验人工终点审计，再把累计状态接入图；不改分集历史。"""
import json
from persist import HERE,CH,json_text

def main():
    audit=json.loads((HERE/'thread-final-review.json').read_text(encoding='utf-8'))
    assert audit['complete_as_of_volume']==18
    entries=audit['entries'];keys=[e['key'] for e in entries]
    assert len(keys)==len(set(keys))
    config=json.loads((HERE/'cross-input.json').read_text(encoding='utf-8'))
    expected={config['aliases'].get(t['key'],t['key']) for n in range(1,19)
              for t in json.loads((HERE/f'vol{n:02d}.json').read_text(encoding='utf-8'))['threads']}
    expected.update(k for edge in config['edges'] for k in edge['tracking_keys'])
    assert set(keys)==expected
    updates={(u['key'],u['volume']):u for u in config['state_updates']}
    lines=['# 全书剧情线终点审计','','阶段稿保留当时状态；以下逐条记录读完全书后的累计结论。','']
    for item in entries:
        assert item['reviewed_at_book_end'] is True,item['key']
        final=item['final']
        assert final['key']==item['key'] and final['volume']==18 and final['audit_scope']=='whole-book'
        assert final['status'] in {'open','partial','resolved'}
        assert all(final.get(k) for k in ['title','kind','question','resolution_note','evidence'])
        for e in final['evidence']:
            c=CH[e['chapter_id']]
            assert c['start_line']<=e['start_line']<=e['end_line']<=c['end_line']
        updates[(final['key'],18)]=final
        lines.extend([f"## {final['title']}（{final['status']}）",'',f"追踪：`{final['key']}`",'',final['question'],'',final['resolution_note'],'',
                      '证据：'+'；'.join(f"{e['chapter_id']} L{e['start_line']}–{e['end_line']}" for e in final['evidence']),''])
    config['state_updates']=list(updates.values())
    (HERE/'cross-input.json').write_text(json_text(config),encoding='utf-8')
    (HERE/'thread-final-audit.json').write_text(json_text(audit),encoding='utf-8')
    (HERE/'thread-final-audit.md').write_text('\n'.join(lines),encoding='utf-8')
    print(json.dumps({'final_threads':len(entries)}))

if __name__=='__main__':main()
