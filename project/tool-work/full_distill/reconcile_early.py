"""采纳早期跨集审计：累计状态更新与非姓名别名清理。"""
import json
from pathlib import Path
from persist import ROOT,HERE,SID
from fictionlib.vault import Vault
from fictionlib.storage import locked,commit,json_text

def ev(ch,a,b):return {'chapter_id':f'ch-{ch:04d}','start_line':a,'end_line':b}
config=json.loads((HERE/'cross-input.json').read_text(encoding='utf-8'))
updates=[
 {'key':'th-heiqi-holy-fire','volume':5,'title':'黑七圣焰救援的生死结局','kind':'subplot','status':'resolved',
  'question':'第四集圣焰危机中黑七是否获救？','resolution_note':'第五集确认黑七存活，黄金骨架保留而灵魂退近白银；只关闭这次生死悬念，灵魂恢复与后续受伤仍分别追踪。','evidence':[ev(46,5661,5665)]},
 {'key':'th-rode-music','volume':5,'title':'罗得的旧次逃生与新相遇','kind':'hidden','status':'partial',
  'question':'罗得早先如何逃过审判，何时转生？','resolution_note':'第五集已与黑龙相遇并随队；旧次逃生方式和转生时间仍未明，异常召唤不能自动解释旧案。','evidence':[ev(51,6335,6388)]},
 {'key':'red-moon-destination','volume':6,'title':'亡灵印记的发出者与目的地','kind':'main','status':'resolved',
  'question':'亡灵印记由谁散播，指向哪里？','resolution_note':'斯科特确认散播印记，目的地为哀嚎森林的往生者国度。本状态只关闭定位问题；印记与传统诅咒功能的关系、具体触发机制仍待解释，已保留原问题历史。','evidence':[ev(64,7881,7897)]},
 {'key':'nana-protection','volume':6,'title':'娜娜的保护、身世与主动性','kind':'subplot','status':'partial',
  'question':'娜娜的暗黑气息来源、失亲后果与自主选择将怎样发展？','resolution_note':'第六集明确她能表达保护伙伴的愿望，并已受克丽丝教授法术；天生气息来源、父母遗体后续与追捕后果不能据此关闭。','evidence':[ev(61,7522,7578)]},
]
old={(u['key'],u['volume']):u for u in config.get('state_updates',[])}
old.update({(u['key'],u['volume']):u for u in updates})
config['state_updates']=list(old.values())
(HERE/'cross-input.json').write_text(json_text(config),encoding='utf-8')

v=Vault(ROOT/'writing-vault')
relative='library/reports/super-skeleton/asset-index.json'
index=json.loads((v.root/relative).read_text(encoding='utf-8'))
changed=[]
for alias in ['黑武士侯爵','自称冥月女神','雷神之主']:
    aid=index['characters'].get(alias)
    if not aid:continue
    asset=v.get_asset(aid)
    before={k:asset[k] for k in ['user_notes','favorite','review_status']}
    content=asset['content']
    content['aliases']=[x for x in content.get('aliases',[]) if x!=alias]
    content.setdefault('identity_notes',[])
    note=f'“{alias}”是称号、类别或身份声明，保留出处于分集历史，不用作自动合并人物的别名。'
    if note not in content['identity_notes']:content['identity_notes'].append(note)
    saved=v.put_asset(asset,base_revision=asset['revision'],generated=True)
    assert {k:saved[k] for k in before}==before
    del index['characters'][alias]
    changed.append({'asset_id':aid,'removed_identity_alias':alias})
with locked(v.root):commit(v.root,{relative:json_text(index)})
result={'alias_changes':changed,'audited_thread_updates':len(updates),'human_fields_preserved':True}
(HERE/'early-reconciliation.json').write_text(json_text(result),encoding='utf-8')
print(json_text(result))
