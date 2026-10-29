import pathlib,sys
sys.stdout.reconfigure(encoding='utf-8')
v=pathlib.Path(__file__).parent
name=sys.argv[1]
p=v.parent/'vol01'/name
ls=p.read_text(encoding='utf-8').splitlines()
start,end=map(int,sys.argv[2:4])
for i in range(start-1,min(end,len(ls))):print(f'{i+1}: {ls[i]}')
