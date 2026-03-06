#!/usr/bin/env python3

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ISSUE_PATTERN = re.compile(r"!?#(\d+)")


def parse_args():
    parser = argparse.ArgumentParser(description="Resolve deterministic PR context for gh pr create.")
    parser.add_argument("--repo-root", required=True, help="Repository root to inspect")
    parser.add_argument("--request-file", required=True, help="File containing the user PR request")
    parser.add_argument("--base", default="develop", help="Base branch to use")
    parser.add_argument("--template", help="Explicit template path relative to the repo root")
    return parser.parse_args()


def tool_path(env_name, default_name):
    return os.environ.get(env_name, default_name)


def run_command(command, cwd):
    return subprocess.run(command, cwd=cwd, capture_output=True, text=True, check=False)


def error(code, message):
    return {"code": code, "message": message}


def relative_path(path, repo_root):
    return path.resolve().relative_to(repo_root.resolve()).as_posix()


def validate_repo(repo_root):
    git = tool_path("GIT_BIN", "git")
    completed = run_command([git, "-C", str(repo_root), "rev-parse", "--show-toplevel"], repo_root)
    if completed.returncode != 0:
        return None, error("not_git_repo", "Repository root is not a git checkout.")
    resolved = Path(completed.stdout.strip()).resolve()
    if resolved != repo_root.resolve():
        return None, error("repo_root_mismatch", "Repository root does not match git top-level path.")
    return resolved, None


def resolve_head_branch(repo_root):
    git = tool_path("GIT_BIN", "git")
    completed = run_command([git, "-C", str(repo_root), "branch", "--show-current"], repo_root)
    branch = completed.stdout.strip()
    if completed.returncode != 0 or not branch:
        return None, error("head_branch_missing", "Current branch could not be determined.")
    return branch, None


def has_upstream(repo_root):
    git = tool_path("GIT_BIN", "git")
    completed = run_command(
        [git, "-C", str(repo_root), "rev-parse", "--abbrev-ref", "@{upstream}"],
        repo_root,
    )
    return completed.returncode == 0


def validate_base_branch(repo_root, base_branch):
    git = tool_path("GIT_BIN", "git")
    completed = run_command(
        [git, "-C", str(repo_root), "show-ref", "--verify", f"refs/heads/{base_branch}"],
        repo_root,
    )
    if completed.returncode != 0:
        return error("missing_base_branch", f"Base branch '{base_branch}' does not exist locally.")
    return None


def check_auth(repo_root):
    gh = tool_path("GH_BIN", "gh")
    completed = run_command([gh, "auth", "status"], repo_root)
    if completed.returncode != 0:
        return error("gh_auth_invalid", "gh auth status failed. Re-authenticate with `gh auth login`.")
    return None


def parse_request_text(text):
    classifications = {}
    mention_order = []
    mentioned_set = set()

    for match in ISSUE_PATTERN.finditer(text):
        issue_number = int(match.group(1))
        is_close = match.group(0).startswith("!")
        if issue_number not in mentioned_set:
            mention_order.append(issue_number)
            mentioned_set.add(issue_number)
        if is_close:
            classifications[issue_number] = "close"
            continue
        classifications.setdefault(issue_number, "related")

    close_issues = [issue for issue in mention_order if classifications.get(issue) == "close"]
    related_issues = [issue for issue in mention_order if classifications.get(issue) == "related"]
    return close_issues, related_issues, mention_order


def discover_templates(repo_root):
    github_dir = repo_root / ".github"
    candidates = []
    for name in ("pull_request_template.md", "PULL_REQUEST_TEMPLATE.md"):
        candidate = github_dir / name
        if candidate.is_file():
            candidates.append(candidate)
    template_dir = github_dir / "PULL_REQUEST_TEMPLATE"
    if template_dir.is_dir():
        for candidate in sorted(template_dir.glob("*.md")):
            if candidate.is_file():
                candidates.append(candidate)
    return candidates


def resolve_template(repo_root, explicit_template):
    candidates = discover_templates(repo_root)
    candidate_paths = [relative_path(path, repo_root) for path in candidates]
    if explicit_template:
        selected = (repo_root / explicit_template).resolve()
        if not selected.is_file():
            return None, candidate_paths, False, error("template_missing", "Selected template file does not exist.")
        try:
            relative_selected = selected.relative_to(repo_root.resolve()).as_posix()
        except ValueError:
            return None, candidate_paths, False, error("template_outside_repo", "Selected template must be inside the repository.")
        if not relative_selected.startswith(".github/"):
            return None, candidate_paths, False, error("template_outside_github", "Selected template must be inside .github.")
        if relative_selected not in candidate_paths:
            return None, candidate_paths, False, error("template_not_candidate", "Selected template is not a discovered pull request template.")
        return relative_selected, candidate_paths, False, None
    if len(candidates) == 1:
        return relative_path(candidates[0], repo_root), candidate_paths, False, None
    if len(candidates) > 1:
        return None, candidate_paths, True, None
    return None, candidate_paths, False, None


def fetch_issue(repo_root, issue_number):
    gh = tool_path("GH_BIN", "gh")
    completed = run_command(
        [gh, "issue", "view", str(issue_number), "--json", "milestone,title,url,state"],
        repo_root,
    )
    if completed.returncode != 0:
        return None, error("issue_lookup_failed", f"Issue #{issue_number} could not be loaded.")
    try:
        return json.loads(completed.stdout), None
    except json.JSONDecodeError:
        return None, error("issue_lookup_invalid_json", f"Issue #{issue_number} returned invalid JSON.")


def milestone_title(issue_payload):
    milestone = issue_payload.get("milestone")
    if isinstance(milestone, dict):
        title = milestone.get("title")
        return title or None
    if isinstance(milestone, str) and milestone:
        return milestone
    return None


def choose_milestone(issue_payloads, close_set, mention_order):
    milestone_counts = {}
    close_counts = {}
    earliest_index = {}
    mention_index = {issue: index for index, issue in enumerate(mention_order)}

    for issue_number, payload in issue_payloads.items():
        title = milestone_title(payload)
        if not title:
            continue
        milestone_counts[title] = milestone_counts.get(title, 0) + 1
        close_counts.setdefault(title, 0)
        earliest_index[title] = min(
            earliest_index.get(title, len(mention_order)),
            mention_index.get(issue_number, len(mention_order)),
        )
        if issue_number in close_set:
            close_counts[title] += 1

    if not milestone_counts:
        return None

    ranked = sorted(
        milestone_counts,
        key=lambda title: (-milestone_counts[title], -close_counts.get(title, 0), earliest_index[title]),
    )
    return ranked[0]


def build_result(repo_root, base_branch):
    return {
        "repo_root": str(repo_root.resolve()),
        "head_branch": None,
        "has_upstream": False,
        "base_branch": base_branch,
        "close_issues": [],
        "related_issues": [],
        "template_candidates": [],
        "selected_template": None,
        "needs_template_choice": False,
        "milestone": None,
        "errors": [],
    }


def main():
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    request_file = Path(args.request_file).resolve()
    result = build_result(repo_root, args.base)

    resolved_repo, repo_error = validate_repo(repo_root)
    if repo_error:
        result["errors"].append(repo_error)
        print(json.dumps(result, indent=2))
        return 1

    head_branch, head_error = resolve_head_branch(resolved_repo)
    if head_error:
        result["errors"].append(head_error)
        print(json.dumps(result, indent=2))
        return 1
    result["head_branch"] = head_branch
    result["has_upstream"] = has_upstream(resolved_repo)

    base_error = validate_base_branch(resolved_repo, args.base)
    if base_error:
        result["errors"].append(base_error)
        print(json.dumps(result, indent=2))
        return 1

    auth_error = check_auth(resolved_repo)
    if auth_error:
        result["errors"].append(auth_error)
        print(json.dumps(result, indent=2))
        return 1

    if not request_file.is_file():
        result["errors"].append(error("request_file_missing", "Request file does not exist."))
        print(json.dumps(result, indent=2))
        return 1

    request_text = request_file.read_text()
    close_issues, related_issues, mention_order = parse_request_text(request_text)
    result["close_issues"] = close_issues
    result["related_issues"] = related_issues

    selected_template, candidates, needs_choice, template_error = resolve_template(
        resolved_repo,
        args.template,
    )
    result["selected_template"] = selected_template
    result["template_candidates"] = candidates
    result["needs_template_choice"] = needs_choice
    if template_error:
        result["errors"].append(template_error)
        print(json.dumps(result, indent=2))
        return 1

    issue_payloads = {}
    for issue_number in mention_order:
        payload, issue_error = fetch_issue(resolved_repo, issue_number)
        if issue_error:
            result["errors"].append(issue_error)
            print(json.dumps(result, indent=2))
            return 1
        issue_payloads[issue_number] = payload

    result["milestone"] = choose_milestone(issue_payloads, set(close_issues), mention_order)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
