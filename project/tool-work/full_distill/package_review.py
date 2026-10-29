"""生成解压即可打开的离线审查副本；正式JSON与历史仍由资料库备份保存。"""
import hashlib
import json
from pathlib import Path
import zipfile
from persist import ROOT,HERE,SID,json_text

def main():
    vault=ROOT/'writing-vault'
    reports=vault/'library/reports/super-skeleton'
    assert len(list(reports.glob('vol[0-9][0-9].json')))==18
    ledger=json.loads((reports/'question-ledger.json').read_text(encoding='utf-8'))
    assert ledger['completion']=='complete_as_of_volume_18'
    views=vault/'library/views'
    title='超级骷髅兵全书审查.html'
    files={title:(views/title).read_bytes()}
    graph=views/'plots'/(SID+'-full-nine')
    for path in graph.rglob('*'):
        if path.is_file():files[path.relative_to(views).as_posix()]=path.read_bytes()
    for name in ['book-synthesis.md','question-ledger.md']:
        files['研究报告/'+name]=(reports/name).read_bytes()
    files['请先阅读.txt']=('《超级骷髅兵》全书离线审查副本\n\n'
        '完整解压后，使用浏览器打开“超级骷髅兵全书审查.html”。主线/暗线图使用相对链接，保留plots文件夹的位置。\n'
        '本包包含18集研究草稿、人物及素材阅读副本、九维综合与疑点回收；不需要联网或Python。\n'
        '页面可筛选和查看，但不会直接保存个人收藏或笔记。持久编辑请通过原资料库工具操作，JSON主档与历史以资料库备份为准。\n'
        '不包含原小说TXT。核对原文仍需要本机原书和同一修订的章节行号。其他三本保持开篇样段，Space尚未接入。\n').encode('utf-8')
    archive=ROOT/'backups/超级骷髅兵-离线审查包-20261022-终审.zip'
    target=ROOT/'.verify/r18-final'
    assert not archive.exists() and not target.exists()
    archive.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=7) as z:
        for name,data in files.items():
            assert not name.startswith('/') and '..' not in Path(name).parts and 'private-sources' not in name
            z.writestr(name,data)
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        z.extractall(target)
    for name,data in files.items():assert (target/name).read_bytes()==data
    assert (target/'plots'/(SID+'-full-nine')/'index.html').exists()
    result={'archive':str(archive),'files':len(files),'bytes':archive.stat().st_size,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),
            'extracted_files_identical':True,'entry':str(target/title),'browser_check':'pending'}
    (HERE/'review-package.json').write_text(json_text(result),encoding='utf-8')
    print(json_text(result))

if __name__=='__main__':main()
