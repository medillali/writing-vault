"""核对当前已正式保存的斩龙阅读链接，不声称全书已经完成。"""
import json
import sys
from book_audit_common import DEFAULT_ROOT, check_md_links

sys.stdout.reconfigure(encoding="utf-8")
folder = DEFAULT_ROOT / "writing-vault" / "library" / "reports" / "zhanlong"
checked = 0
errors = []
paths = sorted(folder.rglob("*.md"))
for path in paths:
    try:
        checked += check_md_links(path)
    except ValueError as error:
        errors.append(str(error))
print(json.dumps({"markdown_files": len(paths), "links_checked": checked, "errors": errors, "complete_book": False}, ensure_ascii=False))
assert not errors
