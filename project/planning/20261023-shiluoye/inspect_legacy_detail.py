import pathlib,json,sys,collections
sys.stdout.reconfigure(encoding='utf-8')
p=pathlib.Path('C:/Users/Administrator/Documents/ChatGPT/Chinese Novel/books/zeidan/distillation')
for filename in ['entities.json','entity-groups.json','scenes.json','threads.json']:
    j=json.loads((p/filename).read_text(encoding='utf-8'))
    print(filename,'type',type(j).__name__,'count',len(j))
    if isinstance(j,list):
        print('keys',collections.Counter(k for x in j for k in x))
        for field in ['record_type','status','maintenance_depth','record_kind','category','worker_part']:
            print(field,collections.Counter(str(x.get(field)) for x in j))
        print('last',json.dumps(j[-2:],ensure_ascii=False)[:7000])
    else:print(json.dumps(j,ensure_ascii=False)[:5000])
print((p/'appearance-candidates.md').read_text(encoding='utf-8')[:3000])
