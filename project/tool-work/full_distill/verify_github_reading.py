"""校验阅读副本的内容保留、导航及主档保护；通过GitHub渲染API检查样页。"""
import importlib.util
import json
import re
import sys
from urllib.parse import unquote,urlsplit
from pathlib import Path
from check_and_publish import ROOT,HERE,GH,command,git

v=ROOT/'writing-vault'
sys.dont_write_bytecode=True
report=v/'library/reports/super-skeleton'
spec=importlib.util.spec_from_file_location('reading',report/'rebuild_github_reading.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
manifest=json.loads((m.OUT/'manifest.json').read_text(encoding='utf-8'))
pages=list(m.OUT.rglob('*.md'))
assert len(pages)==len(manifest['pages'])==296
changed=[x for x in git('diff','--name-only','-z').split('\0') if x]
assert all(p in {'README.md','library/reports/super-skeleton/README.md','library/reports/super-skeleton/rebuild_github_reading.py'} or p.startswith('library/reports/super-skeleton/reading/') for p in changed),changed
def leaves(value):
    if isinstance(value,str):yield value
    elif isinstance(value,dict):
        for k,val in value.items():
            if k not in {'evidence'}:yield from leaves(val)
    elif isinstance(value,list):
        for val in value:yield from leaves(val)
for card in m.cards:
    body=(m.OUT/'cards'/f"{card['asset_id']}.md").read_text(encoding='utf-8')
    for value in leaves(card['content']):
        assert m.text(value) in body,(card['asset_id'],value)
    assert m.text(card.get('user_notes','')) in body
    for e in card['evidence']:
        assert e['chapter_id'] in body
        if 'start_line' in e:assert f"{e['start_line']}–{e['end_line']}" in body
    assert '```json' not in body
relations=(m.OUT/'plot/relations.md').read_text(encoding='utf-8')
for edge in m.graph['edges']:assert m.text(edge.get('label',edge['id'])) in relations
for thread in m.book_threads:
    body=(m.OUT/'plot/threads'/f"{thread['id']}.md").read_text(encoding='utf-8')
    assert m.text(thread.get('resolution_note','')) in body
    assert m.STATES[thread['status']] in body
link_count=0
for p in pages+[v/'README.md',report/'README.md']:
    body=p.read_text(encoding='utf-8')
    for raw in re.findall(r'(?<!\\)\[[^\]]+\]\(([^)]+)\)',body):
        url=urlsplit(raw)
        if url.scheme or raw.startswith('#'):continue
        target=(p.parent/unquote(url.path)).resolve()
        assert target.is_relative_to(v.resolve()) and target.exists(),(p,raw,target)
        link_count+=1
    assert not re.search(r'[CE]:[\\/]',body),p
meta=json.loads(command([GH,'api','repos/medillali/writing-vault']))
assert meta['private'] is True and meta['owner']['login']=='medillali'
samples=[m.OUT/'README.md',m.OUT/'characters.md',m.OUT/'cards'/next(c['asset_id']+'.md' for c in m.cards if c['content'].get('name')=='黑龙'),m.OUT/'plot/vol-18.md']
rendered=[]
for i,path in enumerate(samples):
    payload=HERE/f'github-reading-render-{i}.json'
    payload.write_text(json.dumps({'text':path.read_text(encoding='utf-8'),'mode':'gfm','context':'medillali/writing-vault'},ensure_ascii=False),encoding='utf-8')
    output=command([GH,'api','markdown','--method','POST','--input',payload])
    assert re.search(r'<h1(?:\s|>)',output) and re.search(r'<p(?:\s|>)',output)
    assert '<pre>' not in output or 'mermaid' in output
    (HERE/f'github-reading-render-{i}.html').write_text(output,encoding='utf-8')
    rendered.append(path.relative_to(v).as_posix())
result={'markdown_pages':len(pages),'local_links_checked':link_count,'card_content_preserved':len(m.cards),
        'relations_preserved':len(m.graph['edges']),'book_thread_conclusions_preserved':len(m.book_threads),
        'research_json_history_and_user_fields_unchanged':True,'github_gfm_samples':rendered,'repository_private':True}
(HERE/'github-reading-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
