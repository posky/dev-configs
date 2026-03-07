---
name: gh-issue-manage
description: Manage GitHub issues with GitHub CLI and the GitHub REST API. Use this skill when Codex needs to list, inspect, create, or edit issues with `gh issue`, validate labels or milestones against repository state, infer the target GitHub repository from the current checkout, or manage sub-issue relationships through `gh api`.
---

# GH Issue Manage

## Overview

Use this skill to manage GitHub issues through a deterministic helper instead of ad hoc `gh issue` and `gh api` commands.
Resolve the target repository first, validate inputs locally, then run the helper with explicit subcommands.

## Path Resolution

- Resolve relative paths from the skill directory first, especially under `scripts/`.
- Canonical helper invocation:
  ```bash
  python3 /path/to/gh-issue-manage/scripts/manage_issues.py list --repo owner/repo
  ```

## Required Workflow

1. Confirm whether the target repository should come from the current checkout or explicit `--repo owner/repo`.
2. Treat every `gh` network operation as an escalated command.
3. Run `gh auth status` before issue operations. If it fails, stop and tell the user to re-authenticate.
4. Use the bundled helper when it exists. Do not rewrite `gh issue` or sub-issue API commands manually unless the helper is missing or unreadable.
5. Validate issue numbers, sub-issue ids, labels, milestones, and body-file paths locally before network writes.
6. Use automatic label and milestone attachment only for `create`, only when the user did not specify metadata, and only with exact normalized phrase matches from the issue title/body.
7. If multiple milestone titles match the issue text, do not pick one automatically; return a warning and continue without a milestone.
8. Summarize normalized helper output instead of printing verbose `gh` diagnostics.

## Command Rules

- Run the helper with explicit subcommands only:
  - `list`
  - `view`
  - `create`
  - `edit`
  - `list-sub-issues`
  - `get-parent`
  - `add-sub-issue`
  - `remove-sub-issue`
- Allow `--repo owner/repo` on every command. If omitted, the helper may infer the repo from `git remote get-url origin`.
- Do not continue when repo inference fails and no explicit repo was given.
- Do not rely on interactive `gh` prompts.
- Do not use `--project`, `--web`, or `--template` in this workflow.

## Metadata Rules

- `create --label` and `create --milestone` are explicit overrides and must be validated against repository state.
- If explicit metadata was not provided, `create` may auto-select:
  - labels from exact normalized phrase matches against existing repository label names
  - one open milestone from an exact normalized phrase match against the issue title/body
- `edit` never auto-selects metadata. It applies only the user-requested `--add-label`, `--remove-label`, `--milestone`, or `--remove-milestone` changes.
- If repository label or milestone lookup fails during auto-selection, continue without that metadata and surface a warning.
- If explicit label or milestone validation fails, stop before the write.

## Sub-Issue Rules

- Use `gh api` only for sub-issue operations that `gh issue` does not support directly.
- `list-sub-issues` maps to `GET /repos/{owner}/{repo}/issues/{issue_number}/sub_issues`.
- `get-parent` maps to `GET /repos/{owner}/{repo}/issues/{issue_number}/parent`.
- `add-sub-issue` maps to `POST /repos/{owner}/{repo}/issues/{issue_number}/sub_issues` with `sub_issue_id`, and optional `replace_parent=true`.
- `remove-sub-issue` maps to `DELETE /repos/{owner}/{repo}/issues/{issue_number}/sub_issue` with `sub_issue_id`.
- `sub_issue_id` is the GitHub issue `id`, not the issue number.
- Do not implement reprioritization in this version.

## Escalation Rules

- `gh auth status`, `gh issue list`, `gh issue view`, `gh issue create`, `gh issue edit`, and every `gh api` invocation require network access. Run them with `exec_command` using:
  - `sandbox_permissions: "require_escalated"`
  - a short justification that explains the GitHub issue action
- If `python3 <skill-dir>/scripts/manage_issues.py ...` will execute `gh`, treat that Python command as networked and escalate it too.
- Avoid printing raw auth errors or verbose HTTP output because they may expose local config details.

## Permissions

- Read operations may require public repository access or `Issues` repository read permission.
- Mutating issue and sub-issue operations may require `Issues` repository write permission.
- If GitHub returns 401 or 403, stop and tell the user that authentication or repository permissions are insufficient.

## Resources

### scripts/manage_issues.py

Use this helper to validate inputs, resolve the repo, call `gh issue` or `gh api`, and emit stable JSON output.

### scripts/issue_metadata.py

Use this helper for exact-match label and milestone lookup, validation, and conservative create-time auto-selection.

### scripts/test_manage_issues.py

Run this regression suite with:
```bash
python3 /path/to/gh-issue-manage/scripts/test_manage_issues.py
```
