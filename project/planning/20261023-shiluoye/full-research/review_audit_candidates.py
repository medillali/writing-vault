"""只压缩重复原记录以便逐批审查终点判断，不代替正文阅读。"""
import pathlib,json,sys
sys.stdout.reconfigure(encoding='utf-8')
data=json.loads(pathlib.Path(sys.argv[1]).read_text(encoding='utf-8'))
rows=data['candidates'][int(sys.argv[2]):int(sys.argv[3])]
def compact(value):
    if isinstance(value,list):return [compact(v) for v in value]
    if isinstance(value,dict):
        if {'source_id','revision','chapter_id'}.issubset(value):
            return value['chapter_id']+f" L{value.get('start_line','?')}—{value.get('end_line','?')}"
        return {k:compact(v) for k,v in value.items()}
    return value
for row in rows:
    result={k:row[k] for k in ['candidate_id','volume','entry_type','original_stage_status','title','terminal_assessment'] if k in row}
    if 'title' not in result:
        result['original_record']=row.get('original_record')
    print(json.dumps(compact(result),ensure_ascii=False,separators=(',',':')))
