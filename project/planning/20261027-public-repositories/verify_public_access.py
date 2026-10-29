"""匿名核验用户明确授权的两个仓库的公开可见性。"""
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

results = []
for name in ("distill-novels", "writing-vault"):
    endpoint = f"https://api.github.com/repos/medillali/{name}"
    request = Request(endpoint, headers={"Accept": "application/vnd.github+json", "User-Agent": "Novel-public-access-verification"})
    try:
        with urlopen(request, timeout=30) as response:
            status = response.status
            metadata = json.load(response)
        assert status == 200 and metadata["private"] is False and metadata["visibility"] == "public", name
        results.append({"repository": metadata["full_name"], "url": metadata["html_url"], "anonymous_http_status": status, "visibility": metadata["visibility"], "private": metadata["private"]})
    except HTTPError as error:
        if error.code != 403:
            raise
        # GitHub 的匿名 API 限流时，改用不带登录凭据的公开网页验证。
        page_url = f"https://github.com/medillali/{name}"
        page_request = Request(page_url, headers={"User-Agent": "Novel-public-access-verification"})
        with urlopen(page_request, timeout=30) as response:
            status = response.status
            final_url = response.url
            page = response.read().decode("utf-8")
        title_match = re.search(r"<title>(.*?)</title>", page, re.S)
        title = title_match.group(1).strip() if title_match else ""
        assert status == 200 and final_url.rstrip("/") == page_url and f"medillali/{name}" in title, name
        assert re.search(r">\s*Public\s*<", page), name
        results.append({"repository": f"medillali/{name}", "url": page_url, "anonymous_http_status": status, "verification_method": "anonymous_repository_html", "public_badge_present": True, "page_title": title, "api_fallback_reason": "anonymous_api_rate_limit_403"})

report = {"checked_at_utc": datetime.now(timezone.utc).isoformat(), "authorization_header_sent": False, "git_push_performed": False, "repositories": results}
Path(__file__).with_name("public-access-verification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report, ensure_ascii=False))
