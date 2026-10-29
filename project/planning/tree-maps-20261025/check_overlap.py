from pathlib import Path
import subprocess,json
V=Path('writing-vault').resolve();p=V/'书库/generated-files.json';raw=p.read_bytes()
base=subprocess.check_output(['git','-c',f'safe.directory={V.as_posix()}','-C',str(V),'show','HEAD:书库/generated-files.json'])
print(json.dumps({'local_bytes':len(raw),'base_bytes':len(base),'same_normalized':raw.replace(b'\r\n',b'\n')==base.replace(b'\r\n',b'\n'),'local_crlf':raw.count(b'\r\n'),'base_crlf':base.count(b'\r\n')}))
if raw!=base and raw.replace(b'\r\n',b'\n')==base:
 Path('.planning/tree-maps-20261025/generated-files-before-lf.json').write_bytes(raw)
 p.write_bytes(base)
 print('仅规范生成清单的LF，内容与HEAD相同；旧字节已另存。')
