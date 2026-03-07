#!/usr/bin/env python3

import os
import re
import subprocess

REPO_PATTERN = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
SSH_REMOTE = re.compile(r"^git@github\.com:(?P<repo>[^/]+/[^/]+?)(?:\.git)?$")
HTTPS_REMOTE = re.compile(r"^https://github\.com/(?P<repo>[^/]+/[^/]+?)(?:\.git)?/?$")
SSH_URL_REMOTE = re.compile(r"^ssh://git@github\.com/(?P<repo>[^/]+/[^/]+?)(?:\.git)?/?$")


def tool(name, default):
    return os.environ.get(name, default)


def run(command, env=None):
    return subprocess.run(command, capture_output=True, text=True, check=False, env=env)


def failure(code, message):
    return {"ok": False, "code": code, "message": message}


def resolve_repo(explicit):
    if explicit:
        return (explicit, None) if REPO_PATTERN.fullmatch(explicit) else (None, failure("invalid_repo", "Repository must match owner/repo."))
    completed = run([tool("GIT_BIN", "git"), "remote", "get-url", "origin"])
    if completed.returncode == 0:
        remote = completed.stdout.strip()
        for pattern in (SSH_REMOTE, HTTPS_REMOTE, SSH_URL_REMOTE):
            match = pattern.match(remote)
            if match:
                return match.group("repo"), None
    return None, failure("repo_unresolved", "Could not infer a GitHub repository. Pass --repo owner/repo.")


def require_positive(value, field_name):
    if value.isdigit() and int(value) > 0:
        return int(value), None
    return None, failure(f"invalid_{field_name}", f"{field_name} must be a positive integer.")


def require_nonempty(value, field_name):
    if value is None or value.strip():
        return None
    return failure(f"empty_{field_name}", f"{field_name} must not be empty.")


def check_auth():
    completed = run([tool("GH_BIN", "gh"), "auth", "status"])
    if completed.returncode == 0:
        return None
    return failure("gh_auth_invalid", "gh auth status failed. Re-authenticate with `gh auth login`.")


def gh_failure(stderr):
    text = stderr or ""
    if "403" in text:
        return failure("gh_forbidden", "GitHub request failed due to insufficient repository permissions.")
    if "401" in text:
        return failure("gh_unauthorized", "GitHub request failed because authentication is invalid.")
    return failure("gh_command_failed", "GitHub CLI command failed.")
