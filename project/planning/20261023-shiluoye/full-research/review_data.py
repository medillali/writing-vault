"""分段审阅研究JSON；压缩固定来源字段，不代替正文阅读。"""
import pathlib,json,sys
sys.stdout.reconfigure(encoding='utf-8')
data=json.loads(pathlib.Path(sys.argv[1]).read_text(encoding='utf-8'))
key=sys.argv[2] if len(sys.argv)>2 else '.'
if key=='keys':
    data={k:(len(v) if isinstance(v,(dict,list)) else v) for k,v in data.items()}
elif key!='.':
    for part in key.split('.'):
        data=data[int(part)] if isinstance(data,list) else data[part]
if len(sys.argv)>3:
    data=data[int(sys.argv[3]):int(sys.argv[4]) if len(sys.argv)>4 else None]
def compact(value):
    if isinstance(value,list):return [compact(v) for v in value]
    if isinstance(value,dict):
        if {'source_id','revision','chapter_id'}.issubset(value):
            return value['chapter_id']+f" L{value.get('start_line','?')}—{value.get('end_line','?')}"+((' '+value['claim_kind']) if value.get('claim_kind') else '')
        return {k:compact(v) for k,v in value.items()}
    return value
print(json.dumps(compact(data),ensure_ascii=False,separators=(',',':')))
