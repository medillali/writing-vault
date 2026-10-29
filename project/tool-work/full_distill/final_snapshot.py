"""将已更新说明和验收记录纳入最终交付快照，逐文件恢复核对。"""
import hashlib
import json
import subprocess
import sys
import zipfile
from persist import ROOT,HERE,SID,json_text
from fictionlib.vault import Vault
from fictionlib.exchange import backup,restore
from fictionlib.graph import render_graph

def main():
    v=Vault(ROOT/'writing-vault')
    assert (v.root/'library/reports/super-skeleton/验收说明.md').exists()
    archive=ROOT/'backups/小说资料库-全书审查交付-20261022.zip'
    target=ROOT/'.verify/f18'
    saved=backup(v,archive);restored=restore(archive,target)
    with zipfile.ZipFile(archive) as z:
        manifest=json.loads(z.read('MANIFEST.json'))
        for name in manifest['files']:
            assert z.read(name)==(v.root/name).read_bytes()==(target/name).read_bytes(),name
    generator=target/'library/reports/super-skeleton/rebuild_review.py'
    r=subprocess.run([sys.executable,'-X','utf8',str(generator)],capture_output=True,text=True,encoding='utf-8')
    assert r.returncode==0,r.stderr
    page='library/views/超级骷髅兵全书审查.html'
    assert (target/page).read_bytes()==(v.root/page).read_bytes()
    graph=json.loads((target/'library/sources'/SID/'plot-graph.json').read_text(encoding='utf-8'))
    render_graph(graph,target/'library/views/plots'/(SID+'-full-nine'))
    Vault(target).build_views()
    result={'backup':saved,'restore':restored,'all_archived_files_identical_to_delivery':True,
            'review_rebuilt_identically_without_original':True,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest()}
    (HERE/'delivery-backup-verification.json').write_text(json_text(result),encoding='utf-8')
    print(json_text(result))

if __name__=='__main__':main()
