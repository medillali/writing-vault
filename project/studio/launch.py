#!/usr/bin/env python3
"""Verify and run the bundled tool in a separate, versioned checkout."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


def main():
    if sys.version_info < (3,10):
        raise ValueError('需要 Python 3.10 或更高版本')
    parser = argparse.ArgumentParser(description='安装并启动私人小说工作台；不覆盖现有工作副本')
    parser.add_argument('--code-dir',help='独立工具目录，必须为空或与本发布版本完全一致')
    parser.add_argument('--private-dir',help='Git 之外的私人作品目录；省略则使用工具默认值')
    parser.add_argument('--research-vault',help='研究库位置；默认使用本文件所在 writing-vault')
    parser.add_argument('--check-only',action='store_true')
    parser.add_argument('--no-open',action='store_true')
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    release = json.loads((here/'release.json').read_text(encoding='utf-8'))
    bundle = here/'distill-novels.bundle'
    if hashlib.sha256(bundle.read_bytes()).hexdigest() != release['artifacts']['distill-novels.bundle']:
        raise ValueError('工具包校验失败，请重新取得完整发布文件')
    base = Path(os.environ['LOCALAPPDATA'])/'NovelStudioCode' if os.name == 'nt' and os.environ.get('LOCALAPPDATA') else Path.home()/'.local/share/novel-studio-code'
    code = Path(args.code_dir).expanduser().resolve() if args.code_dir else base/release['commit'][:12]
    if not code.exists() or not any(code.iterdir()):
        code.parent.mkdir(parents=True,exist_ok=True)
        subprocess.run(['git','clone','-c','core.longpaths=true','-b',release['branch'],str(bundle),str(code)],check=True)
        subprocess.run(['git','-C',str(code),'remote','set-url','origin','https://github.com/medillali/distill-novels.git'],check=True)
    actual = subprocess.check_output(['git','-C',str(code),'rev-parse','HEAD'],text=True).strip()
    dirty = subprocess.check_output(['git','-C',str(code),'status','--porcelain'],text=True).strip()
    if actual != release['commit'] or dirty:
        raise ValueError('工具目录已有其他版本或未提交改动，已停止；请保留它并指定新的 --code-dir')
    print(json.dumps({'code_dir':str(code),'commit':actual,'verified':True},ensure_ascii=False),flush=True)
    if args.check_only:
        return 0
    command = [sys.executable,'-X','utf8',str(code/'scripts/studio.py')]
    if args.private_dir:
        command += ['--vault',args.private_dir]
    command += ['serve']
    if not args.no_open:
        command += ['--open']
    research = Path(args.research_vault).expanduser() if args.research_vault else here.parents[1]
    if (research/'vault.json').is_file():
        command += ['--research-vault',str(research)]
    return subprocess.call(command)


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError,OSError,subprocess.CalledProcessError) as error:
        print('启动失败：'+str(error),file=sys.stderr)
        raise SystemExit(1)
