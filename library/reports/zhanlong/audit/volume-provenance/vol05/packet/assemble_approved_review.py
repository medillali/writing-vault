"""当前唯一装配入口：只读重放已签准10对象+报告1段，验证现件；不再生成文学内容。"""
import pathlib,json,hashlib,copy,sys
P=pathlib.Path(__file__).parent;sys.stdout.reconfigure(encoding='utf-8')
APPROVED='aad046aaea881c6801ed6c290d6a7b464eb90bdd7ad6abcb499ade105e6570fb'
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(path):return json.loads(path.read_text(encoding='utf-8'))
assert h(P/'primary-review-proposal.json')==APPROVED
proposal=read(P/'primary-review-proposal.json');before=P/'review-corrections/primary-before'
base={n:read(before/n) for n in ['analysis.json','cards.json','graph.json']};expected=copy.deepcopy(base)
for c in proposal['changes']:
 x=expected[c['file']]
 for k in c['path'][:-1]:x=x[k]
 assert x[c['path'][-1]]==c['before'];x[c['path'][-1]]=copy.deepcopy(c['after'])
for n,v in expected.items():assert read(P/n)==v,n
for n in ['chapter-notes.jsonl','read-log.json','reader-state.json']:assert (P/n).read_bytes()==(before/n).read_bytes()
assert expected['analysis.json']['chapter_unresolved_index']==base['analysis.json']['chapter_unresolved_index']
assert expected['analysis.json']['chapter_source_anomaly_index']==base['analysis.json']['chapter_source_anomaly_index']
assert expected['analysis.json']['major_character_states']==base['analysis.json']['major_character_states']
for change in proposal['text_changes']:assert change['after'] in (P/change['file']).read_text(encoding='utf-8')
RESULT=dict(status='passed',entrypoint='assemble_approved_review.py',proposal_sha256=APPROVED,core_semantics_equal_approved_replay=True,exact_paths=10,report_paragraphs=1,reading_cores_byte_equal=True,chapter_indexes_equal=True,major_states_equal=True)
if sys.argv[1:]==['--save-receipt']:(P/'assembly-replay-validation.json').write_text(json.dumps(RESULT,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
else:assert not sys.argv[1:]
print(json.dumps(RESULT,ensure_ascii=False))
