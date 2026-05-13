# Subtree Guidelines: packages/rust

## Scope

This file applies to work under `packages/rust/`.

Follow the repository root `AGENTS.md` for global workflow, safety, planning, verification, and git guidance. Use this file only for local package additions.

## Local Overview

`packages/rust/` contains Rust-related development configuration and package documentation.

Local invariant: keep Rust tooling configuration changes explicit and avoid adding project build artifacts or dependency state accidentally.

## Local Structure

```text
README.md       Package purpose, files, and manual apply or backup notes
config/         Rust tooling configuration files when present
scripts/        Rust-specific maintenance scripts when present
docs/           Additional local notes when present
```

## Local Commands

No package-level install, lint, test, or build command is defined. Use commands from `packages/rust/README.md` when available.

Prefer inspection before live application:

```bash
git diff -- packages/rust/
```

## Local Rules

- Keep changes inside `packages/rust/` unless the task explicitly requires shared coordination.
- Update `packages/rust/README.md` when file locations, apply steps, or backup guidance change.
- Do not add `target/`, lockfiles, or generated tool state unless explicitly requested.
- Back up any live Rust tooling configuration before copying repository files over it.

## Local Verification

- Re-read `packages/rust/README.md` and changed files for path accuracy.
- Use relevant Rust tool validation only when documented or needed for the task.
- Report what was run, what was not run, and any remaining local risk.
