# Subtree Guidelines: packages/python

## Scope

This file applies to work under `packages/python/`.

Follow the repository root `AGENTS.md` for global workflow, safety, planning, verification, and git guidance. Use this file only for local package additions.

## Local Overview

`packages/python/` contains Python-related development configuration and package documentation.

Local invariant: keep Python tooling configuration changes explicit and avoid adding project dependency state accidentally.

## Local Structure

```text
README.md       Package purpose, files, and manual apply or backup notes
config/         Python tooling configuration files when present
scripts/        Python-specific maintenance scripts when present
docs/           Additional local notes when present
```

## Local Commands

No package-level install, lint, test, or build command is defined. Use commands from `packages/python/README.md` when available.

Prefer inspection before live application:

```bash
git diff -- packages/python/
```

## Local Rules

- Keep changes inside `packages/python/` unless the task explicitly requires shared coordination.
- Update `packages/python/README.md` when file locations, apply steps, or backup guidance change.
- Do not add virtual environments, lockfiles, or generated caches unless explicitly requested.
- Back up any live Python tooling configuration before copying repository files over it.

## Local Verification

- Re-read `packages/python/README.md` and changed files for path accuracy.
- Use relevant Python tool validation only when documented or needed for the task.
- Report what was run, what was not run, and any remaining local risk.
