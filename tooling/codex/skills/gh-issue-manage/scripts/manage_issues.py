#!/usr/bin/env python3

import argparse
import json
import re
import sys

from gh_common import check_auth, failure, gh_failure, require_nonempty, require_positive, resolve_repo, run, tool
import issue_metadata

API_HEADERS = ["-H", "Accept: application/vnd.github+json", "-H", "X-GitHub-Api-Version: 2022-11-28"]
ISSUE_URL_PATTERN = re.compile(r"/issues/(?P<number>\d+)")
VIEW_FIELDS = "assignees,author,body,comments,createdAt,id,labels,milestone,number,state,title,updatedAt,url"


def build_parser():
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--repo", help="Explicit owner/repo override")
    parser = argparse.ArgumentParser(description="Manage GitHub issues via gh.")
    commands = parser.add_subparsers(dest="action", required=True)

    child = commands.add_parser("list", parents=[common])
    child.add_argument("--state", default="open")
    child.add_argument("--label", action="append", default=[])
    child.add_argument("--milestone")
    child.add_argument("--author")
    child.add_argument("--assignee")
    child.add_argument("--search")
    child.add_argument("--limit", type=int, default=30)

    child = commands.add_parser("view", parents=[common])
    child.add_argument("issue_number")
    child.add_argument("--comments", action="store_true")

    for name in ("create", "edit"):
        child = commands.add_parser(name, parents=[common])
        if name == "edit":
            child.add_argument("issue_number")
        child.add_argument("--title")
        group = child.add_mutually_exclusive_group()
        group.add_argument("--body")
        group.add_argument("--body-file")
        child.add_argument("--milestone")
        if name == "create":
            child.add_argument("--label", action="append", default=[])
        else:
            child.add_argument("--add-label", action="append", default=[])
            child.add_argument("--remove-label", action="append", default=[])
            child.add_argument("--remove-milestone", action="store_true")

    for name in ("list-sub-issues", "get-parent"):
        child = commands.add_parser(name, parents=[common])
        child.add_argument("issue_number")
        if name == "list-sub-issues":
            child.add_argument("--per-page", type=int, default=30)
            child.add_argument("--page", type=int, default=1)

    child = commands.add_parser("add-sub-issue", parents=[common])
    child.add_argument("parent_issue_number")
    child.add_argument("--sub-issue-id", required=True)
    child.add_argument("--replace-parent", action="store_true")

    child = commands.add_parser("remove-sub-issue", parents=[common])
    child.add_argument("parent_issue_number")
    child.add_argument("--sub-issue-id", required=True)
    return parser

def success(action, repo, data=None, warnings=None):
    return {"ok": True, "action": action, "repo": repo, "data": data, "warnings": warnings or []}


def read_body(args):
    if not hasattr(args, "body"):
        return None, None
    if args.body is not None:
        return args.body, None
    if not getattr(args, "body_file", None):
        return None, None
    try:
        with open(args.body_file, encoding="utf-8") as handle:
            return handle.read(), None
    except OSError:
        return None, failure("body_file_unreadable", "body_file could not be read.")


def parse_json(stdout, code):
    try:
        return json.loads(stdout or "null"), None
    except json.JSONDecodeError:
        return None, failure(code, "GitHub CLI returned invalid JSON.")


def parse_created_issue_number(stdout):
    match = ISSUE_URL_PATTERN.search(stdout or "")
    if match:
        return int(match.group("number"))
    stripped = (stdout or "").strip()
    return int(stripped) if stripped.isdigit() else None


def run_gh_json(command, invalid_json_code):
    completed = run(command)
    return (None, gh_failure(completed.stderr)) if completed.returncode != 0 else parse_json(completed.stdout, invalid_json_code)


def view_issue(repo, issue_number, include_comments):
    return run_gh_json(
        [tool("GH_BIN", "gh"), "issue", "view", str(issue_number), "--repo", repo, "--json", VIEW_FIELDS if include_comments else VIEW_FIELDS.replace("comments,", "")],
        "gh_issue_view_invalid_json",
    )


def validate_args(args):
    repo, repo_error = resolve_repo(args.repo)
    if repo_error:
        return None, None, repo_error
    body_text, body_error = read_body(args)
    if body_error:
        return None, None, body_error
    if args.action == "list":
        if args.state not in {"open", "closed", "all"}:
            return None, None, failure("invalid_state", "state must be one of: open, closed, all.")
        if args.limit <= 0:
            return None, None, failure("invalid_limit", "limit must be a positive integer.")
    if args.action in {"view", "edit", "list-sub-issues", "get-parent"}:
        args.issue_number, issue_error = require_positive(args.issue_number, "issue_number")
        if issue_error:
            return None, None, issue_error
    if args.action in {"add-sub-issue", "remove-sub-issue"}:
        args.parent_issue_number, issue_error = require_positive(args.parent_issue_number, "parent_issue_number")
        if issue_error:
            return None, None, issue_error
        args.sub_issue_id, sub_issue_error = require_positive(args.sub_issue_id, "sub_issue_id")
        if sub_issue_error:
            return None, None, sub_issue_error
    if args.action == "list-sub-issues" and (args.per_page <= 0 or args.page <= 0):
        return None, None, failure("invalid_pagination", "per-page and page must be positive integers.")
    if args.action == "create":
        title_error = require_nonempty(args.title, "title") or (failure("empty_title", "title must not be empty.") if args.title is None else None)
        if title_error:
            return None, None, title_error
    if args.action in {"create", "edit"}:
        for field_name, values in (
            ("title", [args.title]),
            ("milestone", [args.milestone]),
            ("label", getattr(args, "label", [])),
            ("label", getattr(args, "add_label", [])),
            ("label", getattr(args, "remove_label", [])),
        ):
            for value in values:
                string_error = require_nonempty(value, field_name)
                if string_error:
                    return None, None, string_error
        if args.action == "edit":
            changed = any([args.title, body_text is not None, args.add_label, args.remove_label, args.milestone, args.remove_milestone])
            if not changed:
                return None, None, failure("missing_update_fields", "edit requires at least one mutable field.")
            if args.milestone and args.remove_milestone:
                return None, None, failure("invalid_milestone_change", "Cannot set and remove milestone in the same edit.")
    return repo, body_text, None


def handle_list(args, repo):
    command = [tool("GH_BIN", "gh"), "issue", "list", "--repo", repo, "--state", args.state, "--limit", str(args.limit), "--json", VIEW_FIELDS]
    for name in args.label:
        command.extend(["--label", name])
    for flag, value in (("--milestone", args.milestone), ("--author", args.author), ("--assignee", args.assignee), ("--search", args.search)):
        if value:
            command.extend([flag, value])
    return run_gh_json(command, "gh_issue_list_invalid_json")


def handle_create(args, repo, body_text):
    warnings = []
    labels = list(args.label)
    milestone = args.milestone
    if labels:
        labels, label_error = issue_metadata.validate_labels(repo, labels)
        if label_error:
            return None, label_error, warnings
    if milestone:
        milestone, milestone_error = issue_metadata.validate_milestone(repo, milestone)
        if milestone_error:
            return None, milestone_error, warnings
    if not labels and not milestone:
        labels, milestone, warnings = issue_metadata.suggest_create_metadata(repo, args.title, body_text)
    command = [tool("GH_BIN", "gh"), "issue", "create", "--repo", repo, "--title", args.title]
    if body_text is not None:
        command.extend(["--body", body_text])
    for name in labels:
        command.extend(["--label", name])
    if milestone:
        command.extend(["--milestone", milestone])
    completed = run(command)
    if completed.returncode != 0:
        return None, gh_failure(completed.stderr), warnings
    issue_number = parse_created_issue_number(completed.stdout)
    if issue_number is None:
        return None, failure("issue_create_unparseable", "Created issue number could not be determined."), warnings
    payload, view_error = view_issue(repo, issue_number, False)
    return (None, view_error, warnings) if view_error else ({"issue": payload, "applied_labels": labels, "applied_milestone": milestone}, None, warnings)


def handle_edit(args, repo, body_text):
    labels_to_check = list(args.add_label) + list(args.remove_label)
    if labels_to_check:
        _, label_error = issue_metadata.validate_labels(repo, labels_to_check)
        if label_error:
            return None, label_error
    milestone = args.milestone
    if milestone:
        milestone, milestone_error = issue_metadata.validate_milestone(repo, milestone)
        if milestone_error:
            return None, milestone_error
    command = [tool("GH_BIN", "gh"), "issue", "edit", str(args.issue_number), "--repo", repo]
    for flag, value in (("--title", args.title), ("--body", body_text), ("--milestone", milestone)):
        if value is not None:
            command.extend([flag, value])
    for name in args.add_label:
        command.extend(["--add-label", name])
    for name in args.remove_label:
        command.extend(["--remove-label", name])
    if args.remove_milestone:
        command.append("--remove-milestone")
    completed = run(command)
    if completed.returncode != 0:
        return None, gh_failure(completed.stderr)
    payload, view_error = view_issue(repo, args.issue_number, False)
    return payload, view_error


def sub_issue_path(repo, issue_number, suffix):
    owner, name = repo.split("/", 1)
    return f"repos/{owner}/{name}/issues/{issue_number}/{suffix}"


def handle_sub_issue_api(repo, method, path, fields=None):
    command = [tool("GH_BIN", "gh"), "api", "-X", method, *API_HEADERS, path]
    for key, value in fields or []:
        command.extend(["-F", f"{key}={value}"])
    return run_gh_json(command, "gh_api_invalid_json")


def execute(args, repo, body_text):
    if args.action == "list":
        payload, request_error = handle_list(args, repo)
        return payload, request_error, []
    if args.action == "view":
        payload, request_error = view_issue(repo, args.issue_number, args.comments)
        return payload, request_error, []
    if args.action == "create":
        return handle_create(args, repo, body_text)
    if args.action == "edit":
        payload, request_error = handle_edit(args, repo, body_text)
        return payload, request_error, []
    if args.action == "list-sub-issues":
        payload, request_error = handle_sub_issue_api(repo, "GET", f"{sub_issue_path(repo, args.issue_number, 'sub_issues')}?per_page={args.per_page}&page={args.page}")
        return payload, request_error, []
    if args.action == "get-parent":
        payload, request_error = handle_sub_issue_api(repo, "GET", sub_issue_path(repo, args.issue_number, "parent"))
        return payload, request_error, []
    if args.action == "add-sub-issue":
        fields = [("sub_issue_id", args.sub_issue_id)]
        if args.replace_parent:
            fields.append(("replace_parent", "true"))
        payload, request_error = handle_sub_issue_api(repo, "POST", sub_issue_path(repo, args.parent_issue_number, "sub_issues"), fields)
        return payload, request_error, []
    payload, request_error = handle_sub_issue_api(repo, "DELETE", sub_issue_path(repo, args.parent_issue_number, "sub_issue"), [("sub_issue_id", args.sub_issue_id)])
    return payload, request_error, []


def main():
    args = build_parser().parse_args()
    repo, body_text, validation_error = validate_args(args)
    if validation_error:
        print(json.dumps(validation_error))
        return 1
    auth_error = check_auth()
    if auth_error:
        print(json.dumps(auth_error))
        return 1
    payload, request_error, warnings = execute(args, repo, body_text)
    if request_error:
        print(json.dumps(request_error))
        return 1
    print(json.dumps(success(args.action, repo, data=payload, warnings=warnings)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
