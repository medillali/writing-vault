"""列人物组的既有名称供身份复核；不产生人物或阅读记录。"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
directory = Path(__file__).parent / sys.argv[1] / 'audit/whole-book'
for path in sorted(directory.glob('character-arcs-part*.json')):
    data = json.loads(path.read_text(encoding='utf-8'))
    for row in data['characters']:
        print(row['audit_id'], row['name'])
