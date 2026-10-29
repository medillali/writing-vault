"""只识别本任务启动的具体只读校验进程，不输出其他进程命令。"""
import csv,io,json,os,signal,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[3]
p=subprocess.run(['wmic','process','where',"name='python.exe'",'get','CommandLine,ProcessId,CreationDate','/FORMAT:CSV'],capture_output=True,check=True)
raw=p.stdout
s=raw.decode('utf-16') if b'\x00' in raw[:200] else raw.decode('mbcs')
target=str(R/'distill-novels/scripts/library.py').lower()
matches=[]
for row in csv.DictReader(io.StringIO(s.strip())):
 cmd=row.get('CommandLine','')
 if target in cmd.lower() and cmd.rstrip().endswith(' validate') and str(R/'writing-vault').lower() in cmd.lower():
  matches.append(dict(pid=int(row['ProcessId']),command=cmd,created=row['CreationDate']))
sys.stdout.reconfigure(encoding='utf-8');print(json.dumps({'exact_task_validation_matches':matches},ensure_ascii=False))
if '--stop-own-read-only-validation' in sys.argv:
 assert len(matches)==1,'只能停止唯一的本任务只读校验'
 assert not (R/'writing-vault/.journal.json').exists(),'存在事务日志，拒绝停止'
 os.kill(matches[0]['pid'],signal.SIGTERM)
 print('STOPPED_OWN_READ_ONLY_VALIDATION_OS_LOCK_RELEASES_ON_PROCESS_EXIT')
