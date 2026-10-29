"""核对第13集已发表关系仍保留原有端点，防止手工编号碰撞。"""
import json
import re
from collections import defaultdict
from check_and_publish import git,HERE

def verify():
    old=json.loads(git('show','d4a0d4f7bbbb91299d66ccb48641d96431bde456:library/reports/super-skeleton/cross-input.json'))
    now=json.loads((HERE/'cross-input.json').read_text(encoding='utf-8'))
    current={e['id']:e for e in now['edges']}
    assert len(current)==len(now['edges'])
    for e in old['edges']:
        assert e['id'] in current,e['id']
        assert (current[e['id']]['from'],current[e['id']]['to'])==(e['from'],e['to']),e['id']
    seen=defaultdict(list)
    for path in HERE.glob('add_cross*.py'):
        for key in re.findall("edge\\('([^']+)'",path.read_text(encoding='utf-8')):seen[key].append(path.name)
    assert not {k:v for k,v in seen.items() if len(v)>1}
    return {'prior_relations_retained':len(old['edges']),'current_relations':len(current),'authored_ids_unique':True}

if __name__=='__main__':print(json.dumps(verify()))
