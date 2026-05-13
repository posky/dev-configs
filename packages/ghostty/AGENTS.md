# Subtree Guidelines: packages/ghostty

## Scope

This file applies to work under `packages/ghostty/`.

Follow the repository root `AGENTS.md` for global workflow, safety, planning, verification, and git guidance. Use this file only for local package additions.

## Local Overview

`packages/ghostty/` contains Ghostty terminal configuration assets and package documentation.

Local invariant: keep terminal configuration changes reversible and documented before applying them to a live Ghostty config location.

## Local Structure

```text
README.md       Package purpose, files, and manual apply or backup notes
config/         Ghostty configuration files when present
themes/         Ghostty theme assets when present
scripts/        Ghostty-specific maintenance scripts when present
docs/           Additional local notes when present
```

## Local Commands

No package-level install, lint, test, or build command is defined. Use commands from `packages/ghostty/README.md` when available.

Prefer inspection before live application:

```bash
git diff -- packages/ghostty/
```

## Local Rules

- Keep changes inside `packages/ghostty/` unless the task explicitly requires shared coordination.
- Update `packages/ghostty/README.md` when file locations, apply steps, or backup guidance change.
- Back up any live Ghostty configuration before copying repository files over it.
- Verify target paths before overwrite, delete, or symlink operations.

## Local Verification

- Re-read `packages/ghostty/README.md` and changed files for path accuracy.
- Use Ghostty's own validation or reload checks when documented or relevant.
- Report what was run, what was not run, and any remaining local risk.
