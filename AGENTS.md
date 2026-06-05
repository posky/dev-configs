# Repository Guidelines

## Overview
This repository stores personal development environment configuration as
tool-owned packages under `packages/`.

Primary invariant: preserve the manual, review-first dotfiles workflow. Do not
overwrite live files in `~`, add repository-wide install automation, or introduce
package manager state unless the user explicitly asks.

There is no global package manager, lockfile, build system, or test command for
this repository.

## Structure
```text
packages/<tool>/        Tool-owned config, docs, scripts, themes, and examples
packages/shared-scripts/ Scripts that are not owned by one specific tool
packages/shared-themes/  Theme reference docs and reusable theme snippets
tasks/                  PRDs and task-specific execution notes
README.md               Repository structure, package rules, and safety notes
```

Default to one root `AGENTS.md`. Do not add nested `AGENTS.md` files unless a
subtree gains materially different commands, ownership, or safety rules that
cannot live in its package README.

## Key Docs

- `README.md`: package ownership rules, current package list, and change safety.
- `packages/*/README.md`: source of truth for that tool's files, apply steps,
  backup steps, and diff commands.
- `tasks/*.md`: living PRDs when a task already has scoped requirements.

Keep detailed tool behavior in the relevant package README or task PRD instead
of expanding this file.

## Workflow

- Treat each `packages/<tool>/` directory as the ownership boundary for that
  tool or runtime.
- Put tool-specific scripts in that tool's `scripts/` directory.
- Put cross-tool maintenance scripts only in `packages/shared-scripts/`.
- Put reusable theme references in `packages/shared-themes/`.
- When moving files or changing paths, update the relevant README examples so
  `cp`, `ln -sf`, `code --diff`, and `vim -d` paths still match reality.

## Commands

There are no repository-wide install, lint, format, test, or build commands.
Use the smallest command that validates the touched package:

```sh
git diff --check
code --diff <repo-file> <local-file>
vim -d <repo-file> <local-file>
nvim --headless "+Lazy! sync" +qa   # only for Neovim plugin sync checks
cargo make <task>                   # only after copying Rust config into a Rust project
```

Run package-specific commands only when their README or task PRD calls for them
and the required local tools are available. `packages/shared-scripts/scripts/update`
updates Homebrew, rustup, cargo-installed tools, uv, Neovim plugins, yazi
packages, and local git repos under `~/.local/src`; do not run it as routine
validation.

## Non-Negotiables

- Never copy, delete, symlink, or overwrite live home-directory config paths
  without explicit user approval and a backup/diff plan from the package README.
- Do not run destructive examples such as `rm -rf ~/.config/nvim/...` unless the
  user explicitly requests live application and the target path has been checked.
- Preserve unrelated dirty worktree changes.
- Do not add secrets, credentials, tokens, private keys, machine-local caches,
  generated plugin state, or runtime artifacts.
- Do not add repository-wide package manager files, lockfiles, generated
  dependency state, or install automation unless the user explicitly asks.
- Keep `.DS_Store`, `__pycache__/`, and other local artifacts out of the repo.

## Planning

For non-trivial work, especially changes that touch live-config instructions,
multiple packages, generated output, external tools, or task PRDs, write or
update the relevant plan in `tasks/` rather than creating a competing checklist.

For small package edits, read the package README and adjacent config first, then
make the focused change.

## Code And Config Quality

- Prefer minimal, reversible edits that preserve existing file layout and key
  order unless the task requires a structural change.
- Use structured parsers or tool-native validation for JSON, YAML, TOML, Lua,
  shell, PowerShell, and KDL when available.
- Keep language- or tool-specific conventions local to the package:
  `packages/neovim/` manages LazyVim and NvChad Lua config, `packages/python/`
  stores Ruff/VS Code examples, `packages/rust/` stores rustfmt/cargo-make/log4rs
  examples, and editor/terminal packages store their direct app configs.
- When updating prompt, commit, or UI templates shared by tools, check linked
  consumers such as `packages/git/.gitmessage.txt` and `packages/lazygit/config.yml`.

## Verification

- Match validation to the risk: static diff review for simple config changes,
  parser or formatter checks for structured files, and tool startup/sync smoke
  checks only when safe and available.
- Re-read changed files and confirm README command paths still point to existing
  repository files.
- If live application is intentionally performed, record the backup path,
  command used, and manual smoke result.
- In final responses, state changed files, validation run, validation skipped,
  and any remaining live-apply risk.

## Git And PR

- Keep commits focused and reversible.
- Stage only files related to the current task.
- Do not rewrite history, move tags, force-push, or discard user changes unless
  explicitly requested.
- PR descriptions should mention behavior/config changes, affected packages,
  live-apply risk, and verification performed.
