#!/usr/bin/env python3

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

API_VERSION = "2022-11-28"
ACCEPT_HEADER = "Accept: application/vnd.github+json"
VERSION_HEADER = f"X-GitHub-Api-Version: {API_VERSION}"
REPO_PATTERN = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
SSH_REMOTE = re.compile(r"^git@github\.com:(?P<repo>[^/]+/[^/]+?)(?:\.git)?$")
HTTPS_REMOTE = re.compile(r"^https://github\.com/(?P<repo>[^/]+/[^/]+?)(?:\.git)?/?$")
LIST_SORTS = ("due_on", "completeness")
LIST_DIRECTIONS = ("asc", "desc")


def build_parser():
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--repo", help="Explicit owner/repo override")
    parser = argparse.ArgumentParser(description="Manage GitHub milestones via gh api.")
    commands = parser.add_subparsers(dest="action", required=True)
    for name in ("list", "get", "create", "update", "close", "reopen", "delete"):
        child = commands.add_parser(name, parents=[common])
        if name == "list":
            child.add_argument("--state", default="open")
            child.add_argument("--sort", default="due_on")
            child.add_argument("--direction", default="asc")
            child.add_argument("--per-page", type=int, default=30)
            child.add_argument("--page", type=int, default=1)
        if name in {"get", "update", "close", "reopen", "delete"}:
            child.add_argument("milestone_number")
        if name in {"create", "update"}:
            child.add_argument("--title")
            child.add_argument("--description")
            child.add_argument("--due-on")
            child.add_argument("--state")
        if name == "delete":
            child.add_argument("--confirm-delete", action="store_true")
    return parser


def tool(name, default):
    return os.environ.get(name, default)


def success(action, repo, data=None, milestone_number=None):
    payload = {"ok": True, "action": action, "repo": repo}
    if milestone_number is not None:
        payload["milestone_number"] = milestone_number
    if data is not None:
        payload["data"] = data
    return payload


def error(code, message):
    return {"ok": False, "code": code, "message": message}


def run(command, env=None):
    return subprocess.run(command, capture_output=True, text=True, check=False, env=env)


def parse_repo(value):
    return value if value and REPO_PATTERN.fullmatch(value) else None


def infer_repo():
    completed = run([tool("GIT_BIN", "git"), "remote", "get-url", "origin"])
    if completed.returncode != 0:
        return None
    remote = completed.stdout.strip()
    for pattern in (SSH_REMOTE, HTTPS_REMOTE):
        match = pattern.match(remote)
        if match:
            return match.group("repo")
    return None


def resolve_repo(explicit):
    if explicit:
        repo = parse_repo(explicit)
        return repo, None if repo else error("invalid_repo", "Repository must match owner/repo.")
    repo = infer_repo()
    if repo:
        return repo, None
    return None, error("repo_unresolved", "Could not infer a GitHub repository. Pass --repo owner/repo.")


def positive_number(value):
    return int(value) if value.isdigit() and int(value) > 0 else None


def require_positive(value, field_name):
    if value <= 0:
        return error(f"invalid_{field_name}", f"{field_name} must be a positive integer.")
    return None


def require_choice(value, allowed, field_name):
    if value is None:
        return None
    if value not in allowed:
        return error(f"invalid_{field_name}", f"{field_name} must be one of: {', '.join(allowed)}.")
    return None


def require_title(value, required=False):
    if value is None:
        return error("empty_title", "title must not be empty.") if required else None
    if value.strip():
        return None
    return error("empty_title", "title must not be empty.")


def normalize_due_on(value):
    if value is None:
        return None, None
    text = value.strip()
    if not text:
        return None, error("invalid_due_on", "due_on must be a non-empty ISO-8601 value.")
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}$", text):
        text = f"{text}T00:00:00+00:00"
    elif text.endswith("Z"):
        text = f"{text[:-1]}+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None, error("invalid_due_on", "due_on must be ISO-8601 compatible.")
    if parsed.tzinfo is None:
        return None, error(
            "invalid_due_on",
            "due_on must be YYYY-MM-DD or a timezone-aware ISO-8601 timestamp.",
        )
    return parsed.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), None


def check_auth():
    completed = run([tool("GH_BIN", "gh"), "auth", "status"])
    if completed.returncode == 0:
        return None
    return error("gh_auth_invalid", "gh auth status failed. Re-authenticate with `gh auth login`.")


def endpoint(repo, milestone_number=None):
    owner, name = repo.split("/", 1)
    path = f"repos/{owner}/{name}/milestones"
    return path if milestone_number is None else f"{path}/{milestone_number}"


def api_error(stderr):
    if "403" in stderr:
        return error("gh_api_forbidden", "GitHub API request failed due to insufficient repository permissions.")
    if "401" in stderr:
        return error("gh_api_unauthorized", "GitHub API request failed because authentication is invalid.")
    return error("gh_api_failed", "GitHub API request failed.")


def api_call(repo, method, path, fields=None, silent=False):
    command = [tool("GH_BIN", "gh"), "api", "-X", method, "-H", ACCEPT_HEADER, "-H", VERSION_HEADER]
    for key, value in fields or []:
        command.extend(["-F", f"{key}={value}"])
    if silent:
        command.append("--silent")
    command.append(path)
    env = os.environ.copy()
    env["GH_REPO"] = repo
    completed = run(command, env=env)
    if completed.returncode != 0:
        return None, api_error(completed.stderr or "")
    if silent:
        return {}, None
    try:
        return json.loads(completed.stdout or "null"), None
    except json.JSONDecodeError:
        return None, error("gh_api_invalid_json", "GitHub API returned invalid JSON.")


def update_fields(args):
    normalized_due_on, due_error = normalize_due_on(args.due_on)
    if due_error:
        return None, due_error
    fields = []
    for key, value in (("title", args.title), ("description", args.description), ("state", args.state)):
        if value is not None:
            fields.append((key, value.strip() if key == "title" else value))
    if normalized_due_on is not None:
        fields.append(("due_on", normalized_due_on))
    if not fields:
        return None, error("missing_update_fields", "update requires at least one mutable field.")
    return fields, None


def validate(args):
    repo, repo_error = resolve_repo(args.repo)
    if repo_error:
        return None, repo_error
    if args.action == "list":
        checks = (
            require_choice(args.state, ("open", "closed", "all"), "state"),
            require_choice(args.sort, LIST_SORTS, "sort"),
            require_choice(args.direction, LIST_DIRECTIONS, "direction"),
            require_positive(args.per_page, "per_page"),
            require_positive(args.page, "page"),
        )
        for check in checks:
            if check:
                return None, check
    if args.action in {"create", "update"}:
        checks = (
            require_choice(args.state, ("open", "closed"), "state"),
            require_title(args.title, required=args.action == "create"),
        )
        for check in checks:
            if check:
                return None, check
    if args.action in {"get", "update", "close", "reopen", "delete"}:
        number = positive_number(args.milestone_number)
        if number is None:
            return None, error("invalid_milestone_number", "milestone_number must be a positive integer.")
        args.milestone_number = number
    return repo, None


def list_milestones(args, repo):
    fields = [("state", args.state), ("sort", args.sort), ("direction", args.direction), ("per_page", args.per_page), ("page", args.page)]
    return api_call(repo, "GET", endpoint(repo), fields)


def write_milestone(args, repo):
    fields = [("title", args.title.strip())]
    for key, value in (("description", args.description), ("state", args.state)):
        if value is not None:
            fields.append((key, value))
    normalized_due_on, due_error = normalize_due_on(args.due_on)
    if due_error:
        return None, due_error
    if normalized_due_on is not None:
        fields.append(("due_on", normalized_due_on))
    return api_call(repo, "POST", endpoint(repo), fields)


def execute(args, repo):
    if args.action == "list":
        return list_milestones(args, repo)
    if args.action == "get":
        return api_call(repo, "GET", endpoint(repo, args.milestone_number))
    if args.action == "create":
        return write_milestone(args, repo)
    if args.action == "update":
        fields, field_error = update_fields(args)
        return (None, field_error) if field_error else api_call(repo, "PATCH", endpoint(repo, args.milestone_number), fields)
    if args.action in {"close", "reopen"}:
        state = "closed" if args.action == "close" else "open"
        return api_call(repo, "PATCH", endpoint(repo, args.milestone_number), [("state", state)])
    if not args.confirm_delete:
        return None, error("delete_confirmation_required", "delete requires --confirm-delete.")
    payload, get_error = api_call(repo, "GET", endpoint(repo, args.milestone_number))
    if get_error:
        return None, get_error
    _, delete_error = api_call(repo, "DELETE", endpoint(repo, args.milestone_number), silent=True)
    return (None, delete_error) if delete_error else (payload, None)


def main():
    args = build_parser().parse_args()
    repo, validation_error = validate(args)
    if validation_error:
        print(json.dumps(validation_error))
        return 1
    auth_error = check_auth()
    if auth_error:
        print(json.dumps(auth_error))
        return 1
    payload, request_error = execute(args, repo)
    if request_error:
        print(json.dumps(request_error))
        return 1
    print(json.dumps(success(args.action, repo, data=payload, milestone_number=getattr(args, "milestone_number", None))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
