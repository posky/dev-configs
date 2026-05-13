# Repository Guidelines

## Overview

`dev-configs` manages personal development environment configuration as tool-oriented packages.

Primary invariant: protect local user configuration from accidental destructive overwrite, deletion, or unreviewed path drift.

This repository does not define a package manager or automated install workflow. Do not introduce lockfiles, generated dependency state, or broad automation unless a task explicitly approves it.

Core stack:

- Tool-specific dotfiles, editor settings, terminal settings, themes, and maintenance scripts
- Manual copy, backup, compare, and apply workflows documented in package `README.md` files
- Cross-platform notes where individual tools require macOS, Windows, PowerShell, or shell-specific commands

## Structure

```text
packages/<tool>/       Tool, runtime, editor, terminal, or shared configuration package
packages/shared-scripts/   Shared maintenance scripts not owned by one tool
packages/shared-themes/    Theme references shared across tools
tasks/<slug>/          Planning, implementation, and review documents for non-trivial work
README.md              Repository structure, package rules, and change-safety notes
```

## Key Docs

- `README.md`: repository structure, package ownership rules, and current package list.
- `packages/*/README.md`: package-specific files, manual apply/backup steps, and comparison guidance.
- `tasks/<slug>/spec.md`, `tasks/<slug>/plan.md`, `tasks/<slug>/review.md`: source of truth for planned work.

Keep this file concise. Put detailed package runbooks and tool-specific procedures in the relevant package `README.md`.

## Commands

There is no repository-wide install, lint, test, or build command.

Use the smallest package-level check that proves the change. Prefer dry inspection and comparison commands before copying into live configuration locations.

Examples from package docs include:

```bash
code --diff <repo-file> <local-config-file>
vim -d <repo-file> <local-config-file>
git diff -- packages/<tool>/
```

Do not run destructive commands such as `rm -rf`, overwrite copies, symlink replacement, or global tool configuration changes unless the task explicitly calls for them and the target path has been checked.

## Non-Negotiables

- Preserve existing local configuration unless the user explicitly asks to overwrite it.
- Back up live config files before applying repository files to user locations.
- Check every destructive or overwrite target path twice before running a command.
- Keep changes inside the relevant `packages/<tool>/` subtree unless the task requires repository-level coordination.
- Do not treat `.DS_Store`, generated outputs, caches, or tool state as configuration packages.
- Leave unrelated dirty worktree changes untouched.
- Do not silently overwrite or silently merge `AGENTS.md`; use the canonical command contract for confirmation-first init/update behavior.

## Planning

For non-trivial, ambiguous, risky, cross-package, or destructive work, create task documents first:

```text
tasks/<slug>/
  spec.md
  plan.md
  review.md
```

For small and obvious changes, a compact plan inside `spec.md` is acceptable.

## Code Quality

- Read the relevant package `README.md` and surrounding files before editing.
- Preserve documented manual workflows unless a task explicitly changes them.
- Keep examples copy-pasteable and quote paths that may contain spaces.
- Prefer clear, reversible file updates over broad reorganization.
- Keep scripts conservative: validate paths, avoid hidden destructive side effects, and document assumptions.
- Consider platform differences in paths, shells, encodings, and config locations.

## Verification

- Match validation depth to risk and package scope.
- For documentation-only changes, re-read rendered source and check paths/commands against the package tree.
- For config changes, inspect diffs and use the owning tool's validation command when one is documented.
- For scripts, check shebangs, permissions, relative paths, and shell assumptions before suggesting execution.
- Report what was run, what was not run, and remaining risks.

## Git And PR

- Keep commits small, focused, and reversible.
- Stage only files relevant to the current task.
- Do not rewrite history or force-push unless explicitly requested.
- Describe configuration impact, local overwrite risk, and verification evidence in PRs.
