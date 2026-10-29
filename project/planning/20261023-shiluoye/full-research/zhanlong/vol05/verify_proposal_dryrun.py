"""只读验证当前提案/支持路径，不应用。"""
import pathlib,json,copy,hashlib,sys,re
P=pathlib.Path(__file__).parent;sys.stdout.reconfigure(encoding='utf-8')
def read(n):return json.loads((P/n).read_text(encoding='utf-8'))
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
p=read('primary-review-proposal.json');m=read('freeze-manifest.json')
assert all(h(P/n)==d for n,d in p['before_core_sha256'].items())
assert all(h(P/n)==d for n,d in m['support_sha256'].items())
data={n:read(n) for n in ['analysis.json','cards.json','graph.json']};before=copy.deepcopy(data)
for c in p['changes']:
 obj=data[c['file']]
 for key in c['path'][:-1]:obj=obj[key]
 assert obj[c['path'][-1]]==c['before'];obj[c['path'][-1]]=copy.deepcopy(c['after'])
for c in reversed(p['changes']):
 obj=data[c['file']]
 for key in c['path'][:-1]:obj=obj[key]
 assert obj[c['path'][-1]]==c['after'];obj[c['path'][-1]]=copy.deepcopy(c['before'])
assert data==before
links=[]
for name in ['report.md','handoff.md']:
 text=(P/name).read_text(encoding='utf-8')
 for x in re.findall(r'\]\((C:/[^)]+)\)',text):assert pathlib.Path(x).exists(),x;links.append(x)
for c in p.get('text_changes',[]):assert (P/c['file']).read_text(encoding='utf-8').count(c['before'])==1
print(json.dumps(dict(status='passed-read-only',proposal_paths=len(p['changes']),text_paths=len(p.get('text_changes',[])),reverse_replay_equal=True,all_six_current_sha_unchanged=True,support_hashes_match=True,existing_markdown_link_targets=len(links)),ensure_ascii=False))
