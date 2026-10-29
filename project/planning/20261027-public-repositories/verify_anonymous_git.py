"""禁用 Git 凭据后核验两个仓库的公开读取，并保留设置回读结果。"""
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

results = []
for name in ("distill-novels", "writing-vault"):
    repository = f"medillali/{name}"
    url = f"https://github.com/{repository}"
    metadata_process = subprocess.run(["gh", "repo", "view", repository, "--json", "nameWithOwner,visibility,url"], check=True, capture_output=True, text=True, encoding="utf-8")
    metadata = json.loads(metadata_process.stdout)
    assert metadata["visibility"] == "PUBLIC", repository
    anonymous_env = os.environ.copy()
    for key in list(anonymous_env):
        if key.startswith("GIT_CONFIG_") or key in ("GH_TOKEN", "GITHUB_TOKEN", "GIT_ASKPASS", "SSH_ASKPASS"):
            anonymous_env.pop(key, None)
    anonymous_env.update({"GIT_TERMINAL_PROMPT": "0", "GCM_INTERACTIVE": "never", "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull})
    anonymous_process = subprocess.run(["git", "-c", "credential.helper=", "-c", "core.askPass=", "-c", "http.extraHeader=", "ls-remote", url + ".git", "HEAD", "refs/heads/main"], check=False, capture_output=True, text=True, encoding="utf-8", env=anonymous_env, timeout=45)
    remote_refs = dict((ref, oid) for oid, ref in (line.split() for line in anonymous_process.stdout.splitlines()))
    read_passed = anonymous_process.returncode == 0 and "HEAD" in remote_refs and "refs/heads/main" in remote_refs
    results.append({**metadata, "anonymous_git_read_passed": read_passed, "remote_refs": remote_refs, "git_exit_code": anonymous_process.returncode, "git_error": anonymous_process.stderr.strip()})

report = {"checked_at_utc": datetime.now(timezone.utc).isoformat(), "git_credentials_disabled": True, "git_global_and_system_config_disabled": True, "git_push_performed": False, "repositories": results, "web_verification_notes": "两仓库CLI可见性回读均为PUBLIC。匿名API被限流；工具库网页返回500，研究库匿名网页可访问并显示Public；匿名Git读取的独立结果见各仓库条目。"}
Path(__file__).with_name("public-access-verification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report, ensure_ascii=False))
