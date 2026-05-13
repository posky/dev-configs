# Subtree Guidelines: packages/bat

## Scope

This file applies to work under `packages/bat/`.

Follow the repository root `AGENTS.md` for global workflow, safety, planning, verification, and git guidance. Use this file only for local package additions.

## Local Overview

`packages/bat/` contains Bat configuration assets and package documentation.

Local invariant: keep Bat configuration changes reversible and documented before applying them to a live user config location.

## Local Structure

```text
README.md       Package purpose, files, and manual apply or backup notes
config/         Bat configuration files when present
themes/         Bat theme assets when present
scripts/        Bat-specific maintenance scripts when present
docs/           Additional local notes when present
```

## Local Commands

No package-level install, lint, test, or build command is defined. Use commands from `packages/bat/README.md` when available.

Prefer inspection before live application:

```bash
git diff -- packages/bat/
```

## Local Rules

- Keep changes inside `packages/bat/` unless the task explicitly requires shared coordination.
- Update `packages/bat/README.md` when file locations, apply steps, or backup guidance change.
- Back up any live Bat configuration before copying repository files over it.
- Verify target paths before overwrite, delete, or symlink operations.

## Local Verification

- Re-read `packages/bat/README.md` and changed files for path accuracy.
- Use Bat's own validation or preview commands when documented or relevant.
- Report what was run, what was not run, and any remaining local risk.
