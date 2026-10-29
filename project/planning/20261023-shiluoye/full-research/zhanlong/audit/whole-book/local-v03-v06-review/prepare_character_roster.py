"""按已实际读完的271阶段卡手工归并身份，输出互斥分工建议，不裁定终态。"""
from pathlib import Path
import json,hashlib,sys
sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;A=H.parent;R=Path('C:/Users/Administrator/Documents/ChatGPT/Novel');F=R/'writing-vault/library/reports/zhanlong'
manual={
1:'李逍遥|林婉儿|东城月|宋寒|冉闵（玩家老K）|狐狸（刘庸）|凫水囡囡|薛柔|东城雷|李牧|王翦|白起|廉颇|剑锋寒|简简单单|堕落苍狼|飞龙在天|花枪一壶酒|月倾浅|月微凉|寒碑颂|雪域千阳（唐雪）|刘英|小猪快跑|徐月|问剑|林天南|王信|沈冰|林成|汪泽诚|流霜|达林|卡尔|罗林|冉闵（古王NPC）|云辰|百炼老人|风烨|南宫决|南宫灵|与子成说|谁家蓝颜',
2:'李逍遥|林婉儿|东城月|薛柔|李牧|王翦|宋寒|冉闵（玩家老K）|狐狸（刘庸）|月倾浅|月微凉|林小舞|雪域千阳（唐雪）|凫水囡囡|千顷瑶池|陈勇洁（一秒英雄）|东城雷|飘渺云烟|剑锋寒|问剑|方歌阙|汪泽诚|魏凡|沈冰|王信|秦雨|秦蒙|欧阳川|唐琦|林天南|流霜|罗雷|罗林|安吉拉|池羽寒|池玉清|池阳|林穹|火犁（神圣魔龙）|南宫决|南宫灵|月妖颜|简简单单|叶来|燕赵无双',
3:'李逍遥|林婉儿|东城月|薛柔|李梦瑶|李牧|王翦|冉闵（玩家老K）|宋寒|狐狸（刘庸）|月倾浅|凫水囡囡|林小舞|东城雷|上将星痕|邢烈|唐琦|唐古|沈冰|王信|林天南|游弋（赵冉）|欧阳川|魏凡|汪泽诚|问剑|剑锋寒|简简单单|方歌阙|纸上画魅（薛景）|流霜|罗林|罗雷|安吉拉|苏克|达林|青萝|冉闵（古王NPC）|池玉清|池羽寒|落海|洛克林|奥蒂莉亚|子舒|艾伦|凌寒|流言（刘彦）|微笑|叶来|秦雯',
4:'李逍遥|林婉儿|东城月|东城雷|薛柔|方歌阙|纸上画魅（薛景）|韩渊|萧厉|龙硎|夏叶|绫罗|菲奥娜|佩儿（原魂）|欧恩|洛克大帝|洛浅林|洛洵|徐翊|罗嗣|罗特|流霜|青萝|子舒|奥蒂莉亚|王信|沈冰|林成|汪泽诚|李牧|王翦|冉闵（玩家老K）|宋寒|月倾浅|月微凉|凫水囡囡|陈勇洁（一秒英雄）|林小舞|花枪一壶酒|问剑|清眸拓墨|魔山|南宫决|南宫灵|罗林',
5:'李逍遥|林婉儿|东城月|薛柔|李牧|王翦|冉闵（玩家老K）|冉闵（古王NPC）|狐狸（刘庸）|宋寒|李梦瑶|林小舞|凫水囡囡|月倾浅|月妖颜|纸上画魅（薛景）|颜沫（牛奶）|花枪一壶酒|方歌阙|问剑|唐琦|叶来|慕萱|沈冰|王信|林天南|林成|北辰观|汪泽诚|未具名日本天道流武士|流霜|子舒|兰娜瑟尔|奥蒂莉亚|青萝|莓儿|洛浅林|洛洵|云飘飘|火狮榛|刘骏|韩渊|萧厉|龙硎|夏叶|林穹|梁印|魔山|清眸拓墨|枫林醉|弗雷|徐焰|雷丁|银戈|安娜|罗布',
6:'李逍遥|林婉儿|东城月|流霜|佩儿（原魂）|西瓦娜|洛浅林|燕赵无双|方歌阙|问剑|薛柔|韩渊|景音|夏叶|龙硎|祝海|清眸拓墨|希芙|子舒|兰蔻|伊薇|奈克|罗躁|云浅|王信|邢烈|斧头|汪泽诚|沈冰|东城雷|傲天战皇|北海神侯'}
npcs=set('流霜|达林|卡尔|罗林|冉闵（古王NPC）|云辰|百炼老人|风烨|罗雷|安吉拉|池羽寒|池玉清|池阳|林穹|火犁（神圣魔龙）|苏克|青萝|落海|洛克林|奥蒂莉亚|子舒|艾伦|凌寒|韩渊|萧厉|龙硎|夏叶|绫罗|菲奥娜|佩儿（原魂）|欧恩|洛克大帝|洛浅林|洛洵|徐翊|罗嗣|罗特|兰娜瑟尔|莓儿|云飘飘|火狮榛|刘骏|梁印|弗雷|徐焰|雷丁|银戈|安娜|罗布|西瓦娜|景音|祝海|希芙|兰蔻|伊薇|奈克|罗躁|云浅|傲天战皇|北海神侯'.split('|'))
opponents=set('剑锋寒|简简单单|堕落苍狼|飞龙在天|花枪一壶酒|寒碑颂|刘英|小猪快跑|徐月|问剑|飘渺云烟|方歌阙|叶来|燕赵无双|流言（刘彦）|微笑|纸上画魅（薛景）|清眸拓墨|魔山|枫林醉|慕萱|颜沫（牛奶）|与子成说|谁家蓝颜|唐古|上将星痕'.split('|'))
written={'李逍遥':1,'林婉儿':2,'东城月':3,'薛柔':4,'沈冰':5,'东城雷':6,'宋寒':7,'冉闵（玩家老K）':8,'李牧':9,'王翦':10,'白起':11,'廉颇':12,'李梦瑶':13}
entities={};pins={}
for v,names in manual.items():
 p=F/f'vol{v:02d}-cards.json';cards=json.loads(p.read_text(encoding='utf-8'));cards=[x for x in cards if x.get('asset_type')=='character' or x.get('kind')=='character' or x.get('card_type')=='character' or x.get('type')=='character'];names=names.split('|');assert len(cards)==len(names),(v,len(cards),len(names));pins[p.relative_to(R).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
 for i,(name,c) in enumerate(zip(names,cards),1):
  if name not in entities:entities[name]=dict(name=name,proposed_owner='reader3_npc' if name in npcs else 'reader4_external_players' if name in opponents else 'zongheng_vol05_full_main_and_reality',status='already_authored_frozen_group' if name in written else 'not_yet_authored',audit_id=f'character-arc-{written[name]:03d}' if name in written else None,stage_cards=[])
  entities[name]['stage_cards'].append(dict(volume=v,index=i,title=c['title'],origin_key=c['origin_key'],asset_id=c.get('asset_id')))
rows=list(entities.values());extra={'reader3_npc':['沧澜','西奥多','百里宁','百里伦','龙忠','罗戟','雷斯','秦烨','司徒薪','高连城','石林卡','琴歌','刑天','火犁（异魔军团统领，勿并已死神圣魔龙）','胡勇','鲁熊','冬茗','克雷斯','云禹','兰斯','孔房','刘维铭','傅雷（伪装工匠，勿并弗雷）','第17代龙神（莓父，勿并银戈或旧书龙神）'],'reader4_external_players':['天空玫瑰','百里若风（玩家，勿并百里伦）','剑泪','吕纯阳','轩辕枫','长生诀'],'zongheng_vol05_full_main_and_reality':['东城风','孙翔','欧阳喏颜','TOM／刘蔚技术说明层','裴姓Andy线索对象','楚天寻','守护者基地／军方编制与KILLS组织接口']}
out=dict(status='mutually_exclusive_assignment_proposal_pending_primary',scope='已实际接读六卷271人物阶段卡后手工归并；不是以目录或哈希代读。无双固定人数不沿用，补漏名单另列待源核而不伪算已完成。',input_sha256=pins,stage_card_count=sum(len(x['stage_cards']) for x in rows),distinct_entities_from_cards=len(rows),counts={owner:sum(x['proposed_owner']==owner for x in rows) for owner in sorted({x['proposed_owner'] for x in rows})},entities=rows,supplementary_entities_for_source_check=extra,identity_limits=['卷四卡题美丽清眸与后清眸拓墨暂按同一印度指挥链提出归并，交reader4具体原文复核；若不同则须拆而非据卡题强并。','狐狸卷三慕天已核为派生无证名并经root批准正式外置，后人物应采用刘庸/琉璃狐；原卡不改。','玩家/古王冉闵分体，原佩/西瓦娜分意志，火犁两体/傅弗两人/龙忠龙硎/百里玩家NPC不可自动并。','NPC死后重塑/游戏玩家掉级复活/现实死亡/记忆人物为不同状态字段；角色命名源差不靠统一数组抹平。'],coordination='已写13项由本代理保持冻结；等待primary确认后三域互斥。各reader分组使用独立前缀稳定ID，主根统一final ID或提前分配，合稿不改已签对象。')
p=A/'character-arc-entity-roster-proposal.json';p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
md=['# 《斩龙》人物实际清单与互斥分工提案','',f'271阶段卡归并{len(rows)}个实体；13条已写。仅分工提案，不改变已签人物/分卷。','']
for owner in out['counts']:
 md+=['## '+owner,'','；'.join(x['name']+('（已写'+x['audit_id']+'）' if x['audit_id'] else '') for x in rows if x['proposed_owner']==owner),'','另需定向补核：'+'；'.join(extra[owner]),'']
md+=['原始阶段标题/asset/origin索引与六正式卡文件SHA全在JSON；补核对象尚未冒算为已完成人物。']
p.with_suffix('.md').write_text('\n'.join(md)+'\n',encoding='utf-8');print(json.dumps({k:out[k] for k in ['stage_card_count','distinct_entities_from_cards','counts']},ensure_ascii=False));print('JSON_SHA '+hashlib.sha256(p.read_bytes()).hexdigest());print('MD_SHA '+hashlib.sha256(p.with_suffix('.md').read_bytes()).hexdigest())
