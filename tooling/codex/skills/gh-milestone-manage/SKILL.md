---
name: gh-milestone-manage
description: Manage GitHub repository milestones with GitHub CLI and the GitHub REST API. Use this skill when Codex needs to list, inspect, create, update, close, reopen, or delete milestones, validate milestone inputs, normalize due dates, infer a target GitHub repository from the current checkout, or run `gh api` milestone commands safely.
---

# GH Milestone Manage

## Overview

Use this skill to manage GitHub milestones through a deterministic helper instead of ad hoc `gh api` commands.
Resolve the target repository first, validate inputs locally, then run the helper with explicit flags.

## Path Resolution

- Resolve any relative path mentioned by this skill from the skill directory first, especially paths under `scripts/`.
- Canonical helper invocation:
  ```bash
  uv run /path/to/gh-milestone-manage/scripts/manage_milestones.py list --repo owner/repo
  ```

## Required Workflow

1. Confirm whether the target repository should come from the current checkout or an explicit `--repo owner/repo`.
2. Treat every `gh` network operation as an escalated command.
3. Run `gh auth status` before milestone operations. If it fails, stop and tell the user to re-authenticate.
4. Use the bundled helper when it exists. Do not rewrite milestone commands manually unless the helper is missing or unreadable.
5. Validate milestone numbers, state values, titles, and `due_on` locally before any network write.
6. Prefer `close` over `delete` when the user intent is ambiguous.
7. For `delete`, resolve and show the target milestone first, then require an explicit confirmation step before running `--confirm-delete`.
8. Summarize normalized helper output instead of printing verbose `gh` diagnostics.

## Command Rules

- Run the helper with explicit subcommands only:
  - `list`
  - `get`
  - `create`
  - `update`
  - `close`
  - `reopen`
  - `delete`
- Allow `--repo owner/repo` on every command. If omitted, the helper may infer the repo from `git remote get-url origin`.
- Do not continue when repo inference fails and no explicit repo was given.
- Do not rely on interactive `gh` prompts.
- Use `application/vnd.github+json` and `X-GitHub-Api-Version: 2022-11-28` on every API request.

## Escalation Rules

- `gh auth status` and every `gh api` invocation require network access. Run them with `exec_command` using:
  - `sandbox_permissions: "require_escalated"`
  - a short justification that explains the GitHub milestone action
- If `uv run <skill-dir>/scripts/manage_milestones.py ...` will execute `gh`, treat that `uv run` command as networked and escalate it too.
- Avoid printing raw auth errors or verbose HTTP output because they may expose local config details.

## Input Rules

- Accept only positive integers for milestone numbers.
- Accept `open|closed|all` for `list --state`.
- Accept `due_on|completeness` for `list --sort`.
- Accept `asc|desc` for `list --direction`.
- Accept `open|closed` for `create --state` and `update --state`.
- Accept only positive integers for `list --per-page` and `list --page`.
- Reject empty titles for `create` and `update --title`.
- Accept `due_on` only as `YYYY-MM-DD` or a timezone-aware ISO-8601 timestamp, then normalize it to UTC `YYYY-MM-DDTHH:MM:SSZ`.
- Reject `update` when no mutable fields were provided.

## Permissions

- Read operations may require public repository access or `Issues`/`Pull requests` read permission.
- Mutating operations may require `Issues` or `Pull requests` write permission.
- If GitHub returns 401 or 403, stop and tell the user that authentication or repository permissions are insufficient.

## Resources

### scripts/manage_milestones.py

Use this helper to validate inputs, resolve the repo, run `gh api`, and emit stable JSON output.

### scripts/test_manage_milestones.py

Run this regression suite with:
```bash
python3 /path/to/gh-milestone-manage/scripts/test_manage_milestones.py
```
