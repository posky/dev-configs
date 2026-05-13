# Subtree Guidelines: packages/wezterm

## Scope

This file applies to work under `packages/wezterm/`.

Follow the repository root `AGENTS.md` for global workflow, safety, planning, verification, and git guidance. Use this file only for local package additions.

## Local Overview

`packages/wezterm/` contains WezTerm terminal configuration assets and package documentation.

Local invariant: keep terminal configuration changes reversible and documented before applying them to a live WezTerm config location.

## Local Structure

```text
README.md       Package purpose, files, and manual apply or backup notes
config/         WezTerm configuration files when present
themes/         WezTerm theme assets when present
scripts/        WezTerm-specific maintenance scripts when present
docs/           Additional local notes when present
```

## Local Commands

No package-level install, lint, test, or build command is defined. Use commands from `packages/wezterm/README.md` when available.

Prefer inspection before live application:

```bash
git diff -- packages/wezterm/
```

## Local Rules

- Keep changes inside `packages/wezterm/` unless the task explicitly requires shared coordination.
- Update `packages/wezterm/README.md` when file locations, apply steps, or backup guidance change.
- Back up any live WezTerm configuration before copying repository files over it.
- Verify target paths before overwrite, delete, or symlink operations.

## Local Verification

- Re-read `packages/wezterm/README.md` and changed files for path accuracy.
- Use WezTerm config validation or reload checks when documented or relevant.
- Report what was run, what was not run, and any remaining local risk.
