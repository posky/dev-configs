---
name: gh-pr-create
description: Create GitHub pull requests with GitHub CLI using repository rules for the `.github/PULL_REQUEST_TEMPLATE.md` pull request template, issue references, milestone selection, repository label selection, self-assignment, draft creation, and base branch defaults. Use this skill when Codex needs to prepare or run `gh pr create`, translate `!#123` into close links and `#456` into related links, choose a PR milestone from referenced issues, attach appropriate existing labels, or apply the repository's `.github/PULL_REQUEST_TEMPLATE.md` template.
---

# GitHub PR Create

## Overview

Use this skill to prepare and create pull requests with `gh` in a repeatable way.
Resolve deterministic context first, then create the PR with explicit flags.
Decide the PR title before running `gh pr create`; when the title is written in Korean, use a noun phrase rather than a sentence.

## Path Resolution

- Resolve any relative path mentioned by this skill from the skill directory first, especially paths under `scripts/`.
- `--repo-root` points to the target repository being inspected; it does not change where bundled helpers live.
- Canonical helper invocation:
  ```bash
  uv run /path/to/gh-pr-create/scripts/resolve_pr_context.py --repo-root <repo> --request-file <file>
  ```

## Required Workflow

1. Confirm the repository root and current branch.
2. Treat any `gh` command that needs network access as an escalated command.
3. Run `gh auth status` before issue lookups or PR creation. If it fails, stop and tell the user to re-authenticate.
4. Resolve request context with the bundled helper: `uv run <skill-dir>/scripts/resolve_pr_context.py --repo-root <repo> --request-file <file> [--base <branch>] [--template <path>]`.
5. If the bundled helper exists, do not skip it. Only fall back to a manual process when the helper is actually missing or unreadable.
6. Use the selected template file as the PR body scaffold. If the resolver completes and no template is selected, use a minimal fallback body with:
   - `## Summary`
   - `## Testing`
7. Append issue footer lines at the end of the final PR body in this order:
   - one `close #<number>` line for each entry in `close_issues`
   - one `related #<number>` line for each entry in `related_issues`
8. Use resolver-selected labels from `labels` when present. Pass them with repeated `--label "<name>"` flags in ascending order.
9. If the resolver reports non-fatal `warnings`, continue unless the user asks to inspect them.
10. Create the PR with explicit flags. Prefer `--body-file` over interactive editing.

## Command Rules

- Use the user-specified base branch when present.
- Use `develop` when the user did not specify a base branch.
- Do not silently fall back to another base branch if `develop` or the requested branch does not exist.
- Keep the current checked-out branch as the PR head branch.
- Before `gh pr create`, verify the current branch has an upstream. If it does not, stop and ask the user before any push-related action.
- Always pass `--draft`.
- Always pass `--assignee @me`.
- Do not rely on `gh pr create` prompts for title, body, template selection, or milestone selection.
- Omit `--label` entirely when `labels` is empty.

## Title Rules

- Finalize the PR title before running `gh pr create --title`.
- When the title is written in Korean, use a concise noun phrase.
- Prefer Korean noun-phrase titles in Korean-language requests.
- Allow an English title only when the repository convention is English or the user explicitly asks for English.
- Good Korean title examples:
  - `로그인 오류 수정`
  - `배치 작업 실패 원인 정리`
- Avoid sentence-style Korean titles such as:
  - `로그인 오류를 수정합니다`
  - `배치 작업 실패 원인을 정리했습니다`

## Issue And Milestone Rules

- Parse `!#123` as `close #123`.
- Parse `#456` as `related #456`.
- If the same issue appears as both `!#123` and `#123`, keep only `close #123`.
- Deduplicate issue references while preserving first mention order.
- Query referenced issues with `gh issue view <number> --json milestone,title,url,state`.
- Choose the PR milestone from referenced issues only:
  - use the most frequent non-null milestone
  - if tied, prefer the milestone attached to more `!#` issues
  - if still tied, use the milestone from the earliest mentioned tied issue
- If no referenced issue has a milestone, omit the PR milestone.

## Template Rules

- Only inspect `.github` for pull request templates.
- Check only `.github/PULL_REQUEST_TEMPLATE.md`.
- If that file exists, use it automatically.
- If no candidate exists, build the PR body from the fallback sections after the resolver step has completed.

## Label Rules

- Query repository labels with `gh label list --json name,description --limit 100 --sort name --order asc`.
- Treat label selection as conservative and deterministic:
  - select a label only when its normalized name is an exact phrase match in the request text or a referenced issue title
  - or when its normalized name exactly matches a changed file path segment or stem from `git diff --name-only <base>...HEAD`
- Use repository label descriptions for context only; do not select labels from description-only matches.
- Sort selected labels by label name ascending.
- If label lookup fails or returns invalid JSON, continue with `labels: []` and review `warnings` if needed.
- Do not create, edit, or delete labels in this workflow.

## Escalation Rules

- `gh auth status`, `gh issue view`, `gh label list`, and `gh pr create` need network access. Run them with `exec_command` using:
  - `sandbox_permissions: "require_escalated"`
  - a short justification that explains the GitHub action
- If `uv run <skill-dir>/scripts/resolve_pr_context.py ...` will execute `gh`, treat that `uv run` command as networked and escalate it too.
- Avoid printing raw auth errors that may include local config paths. Summarize the failure and suggest `gh auth login`.

## If Bundled Helpers Are Missing

- If `scripts/resolve_pr_context.py` is missing from the skill bundle, say that the helper is unavailable and switch to a manual process.
- In that manual process, still verify auth, base branch, upstream, templates, and issue references explicitly before `gh pr create`.
- Do not treat “I did not run the helper” as equivalent to “the helper is unavailable.”

## Common Pitfalls

- Do not search the target repository's `scripts/` directory first for bundled helpers referenced by this skill.
- Do not use fallback body generation as a substitute for running the resolver.
- Do not infer milestone, issue footer, or template-selection results manually when the bundled helper exists.

## Example Sequence

1. Write the user's PR request into a temporary file.
2. Run:
   ```bash
   uv run /path/to/gh-pr-create/scripts/resolve_pr_context.py --repo-root /path/to/repo --request-file /tmp/pr-request.txt
   ```
3. Read the JSON result.
4. Decide the PR title. In Korean contexts, write it as a noun phrase such as `로그인 오류 수정`.
5. Build the final body from the selected template or fallback scaffold.
6. Create the PR:
   ```bash
   gh pr create --base develop --draft --assignee @me --title "<title>" --body-file /tmp/pr-body.md [--label "<name>"] [--milestone "<name>"]
   ```

## Resources

### scripts/resolve_pr_context.py

Use this helper to resolve deterministic PR context before creating the PR.
Always run it with `uv run`, and resolve its relative path from the skill directory rather than the target repository.
It returns `labels` for `gh pr create --label` and non-fatal `warnings` for optional context resolution problems.

### scripts/label_selection.py

This helper contains the conservative label lookup and matching logic used by the resolver.

### scripts/test_resolve_pr_context.py

Run this regression suite with `uv run <skill-dir>/scripts/test_resolve_pr_context.py`.

### scripts/test_label_selection.py

Run this label-selection regression suite with `uv run <skill-dir>/scripts/test_label_selection.py`.
