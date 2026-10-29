"""归并已人工核对的同一剧情线；不自动推断因果或回收。"""
import argparse
import hashlib
import json
from persist import HERE, CH, json_text

def build(n):
    config=json.loads((HERE/'cross-input.json').read_text(encoding='utf-8'))
    aliases=config['aliases']
    groups={}
    nodes=set()
    edge_info=[]
    for number in range(1,n+1):
        report=json.loads((HERE/f'vol{number:02d}.json').read_text(encoding='utf-8'))
        nodes.update(e['key'] for e in report['events'])
        pairs={}
        for i,e in enumerate(report['edges'],1):
            eid=f'v{number:02d}-edge-{i:02d}'
            pairs.setdefault((e['from'],e['to']),[]).append(eid)
            edge_info.append({**e,'id':eid})
        for t in report['threads']:
            key=aliases.get(t['key'],t['key'])
            g=groups.setdefault(key,{'members':[],'edges':[],'history':[]})
            g['members']+=t['event_keys']
            g['edges'] += [e for pair in t.get('edge_pairs',[]) for e in pairs[tuple(pair)]]
            g['history'].append({'volume':number,'title':t['title'],'kind':t['kind'],'status':t['status'],'question':t['question'],'resolution_note':t['resolution_note']})
    cross=[]
    for e in config['edges']:
        if e['from'] not in nodes or e['to'] not in nodes:continue
        for evidence in e['evidence']:
            c=CH[evidence['chapter_id']]
            assert c['start_line']<=evidence['start_line']<=evidence['end_line']<=c['end_line'],evidence
        cross.append({k:v for k,v in e.items() if k!='tracking_keys'})
        for key in e['tracking_keys']:
            g=groups.setdefault(key,{'members':[],'edges':[],'history':[]})
            g['members'] += [e['from'],e['to']]
            g['edges'].append(e['id'])
    # 后续正文可回答早期问题而未重复同一个局部线程；人工审计单独补记状态。
    for update in config.get('state_updates',[]):
        if update['volume']>n:continue
        key=aliases.get(update['key'],update['key'])
        assert key in groups,('unknown audited thread',key)
        for evidence in update['evidence']:
            c=CH[evidence['chapter_id']]
            assert c['start_line']<=evidence['start_line']<=evidence['end_line']<=c['end_line']
        groups[key]['history'].append({k:v for k,v in update.items() if k!='key'})
    threads=[]
    for key,g in groups.items():
        volumes={int(x[1:3]) for x in g['members']}
        final_audited=any(item.get('volume')==18 and item.get('audit_scope')=='whole-book' for item in g['history'])
        if len(volumes)<2 and not final_audited:continue
        g['history'].sort(key=lambda item:item['volume'])
        last=g['history'][-1] if g['history'] else {'title':'记忆、知识与力量','kind':'hidden','status':'partial','question':'记忆所得如何改变选择，哪些能力仍不能继承？','resolution_note':'跨集信息优势得到兑现；知识与魔力仍须分开。'}
        latest_state=max((item['volume'] for item in g['history']),default=0)
        state_note=f'最新状态审计在第{latest_state}集。' if latest_state else '状态来自人工跨集关系整理。'
        threads.append({'id':'book-'+hashlib.sha256(key.encode()).hexdigest()[:12],'tracking_key':key,
            'title':('跨集 · ' if len(volumes)>=2 else '全书复核 · ')+last['title'],'kind':last['kind'],'status':last['status'],
            'node_ids':list(dict.fromkeys(g['members'])),'edge_ids':list(dict.fromkeys(g['edges'])),
            'question':last['question'],'resolution_note':f"已入库至第{n}集；最近关联事件在第{max(volumes)}集。"+state_note+last['resolution_note'],
            'volume_history':g['history']})
    result={'covered_volumes':list(range(1,n+1)),'edges':cross,'threads':threads}
    (HERE/'cross-volume.json').write_text(json_text(result),encoding='utf-8')
    print(json.dumps({'volumes':n,'cross_edges':len(cross),'cross_threads':len(threads)},ensure_ascii=False))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('volume',type=int);a=p.parse_args();build(a.volume)
