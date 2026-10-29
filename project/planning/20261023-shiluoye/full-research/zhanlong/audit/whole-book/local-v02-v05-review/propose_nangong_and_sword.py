from save_manual_batch import P,F,read,write,sha
import json,copy
def evidence(k,direct=False):
 for v in range(1,7):
  f=F/f'vol{v:02d}-chapter-notes.jsonl'
  for line in f.read_text(encoding='utf-8').splitlines():
   if line.strip():
    n=json.loads(line)
    if n['chapter_id']==f'ch-{k:04d}':return dict(source_id=n['source_id'],revision=n['revision'],chapter_id=n['chapter_id'],start_line=n['start_line'],end_line=n['end_line'],claim_kind='fact',evidence_access='本轮定向BEGIN-END全文复读且匹配正式原reader笔记' if direct else '正式逐章四栏派生完整读取；原文归属不转移',material_path=str(f.relative_to(P.parents[5])).replace('\\','/') if False else f'writing-vault/library/reports/zhanlong/{f.name}',material_sha256=sha(f),source_reader=n.get('reader'))
 raise ValueError(k)
items=[]
for batch,cid,status,rationale,chapters in [
 (3,'v02-local-chapter_unresolved_index-0005-02','answered','258兄妹因史诗旧恩亲自婉拒，921两人国战后已退史诗、922决实际接受斩龙邀请；957 L71533决本人明确自列斩龙骑士，灵称主盟主并替其重铸，1266 L91601主叙明确“斩龙第一兵器铸造师南宫灵”且真陪她过S6。最终两人的组织归属已有实际角色后证，不能因未逐一演灵入盟UI继续悬置会员身份；具体加入时刻/手续未叙不妨碍终态已答。',[258,921,922,957,1266]),
 (7,'v02-local-chapter_unresolved_index-0050-01','answered','309补丁面板真生效；443秦王进化龙池，633再以圣天融合龙池升鬼阶并保绑定/饮血与可进化1，957旧龙池加罗鼎神晶/定海石重铸五星游戏蝴蝶且实装，成长链已有实际后证。587崩残未等原武器永久消失，不能因此漏掉后续升级；不把每次融合/重铸擅算为同一额度扣次器。千阳309亲拒旧恋留会、310对方撤离亦已闭。',[308,309,310,443,587,633,957]),
]:
 file=P/f'adjudications-local-v02-batch{batch:03d}.json';rows=read(file);before=next(x for x in rows if x['candidate_id']==cid);after=copy.deepcopy(before)
 after.update(status=status,rationale=rationale,later_chapters=chapters,later_evidence=[evidence(k,k in [957,1266]) for k in chapters])
 items.append(dict(path=file.name,candidate_id=cid,input_sha256=sha(file),before=before,after=after,scope='仅所列终判/理由/后证字段；原ID/title/reader/原记录及其余对象完全不动'))
out=P/'nangong-membership-and-sword-growth-proposal.json';assert not out.exists();write(out,dict(status='proposal-pending-primary-review-not-applied',actual_reviewer='/root/zongheng_vol04_full',reason='主审指出灵归属后文已明；同次957回读并发现本代理另一已交条目漏633/957成长后证，主动列独立纠正链。',direct_rereads=[dict(raw=957,start_line=71463,end_line=71550,full_text_read=True),dict(raw=1266,start_line=91586,end_line=91652,full_text_read=True)],changes=items,original_batches_unchanged=True))
out.with_suffix('.md').write_text('# 南宫归属与龙池成长定向提案\n\n尚未合入，不改已交批SHA。\n\n'+'\n\n'.join(f"- {x['candidate_id']}：{x['before']['status']} → {x['after']['status']}\n  {x['after']['rationale']}" for x in items)+'\n',encoding='utf-8');print(sha(out))
