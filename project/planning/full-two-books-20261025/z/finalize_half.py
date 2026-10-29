from pathlib import Path
import json,sys
sys.stdout.reconfigure(encoding='utf-8')
P=Path(__file__).parent
for f in list(P.glob('batch-*.json'))+list(P.glob('authored-*.json')):
 t=f.read_text(encoding='utf-8').replace('"zhaolanxin"','"zhao-lanxin"').replace('三十万加五成百中五','三十万加5%奖金')
 f.write_text(t,encoding='utf-8')
bs=[json.loads(f.read_text(encoding='utf-8')) for f in sorted(P.glob('batch-*.json'))]
latest={};history={};threads={};questions={}
for b in bs:
 for c in b['characters']:
  latest[c['key']]={**c,'snapshot_through_unit':b['unit_end']}
  history.setdefault(c['key'],[]).append({'unit_start':b['unit_start'],'unit_end':b['unit_end'],'evidence':c['evidence']})
 for t in b['threads']:threads[t['key']]={**t,'snapshot_through_unit':b['unit_end']}
 for q in b['questions']:questions[q['key']]={**q,'snapshot_through_unit':b['unit_end']}
mapping=[]
for k,c in latest.items():
 aliases=c.get('aliases',[])
 if k=='zhao-lanxin':aliases=list(dict.fromkeys(aliases+['赵医生','夜岚','小岚']))
 variants=[a for a in aliases if '源' in a or '变体' in a]
 aliases=[a for a in aliases if a not in variants]
 if k=='xiaoyu':variants.append('萧翎（本源误写，不作为已证别名）')
 mapping.append({'key':k,'canonical_name':c['name'],'verified_aliases':aliases,'source_name_variants':variants,'identity_boundary':'仅本书来源；人物原文误写与跨书同名不并人','history':history[k]})
for name,data in [('character-key-map.json',mapping),('characters-half.json',list(latest.values())),('threads-half.json',list(threads.values())),('question-ledger-half.json',list(questions.values()))]:
 (P/name).write_text(json.dumps({'source_key':'z','scope':'实际阅读1..232的阶段快照，非全书终点','items':data},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(P/'progress.md').write_text('''# 《贼胆》前半阅读全文完成检查点

- 本代理实际完整模型阅读单元1–232，共232单元；233–463由其他研究者负责。分工标签是研究分段，不是原书卷名。
- 已存batch-01.json至batch-12.json，逐单元事实、状态变化、证据，以及每阶段九维、人物快照、场景、机制、线索和问题。
- 1–10初次合输截断，已补2–5、6–7；1及8–10原输出完整。181–184合输中182缺696 tokens，已单章182完整重读。其余逐批无截断。
- author_batch.py只展开模型手工紧凑稿、补来源元数据；不自动生成文学判断。authored-05至12保留紧凑稿。
- check_research.py确认232单元连续、九维非空、893处章节行号界内。该检查不能替代文学判断质量。
- 前半截止：232易物尚未成交；231遗失城完成，24级63%，费思自爆、哈尔被献祭、女皇被审判，书消散、人偶残球仍持有。下接233由root研究。
- 重要回收：雪兰草191交回；逃脱匕167明确临换未售；古德151完成；630万黑赛202到账并银行核实。
- 重要未解候选：噬魂戒及双戒纸、圣言圣水修复、翡翠藏宝图、恶魔之角回梦魇、沃卡德复生、深白周内五包、C型核心、尖牙招魂、搬家恋情、影砂组织；后半研究须逐一核，不据未再提判弃线。
- 真实writing-vault、Git、生产工具均未修改。本目录为研究草稿，不记录用户偏好。
''',encoding='utf-8')
print('half artifacts written',len(mapping),'character identities',len(threads),'threads',len(questions),'questions')
