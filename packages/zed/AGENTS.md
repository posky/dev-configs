# Subtree Guidelines: packages/zed

## Scope

This file applies to work under `packages/zed/`.

Follow the repository root `AGENTS.md` for global workflow, safety, planning, verification, and git guidance. Use this file only for local package additions.

## Local Overview

`packages/zed/` contains Zed editor configuration assets and package documentation.

Local invariant: keep editor configuration changes reversible and documented before applying them to a live Zed config location.

## Local Structure

```text
README.md       Package purpose, files, and manual apply or backup notes
config/         Zed configuration files when present
scripts/        Zed-specific maintenance scripts when present
docs/           Additional local notes when present
```

## Local Commands

No package-level install, lint, test, or build command is defined. Use commands from `packages/zed/README.md` when available.

Prefer inspection before live application:

```bash
git diff -- packages/zed/
```

## Local Rules

- Keep changes inside `packages/zed/` unless the task explicitly requires shared coordination.
- Update `packages/zed/README.md` when file locations, apply steps, or backup guidance change.
- Back up any live Zed configuration before copying repository files over it.
- Verify target paths before overwrite, delete, or symlink operations.

## Local Verification

- Re-read `packages/zed/README.md` and changed files for path accuracy.
- Use Zed comparison or startup checks when documented or relevant.
- Report what was run, what was not run, and any remaining local risk.
