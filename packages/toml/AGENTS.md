# Subtree Guidelines: packages/toml

## Scope

This file applies to work under `packages/toml/`.

Follow the repository root `AGENTS.md` for global workflow, safety, planning, verification, and git guidance. Use this file only for local package additions.

## Local Overview

`packages/toml/` contains TOML-related configuration assets and package documentation.

Local invariant: keep TOML configuration examples valid and avoid changing consumers silently.

## Local Structure

```text
README.md       Package purpose, files, and manual apply or backup notes
config/         TOML configuration files when present
docs/           Additional local notes when present
```

## Local Commands

No package-level install, lint, test, or build command is defined. Use commands from `packages/toml/README.md` when available.

Prefer inspection before live application:

```bash
git diff -- packages/toml/
```

## Local Rules

- Keep changes inside `packages/toml/` unless the task explicitly requires shared coordination.
- Update `packages/toml/README.md` when file locations, apply steps, or backup guidance change.
- Validate TOML syntax when changing files consumed by tools.

## Local Verification

- Re-read `packages/toml/README.md` and changed files for path accuracy.
- Use a TOML parser or owning tool validation when relevant and available.
- Report what was run, what was not run, and any remaining local risk.
