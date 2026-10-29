"""本读者逐段完整回看1180—1339原人工笔记后的第二轮定向校正。"""
from pathlib import Path
import json,sys
sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).parent
changes={
'build_artifacts.py':[
("[1259,1260,1266,1281,1385,1386]","[1259,1260,1267,1281,1385,1386]"),
("[1248,1288,1345,1358,1359,1360,1386]","[1248,1289,1345,1358,1359,1360,1386]"),
("[1252,1263,1264,1324,1340,1384]","[1251,1253,1262,1264,1324,1325,1340,1384]")
],
'research_cards.py':[
("'bargain-operator','霸王改动的延期与落地属性',1266","'bargain-operator','霸王改动的延期与落地属性',1267"),
("[1266,1267,1281],['li-xiaoyao']","[1266,1267,1281],['li-xiaoyao']"),
("[1282,1283,1284,1285,1286,1287,1288],['li-xiaoyao','lin-waner','dongcheng-yue']","[1282,1283,1284,1285,1286,1287,1288,1289],['li-xiaoyao','lin-waner','dongcheng-yue']"),
("'space-father','因救父暂留俘虏，再杀取格',1252","'space-father','因救父暂留俘虏，再杀取格',1253"),
("[1252,1253,1254],['li-xiaoyao','natalie-allies','luo-zao']","[1253,1254],['li-xiaoyao','yiwei','naike','luo-zao']"),
("['li-xiaoyao','natalie-allies','luo-zao']","['li-xiaoyao','yiwei','luo-zao']"),
("['li-xiaoyao','dongcheng-yue','natalie-allies']","['li-xiaoyao','dongcheng-yue','naike']"),
("[1266,1272])","[1267,1272])")
],
'research_interfaces.py':[
("[1288,1290]","[1289,1290]"),
("[1244,1305,1374,1384]","[1244,1304,1309,1374,1384]"),
("[1212,1214,1215,1219,1281,1324]","[1212,1214,1215,1219,1281,1324,1325]"),
("[1252,1253])","[1251,1253,1254])"),
("1263一处称上位","1262一处称上位"),
("[1263,1266])","[1262,1263,1266])"),
("1263主旁的己NPC守军单处用玩家称谓。","1262主旁的己NPC守军单处用玩家称谓。"),
("[1263])","[1262])"),
("1286小舞被秒/待复，后攻段一处仍写小舞动作。","1288小舞被秒/待复，后攻段一处仍写小舞动作。"),
("[1286])","[1288])"),
("[1283,1286])","[1282,1286])"),
("[1284,1288])","[1284,1289])"),
("[1298,1299])","[1298,1309])"),
("[1304])","[1302])"),
("[1281,1324])","[1281,1324,1325])"),
("1335霜林/妖月/战雷对话中","1334霜林/妖月/战雷对话中"),
("[1335])","[1334])"),
("[1229,1230,1235,1236])","[1229,1230,1235,1236])"),
("[1238,1244])","[1238,1244])"),
("[1251,1252,1253])","[1251,1253,1254])"),
("[1259,1260,1262])","[1259,1260,1262])"),
("[1266,1272])","[1267,1272])")
]}
applied=[]
for name,pairs in changes.items():
    p=H/name;t=p.read_text(encoding='utf-8')
    for b,a in pairs:
        n=t.count(b)
        if b!=a:
            if n:t=t.replace(b,a)
            applied.append(dict(file=name,before=b,after=a,occurrences=n))
    p.write_text(t,encoding='utf-8')
(H/'prefreeze-reference-corrections-2.json').write_text(json.dumps(dict(reason='人物施为与原raw证据精确对齐，不改原notes',changes=applied),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(applied,ensure_ascii=False))
