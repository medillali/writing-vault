import pathlib,re,json,sys,hashlib
sys.stdout.reconfigure(encoding='utf-8')
root=pathlib.Path(__file__).resolve().parents[2]
old=root.parent/'Chinese Novel/books/zeidan/distillation'
dest=root/'writing-vault/library/reports/zeidan/legacy-reading';dest.mkdir(exist_ok=True)
files=['README.md','core-characters.md','story-map.md','scene-close-reading.md','chapter-events.md','characters.md','appearance-candidates.md','scene-library.md','thread-register.md']
mapping=json.loads((dest.parent/'chapter-map.json').read_text(encoding='utf-8'))
chapters_by_line={}
for c in mapping:
    for n in range(c['start_line'],c['end_line']+1):chapters_by_line[n]=c['chapter_id']
replaced=0;unresolved=[]
for name in files:
    raw=(old/name).read_text(encoding='utf-8')
    def link(match):
        global replaced
        label,target=match[1],match[2].strip('<>')
        if 'source/decoded.txt:' in target or 'source\\decoded.txt:' in target:
            n=int(target.rsplit(':',1)[1]);ch=chapters_by_line.get(n)
            if not ch:unresolved.append(target);return label+'（原定位：'+target+'）'
            if not re.search(r'L\d+',label):label+=' · L'+str(n)
            replaced+=1;return '['+label+'](evidence-index.md#'+ch+')'
        base=pathlib.Path(target).name
        if target.endswith('.md') and base in files:return '['+label+']('+base+')'
        if base in ['coverage.json','validation.json','entities.json','entity-groups.json','scenes.json','threads.json','chapter-notes.jsonl','review-statistics.json','artifact-check.json']:return '['+label+'](../legacy/'+base+')'
        if target.startswith(('http:','https:','#')):return match[0]
        # 旧工具输出或未迁入附件保留路径文字，避免伪造可点击且失效的阅读入口。
        if not (dest/target).exists():return label+'（旧附件：`'+target+'`）'
        return match[0]
    text=re.sub(r'\[([^\]\n]+)\]\(([^)\n]+)\)',link,raw)
    text='> 旧研究阅读副本。正文分析保持原文；链接已转为本库证据定位。旧报告中的“完成”仅指当时研究范围，不是本轮重读或用户确认。\n\n'+text
    (dest/name).write_text(text,encoding='utf-8')
idx=['# 《贼胆》旧研究证据定位','', '此处保留章节身份与原文行号，不复制原书正文。原文本在本机private-sources；跨设备核对时需要同修订原文。','']
for c in mapping:
    idx+=['<a id="'+c['chapter_id']+'"></a>','', '## '+c['chapter_id']+' · '+c['title'],'',f"旧顺序 {c['legacy_sequence']}；原文 L{c['start_line']}—L{c['end_line']}。",'']
(dest/'evidence-index.md').write_text('\n'.join(idx)+'\n',encoding='utf-8')
(dest/'migration-links.json').write_text(json.dumps({'rewritten_source_links':replaced,'unresolved_source_lines':unresolved,'files':files,'original_markdown_sha256':{n:hashlib.sha256((old/n).read_bytes()).hexdigest() for n in files}},ensure_ascii=False,indent=2),encoding='utf-8')
print('copied',len(files),'rewritten',replaced,'unresolved',unresolved)
