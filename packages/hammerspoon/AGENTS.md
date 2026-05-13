# Subtree Guidelines: packages/hammerspoon

## Scope

This file applies to work under `packages/hammerspoon/`.

Follow the repository root `AGENTS.md` for global workflow, safety, planning, verification, and git guidance. Use this file only for local package additions.

## Local Overview

`packages/hammerspoon/` contains Hammerspoon automation configuration and package documentation.

Local invariant: keep automation changes explicit, reversible, and safe for the user's desktop environment.

## Local Structure

```text
README.md       Package purpose, files, and manual apply or backup notes
config/         Hammerspoon configuration files when present
scripts/        Hammerspoon-specific helper scripts when present
docs/           Additional local notes when present
```

## Local Commands

No package-level install, lint, test, or build command is defined. Use commands from `packages/hammerspoon/README.md` when available.

Prefer inspection before live application:

```bash
git diff -- packages/hammerspoon/
```

## Local Rules

- Keep changes inside `packages/hammerspoon/` unless the task explicitly requires shared coordination.
- Update `packages/hammerspoon/README.md` when file locations, apply steps, or backup guidance change.
- Back up any live Hammerspoon configuration before copying repository files over it.
- Treat automation side effects, hotkeys, and application-control scripts as user-impacting behavior.

## Local Verification

- Re-read `packages/hammerspoon/README.md` and changed files for path accuracy.
- Use Hammerspoon reload or console checks when documented or relevant.
- Report what was run, what was not run, and any remaining local risk.
