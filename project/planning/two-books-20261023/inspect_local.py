from pathlib import Path
import json, sys, subprocess
root = Path(__file__).resolve().parents[2]
print('PYTHON', sys.executable)
print('SOURCE_FILES')
for title in ['贼胆', '网游之练级专家']:
    for p in Path('E:/chromedownload').glob(f'*{title}*.txt'):
        print(str(p), p.stat().st_size)
old = root.parent / 'Chinese Novel' / 'books' / 'zeidan' / 'distillation'
print('OLD_RESEARCH', old, old.exists())
if old.exists():
    print('\n'.join(p.name for p in old.iterdir()))
print('SOURCES')
for p in (root/'writing-vault/library/sources').glob('*.json'):
    d=json.loads(p.read_text(encoding='utf-8'))
    print(p.name, json.dumps(d,ensure_ascii=False)[:1500])
print('VAULT', (root/'writing-vault/vault.json').read_text(encoding='utf-8'))
