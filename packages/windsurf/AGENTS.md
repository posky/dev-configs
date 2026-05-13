# Subtree Guidelines: packages/windsurf

## Scope

This file applies to work under `packages/windsurf/`.

Follow the repository root `AGENTS.md` for global workflow, safety, planning, verification, and git guidance. Use this file only for local package additions.

## Local Overview

`packages/windsurf/` contains Windsurf editor configuration assets and package documentation.

Local invariant: keep editor configuration changes reversible and documented before applying them to a live Windsurf config location.

## Local Structure

```text
README.md       Package purpose, files, and manual apply or backup notes
config/         Windsurf configuration files when present
scripts/        Windsurf-specific maintenance scripts when present
docs/           Additional local notes when present
```

## Local Commands

No package-level install, lint, test, or build command is defined. Use commands from `packages/windsurf/README.md` when available.

Prefer inspection before live application:

```bash
git diff -- packages/windsurf/
```

## Local Rules

- Keep changes inside `packages/windsurf/` unless the task explicitly requires shared coordination.
- Update `packages/windsurf/README.md` when file locations, apply steps, or backup guidance change.
- Back up any live Windsurf configuration before copying repository files over it.
- Verify target paths before overwrite, delete, or symlink operations.

## Local Verification

- Re-read `packages/windsurf/README.md` and changed files for path accuracy.
- Use Windsurf comparison or startup checks when documented or relevant.
- Report what was run, what was not run, and any remaining local risk.
