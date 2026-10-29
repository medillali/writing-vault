"""卷七逐项主审与定向纠错复核后签收六文件SHA。"""
import hashlib,json
from pathlib import Path
from check_volume import load_and_check
B=Path(__file__).parent;book='tianxia-wushuang';d=B/book/'vol07'
_,_,_,a,c,g,_,r=load_and_check(book,7)
assert r['cards']=={'character':65,'scene':57,'pattern':14}
assert (len(g['nodes']),len(g['edges']),len(g['threads']))==(65,55,16)
rows=[x for v in a['dimensions'].values() for x in v]
assert len(rows)==45 and all(x.get('mechanism') and x.get('limits_and_counterevidence') for x in rows)
assert hashlib.sha256((d/'chapter-notes.jsonl').read_bytes()).hexdigest()=='5fcedf147fb7d937a9fc0ac329fb04925b70d4e61aa04e83cbb39f131b8be10a'
review=dict(volume=7,reviewer='primary',status='reviewed_for_library_import',user_approval=False,
 scope='原文210正文/211片由agent4实际全文读完；primary完整逐项读211四栏笔记，不冒称独立原文全读。45九维事实推断及新增90机制/限制栏，65人物状态，36末问35异常211本地历史、14机制4得失3局限；65人物57场景14机制卡，65节点55边16线程与内嵌知识全部语义审阅，定向改动逐字段复核。',
 semantic_review_document='review-wushuang-vol07.md',
 corrections_verified=json.loads((d/'primary-review-delta.json').read_text(encoding='utf-8'))['corrections']+['primary完整回读raw1305，另定向1300，确认分盟非分钟；集中异常已纠为分盟规模口径，原研究误读与真实未知分开。'],
 preflight=r,remaining=['按序正式导入7、8；全书综合、人物弧与终点问题审计另验。'],
 input_sha256={n:hashlib.sha256((d/n).read_bytes()).hexdigest() for n in ['analysis.json','cards.json','graph.json','read-log.json','chapter-notes.jsonl','reader-state.json']})
(B/book/'review-vol07.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
with (B/'review-wushuang-vol07.md').open('a',encoding='utf-8') as f:
 f.write('\n\n## 最终主审\n\n已逐项完成45九维及90新增方法/限制栏、65人物状态、14机制、36集中问题35源异常4文学得失3局限；所有136卡、65节点55边16线程和知识记录已审，原始211笔记保持SHA不变。新增吕布衣、未名女骑、月露分别建卡避免实体误并。纠正详见该卷primary-review-delta.json及六SHA签收；知识差修正为心只就当前装病求陪与陆明确约定，苏伦真实所知unknown。正式导入资格通过，用户审美仍待审阅，全书终点审计尚未由此完成。\n')
print(json.dumps({'review':'vol07-primary-passed-six-hashes-pinned','preflight':r},ensure_ascii=False))
