# Subtree Guidelines: packages/shared-themes

## Scope

This file applies to work under `packages/shared-themes/`.

Follow the repository root `AGENTS.md` for global workflow, safety, planning, verification, and git guidance. Use this file only for local package additions.

## Local Overview

`packages/shared-themes/` contains theme references or assets shared across multiple tools.

Local invariant: keep shared theme changes coordinated so downstream tool packages do not drift silently.

## Local Structure

```text
README.md       Theme purpose, references, and usage notes
themes/         Shared theme assets when present
docs/           Additional local notes when present
```

## Local Commands

No package-level install, lint, test, or build command is defined. Use commands from `packages/shared-themes/README.md` when available.

Prefer inspection before live application:

```bash
git diff -- packages/shared-themes/
```

## Local Rules

- Keep generic theme references here and tool-specific theme application details in the owning tool package.
- Update affected package `README.md` files when a shared theme change changes local application steps.
- Do not duplicate large generated theme outputs unless explicitly requested.

## Local Verification

- Re-read `packages/shared-themes/README.md` and changed theme files for path accuracy.
- Check affected downstream tool packages when a shared theme contract changes.
- Report what was run, what was not run, and any remaining local risk.
