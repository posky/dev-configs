# Subtree Guidelines: packages/lazygit

## Scope

This file applies to work under `packages/lazygit/`.

Follow the repository root `AGENTS.md` for global workflow, safety, planning, verification, and git guidance. Use this file only for local package additions.

## Local Overview

`packages/lazygit/` contains Lazygit configuration assets and package documentation.

Local invariant: keep Lazygit configuration changes reversible and documented before applying them to a live user config location.

## Local Structure

```text
README.md       Package purpose, files, and manual apply or backup notes
config/         Lazygit configuration files when present
scripts/        Lazygit-specific maintenance scripts when present
docs/           Additional local notes when present
```

## Local Commands

No package-level install, lint, test, or build command is defined. Use commands from `packages/lazygit/README.md` when available.

Prefer inspection before live application:

```bash
git diff -- packages/lazygit/
```

## Local Rules

- Keep changes inside `packages/lazygit/` unless the task explicitly requires shared coordination.
- Update `packages/lazygit/README.md` when file locations, apply steps, or backup guidance change.
- Back up any live Lazygit configuration before copying repository files over it.
- Verify target paths before overwrite, delete, or symlink operations.

## Local Verification

- Re-read `packages/lazygit/README.md` and changed files for path accuracy.
- Use Lazygit's own validation or startup checks when documented or relevant.
- Report what was run, what was not run, and any remaining local risk.
