"""仅整理已实际完成的终点复核，生成供用户审查的账本。"""
from collections import Counter
import json
from persist import HERE,CH,json_text

data=json.loads((HERE/'question-ledger-review.json').read_text(encoding='utf-8'))
states={'answered':'已有答案','partial':'部分回答','open':'仍未回答','text-uncertain':'文本待辨'}
reports=[json.loads((HERE/f'vol{n:02d}.json').read_text(encoding='utf-8')) for n in range(1,19)]
chapter_volume={cid:r['volume'] for r in reports for cid in r['chapter_ids']}
question_keys=[(e['origin_volume'],e['source_question_index']) for e in data['entries']]
assert len(question_keys)==len(set(question_keys))
assert set(question_keys)=={(r['volume'],i) for r in reports for i in range(1,len(r['questions'])+1)}
for e in data['entries']:
    assert e.get('reviewed_at_book_end') is True,e['id']
    assert e.get('answer') and e['status'] in states,e['id']
    report=reports[e['origin_volume']-1]
    q=report['questions'][e['source_question_index']-1]
    assert e['question']==q['question'] and e['origin_evidence']==q['evidence'],e['id']
    for ref in e['origin_evidence']+e.get('answer_evidence',[]):
        chapter=CH[ref['chapter_id']]
        assert chapter['start_line']<=ref['start_line']<=ref['end_line']<=chapter['end_line'],e['id']
    e['revisit_at_book_end']=False
    e['review_state']='reviewed'
    e['reviewed_through_volume']=18
    e['latest_volume']=max((chapter_volume[r['chapter_id']] for r in e.get('answer_evidence',[])),default=e['origin_volume'])
    e.pop('seed_review_scope',None)
expected={(r['volume'],i):revision for r in reports for i,revision in enumerate(r['revisions_to_earlier'],1)}
reviews={(r['origin_volume'],r['source_revision_index']):r for r in data.get('revision_reviews',[])}
assert len(reviews)==len(data.get('revision_reviews',[])) and set(reviews)==set(expected)
for key,original in expected.items():
    review=reviews[key]
    assert review['original_revision']==original and review.get('reviewed_at_book_end') is True,key
    assert review.get('review') and review.get('evidence'),key
    for ref in review['evidence']:
        chapter=CH[ref['chapter_id']]
        assert chapter['start_line']<=ref['start_line']<=ref['end_line']<=chapter['end_line'],key
data['completion']='complete_as_of_volume_18'
data['pending_questions']=[]
data['status_counts']=dict(Counter(e['status'] for e in data['entries']))
data['book_end_review']='逐项复核至第18集；状态反映整书证据，不等同用户已确认通过。'
(HERE/'question-ledger.json').write_text(json_text(data),encoding='utf-8')
lines=['# 《超级骷髅兵》整书疑点与回收清单','',
       f"覆盖18集全部{len(data['entries'])}个原始问题。相似问题仍按原位置保留，部分回答和文本待辨分别列明。",'',
       '这是研究草稿的终点复核；事实、人物自述、推断和原文口径冲突仍有边界，用户审查状态另行决定。','']
def refs(items):
    return '；'.join(f"{r['chapter_id']} L{r['start_line']}—{r['end_line']}" for r in items) or '未出现可作为答案的新增证据。'
for state,label in states.items():
    selected=[e for e in data['entries'] if e['status']==state]
    lines += [f'## {label}（{len(selected)}）','']
    for e in selected:
        lines += [f"### {e['id']} · {e['question']}",'',e['answer'],'',
                  f"原问题证据：{refs(e['origin_evidence'])}",'',f"终点复核证据：{refs(e.get('answer_evidence',[]))}",'',
                  f"审查边界：{e.get('revisit_focus','请结合原文核对表述。')}",'']
lines += [f'## 分集后见修订的终点复核（{len(reviews)}）','']
for item in data['revision_reviews']:
    original=item['original_revision']
    description=original['description'] if isinstance(original,dict) else original
    lines += [f"### 第{item['origin_volume']}集 · 修订{item['source_revision_index']}",'',
              '原修订：'+description,'',item['review'],'',f"终点复核证据：{refs(item['evidence'])}",'']
(HERE/'question-ledger.md').write_text('\n'.join(lines),encoding='utf-8')
print(json_text({'questions':len(data['entries']),'revisions_reviewed':len(reviews),'status_counts':data['status_counts'],'completion':data['completion']}))
