"""保存主审前私有装配源历史，防止旧写法被误认当前冻结语义。"""
import pathlib,json,hashlib,sys
P=pathlib.Path(__file__).parent;sys.stdout.reconfigure(encoding='utf-8');out=P/'review-corrections/assembly-source-before';out.mkdir(exist_ok=False)
names=['build_research.py','research_dimensions.py','research_characters.py','research_scenes.py','research_patterns.py','research_graph.py','research_supplements.py','research_refinement.py']
sha={}
for n in names:
 (out/n).write_bytes((P/n).read_bytes());sha[n]=hashlib.sha256((out/n).read_bytes()).hexdigest()
(out/'manifest.json').write_text(json.dumps(dict(status='historical-private-authoring-source-not-current-rebuild-entrypoint',sha256=sha,warning='freeze前已有未应用的私有草稿调整，冻结六核心才是主审基底；主审后不重新运行手写builder，以before六核心+已批准proposal重放。'),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(files=len(names),manifest_sha256=hashlib.sha256((out/'manifest.json').read_bytes()).hexdigest()),ensure_ascii=False))
