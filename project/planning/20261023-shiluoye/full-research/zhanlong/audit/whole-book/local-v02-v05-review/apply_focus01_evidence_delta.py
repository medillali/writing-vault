from save_focus_manual import P,A,E,read,write,sha
import copy
f=A/'focused-findings-part01.json';data=read(f);before=copy.deepcopy(data);data['findings'][0]['evidence'].append(E(1380))
write(P/'focus01-before-1380-evidence.json',before);write(f,data)
assert before['findings'][1:]==data['findings'][1:]
b=copy.deepcopy(before['findings'][0]);a=copy.deepcopy(data['findings'][0]);assert {k:v for k,v in b.items() if k!='evidence'}=={k:v for k,v in a.items() if k!='evidence'}
write(P/'focus01-1380-evidence-delta.json',{'approval':'primary已完整读八项后要求仅identity追加1380就近断臂证据','before':b,'after':a,'all_other_findings_identical':True,'all_other_fields_identical':True,'after_sha256':sha(f),'reading_attribution_confirmation':'1358本代理本轮原文完整BEGIN ch-1358 L97679—97755至END L97755已读，不是仅97698—97710；root的限定补读不归为本代理或root全章重复覆盖。'})
md=f.with_suffix('.md');s=md.read_text(encoding='utf-8').replace('ch-0919\n','ch-0919, ch-1380\n');md.write_text(s,encoding='utf-8');print(sha(f));print(sha(P/'focus01-1380-evidence-delta.json'))
