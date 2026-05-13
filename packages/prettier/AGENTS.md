# Subtree Guidelines: packages/prettier

## Scope

This file applies to work under `packages/prettier/`.

Follow the repository root `AGENTS.md` for global workflow, safety, planning, verification, and git guidance. Use this file only for local package additions.

## Local Overview

`packages/prettier/` contains Prettier configuration assets and package documentation.

Local invariant: keep formatting configuration changes explicit and avoid introducing repository-wide tooling state accidentally.

## Local Structure

```text
README.md       Package purpose, files, and manual apply or backup notes
config/         Prettier configuration files when present
scripts/        Prettier-specific maintenance scripts when present
docs/           Additional local notes when present
```

## Local Commands

No package-level install, lint, test, or build command is defined. Use commands from `packages/prettier/README.md` when available.

Prefer inspection before live application:

```bash
git diff -- packages/prettier/
```

## Local Rules

- Keep changes inside `packages/prettier/` unless the task explicitly requires shared coordination.
- Update `packages/prettier/README.md` when file locations, apply steps, or backup guidance change.
- Do not add package-manager lockfiles or formatter dependencies unless the task explicitly approves them.
- Back up any live Prettier configuration before copying repository files over it.

## Local Verification

- Re-read `packages/prettier/README.md` and changed files for path accuracy.
- Use Prettier config checks only when the needed tool is available and the task requires it.
- Report what was run, what was not run, and any remaining local risk.
