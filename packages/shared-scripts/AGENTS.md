# Subtree Guidelines: packages/shared-scripts

## Scope

This file applies to work under `packages/shared-scripts/`.

Follow the repository root `AGENTS.md` for global workflow, safety, planning, verification, and git guidance. Use this file only for local package additions.

## Local Overview

`packages/shared-scripts/` contains maintenance scripts that are not owned by a single tool package.

Local invariant: keep shared scripts conservative, path-safe, and explicit about shell, permission, and environment assumptions.

## Local Structure

```text
README.md       Ownership criteria, apply examples, and pre-run checks
scripts/        Shared maintenance scripts
```

## Local Commands

Use commands from `packages/shared-scripts/README.md` only after checking shebangs, permissions, `PATH` assumptions, and relative paths.

Prefer inspection before live application:

```bash
git diff -- packages/shared-scripts/
```

## Local Rules

- Keep scripts here only when they are not strongly coupled to one tool package.
- Move tool-specific scripts to that tool's `scripts/` directory when ownership is clear.
- Do not execute shared scripts unless the task explicitly asks for execution and the side effects are understood.
- Update `packages/shared-scripts/README.md` when ownership criteria, apply steps, or pre-run checks change.

## Local Verification

- Re-read `packages/shared-scripts/README.md` and changed scripts for path accuracy.
- Check shebangs, permissions, quoting, and relative path assumptions.
- Report what was run, what was not run, and any remaining local risk.
