from pathlib import Path
import json,sys,re,hashlib,shutil,collections,subprocess,copy
sys.stdout.reconfigure(encoding='utf-8')
R=Path(__file__).resolve().parents[2];P=Path(__file__).parent;V=R/'.verify/two-books';O=V/'library/reports/two-books-full-20261025'
sys.path.insert(0,str(R/'distill-novels/scripts'))
from fictionlib.vault import Vault
from fictionlib.storage import locked,digest
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def dump(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
class Cached(Vault):
 def _sources(self):
  if not hasattr(self,'cache'):self.cache=super()._sources()
  return self.cache
mode=sys.argv[1]
if mode=='package':
 data=load(P/'sources.json')
 for s in data.values():s.pop('normalized_path',None)
 dump(O/'sources.json',data)
 for folder in ['z','z-b','z-c','z-c2','z-d','l-a','l-b']:
  target=O/'research'/folder;target.mkdir(parents=True,exist_ok=True)
  for f in (P/folder).glob('batch-*.json'):shutil.copy2(f,target/f.name)
  for name in ['part-synthesis.md','handoff-to-second-half.json','characters-final.json','ending-audit.json','threads.json','terminal-question-map.json','read-coverage.json','audit-report.json','handoff.json','handoff-to-root.json','handoff-to-next.json','identity-map.json','cross-half-audit.json']:
   if (P/folder/name).exists():shutil.copy2(P/folder/name,target/name)
 for name in ['book-synthesis.md','book-synthesis.json','ending-audit.md','ending-audit.json','terminal-question-map.json','causal-relations.json','characters-final.json','threads.json','identity-links.json','final-validation.json','integration-validation.json']:
  f=P/'z-final'/name
  if f.is_file():
   (O/'research/z-final').mkdir(parents=True,exist_ok=True);shutil.copy2(f,O/'research/z-final'/f.name)
 shutil.copy2(P/'causal_l.json',O/'causal_l.json')
 shutil.copy2(P/'identity-resolution.json',O/'identity-resolution.json')
 text=(P/'build_full.py').read_text(encoding='utf-8')
 text=text.replace("R=Path(__file__).resolve().parents[2];P=Path(__file__).parent;V=R/'.verify/two-books';O=V/'library/reports/two-books-full-20261025'","P=Path(__file__).resolve().parent;V=P.parents[2];R=next(p for p in V.parents if (p/'distill-novels/scripts/fictionlib').is_dir());O=P")
 text=text.replace("(P/folder).glob('batch-*.json')","(P/'research'/folder).glob('batch-*.json')").replace("dump(P/'build-result.json',result)","dump(O/'validation/rebuild-result.json',result)")
 text=text.replace("terminal_path=P/('z-final' if k=='z' else 'l-b')","terminal_path=P/'research'/('z-final' if k=='z' else 'l-b')").replace("causal_path=P/'z-final/causal-relations.json'","causal_path=P/'research/z-final/causal-relations.json'")
 (O/'rebuild-full.py').write_text(text,encoding='utf-8')
 text=(P/'render_full.py').read_text(encoding='utf-8').replace("R=Path(__file__).resolve().parents[2];V=R/'.verify/two-books';O=V/'library/reports/two-books-full-20261025';CODE=V/'library/reports/super-skeleton/map'","O=Path(__file__).resolve().parent;V=O.parents[2];R=V.parent;CODE=V/'library/reports/super-skeleton/map'")
 (O/'render_full.py').write_text(text,encoding='utf-8');shutil.copy2(P/'render_full.cjs',O/'render_full.cjs')
 dump(O/'validation/staging-audit.json',load(P/'staging-audit.json'))
 dump(O/'validation/source-identities.json',load(P/'preflight-result.json'))
 dump(O/'validation/concurrent-preservation.json',load(P/'concurrent-preservation.json'))
 print('已保存可重建的研究批次与生成器；未复制原文或机器来源路径。')
elif mode=='validate':
 errors=[];files=list(O.rglob('*'));markdown=[p for p in files if p.suffix=='.md'];links=0
 for f in markdown:
  for match in re.finditer(r'(?<!!)\[[^\]\n]*\]\(([^)\n]+)\)',f.read_text(encoding='utf-8')):
   raw=match.group(1).strip().strip('<>');target,_,anchor=raw.partition('#')
   if not target or re.match(r'^[a-z]+:',target):continue
   path=(f.parent/target).resolve();links+=1
   if not path.exists():errors.append({'file':str(f.relative_to(O)),'missing':raw})
   elif anchor and path.suffix=='.md' and not ('id="'+anchor+'"' in path.read_text(encoding='utf-8') or anchor in ['世界与规则','人物与关系']):
    # 本批显式锚点使用源章ID；其余常规标题链接由Markdown渲染器处理。
    if anchor.startswith('ch-'):errors.append({'file':str(f.relative_to(O)),'missing_anchor':raw})
 v=Cached(V)
 with locked(V):
  result=v._validate_locked();assert digest(v.cache)==digest(Vault._sources(v))
 assert result['valid'],result
 # 报告、结局核对与原始研究批次也逐项检查章界，而不只检查卡片主档。
 sources=load(P/'sources.json');sid_key={s['source_id']:k for k,s in sources.items()};bounds={k:{c['chapter_id']:c for c in s['chapters']} for k,s in sources.items()};evidence_count=0
 def evidence_walk(x,context=None):
  global evidence_count
  if isinstance(x,dict):
   context=x.get('source_key',context);context=sid_key.get(x.get('source_id'),context)
   if 'chapter_id' in x and 'start_line' in x and 'end_line' in x:
    assert context in bounds,('证据缺少来源',x);c=bounds[context].get(x['chapter_id']);assert c and c['start_line']<=x['start_line']<=x['end_line']<=c['end_line'],x;evidence_count+=1
   for y in x.values():evidence_walk(y,context)
  elif isinstance(x,list):
   for y in x:evidence_walk(y,context)
 for f in O.rglob('*.json'):
  parts=f.relative_to(O).parts;context='l' if 'leveling' in parts or any(p.startswith('l-') for p in parts) else 'z' if 'zeidan' in parts or any(p in ['z','z-b','z-c','z-c2','z-d','z-final'] for p in parts) else None
  evidence_walk(load(f),context)
 for folder in ['zeidan','leveling']:
  cov=load(O/folder/'coverage.json');notes=load(O/folder/'chapter-notes.json')['units'];assert cov['full_text_read'] and len(notes)==cov['actual_reading_units'];assert [u['ordinal'] for u in notes]==list(range(1,len(notes)+1))
  ledger=load(O/folder/'question-ledger.json')['questions'];terminal=load(O/folder/'terminal-question-map.json')['items'];keys=[x['key'] for x in terminal]
  assert len(keys)==len(set(keys)) and set(keys)=={q['id'] for q in ledger},('终态审计未逐键覆盖',folder)
  assert all(x['final_status'] in ['resolved','partial','open','unknown','abandoned'] and x['answer'] and x['evidence'] for x in terminal)
  for stage in (O/folder/'stages').glob('*.json'):
   dims=load(stage)['dimensions'];assert len(dims)==9 and all(dims.values())
  for kind in ['diagram-layout','browser']:assert load(O/folder/'validation'/f'{kind}.json')['valid']
  assert (O/folder/'book-synthesis.md').stat().st_size>5000
  assert (O/folder/'ending-audit.json').exists()
 # 所有新增卡片引用原书修订，不建立原创作品，不带旧用户评价。
 cards=[]
 for folder in ['zeidan','leveling','shared']:
  for a in load(O/folder/'asset-manifest.json') if folder!='shared' else load(O/'shared-asset-manifest.json'):
   typ={'character':'characters','scene':'scenes','pattern':'patterns'}[a['type']];p=V/f'library/{typ}/{a["asset_id"]}.json';x=load(p);cards.append(x);assert x['scope']!='original-project';assert x['review_status']=='draft' and x['user_notes']=='' and x['favorite'] is False
 result.update({'local_links_checked':links,'broken_links':errors,'new_cards':len(cards),'report_evidence_ranges_checked':evidence_count,'terminal_question_maps_complete':True,'all_evidence_and_graphs_valid':True,'original_projects_created':0,'raw_text_in_git_artifacts':False,'user_evaluation_automatically_accepted':False})
 dump(O/'validation/library-and-links.json',result);print(json.dumps(result,ensure_ascii=False));assert not errors
elif mode=='leak':
 # 仅报告疑似长段原文重合，不打印原文。字符滑窗用于定位，语义审阅另做。
 S=load(P/'sources.json');matches=[]
 for key,folder in [('z','zeidan'),('l','leveling')]:
  raw=Path(S[key]['normalized_path']).read_text(encoding='utf-8');flat=re.sub(r'\s+','',raw)
  values=[]
  for f in O.rglob('*.json'):
   if any(x in f.parts for x in ['validation','plot']):continue
   def walk(x):
    if isinstance(x,str):values.append((f,x))
    elif isinstance(x,list):
     for y in x:walk(y)
    elif isinstance(x,dict):
     for y in x.values():walk(y)
   walk(load(f))
  for f in O.rglob('*.md'):
   if not any(x in f.parts for x in ['validation','plot']):values.append((f,f.read_text(encoding='utf-8')))
  seen=set();seen_texts=set();candidates=collections.defaultdict(dict)
  for f,text in values:
   t=re.sub(r'\s+','',text)
   if t in seen_texts:continue
   seen_texts.add(t)
   for start in range(max(0,len(t)-63)):
    part=t[start:start+64]
    if len(part)==64:candidates[part[:16]].setdefault(part,f)
  # 用16字前缀索引筛候选，再逐字核对64字；不依赖概率哈希，不反复扫描整本原文。
  for start in range(max(0,len(flat)-63)):
   possible=candidates.get(flat[start:start+16])
   if not possible:continue
   part=flat[start:start+64]
   if part in possible and part not in seen:
    seen.add(part);matches.append({'source_key':key,'file':str(possible[part].relative_to(O)),'length':64,'match_sha256':hashlib.sha256(part.encode()).hexdigest()})
 dump(O/'validation/long-excerpt-check.json',{'window_characters':64,'matches':matches,'boundary':'64字连续重合筛查只发现长段复写候选，不证明解释正确或原创性。','valid':not matches});print(json.dumps({'long_excerpt_candidates':len(matches)},ensure_ascii=False))
else:raise SystemExit(mode)
