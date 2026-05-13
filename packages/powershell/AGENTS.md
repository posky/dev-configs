# Subtree Guidelines: packages/powershell

## Scope

This file applies to work under `packages/powershell/`.

Follow the repository root `AGENTS.md` for global workflow, safety, planning, verification, and git guidance. Use this file only for local package additions.

## Local Overview

`packages/powershell/` contains PowerShell configuration assets and package documentation.

Local invariant: keep profile and script changes reversible, shell-compatible, and documented before applying them to a live PowerShell profile location.

## Local Structure

```text
README.md       Package purpose, files, and manual apply or backup notes
config/         PowerShell configuration files when present
scripts/        PowerShell-specific maintenance scripts when present
docs/           Additional local notes when present
```

## Local Commands

No package-level install, lint, test, or build command is defined. Use commands from `packages/powershell/README.md` when available.

Prefer inspection before live application:

```bash
git diff -- packages/powershell/
```

## Local Rules

- Keep changes inside `packages/powershell/` unless the task explicitly requires shared coordination.
- Update `packages/powershell/README.md` when file locations, apply steps, or backup guidance change.
- Back up any live PowerShell profile before copying repository files over it.
- Preserve PowerShell syntax and platform-specific path quoting.

## Local Verification

- Re-read `packages/powershell/README.md` and changed files for path accuracy.
- Use PowerShell parser or profile-load checks when documented or relevant.
- Report what was run, what was not run, and any remaining local risk.
