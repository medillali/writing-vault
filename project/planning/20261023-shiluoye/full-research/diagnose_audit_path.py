from pathlib import Path
p = Path(r'C:\Users\Administrator\Documents\ChatGPT\Novel\.planning\20261023-shiluoye\full-research\audit-fixture-prkezxap\writing-vault\library\reports\fixture-book\audit\.whole-book-preparing-85aee729614345dd95059f036f20f12f\provenance\frozen-volume\chapter-notes.jsonl')
print('failing_path_length', len(str(p)), 'parent_length', len(str(p.parent)))
print('short_temp_path_length', len(str(p).replace('.whole-book-preparing-85aee729614345dd95059f036f20f12f', '.wb-123456789abc')))
