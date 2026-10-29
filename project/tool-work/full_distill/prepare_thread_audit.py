"""收集全部剧情线的阶段记录，供人工做终点审计。"""
import json
from persist import HERE,json_text

def main():
    output=HERE/'thread-final-review.json'
    assert not output.exists()
    config=json.loads((HERE/'cross-input.json').read_text(encoding='utf-8'))
    aliases=config['aliases'];groups={}
    for n in range(1,19):
        report=json.loads((HERE/f'vol{n:02d}.json').read_text(encoding='utf-8'))
        for thread in report['threads']:
            key=aliases.get(thread['key'],thread['key'])
            groups.setdefault(key,[]).append({'volume':n,**thread})
    for update in config['state_updates']:
        key=aliases.get(update['key'],update['key'])
        groups.setdefault(key,[]).append(update)
    for edge in config['edges']:
        for key in edge['tracking_keys']:
            if key not in groups:
                groups[key]=[{'volume':0,'title':'记忆、知识与力量','kind':'hidden','status':'partial',
                    'question':'记忆所得如何改变选择，哪些能力仍不能继承？','resolution_note':'原跨集关系整理，等待全书终点核对。','evidence':edge['evidence']}]
    items=[]
    for key,history in groups.items():
        history.sort(key=lambda x:x['volume']);latest=history[-1]
        items.append({'key':key,'reviewed_at_book_end':False,'history':history,
            'final':{'key':key,'volume':18,'audit_scope':'whole-book',
                     **{k:latest[k] for k in ['title','kind','status','question','resolution_note']},
                     'evidence':latest.get('evidence',[])}})
    output.write_text(json_text({'complete_as_of_volume':None,'entries':items}),encoding='utf-8')
    print(json.dumps({'threads_to_review':len(items)}))

if __name__=='__main__':main()
