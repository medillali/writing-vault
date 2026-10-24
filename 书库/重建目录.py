"""从书目元数据重建Git阅读导航，保留研究主档和人工修改。"""
from pathlib import Path
import hashlib,json,os,re,sys

HERE=Path(__file__).resolve().parent
VAULT=HERE.parent
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(raw):return hashlib.sha256(raw).hexdigest()
def name(value):
    if not value or value in ['.','..'] or re.search(r'[\\/:*?"<>|]',value) or value.endswith(('.',' ')):
        raise ValueError('目录名不合法：'+value)
    return value
def main():
    data=load(HERE/'catalog.json');books=data['books'];assert len({b['source_id'] for b in books})==len(books)
    assert len({b['directory'] for b in books})==len(books),'同名书需另设唯一directory'
    manifest=HERE/'generated-files.json';old=load(manifest).get('files',{}) if manifest.exists() else {};outputs={}
    def write(path,body):
        p=HERE/path;assert p.resolve().is_relative_to(HERE.resolve())
        raw=(body.rstrip()+'\n').encode('utf-8')
        if p.exists() and p.read_bytes()!=raw:
            key=p.relative_to(HERE).as_posix()
            if key not in old or sha(p.read_bytes())!=old[key]:raise ValueError('保留人工修改，未覆盖：'+key)
        outputs[p]=raw
    def link(label,target,page):
        p=VAULT/target;relative=os.path.relpath(p,(HERE/page).parent).replace('\\','/')
        return '['+label+']('+relative+')'
    def book_path(b):return '按书名/'+name(b['directory'])+'/README.md'
    def hub(label,path,page):return link(label,'书库/'+path,page)
    def row(b,page):
        return '| '+hub('《'+b['title']+'》',book_path(b),page)+' | '+hub(b['author'],'按作者/'+b['author']+'/README.md',page)+' | '+b['coverage_label']+' |'
    def table(group,page):return '| 作品 | 作者 | 已发布研究范围 |\n|---|---|---|\n'+'\n'.join(row(b,page) for b in group)
    for b in books:
        name(b['directory']);name(b['author']);assert b['genres']
        for genre in b['genres']:name(genre)
        page=book_path(b);types=' · '.join(hub(g,'按类型/'+g+'/README.md',page) for g in b['genres'])
        body='# 《'+b['title']+'》\n\n作者：'+hub(b['author'],'按作者/'+b['author']+'/README.md',page)+'。类型：'+types+'。标签：'+'、'.join(b.get('tags',[]))+'。\n\n'
        body+='**'+b['coverage_label']+'。**\n\n'+hub('书库总入口','README.md',page)+' · '+hub('按书名浏览','按书名/README.md',page)+'\n\n'
        if b.get('local_progress_note'):body+=b['local_progress_note']+'\n\n'
        if b.get('report'):body+='- '+link('全书研究报告',b['report'],page)+'\n'
        if b.get('map'):body+='- [全书剧情地图](剧情地图.md)：Git图片、可缩放HTML与证据阅读器。\n'
        for x in b['published_links']:body+='- '+link(x['label'],x['path'],page)+'\n'
        body+='\n来源身份：`'+b['source_id']+'`；文本修订：`'+b['source_revision']+'`。\n\n研究分析仍待用户审阅；这里的归类和目录不会自动进入原创项目正典。\n'
        if not b.get('map'):body+='\n本书尚无已发布的全书剧情地图，开篇研究和建档不标成全书完成。\n'
        write(page,body)
        if b.get('map'):
            page='按书名/'+b['directory']+'/剧情地图.md';m=b['map']
            body='# 《'+b['title']+'》全书剧情地图\n\n'+hub('返回本书',book_path(b),page)+' · '+hub('全部全书地图','全书剧情地图/README.md',page)+'\n\n'
            if m.get('form')=='branching-tree':
                body+=f'覆盖全书{m["unit_count"]}个实际正文/序章单元，保留{m["events"]}个精选事件。沿用《超级骷髅兵》的主干、分枝、共享交汇与暗线终态形式；{m["stages"]}个研究阶段仅用于定位。\n\n'
                body+=f'展示层有{m["relations"]}条语义联系（{m["progress_relations"]}条推进关系、{m["echo_relations"]}条主题呼应），另有{m["reading_links"]}条主干阅读衔接。阅读衔接不是因果；主题呼应和阅读衔接均不虚增交汇点。逐章记录负责全量覆盖，地图精选事件负责呈现结构。\n\n'
            else:
                body+=f'覆盖全书{m["unit_count"]}个实际正文/序章单元；图按{m["stages"]}个阶段组织，含{m["events"]}个精选事件、{m["relations"]}条关系。逐章记录负责全量覆盖，地图精选事件负责呈现结构与因果。\n\n'
            body+='| 阅读方式 | 入口 |\n|---|---|\n'
            for label,key in [('Git直接查看PNG原图','png'),('Git直接查看SVG矢量图','svg'),('下载后离线缩放、拖动和定位','html'),('地图详细说明','overview'),('查询节点、伏笔与来源证据','reader')]:
                if key in m:body+='| '+label+' | '+link(label,m[key],page)+' |\n'
            body+='\nGitHub仓库页显示图片和文件源码，不执行HTML。交互地图可在文件页点击下载，保存为HTML后用浏览器打开；无需公开发布仓库。PC可拖动和滚轮缩放，手机可双指缩放。\n\n'
            body+='[!['+b['title']+'全书剧情地图预览]('+os.path.relpath(VAULT/m['preview'],(HERE/page).parent).replace('\\','/')+')]('+os.path.relpath(VAULT/m['png'],(HERE/page).parent).replace('\\','/')+')\n\n'
            body+='连线以已保存的剧情关系为准，视觉交叉不自动等于剧情交汇；研究分段也不等于原著卷名。\n'
            write(page,body)
    page='按书名/README.md';write(page,'# 按书名浏览\n\n'+hub('书库总入口','README.md',page)+'\n\n'+table(sorted(books,key=lambda b:b['title']),page))
    for dimension,field,title in [('按作者','author','作者'),('按类型','genres','小说类型')]:
        groups={}
        for b in books:
            for value in b[field] if isinstance(b[field],list) else [b[field]]:groups.setdefault(value,[]).append(b)
        page=dimension+'/README.md';body='# 按'+title+'浏览\n\n'+hub('书库总入口','README.md',page)+'\n\n'
        for value,group in sorted(groups.items()):
            path=dimension+'/'+value+'/README.md';body+='- '+hub(value,path,page)+f'：{len(group)}本。\n';ordered=sorted(group,key=lambda b:(b['author'],b['author_order']))
            details='# '+value+'\n\n'+hub('书库总入口','README.md',path)+' · '+hub('全部'+title,dimension+'/README.md',path)+'\n\n'+table(ordered,path)
            details+='\n\n类型为本资料库研究分类，可用多标签；作者内沿既有书目顺序，不新增创作日期判断。\n';write(path,details)
        write(page,body)
    page='全书剧情地图/README.md';full=[b for b in books if b.get('map')]
    body='# 全书剧情地图\n\n'+hub('书库总入口','README.md',page)+'\n\n已完成全书研究的地图集中于此；尚未完成的作品在各自书页显示实际范围。\n\n'
    for b in full:body+='- '+hub('《'+b['title']+'》：全书地图','按书名/'+b['directory']+'/剧情地图.md',page)+'。\n'
    write(page,body)
    write('README.md','# 小说书库\n\n按书名、作者或小说类型进入同一本书，查看研究范围、全书地图、人物、场景、机制和证据。\n\n- [按书名浏览](按书名/README.md)\n- [按作者浏览](按作者/README.md)\n- [按小说类型浏览](按类型/README.md)\n- [全书剧情地图](全书剧情地图/README.md)\n- [维护与增加新书](维护说明.md)\n\n'+table(books,'README.md')+'\n\n当前索引'+str(len(books))+'本书；建档、开篇研究、进行中与全书完成分别标记。研究范围表示Git已发布检查点，本地续读可能正在更新。类型是研究标签，个人评价与原创正典仍分别保存。')
    for p,raw in outputs.items():p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
    manifest.write_text(json.dumps({'schema_version':1,'files':{p.relative_to(HERE).as_posix():sha(raw) for p,raw in outputs.items()},'stale_generated_paths':sorted(set(old)-{p.relative_to(HERE).as_posix() for p in outputs})},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'books':len(books),'authors':len({b['author'] for b in books}),'genres':len({g for b in books for g in b['genres']}),'full_book_maps':len(full),'generated_pages':len(outputs)},ensure_ascii=False))
if __name__=='__main__':main()
