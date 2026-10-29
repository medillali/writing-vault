from pathlib import Path
import json
V=Path('.verify/tree-maps-20261025');O=V/'library/reports/two-books-full-20261025'
p=V/'书库/catalog.json';data=json.loads(p.read_text(encoding='utf-8'))
for b in data['books']:
 if b['title'] not in ('贼胆','网游之练级专家'):continue
 f='zeidan' if b['title']=='贼胆' else 'leveling';m=b['map'];model=json.loads((O/f/'plot/topology.json').read_text(encoding='utf-8'))
 m.update(form='branching-tree',source_relations=73 if f=='zeidan' else 66,relations=sum(e['kind']!='sequence' for e in model['edges']),
          progress_relations=sum(e['kind'] not in ('sequence','echo') for e in model['edges']),echo_relations=sum(e['kind']=='echo' for e in model['edges']),reading_links=sum(e['kind']=='sequence' for e in model['edges']),
          reader=f'library/reports/two-books-full-20261025/{f}/plot/whole-book/index.html',topology=f'library/reports/two-books-full-20261025/{f}/plot/topology.json')
p.write_bytes((json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
