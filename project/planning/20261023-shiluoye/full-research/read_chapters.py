"""按已登记章节定位输出实际原文；只读，不自动声明模型已读。"""
import pathlib,json,sys,argparse
sys.stdout.reconfigure(encoding='utf-8')
parser=argparse.ArgumentParser();parser.add_argument('book');parser.add_argument('start',type=int);parser.add_argument('end',type=int,nargs='?');args=parser.parse_args()
work=pathlib.Path(__file__).resolve().parent
source=json.loads((work/args.book/'source.json').read_text(encoding='utf-8'))
lines=pathlib.Path(source['normalized_path']).read_text(encoding='utf-8').splitlines()
end=args.end if args.end is not None else args.start
assert 1<=args.start<=end<=len(source['chapters']) and end-args.start<5
for chapter in source['chapters'][args.start-1:end]:
    print(f"BEGIN {chapter['chapter_id']} {chapter['title']} L{chapter['start_line']}—{chapter['end_line']}")
    for number in range(chapter['start_line'],chapter['end_line']+1):print(f'L{number}: {lines[number-1]}')
    print(f"END {chapter['chapter_id']} L{chapter['end_line']}")
