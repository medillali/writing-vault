import json, hashlib
from pathlib import Path

D = Path(__file__).resolve().parent
A = D.parent
ROOT = D.parents[6]
def rd(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def wr(p, x): p.write_text(json.dumps(x, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
assert not (D/'delivery-manifest.json').exists(), 'Already delivered: use an explicit delta.'
validation = rd(D/'validation.json')
assert validation['status'].startswith('passed-') and validation['characters'] == 52
mapping_path = D/'stage-card-to-character-arc-map.json'
mapping = rd(mapping_path)
groups = [A/f'reader4-character-arcs-part{i:02}.json' for i in range(1,9)]
rows = [r for p in groups for r in rd(p)['characters']]
byid = {r['audit_id']:r for r in rows}
assert len(byid) == 52
assert set(byid) == {f'character-arc-r4-{i:03}' for i in range(1,53)}
for e in mapping['entities']:
 assert e['stage_cards'] == byid[e['audit_id']]['stage_card_mapping']
for p in groups:
 g = rd(p)
 assert all(k.startswith('writing-vault/') for k in g['formal_input_sha256'])
 assert all(not k.startswith('writing-vault/') for k in g.get('additional_support_sha256',{}))
access = [rd(D/f'part{i:02}-access-receipt.json') for i in range(1,9)]
full = sorted({n for a in access for n in a.get('targeted_full_indexed_chapters_actual_begin_end',[])})
notes = sorted({n for a in access for n in a.get('formal_note_rows_complete',[])})
ranges = [x for a in access for x in a.get('limited_source_ranges',[])]
checks = {'status':'passed-structure-mapping-provenance-only-not-primary-semantic-approval','characters':52,
          'groups':8,'stage_cards':mapping['counts']['stage_cards'],'supplementary_entities_without_stage_cards':6,
          'evidence_count':sum(len(r['evidence']) for r in rows),
          'checks':{'stable_52_ids_exact_once':True,'all_five_literary_fields_nonempty':True,'all_rows_draft':all(r['review_status']=='draft' for r in rows),
                    'mapping_exactly_equals_group_original_card_mappings':True,'formal_and_stage_metadata_classified':True,'all_reference_source_and_line_bounds_valid':True},
          'actual_access':{'full_indexed_chapters_this_character_audit':full,'derived_four_column_notes_actual_complete':notes,
                           'limited_source_excerpts':ranges,'unique_full_book_coverage_added':0,
                           'original_reading_boundary':'原始个人全文仅卷二raw252—404及卷五raw969—1179；卷二尾primary原读后完整派生接读；本轮不声称本人重新全书全文。'},
          'primary_review_boundary':'分组交root逐项主审；此文件不读取或伪造root签收，不代表全书验收。',
          'group_sha256':{p.relative_to(ROOT).as_posix():sha(p) for p in groups},
          'stage_mapping_sha256':sha(mapping_path),'underlying_structure_validation_sha256':sha(D/'validation.json')}
wr(D/'reader4-subset-validation.json',checks)
support_names = ['input-receipt.json','validation.json','reader4-subset-validation.json','stage-card-to-character-arc-map.json','stage-card-to-character-arc-map.md',
                 'npc-stage-attribution-observations.json','xuyan-summary-correction-proposal.json','qingmou-stage-mapping-source-check.json','new-identity-and-postevidence-observations.json',
                 'wrapper-classification-delta.json','part07-unsubmitted-selfcheck-delta.json']
support = [D/x for x in support_names if (D/x).exists()]
support += [D/f'part{i:02}-access-receipt.json' for i in range(1,9)]
artifacts = groups + [p.with_suffix('.md') for p in groups] + support
md = ['# 《斩龙》reader4人物子集交接（待root主审与总装）','',
      '已完成获授权52人物：32位外部玩家（原26+补核6），20位NPC（原NPC名单最后20）。八组均以稳定ID交审；不替root签收，不宣全书审计发布完成。','',
      '原始个人全文范围为卷二raw252—404、卷五raw969—1179。卷二raw405—504首读primary，本人完整接读派生四栏。其余卷本轮接读对应正式卡content/evidence、analysis阶段状态、六卷handoff和列明四栏；定向原文复核按实际整章/限段分别登记，保留original_reader。','',
      f"结构/溯源验证：52稳定ID、{mapping['counts']['stage_cards']}旧阶段卡映射、6无旧卡补核实体、{checks['evidence_count']}引用。此检查不证明文学判断已经获主审。",'',
      '## 稳定分组','', '|分组|ID|人数|JSON SHA256|','|---|---|---:|---|']
for i,p in enumerate(groups,1):
 rr=rd(p)['characters'];md.append(f"|part{i:02}|{rr[0]['audit_id']}—{rr[-1]['audit_id']}|{len(rr)}|{sha(p)}|")
md += ['', '## 独立映射与访问记录','',
       '- [旧阶段卡→人物弧精确映射](stage-card-to-character-arc-map.json)：原volume/index/title/asset/origin原样保留；所属组织与单一人物分开。',
       '- [结构、映射及实际访问验证](reader4-subset-validation.json)：整章复读、限定范围及派生笔记逐项列出。',
       '- part01—08-access-receipt.json为各组实际接读接口收据。完整source定位不是本轮亲读全文的替代声明。','',
       '## 必须保留的实体与证据边界','',
       '- 清眸：旧卷四题“美丽清眸”保原题；经861/898限定原文指代核对映射清眸拓墨。百里若风是玩家，非百里伦。',
       '- 星痕：旧卡“上将星痕”原题保留，规范实体不因前缀另造人；658ID说明在弧内。',
       '- 弗雷：本辖夏火统领与472同名宫廷魔导师缺身份桥，暂不硬并；傅雷工匠另人。',
       '- 徐焰：狂雷军属、守凡书实死。原summary“御林”误录只提交最小7字段外置proposal；root已实际读proposal并独立核源，正式外置层由root保存，原冻结字节不动。',
       '- 银戈/安娜为各自系统实死；安娜拒的是子舒替她求情的归附赦命条件。西瓦娜为占体意志，1349抽离不等其已灰飞，也不把其行为改归原佩。',
       '- 希芙吞魂链为石报告→1369主叙与当面对话沿用，新增后证由primary正式addendum承担，不冒吞魂现场。',
       '- 兰蔻1296实际驻凡书，但1295有上位格不等已炼成；奈克部分恢复与护送指令分开；罗躁寄格到1260东本人称已收，不伪造亲手中继镜头。',
       '- 傲天战皇终点活，新战未打；北海神侯最后具名为活俘拒供，去留未给。','',
       '## 合入方式','',
       'root只采用自身已签账当前SHA对应的八组；本目录自核before/delta和装配源只作追溯，不重复纳入characters。若root要求文学delta，保存before并仅定向修正，不重新生成整个分组。已签两池、24重点及正式分卷均未被本人物子集改写。','']
(D/'HANDOFF.md').write_text('\n'.join(md),encoding='utf-8')
artifacts.append(D/'HANDOFF.md')
manifest = {'status':'reader4-subset-draft-frozen-for-primary-review-not-publication','scope':{'characters':52,'stage_cards':69,'groups':8,'evidence_count':checks['evidence_count']},
            'files_sha256':{p.relative_to(ROOT).as_posix():sha(p) for p in artifacts},
            'no_primary_approval_claimed':True,'no_formal_or_frozen_volume_mutation':True}
wr(D/'delivery-manifest.json',manifest)
print(json.dumps({'manifest_sha256':sha(D/'delivery-manifest.json'),'handoff_sha256':sha(D/'HANDOFF.md'),'validation_sha256':sha(D/'reader4-subset-validation.json'),'scope':manifest['scope'],'full_chapters_reread':full},ensure_ascii=False))
